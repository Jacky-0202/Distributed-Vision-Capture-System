import asyncio
import os
import shutil
import httpx
import serial
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from datetime import datetime
from contextlib import asynccontextmanager

# ==========================================
# ⚙️ 系統配置 (Configuration)
# ==========================================
IMAGE_BASE_DIR = "./images"
os.makedirs(IMAGE_BASE_DIR, exist_ok=True)

# Slave CM4 IP 配置
SLAVE_IPS = {
    1: "http://10.0.0.2:8000",
    2: "http://10.0.0.3:8000",
    3: "http://10.0.0.4:8000",
    4: "http://10.0.0.5:8000"
}

# ----------------- PLC 配置 -----------------
SERIAL_PORT = '/dev/ttyUSB0'
MY_ID = 8
PLC_ID = 1
BAUDRATE = 19200

# Modbus 暫存器池
registers = {
    0: 0,      # 40001: 複合指令 (光源+相機遮罩)
    2: 2,      # 40003: 狀態 (1:Running, 2:OK)
    3: 0,      # 40004: 異常碼
    9: 1,      # 40010: Watchdog
    16: 100    # 40017: 版本
}

LIGHT_MAP = {1: "RE", 2: "R", 3: "G", 4: "B"}
last_command = -1

# ==========================================
# 📡 Modbus Engine (PLC 通訊與背景邏輯)
# ==========================================

def calculate_crc(data):
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for _ in range(8):
            if (crc & 1) != 0:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return crc.to_bytes(2, 'little')

async def trigger_slave_camera_plc(client, slave_id, light_name):
    """供 PLC 觸發使用的拍照與存檔邏輯 (與 Swagger API 儲存邏輯一致)"""
    url = f"{SLAVE_IPS[slave_id]}/take_photo"
    try:
        res = await client.post(url, json={"light": light_name}, timeout=15.0)
        if res.status_code == 200:
            # 統一命名格式，扁平化存於 images 根目錄
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"CAM{slave_id}_{light_name}_{timestamp}.jpg"
            save_path = os.path.join(IMAGE_BASE_DIR, filename)
            
            with open(save_path, "wb") as f:
                f.write(res.content)
            print(f"✅ [PLC Trigger] Node {slave_id} Photo saved: {filename}")
            return True
        return False
    except Exception as e:
        print(f"⚠️ [PLC Trigger] Node {slave_id} Error: {e}")
        return False

async def process_photo_task(val):
    """解析 PLC 複合指令，並平行觸發多台相機"""
    registers[2] = 1 # Status -> Running
    light_id = val & 0x000F
    camera_mask = (val & 0x0FF0) >> 4
    light_name = LIGHT_MAP.get(light_id, "Unknown")
    
    # 根據 Mask 判斷要觸發哪幾台 (1~4)
    target_slaves = [i+1 for i in range(4) if (camera_mask >> i) & 1]
    print(f"📡 [PLC Command] Triggering Cameras: {target_slaves} with Light: {light_name}")
    
    async with httpx.AsyncClient() as client:
        # 異步並發觸發相機
        tasks = [trigger_slave_camera_plc(client, s_id, light_name) for s_id in target_slaves]
        await asyncio.gather(*tasks)

    registers[2] = 2 # Status -> OK
    print("✅ [PLC Command] Capture Task Completed.")

async def run_master_listener():
    """背景執行 Modbus RTU 監聽"""
    global last_command
    is_first_sync = True
    try:
        ser = serial.Serial(SERIAL_PORT, BAUDRATE, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0.01)
        while True:
            if ser.in_waiting >= 8:
                req = ser.read(ser.in_waiting)
                # 驗證 CRC 與設備 ID
                if req[0] in [PLC_ID, MY_ID] and req[-2:] == calculate_crc(req[:-2]):
                    f_code = req[1]
                    addr = (req[2] << 8) | req[3]
                    
                    # 讀取暫存器 (0x03)
                    if f_code == 0x03:
                        qty = (req[4] << 8) | req[5]
                        res_data = bytearray([qty * 2])
                        for i in range(qty):
                            res_data += registers.get(addr + i, 0).to_bytes(2, 'big')
                        packet = bytearray([req[0], 0x03]) + res_data
                        ser.write(packet + calculate_crc(packet))
                        
                    # 寫入暫存器 (0x06)
                    elif f_code == 0x06:
                        val = (req[4] << 8) | req[5]
                        registers[addr] = val
                        ser.write(req)
                        
                        # 當寫入地址 0 (40001) 且數值改變時觸發拍照
                        if addr == 0 and val > 0:
                            if is_first_sync:
                                last_command, is_first_sync = val, False
                            elif val != last_command:
                                asyncio.create_task(process_photo_task(val))
                                last_command = val
            await asyncio.sleep(0.001)
    except Exception as e:
        print(f"⚠️ [Serial Error] {e}")

