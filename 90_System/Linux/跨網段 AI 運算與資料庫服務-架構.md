---
tags:
  - AI
  - Networking
  - Linux
---
## 摘要

透過多層次中繼轉發，將外部請求安全導向深層內網的 **H200 (Virgo)**。
該節點透過 **SQLite 進行門票式驗證**，確保算力不被濫用，並在運算後將實體檔案存於 **本地儲存空間**，僅將結果以 **JSON 格式回傳**。

---
## 一、 節點角色與職責定義 (Node Roles)

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
## 二、跨網段 AI 推論服務配置 SOP

#### 第一階段：Server A (門戶大開)

**職責：設定公網入口與代理轉發**

- **Apache 代理檢查**： 確保 `/etc/apache2/sites-available/000-default.conf` 已寫入
    ```
    ProxyPass / http://127.0.0.1:38005/
    ProxyPassReverse / http://127.0.0.1:38005/
    ```
    
- **重啟服務**：`sudo systemctl restart apache2`
- **清理地道口**：若地道異常，先確保 Port 38005 沒有被舊連線卡死。
- **金鑰庫**：確認 `~/.ssh/authorized_keys` 已持有 Server B 的公鑰。

---
#### 第二階段：Server B (中繼站)

**職責：建立雙向 SSH 隧道與 VPN 維持**

- **免密碼驗證**：
    
    - 測試連 A：`ssh hipoint@59.125.195.194 "echo A_OK"`
    - 測試連 Virgo：`ssh hipoint@192.168.68.10 "echo Virgo_OK"`
    
- **啟動雙向地道 (autossh)**：
    
    - **向內抓取 (H200 ➡️ Server B)**： 
		```bash
		autossh -M 0 -f -N -o "ServerAliveInterval 30" -L 38005:127.0.0.1:38005 hipoint@192.168.68.10
		```
	- **向外推送 (Server B ➡️ Server A)**： 
		```bash
		autossh -M 0 -f -N -o "ServerAliveInterval 30" -R 38005:127.0.0.1:38005 hipoint@59.125.195.194
		```
        
- **在 Server B 執行這行，看看能不能在本地抓到 H200 的資料：**：
```bash
curl http://127.0.0.1:38005/model_meta
```

---
#### 第三階段：H200 / Virgo (運算核心)

**職責：啟動 GPU 推論環境與 API**

- **環境切換**：`cd /mnt/nas/hipoint/PhotoTake && conda activate phototake`
- **清理舊進程**：`sudo lsof -i :38005` (若有佔用則 kill)。
- **啟動 API**：
    ```
    nohup python -m uvicorn main_test:API --host 0.0.0.0 --port 38005 > api.log 2>&1 &
    ```
    
- **健康檢查**：`tail -f api.log` 確保看到 `Application startup complete`。