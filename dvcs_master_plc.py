import asyncio
import os
import shutil
import httpx
import serial
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from datetime import datetime
from contextlib import asynccontextmanager

# ==========================================
# ⚙️ 系統配置 (Configuration)
# ==========================================
SERIAL_PORT = '/dev/ttyUSB0'
MY_ID = 8
PLC_ID = 1
BAUDRATE = 19200
IMAGE_BASE_DIR = "./images"

# Slave CM4 IP 配置
SLAVE_IPS = {
    1: "http://10.0.0.2:8000",
    2: "http://10.0.0.3:8000",
    3: "http://10.0.0.4:8000",
    4: "http://10.0.0.5:8000"
}

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
# 🚀 FastAPI & 生命周期管理
# ==========================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 當 FastAPI 啟動時，自動在背景開啟 Modbus 監聽任務
    task = asyncio.create_task(run_master_listener())
    print("🛰️  Modbus Background Listener Started.")
    yield
    # 關閉時的操作 (選擇性)
    task.cancel()

app = FastAPI(title="Master CM4 Control Hub", lifespan=lifespan)

# --- 需求 1: 撈取特定資料夾所有照片清單 ---
@app.get("/photos/{cam_id}")
async def list_photos(cam_id: int):
    cam_dir = os.path.join(IMAGE_BASE_DIR, f"cam{cam_id}")
    if not os.path.exists(cam_dir):
        return {"cam_id": cam_id, "count": 0, "photos": []}
    
    photos = [f for f in os.listdir(cam_dir) if f.endswith(".jpg")]
    return {"cam_id": cam_id, "count": len(photos), "photos": sorted(photos)}

# --- 需求 1 補充：下載/查看特定單張照片 ---
@app.get("/photos/{cam_id}/{filename}")
async def get_single_photo(cam_id: int, filename: str):
    file_path = os.path.join(IMAGE_BASE_DIR, f"cam{cam_id}", filename)
    if os.path.exists(file_path):
        return FileResponse(file_path, media_type="image/jpeg")
    raise HTTPException(status_code=404, detail="Photo not found")

# --- 需求 1 補充：打包下載所有照片 (ZIP) ---
@app.get("/download_all/{cam_id}")
async def download_all(cam_id: int):
    cam_dir = os.path.join(IMAGE_BASE_DIR, f"cam{cam_id}")
    if not os.path.exists(cam_dir) or not os.listdir(cam_dir):
        raise HTTPException(status_code=404, detail="No photos to download")
    
    zip_filename = f"cam{cam_id}_backup"
    # 打包壓縮檔
    shutil.make_archive(zip_filename, 'zip', cam_dir)
    return FileResponse(f"{zip_filename}.zip", filename=f"cam{cam_id}_all.zip")

# --- 需求 2: 刪除特定資料夾下的所有照片 ---
@app.delete("/photos/{cam_id}")
async def delete_cam_photos(cam_id: int):
    cam_dir = os.path.join(IMAGE_BASE_DIR, f"cam{cam_id}")
    if os.path.exists(cam_dir):
        for f in os.listdir(cam_dir):
            os.remove(os.path.join(cam_dir, f))
        return {"status": "success", "message": f"Cleared cam{cam_id}"}
    raise HTTPException(status_code=404, detail="Folder not found")

# --- 需求 3: 即時讓某個相機拍照並回傳 ---
@app.post("/capture/{cam_id}")
async def instant_capture(cam_id: int):
    if cam_id not in SLAVE_IPS:
        raise HTTPException(status_code=404, detail="Slave not configured")
    
    async with httpx.AsyncClient() as client:
        try:
            # 觸發 Slave 拍照 (採用全視角模式)
            res = await client.post(f"{SLAVE_IPS[cam_id]}/take_photo", json={"light": "API_TRIGGER"}, timeout=15.0)
            if res.status_code == 200:
                temp_file = f"instant_cam{cam_id}.jpg"
                with open(temp_file, "wb") as f:
                    f.write(res.content)
                return FileResponse(temp_file, media_type="image/jpeg")
            raise HTTPException(status_code=500, detail="Slave failed to capture")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

# ==========================================
# 📡 Modbus Engine (Background Logic)
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

async def trigger_slave_camera(client, slave_id, light_name):
    url = f"{SLAVE_IPS[slave_id]}/take_photo"
    try:
        response = await client.post(url, json={"light": light_name}, timeout=10.0)
        if response.status_code == 200:
            cam_dir = os.path.join(IMAGE_BASE_DIR, f"cam{slave_id}")
            os.makedirs(cam_dir, exist_ok=True)
            filename = f"{light_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            with open(os.path.join(cam_dir, filename), "wb") as f:
                f.write(response.content)
            return f"Cam{slave_id} OK"
    except Exception as e:
        return f"Cam{slave_id} Error: {e}"

async def process_photo_task(val):
    registers[2] = 1 # Status -> Running
    light_id = val & 0x000F
    camera_mask = (val & 0x0FF0) >> 4
    light_name = LIGHT_MAP.get(light_id, "Unknown")
    
    target_slaves = [i+1 for i in range(4) if (camera_mask >> i) & 1]
    
    async with httpx.AsyncClient() as client:
        tasks = [trigger_slave_camera(client, s_id, light_name) for s_id in target_slaves]
        await asyncio.gather(*tasks)

    registers[2] = 2 # Status -> OK

async def run_master_listener():
    global last_command
    is_first_sync = True
    try:
        ser = serial.Serial(SERIAL_PORT, BAUDRATE, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=0.01)
        while True:
            if ser.in_waiting >= 8:
                req = ser.read(ser.in_waiting)
                if req[0] in [PLC_ID, MY_ID] and req[-2:] == calculate_crc(req[:-2]):
                    f_code = req[1]
                    addr = (req[2] << 8) | req[3]
                    if f_code == 0x03:
                        qty = (req[4] << 8) | req[5]
                        res_data = bytearray([qty * 2])
                        for i in range(qty):
                            res_data += registers.get(addr + i, 0).to_bytes(2, 'big')
                        packet = bytearray([req[0], 0x03]) + res_data
                        ser.write(packet + calculate_crc(packet))
                    elif f_code == 0x06:
                        val = (req[4] << 8) | req[5]
                        registers[addr] = val
                        ser.write(req)
                        if addr == 0 and val > 0:
                            if is_first_sync:
                                last_command, is_first_sync = val, False
                            elif val != last_command:
                                asyncio.create_task(process_photo_task(val))
                                last_command = val
            await asyncio.sleep(0.001)
    except Exception as e:
        print(f"Serial Error: {e}")

if __name__ == "__main__":
    import uvicorn
    # 啟動命令
    uvicorn.run(app, host="0.0.0.0", port=8000)