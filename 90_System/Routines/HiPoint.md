---
tags:
---
#### 1. Master 與 PLC 通訊模組 (PLC 橋接)

- [ ] **點位表對接**：與電控工程師確認 Modbus 地址（例如：M100 是拍照觸發、D200 是相機狀態、D210 是錯誤代碼）。
- [ ] **連線類別封裝**：寫一個 Python Class 專門負責讀寫 Delta PLC 的寄存器。
- [ ] **心跳機制 (Heartbeat)**：Master 持續寫入一個數值給 PLC，PLC 若沒收到則報警（確保 Python 程式沒當掉）。
- [ ] **觸發邏輯實作**：偵測到 PLC 拍照訊號位元變為 `True` 時，啟動 Master 的分發程序。

#### 2. Master 與 Slave 通訊模組 (內部網路)

- [ ] **靜態 IP 配置**：確保 5 台 CM4 (1 Master + 4 Slaves) 的 IP 是固定的，且在同一個子網。
- [ ] **指令分發協議**：決定 Master 怎麼叫 Slave 拍照（推薦用 `gRPC` 或簡單的 `FastAPI`，因為需要回傳「拍照完成」的確認）。
- [ ] **並行控制 (Parallel)**：確保 Master 是「同時」叫 4 台 Slave 拍照，而不是一台接一台（減少循環時間/Cycle Time）。
- [ ] **狀態彙整**：4 台 Slave 都拍完且存檔成功後，Master 才回報 PLC 「任務完成」。

#### 3. Slave 拍照執行模組 (視覺端)

- [ ] **相機驅動開發**：確保 CM4 能正確抓取影像（OpenCV / Libcamera）。
- [ ] **燈源同步**：雖然 PLC 控制燈源，但 Slave 拍照的曝光時間需與燈源開啟時間匹配（需確認 PLC 燈開多久）。
- [ ] **影像存檔與命名**：根據 Master 給予的序號（如生產批號）進行檔案命名。
- [ ] **預處理 (選配)**：若有 AI 模型，Slave 需在拍照後立即進行推論。

#### 4. 日誌與監控模組 (Logging & UI)

- [ ] **全域 Log 系統**：Master 記錄所有 PLC 指令；Slave 記錄所有硬體錯誤（如：鏡頭連線失敗）。
- [ ] **LOG 自動清理**：設定 Cron job 或 Python 腳本，定期刪除 30 天前的舊 Log 或照片，避免 CM4 的 eMMC/SD 卡滿載。
- [ ] **簡單 Dashboard**：Master 網頁顯示 4 台 Slave 的在線狀態 (Ping) 與最後拍照時間。

#### 5. 重啟與異常復歸機制 (Robustness)

- [ ] **服務自動重啟**：使用 `systemd` 設定，若 Python 腳本掛掉會自動重跑。
- [ ] **硬體重啟邏輯**：
    
    - Master 偵測到 Slave 斷線 N 次 $\rightarrow$ Master 透過網路下達 `reboot` 指令。
    - PLC 偵測到 Master 沒心跳 $\rightarrow$ PLC 輸出一個硬體點位給 Master 的 GPIO 觸發重啟（或由人工重啟）。