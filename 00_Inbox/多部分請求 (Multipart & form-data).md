---
tags:
---
## 摘要

在 HTTP 協定中，當我們需要透過 API 傳送「文字資料」時，通常會用 JSON 格式 (`application/json`)。但如果我們需要**同時傳送「大型檔案（如圖片、影片）」加上「文字描述（如相機 ID、拍攝時間）」**，JSON 就顯得力不從心了。

`multipart/form-data` 就像是一個分類包裹。它使用特殊的「邊界字串 (Boundary)」當作隔板，把一個 HTTP 請求的身體 (Body) 切分成好幾個部分 (Parts)。

- 第一層隔板裡：裝著純文字的相機 ID。
- 第二層隔板裡：裝著 JPEG 照片的二進位檔案。

---
## Push 架構

- **主動回報 (Event-Driven):** 適合 Slave 節點自行判斷何時該拍照（例如：外接紅外線感測器被觸發），拍完後主動用 `POST` 請求把照片上傳給 Master。
- **夾帶詮釋資料 (Metadata):** 可以一次把「圖片檔案」和「這張圖片的分析結果（例如：這是在幾點幾分拍的、有沒有偵測到人臉）」一起打包丟給伺服器，不需要分兩次 API 呼叫。

---
## FastAPI 實作核心技術

在 FastAPI 中處理多部分請求非常直覺，但必須先安裝 `python-multipart` 套件，否則伺服器無法解析這種包裹。

#### 👉 Master 端 (接收檔案)

Master 端扮演收件中心，使用 `UploadFile` 來接收上傳的資料。`UploadFile` 的好處是它支援「非同步分塊讀取 (Spooling)」，
就算 Slave 傳來 1GB 的超大影片，Master 的記憶體也不會被瞬間塞爆，而是會自動暫存在硬碟中。

```python
from fastapi import FastAPI, UploadFile, Form, File
import shutil

app = FastAPI()

# Master 提供一個接收檔案的端點 (必須使用 POST)
@app.post("/upload-photo/")
async def receive_photo(
    camera_id: int = Form(...),          # 接收純文字欄位
    file: UploadFile = File(...)         # 接收實體檔案
):
    # 將上傳的檔案儲存到 Master 的硬碟中
    file_location = f"./images/cam{camera_id}_{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    return {"info": f"成功接收相機 {camera_id} 的照片", "filename": file.filename}
```

#### 👉 Slave 端 (發送檔案)

Slave 端使用 `httpx` 客戶端，將拍攝好的照片打包成 `files` 字典，並將文字資料打包成 `data` 字典，一併發射出去。

```python
import httpx
import asyncio

async def upload_to_master():
    master_url = "http://192.168.34.188:8000/upload-photo/"
    
    # 假設我們已經在 RAM Disk 中拍好了一張照片
    photo_path = "/dev/shm/temp_snap.jpg"
    
    # 準備純文字表單資料
    form_data = {"camera_id": str(0)}
    
    # 準備檔案資料 (檔名, 檔案物件, MIME 類型)
    with open(photo_path, "rb") as f:
        files = {"file": ("snap.jpg", f, "image/jpeg")}
        
        # 發送 POST 請求
        async with httpx.AsyncClient() as client:
            response = await client.post(master_url, data=form_data, files=files)
            print(response.json())

# 執行上傳
# asyncio.run(upload_to_master())
```