# ==========================================
# 🚀 FastAPI & 生命周期管理
# ==========================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """當 FastAPI 啟動時，自動在背景開啟 Modbus 監聽任務"""
    task = asyncio.create_task(run_master_listener())
    print("🛰️ Modbus Background Listener Started on /dev/ttyUSB0.")
    yield
    task.cancel()
    print("🛑 Modbus Background Listener Stopped.")

app = FastAPI(title="DVCS Master Hub (API + PLC)", lifespan=lifespan)

# ==========================================
# 🌐 核心 API 功能 (與 dvcs_master_cam.py 一致)
# ==========================================

@app.post("/cam/preview/{cam_id}")
async def preview_single(cam_id: int):
    """
    【1. 單機預覽】不需要光源參數，直接覆寫 images 下的預覽檔
    """
    if cam_id not in SLAVE_IPS:
        raise HTTPException(status_code=404, detail="Slave IP not configured")
    
    async with httpx.AsyncClient() as client:
        try:
            url = f"{SLAVE_IPS[cam_id]}/take_photo"
            res = await client.post(url, json={"light": "PREVIEW"}, timeout=15.0)
            
            if res.status_code == 200:
                preview_filename = f"preview_cam{cam_id}.jpg"
                preview_path = os.path.join(IMAGE_BASE_DIR, preview_filename)
                
                with open(preview_path, "wb") as f:
                    f.write(res.content)
                
                return FileResponse(preview_path, media_type="image/jpeg")
            raise HTTPException(status_code=500, detail="Slave preview failed")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.post("/cam/capture/{cam_id}")
async def capture_single(cam_id: int, light: str = Query("CAPTURE", description="光源標記")):
    """
    【2. 單機拍照】API 手動觸發，檔案扁平化存於 images 根目錄
    """
    if cam_id not in SLAVE_IPS:
        raise HTTPException(status_code=404, detail="Slave IP not configured")
    
    async with httpx.AsyncClient() as client:
        try:
            url = f"{SLAVE_IPS[cam_id]}/take_photo"
            res = await client.post(url, json={"light": light}, timeout=15.0)
            
            if res.status_code == 200:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"CAM{cam_id}_{light}_{timestamp}.jpg"
                save_path = os.path.join(IMAGE_BASE_DIR, filename)
                
                with open(save_path, "wb") as f:
                    f.write(res.content)
                
                return {
                    "status": "saved",
                    "filename": filename,
                    "node": cam_id,
                    "timestamp": timestamp
                }
            raise HTTPException(status_code=500, detail="Slave capture failed")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/system/download")
async def download_system_download():
    """
    【3. 打包下載】將整個 images/ 資料夾內容打包成 .zip
    """
    if not os.path.exists(IMAGE_BASE_DIR) or not os.listdir(IMAGE_BASE_DIR):
        raise HTTPException(status_code=404, detail="No images found to backup")
    
    zip_base_name = "dvcs_images_archive"
    final_zip_file = f"{zip_base_name}.zip"

    if os.path.exists(final_zip_file):
        try:
            os.remove(final_zip_file)
            print(f"🗑️ [System] Old temporary file {final_zip_file} deleted.")
        except Exception as e:
            pass
    
    shutil.make_archive(zip_base_name, 'zip', IMAGE_BASE_DIR)
    download_filename = f"DVCS_Backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    
    return FileResponse(final_zip_file, media_type="application/zip", filename=download_filename)

@app.delete("/system/cleanup")
async def cleanup_storage():
    """
    【4. 清理空間】刪除 ./images 目錄下所有照片檔案
    """
    try:
        if os.path.exists(IMAGE_BASE_DIR):
            for file in os.listdir(IMAGE_BASE_DIR):
                file_path = os.path.join(IMAGE_BASE_DIR, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            return {"message": "All images in root directory cleared successfully."}
        else:
            return {"message": "Directory does not exist."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cleanup failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # 啟動 Master 服務 (API + PLC 雙引擎)
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")