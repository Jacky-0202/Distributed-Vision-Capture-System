import asyncio
import os
import shutil
import httpx
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from datetime import datetime

app = FastAPI(title="DVCS Master - Pure API Test Mode")

# ==========================================
# ⚙️ 系統配置 (Configuration)
# ==========================================
IMAGE_BASE_DIR = "./images"
os.makedirs(IMAGE_BASE_DIR, exist_ok=True)

# Slave CM4 IP 配置 (請根據實際網路環境修改)
SLAVE_IPS = {
    1: "http://10.0.0.2:8000",
    2: "http://10.0.0.3:8000",
    3: "http://10.0.0.4:8000",
    4: "http://10.0.0.5:8000"
}

# ==========================================
# 🛰️ 核心通訊邏輯
# ==========================================

async def trigger_slave_camera(client, slave_id, light_name, folder_path):
    """指揮單個 Slave 拍照並將檔案存入 Master 本地資料夾"""
    url = f"{SLAVE_IPS[slave_id]}/take_photo"
    try:
        # 發送拍照請求
        response = await client.post(url, json={"light": light_name}, timeout=15.0)
        
        if response.status_code == 200:
            # 建立該相機的專屬目錄
            cam_dir = os.path.join(folder_path, f"cam{slave_id}")
            os.makedirs(cam_dir, exist_ok=True)
            
            # 存檔名稱範例: RE_164530.jpg
            filename = f"{light_name}_{datetime.now().strftime('%H%M%S')}.jpg"
            save_path = os.path.join(cam_dir, filename)
            
            with open(save_path, "wb") as f:
                f.write(response.content)
            return True
    except Exception as e:
        print(f"❌ Cam{slave_id} 通訊失敗: {e}")
    return False

# ==========================================
# 📑 Swagger UI 測試端點
# ==========================================

@app.post("/test/capture_all")
async def capture_all(light: str = "TEST"):
    """
    【一鍵測試】讓所有在線的 Slave 同時拍照
    """
    start_time = asyncio.get_event_loop().time()
    
    # 建立本次測試的獨立時間標記資料夾
    session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
    session_path = os.path.join(IMAGE_BASE_DIR, session_id)
    os.makedirs(session_path, exist_ok=True)

    async with httpx.AsyncClient() as client:
        # 同時發起 4 個非同步任務
        tasks = [
            trigger_slave_camera(client, s_id, light, session_path) 
            for s_id in SLAVE_IPS.keys()
        ]
        results = await asyncio.gather(*tasks)

    duration = asyncio.get_event_loop().time() - start_time
    success_count = sum(1 for r in results if r)

    return {
        "status": "completed",
        "session": session_id,
        "success_count": success_count,
        "duration_seconds": round(duration, 2),
        "path": os.path.abspath(session_path)
    }

@app.post("/test/capture_single/{cam_id}")
async def capture_single(cam_id: int, light: str = "SINGLE"):
    """
    針對單一特定相機進行拍照測試
    """
    if cam_id not in SLAVE_IPS:
        raise HTTPException(status_code=404, detail="Slave IP not configured")
    
    async with httpx.AsyncClient() as client:
        url = f"{SLAVE_IPS[cam_id]}/take_photo"
        try:
            res = await client.post(url, json={"light": light}, timeout=15.0)
            if res.status_code == 200:
                temp_file = f"temp_cam{cam_id}.jpg"
                with open(temp_file, "wb") as f:
                    f.write(res.content)
                # 直接回傳圖片供 Swagger UI 預覽
                return FileResponse(temp_file, media_type="image/jpeg")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@app.delete("/test/clear_images")
async def clear_all_images():
    """清理 Master 上的所有測試圖片檔"""
    if os.path.exists(IMAGE_BASE_DIR):
        shutil.rmtree(IMAGE_BASE_DIR)
        os.makedirs(IMAGE_BASE_DIR)
    return {"message": "All test images cleared."}

if __name__ == "__main__":
    import uvicorn
    # 啟動 Master 服務，預設 port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)