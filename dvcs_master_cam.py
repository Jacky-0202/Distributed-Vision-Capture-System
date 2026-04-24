import asyncio
import os
import shutil
import httpx
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from datetime import datetime

app = FastAPI(title="DVCS Master Control Hub")

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

# ==========================================
# 🛰️ 核心 API 功能
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
            # 預覽統一發送標記為 PREVIEW
            url = f"{SLAVE_IPS[cam_id]}/take_photo"
            res = await client.post(url, json={"light": "PREVIEW"}, timeout=15.0)
            
            if res.status_code == 200:
                # 儲存於 images 根目錄，檔名固定以便覆寫
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
    【2. 單機拍照】輸入光源並拍照，檔案扁平化存於 images 根目錄
    """
    if cam_id not in SLAVE_IPS:
        raise HTTPException(status_code=404, detail="Slave IP not configured")
    
    async with httpx.AsyncClient() as client:
        try:
            url = f"{SLAVE_IPS[cam_id]}/take_photo"
            res = await client.post(url, json={"light": light}, timeout=15.0)
            
            if res.status_code == 200:
                # 統一命名格式: CAM1_RE_20260424_083015.jpg
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
    【3. 打包下載】檢查並刪除舊的暫存檔後，將整個 images/ 資料夾內容打包成 .zip
    """
    if not os.path.exists(IMAGE_BASE_DIR) or not os.listdir(IMAGE_BASE_DIR):
        raise HTTPException(status_code=404, detail="No images found to backup")
    
    zip_base_name = "dvcs_images_archive"
    final_zip_file = f"{zip_base_name}.zip"

    # 💡 關鍵功能：檢查並刪除舊的暫存 .zip
    if os.path.exists(final_zip_file):
        try:
            os.remove(final_zip_file)
            print(f"🗑️ [System] Old temporary file {final_zip_file} deleted.")
        except Exception as e:
            print(f"⚠️ [Warning] Could not delete old zip: {e}")
    
    # 打包 images 資料夾下所有內容
    shutil.make_archive(zip_base_name, 'zip', IMAGE_BASE_DIR)
    
    download_filename = f"DVCS_Backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip"
    
    return FileResponse(
        final_zip_file, 
        media_type="application/zip", 
        filename=download_filename
    )

@app.delete("/system/cleanup")
async def cleanup_storage():
    """
    【4. 清理空間】刪除 ./images 目錄下所有照片檔案
    """
    try:
        if os.path.exists(IMAGE_BASE_DIR):
            # 刪除目錄下所有檔案但不刪除目錄本身
            for file in os.listdir(IMAGE_BASE_DIR):
                file_path = os.path.join(IMAGE_BASE_DIR, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
            return {"message": "All images in root directory cleared successfully."}
        else:
            return {"message": "Directory does not exist, nothing to clear."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cleanup failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    # 啟動 Master 服務
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")