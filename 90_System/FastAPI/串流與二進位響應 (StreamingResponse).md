---
tags: [AI, StreamingResponse, BinaryData]
---
## 摘要

在處理影像、音訊或大型檔案時，傳統的 JSON 格式會因為需要進行 Base64 編碼而導致體積膨脹且處理緩慢。
直接透過 HTTP 傳輸「二進位資料 (Binary Data)」，是邊緣設備（如單板電腦）最有效率的通訊方式。

---
## 1. 為什麼要避免存成實體檔案？ (I/O 效能與硬體壽命)

在早期的開發習慣中，我們可能會這樣做：

相機拍照 -> 2. 存成 `test.jpg` 在 SD 卡 -> 3. FastAPI 讀取 `test.jpg` -> 4. 透過網路傳出。

**這個做法在分散式系統有兩個致命傷：**

- **磁碟 I/O 延遲：** 寫入實體硬碟的速度遠慢於記憶體操作，會拖慢 API 響應時間。
- **SD 卡耗損：** 如果系統每秒拍一張照片，單板電腦的 SD 卡/eMMC 很快就會因為頻繁的讀寫而提早報廢。

**最佳實務解法：**

- 完全在記憶體中處理影像矩陣（如 OpenCV 的 `imencode` 轉 bytes）。
- 或者利用 Linux 的 `/dev/shm/` (RAM Disk) 作為暫存，拍完讀取成 bytes 後立刻刪除。

---
## 2. 單次二進位響應：`Response`

這是適用於「Master 呼叫一次，Slave 拍一張照片回傳」的情境。
關鍵在於不使用預設的 JSON 回傳，而是直接回傳原始位元組 (Bytes)，並明確告訴接收方這是一張 JPEG。

```python
from fastapi import FastAPI, Response

@app.get("/capture")
async def get_single_frame():
    # 假設 image_bytes 是從相機或 RAM Disk 讀取出的二進位資料
    image_bytes = b'\xff\xd8\xff\xe0\x00\x10JFIF...' 
    
    # media_type (MIME Type) 非常重要！
    # 它告訴瀏覽器或 Master：「這不是亂碼，請用解析圖片的方式打開它」
    return Response(content=image_bytes, media_type="image/jpeg")
```

---
## 3. 真正的即時串流：`StreamingResponse`

如果您的需求變成「Master 想直接在網頁上看 Slave 相機的即時連續畫面（如監視器）」，單次的 `Response` 就不夠用了。
這時需要用到 `StreamingResponse` 配合 Python 的**生成器 (Generator, `yield`)**。它會建立一條不中斷的連線，源源不絕地把每一幀畫面推播出去（這通常稱為 MJPEG 串流）。

```python
import cv2
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()
camera = cv2.VideoCapture(0)

def generate_frames():
    """ 這是一個生成器，會不斷產生新的影像幀 """
    while True:
        success, frame = camera.read()
        if not success:
            break
        
        # 將畫面編碼為 JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        
        # 使用 multipart/x-mixed-replace 格式，這是 MJPEG 的標準規範
        # 每次 yield 就等於把一張新照片「覆蓋」到前一張照片上
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

@app.get("/video_feed")
def video_feed():
    # 將生成器放入 StreamingResponse，並設定特殊的 media_type
    return StreamingResponse(
        generate_frames(), 
        media_type="multipart/x-mixed-replace; boundary=frame"
    )
```

---
## 4. 關鍵字解析：`media_type` (MIME 類型)

不論是哪種響應，`media_type` 都是靈魂。如果沒有它，Master 收到資料只會看到一堆無意義的二進位亂碼。

- **單張圖片：** `"image/jpeg"` 或 `"image/png"`
- **即時影片流：** `"multipart/x-mixed-replace; boundary=frame"`
- **純二進位檔案（如要求對方直接下載）：** `"application/octet-stream"`

