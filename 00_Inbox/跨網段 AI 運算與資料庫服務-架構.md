---
tags: ['AI', 'Networking', 'Database']
---
## 摘要

透過多層次中繼轉發，將外部請求安全導向深層內網的 **H200 (Virgo)**。
該節點透過 **SQLite 進行門票式驗證**，確保算力不被濫用，並在運算後將實體檔案存於 **本地儲存空間**，僅將結果以 **JSON 格式回傳**。

---
## 🏗️ 一、 節點角色與職責定義 (Node Roles)

### 1. Client (客戶端)

- **角色**：請求發起者。
- **邏輯**：僅需知曉 **Server A** 的外網入口。對其而言，後端的轉發邏輯與 H200 的存在完全透明。

### 2. Server A (外網閘道 / Public Gateway)

- **角色**：大門警衛。
- **邏輯**：擁有真實外網 IP，負責接收 HTTP/HTTPS 請求並轉發至 **Server B**。
- **邊界**：第一道防線，不處理邏輯，僅做通訊協定轉發。

### 3. Server B (內網橋樑 / Intranet Bridge)

- **角色**：交通樞紐 (Router)。
- **邏輯**：負責跨越網段，將請求從物理內網導向 H200 的 VPN 網段，對接 H200 的 **Port 38000**。

### 4. H200 / Virgo (驗證與運算核心 / AI & Auth Core)

- **角色**：系統大腦。
- **介面層 (FastAPI)**：接收來自 Server B 的封包，解析 `serial_no` 與 `file` 等參數。
- **驗證層 (SQLite)**：**關鍵門禁**。比對 `Register` 資料表，若 `serial_no` 不合法則直接回傳錯誤，不啟動模型，藉此**保護 GPU 算力資源**。
- **運算層 (PyTorch/AI)**：模型（如 YOLOv9）執行推論，並產出預測座標與類別。
- **存儲層 (Local Storage/NAS)**：將原始圖、標記圖（Annotated）、VOC XML 及 CSV 統計表依目錄層級儲存於 **H200 本地路徑**。

---
## 二、 完整的資料處理生命週期 (Data Flow)

當 Client 上傳一張圖片進行 AI 分析時，邏輯路徑如下：

1. **發出請求:** Client 呼叫 Server A。
2. **中繼轉發:** `Server A` -> `Server B` -> `H200 (FastAPI:38005)`。
3. **驗證門票:** H200 查詢本地 **SQLite**：
    
    - `SELECT 1 FROM Register WHERE serial_no = %s`
    - **Invalid**: 直接中斷，保護算力。
    - **Valid**: 進入 AI 流程。
        
4. **智能運算:** H200 判斷誘蟲板顏色，調用對應 YOLO 模型。
5. **本地持久化:**
    
    - 建立資料夾：`/[Serial]/[User]/[Crop]/[Field]/...`
    - 儲存實體檔案（.jpg, .xml, .csv）。

6. **內存回傳:** 將 `detections` 數據封裝為 **JSON**，原路回傳給 Client，不寫入資料庫。