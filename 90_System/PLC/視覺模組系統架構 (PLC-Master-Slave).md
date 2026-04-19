---
tags: ['PLC', 'Automation']
---
## 🏗️ 系統層級圖 (Hierarchy)

1. **決策層 (The Brain): PLC**
    
    - 負責監測感測器狀態、產線時序。
    - 發送觸發訊號（Trigger Signal）給 Master。

2. **調度層 (The Controller): Master Node (CM4)**
    
    - 負責與 PLC 對接（通常透過 HTTP API、TCP Socket 或 Modbus）。
    - 管理 Slave 節點清單與連線池。
    - 彙整各節點數據（如 CPU 溫度、拍照狀態）。

3. **執行層 (The Actuator): Slave Node (CM4 + Camera)**
    
    - 接收 Master 指令並直接操作相機硬體 (`libcamera-still`)。
    - 負責影像編碼與暫存（使用 `/dev/shm` 提升速度）。

---
## 原子部件職責拆解 (Atomic Components)

### 1. PLC (主控端)

- **職責**：邏輯觸發。
- **動作**：向 Master 的 `/trigger/{id}` 或 `/trigger-all` 發送請求。

### 2. Master Node (管理中樞)

- **通訊管理**：透過 `httpx.AsyncClient` 維護高效連線池，防止併發請求時連線崩潰。
- **路由分配**：根據 `SLAVE_NODES` 設定將指令導向正確的內部 IP (10.0.0.x)。
- **數據聚合**：收集所有 Slave 的健康狀態與溫度，提供統一的監控接口。

### 3. Slave Node (影像採集點)

- **硬體控制**：封裝底層相機指令，處理曝光、解析度等硬體參數。
- **效能優化**：利用記憶體空間 (`/dev/shm`) 進行影像讀寫，保護 SD 卡壽命並降低延遲。
- **健康自檢**：提供 `/health` 或 `/status` 接口回報硬體運行參數（如 CPU 溫度）。