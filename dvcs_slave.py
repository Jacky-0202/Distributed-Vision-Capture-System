import asyncio
import os
import signal
import time
import subprocess
from datetime import datetime
from fastapi import FastAPI, HTTPException, Body, BackgroundTasks
from fastapi.responses import FileResponse

app = FastAPI(title="DVCS Slave Node Service")

# ==========================================
# ⚙️ 系統配置 (Configuration)
# ==========================================
# 💡 終極測試修改：放棄 /dev/shm，直接寫入實體硬碟目錄以排除 Systemd 隔離問題
TEMP_DIR = "/home/tec/DVCS/captures"
os.makedirs(TEMP_DIR, exist_ok=True)

# 💡 重要：每一台 Slave 請根據編號手動修改此數值 (1-4)
NODE_ID = 1 

# 閒置限制 (秒)，預設 600 秒 (10 分鐘) 自動關閉相機
IDLE_LIMIT = 600 

class CameraState:
    def __init__(self):
        self.process = None       # 儲存 rpicam 進程物件
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
        print(f"🚀 [Node {NODE_ID}] Starting Camera Engine...")
        
        # 💡 使用絕對路徑，並移除容易出錯的 --datetime 參數
        cmd = [
            "/usr/bin/rpicam-still", "-t", "0", "--signal", "--nopreview",
            "-o", os.path.join(TEMP_DIR, "capture_.jpg"),
            "--quality", "95", "--width", "4608", "--height", "2592"
        ]
        
        state.process = await asyncio.create_subprocess_exec(
            *cmd, 
            preexec_fn=os.setsid,
            # 💡 把 rpicam-still 的內部報錯也導向給 Python，這樣我們才能在 journalctl 看到真正的錯誤
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE
        )
        state.last_access = time.time()

async def stop_camera():
    """關閉相機進入低功耗模式"""
    if state.process:
        print(f"💤 [Node {NODE_ID}] Idle limit reached. Powering off camera sensor...")
        try:
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
        os.system("sleep 2 && sudo systemctl restart dvcs &")
        return {"message": "Service restarting..."}

@app.post("/take_photo")
async def take_photo(background_tasks: BackgroundTasks, payload: dict = Body(...)):
    """
    執行拍照任務並依照規範重命名
    """
    async with state.lock:
        state.last_access = time.time()
        
        # 檢查相機進程是否存活
        is_alive = state.process is not None and state.process.returncode is None
        
        if not is_alive:
            print(f"⚠️ [Node {NODE_ID}] Camera engine is dead. Restarting...")
            state.process = None
            await start_camera()
            await asyncio.sleep(1.5)

        try:
            print(f"📸 [Node {NODE_ID}] Triggering capture (rpicam)...")
            state.process.send_signal(signal.SIGUSR1)
        except ProcessLookupError:
            state.process = None
            raise HTTPException(status_code=500, detail="Camera engine lost. Please try again.")
        
        # 等待硬體寫入實體硬碟 (稍微加長一點確保寫完)
        await asyncio.sleep(0.8) 
        
        files = [os.path.join(TEMP_DIR, f) for f in os.listdir(TEMP_DIR) if f.endswith(".jpg")]
        if not files:
            raise HTTPException(status_code=500, detail="Capture failed: No file generated in physical drive")
        
        latest_file = max(files, key=os.path.getmtime)
        
        light = payload.get("light", "RE")
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        final_name = f"CAM{NODE_ID}_{light}_{timestamp}.jpg"
        final_path = os.path.join(TEMP_DIR, final_name)
        
        os.rename(latest_file, final_path)
        print(f"✅ [Node {NODE_ID}] Photo saved: {final_name}")

        # 傳輸完成後在背景刪除，保護硬碟空間
        background_tasks.add_task(os.remove, final_path)

        return FileResponse(final_path, media_type="image/jpeg", filename=final_name)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")