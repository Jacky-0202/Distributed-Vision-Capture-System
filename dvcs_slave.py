import asyncio
import os
import signal
import time
import subprocess
from datetime import datetime
from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import FileResponse

app = FastAPI(title="DVCS Slave Node Service")

# ==========================================
# ⚙️ 系統配置 (Configuration)
# ==========================================
TEMP_DIR = "/dev/shm/captures"
os.makedirs(TEMP_DIR, exist_ok=True)

# 💡 重要：每一台 Slave 請根據編號手動修改此數值 (1-4)
NODE_ID = 1 

# 閒置限制 (秒)，預設 600 秒 (10 分鐘) 自動關閉相機
IDLE_LIMIT = 600 

class CameraState:
    def __init__(self):
        self.process = None       # 儲存 libcamera 進程物件
        self.last_access = 0      # 最後一次呼叫 API 的時間
        self.lock = asyncio.Lock() # 確保拍照過程不被重疊觸發

state = CameraState()

def get_cpu_temp():
    """獲取 CM4 當前 CPU 溫度"""
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            return int(f.read()) / 1000.0
    except: return 0.0

# ==========================================
# 核心邏輯：相機生命週期管理
# ==========================================

async def start_camera():
    """啟動相機進入信號模式 (常駐預覽/暖機)"""
    if state.process is None:
        print(f"🚀 [Node {NODE_ID}] Starting Camera Engine (Persistent Mode)...")
        # -t 0: 持續執行; --signal: 等待 SIGUSR1 才拍照; --nopreview: 禁用桌面預覽(省資源)
        cmd = [
            "libcamera-still", "-t", "0", "--signal", "--nopreview",
            "-o", os.path.join(TEMP_DIR, "capture_.jpg"),
            "--datetime", "--quality", "95", "--width", "4608", "--height", "2592"
        ]
        # preexec_fn=os.setsid 確保我們能控制整個進程組的信號
        state.process = await asyncio.create_subprocess_exec(*cmd, preexec_fn=os.setsid)
        state.last_access = time.time()

async def stop_camera():
    """關閉相機進入低功耗模式"""
    if state.process:
        print(f"💤 [Node {NODE_ID}] Idle limit reached. Powering off camera sensor...")
        try:
            # 使用 os.killpg 確保乾淨關閉進程組，不留殘餘
            os.killpg(os.getpgid(state.process.pid), signal.SIGTERM)
            await state.process.wait()
        except Exception as e:
            print(f"Error stopping camera: {e}")
        state.process = None

async def idle_monitor():
    """背景任務：定期檢查是否該休眠"""
    while True:
        await asyncio.sleep(30)
        if state.process and (time.time() - state.last_access > IDLE_LIMIT):
            await stop_camera()

# ==========================================
# 🚀 服務生命週期管理
# ==========================================

@app.on_event("startup")
async def startup_event():
    """系統啟動時自動開啟相機並啟動監控任務"""
    await start_camera()
    asyncio.create_task(idle_monitor())

@app.on_event("shutdown")
async def shutdown_event():
    """服務關閉時強制釋放相機資源"""
    await stop_camera()

# ==========================================
# 📡 API 端點
# ==========================================

@app.get("/health")
async def health_check():
    """查看節點狀態與溫度"""
    return {
        "node_id": NODE_ID,
        "cpu_temp": f"{get_cpu_temp()}°C",
        "camera_active": state.process is not None,
        "idle_seconds": int(time.time() - state.last_access) if state.process else "Idle"
    }

@app.post("/restart")
async def remote_restart(mode: str = "service"):
    """
    遠端重啟命令
    - service: 重啟 FastAPI 服務
    - hardware: 整個 CM4 系統 Reboot
    """
    await stop_camera()
    if mode == "hardware":
        os.system("sleep 2 && sudo reboot &")
        return {"message": "Hardware rebooting..."}
    else:
        os.system("sleep 2 && sudo systemctl restart dvcs_slave &")
        return {"message": "Service restarting..."}

@app.post("/take_photo")
async def take_photo(payload: dict = Body(...)):
    """
    執行拍照任務並依照規範重命名
    命名格式: CAM{ID}_{LIGHT}_{YYYYMMDD_HHMMSS}.jpg
    """
    async with state.lock:
        state.last_access = time.time()
        
        # 若相機已休眠，自動喚醒
        if state.process is None:
            await start_camera()
            await asyncio.sleep(1.2) # 等待硬體暖機

        # 發送拍照信號
        print(f"📸 [Node {NODE_ID}] Triggering capture...")
        state.process.send_signal(signal.SIGUSR1)
        
        # 等待寫入 RAM Disk (調整此數值以確保檔案寫入完整)
        await asyncio.sleep(0.5) 
        
        # 尋找最新產出的照片
        files = [os.path.join(TEMP_DIR, f) for f in os.listdir(TEMP_DIR) if f.endswith(".jpg")]
        if not files:
            raise HTTPException(status_code=500, detail="Capture failed: No file generated")
        
        latest_file = max(files, key=os.path.getmtime)
        
        # 依照規範生成檔名
        light = payload.get("light", "RE")
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        final_name = f"CAM{NODE_ID}_{light}_{timestamp}.jpg"
        final_path = os.path.join(TEMP_DIR, final_name)
        
        # 重新命名並回傳檔案流
        os.rename(latest_file, final_path)
        print(f"✅ [Node {NODE_ID}] Photo saved: {final_name}")

        return FileResponse(final_path, media_type="image/jpeg", filename=final_name)

if __name__ == "__main__":
    import uvicorn
    # 啟動服務，監聽 8000 Port
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")