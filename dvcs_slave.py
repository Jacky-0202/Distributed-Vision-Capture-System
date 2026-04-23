import asyncio
import os
import signal
import time
import subprocess
from datetime import datetime
from fastapi import FastAPI, HTTPException, Body
from fastapi.responses import FileResponse

app = FastAPI(title="DVCS_Slave_Service_Node")

# --- 配置區 ---
TEMP_DIR = "/dev/shm/captures"
os.makedirs(TEMP_DIR, exist_ok=True)
IDLE_LIMIT = 600  # 10 分鐘自動休眠

class CameraState:
    def __init__(self):
        self.process = None
        self.last_access = 0
        self.lock = asyncio.Lock()

state = CameraState()

def get_cpu_temp():
    try:
        with open("/sys/class/thermal/thermal_zone0/temp", "r") as f:
            return int(f.read()) / 1000.0
    except: return 0.0

# ==========================================
# 核心邏輯：相機管理
# ==========================================

async def start_camera():
    """啟動相機進入信號模式 (常駐預覽)"""
    if state.process is None:
        print("🚀 [Service] Starting Camera Engine (Persistent Mode)...")
        cmd = [
            "libcamera-still", "-t", "0", "--signal", "--nopreview",
            "-o", os.path.join(TEMP_DIR, "capture_.jpg"),
            "--datetime", "--quality", "95", "--width", "4608", "--height", "2592"
        ]
        # 💡 重要：setsid 確保我們能控制整個進程組
        state.process = await asyncio.create_subprocess_exec(*cmd, preexec_fn=os.setsid)
        state.last_access = time.time()

async def stop_camera():
    """關閉相機進入低功耗模式"""
    if state.process:
        print("💤 [Service] Idle limit reached. Powering off camera...")
        try:
            # 💡 重要：killpg 確保乾淨關閉，不留殘餘進程
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
    await start_camera()
    asyncio.create_task(idle_monitor())

@app.on_event("shutdown")
async def shutdown_event():
    print("🛑 [Service] Shutdown signal received. Cleaning up...")
    await stop_camera()

@app.post("/restart")
async def restart_system(mode: str = "service"):
    """
    mode='service': 僅重啟 Python 程式 (透過 systemd 重啟)
    mode='hardware': 整個 CM4 系統重新啟動 (sudo reboot)
    """
    state.last_access = time.time()
    
    # 1. 確保重啟前先把相機進程關掉，保護硬體
    await stop_camera()
    
    if mode == "hardware":
        print("🔄 [Critical] Remote Hardware REBOOT triggered!")
        # 💡 等待 2 秒讓 API 能把成功訊息回傳給 Master，然後執行重啟
        os.system("sleep 2 && sudo reboot &")
        return {"message": "CM4 Hardware is rebooting now..."}
    
    else:
        print("♻️ [Info] Remote Service RESTART requested.")
        # 如果你使用 .service，可以透過殺掉自己讓 Restart=always 機制重啟
        # 或者透過系統指令重啟服務
        os.system("sleep 2 && sudo systemctl restart dvcs_slave &")
        return {"message": "FastAPI Service is restarting..."}

@app.get("/health")
async def health():
    temp = get_cpu_temp()
    return {
        "cpu_temp": temp,
        "camera_active": state.process is not None,
        "idle_seconds": int(time.time() - state.last_access)
    }

@app.post("/take_photo")
async def take_photo(payload: dict = Body(...)):
    async with state.lock:
        state.last_access = time.time()
        
        if state.process is None:
            await start_camera()
            await asyncio.sleep(1.2) # 等待初始化

        print(f"📸 [Trigger] Signaling camera sensor...")
        state.process.send_signal(signal.SIGUSR1)
        
        await asyncio.sleep(0.5) 
        
        # 獲取最新照片
        files = [os.path.join(TEMP_DIR, f) for f in os.listdir(TEMP_DIR) if f.endswith(".jpg")]
        if not files:
            raise HTTPException(status_code=500, detail="Capture failed")
        
        latest_file = max(files, key=os.path.getmtime)
        
        light = payload.get("light", "RE")
        final_name = f"{light}_{datetime.now().strftime('%H%M%S')}.jpg"
        final_path = os.path.join(TEMP_DIR, final_name)
        os.rename(latest_file, final_path)

        return FileResponse(final_path, media_type="image/jpeg", filename=final_name)

if __name__ == "__main__":
    import uvicorn
    # 直接傳入 app 對象，減少 import 錯誤風險
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")