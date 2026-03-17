---
tags:
---
## 系統架構簡介

在工業自動化場景中，為了不大幅更動既有的 PLC 邏輯，採用 **PLC 作為 Master（主動發送）**、**Raspberry Pi CM4 作為 Slave（被動接收）** 是一種非常穩定的整合方式。

- **Master (主站)**：台達 Delta DVP 系列 PLC
- **Slave (從站)**：Raspberry Pi CM4 (假設站號設定為 `8`)
- **實體層**：RS-485 (透過 USB 轉 RS-485 模組)
- **通訊格式**：`19200 bps, 8 Data bits, Even Parity, 1 Stop bit` (19200, 8, E, 1)

---

## 台達 PLC 端設定與手冊對照

要讓台達 PLC 扮演好 Master 的角色並與 Python 順利溝通，必須透過階梯圖寫入正確的通訊初始參數。

> [!info] 參考文件
> 以下設定對應《DVP-ES2/EX2/EC5/SS2/SA2/SX2/SE&TP 程式操作手冊》的 **通訊特殊繼電器/暫存器 (M/D)** 以及 **API 100 MODRW** 指令章節。

![[Modbus RTU 通訊實作_20260317102013.pdf]]


---
## 核心特殊暫存器 (Special Registers)

在 PLC 程式啟動時（利用 `M1002` 初始脈衝），需設定以下參數：

1. **通訊格式 (`D1120`)**
   - 目的：設定鮑率、資料位元、同位檢查等。
   - 數值：`H87` (對應 19200, 8, E, 1)。
   - 手冊位置：參考「裝置 M、D 特殊功能說明」章節中的 COM2 通訊格式設定表。
2. **通訊設定保持 (`M1120`)**
   - 目的：將 `D1120` 的設定值寫入並保持。需觸發為 `ON`。
3. **ASCII / RTU 模式切換 (`M1143`)**
   - 目的：台達預設為 ASCII，必須將 `M1143` 設為 `ON` 才能切換為業界標準的 **RTU 模式**。
4. **資料傳送指令：`MODRW` (API 100)**
   - 目的：PLC 核心的 Modbus 讀寫指令。
   - 用法：`MODRW S1 S2 S3 S4 N`
     - `S1`: 連線站號 (樹莓派的站號，即 `K8`)
     - `S2`: 功能碼 (如寫入單一暫存器為 `K6`)
     - `S3`: 寫入的 Modbus 位址 (如 `H0000` 為 D0, `H0001` 為 D1)
     - `S4`: 欲寫入的資料來源暫存器
   - 手冊位置：參考「應用指令說明」章節中的 API 100 說明。

---
## Python 通訊程式碼

```python
import serial
import time

# 1. 嚴格的 CRC-16 (Modbus) 檢查碼計算
def calculate_crc(data):
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for _ in range(8):
            if (crc & 1) != 0:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return crc.to_bytes(2, 'little')

# 2. 開啟序列埠 (參數須與 D1120 吻合)
ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=19200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_EVEN,
    stopbits=serial.STOPBITS_ONE,
    timeout=0.01 
)

MY_ID = 8 # 樹莓派的站號

def run_raw_slave():
    print(f"--- RPi CM4 Modbus Slave (ID: {MY_ID}) 啟動 ---")
    
    try:
        while True:
            if ser.in_waiting >= 8: # 0x06 寫入指令標準長度為 8 bytes
                start_recv = time.perf_counter()
                raw_data = ser.read(ser.in_waiting)
                
                # 驗證站號是否為本機
                if raw_data[0] == MY_ID:
                    payload = raw_data[:-2]
                    received_crc = raw_data[-2:]
                    
                    # 驗證 CRC 檢查碼
                    if received_crc == calculate_crc(payload):
                        func_code = raw_data[1]
                        
                        # 處理 0x06 寫入指令
                        if func_code == 0x06:
                            address = (raw_data[2] << 8) | raw_data[3]
                            value = (raw_data[4] << 8) | raw_data[5]

                            # 必須回傳 ACK 讓 PLC 知道已收到
                            ser.write(raw_data) 
                            proc_time = (time.perf_counter() - start_recv) * 1000

                            print(f"[{time.strftime('%H:%M:%S')}] 📥 接收寫入 | Addr: {address} | Val: {value} | 處理耗時: {proc_time:.2f} ms")
            
            time.sleep(0.001)

    except KeyboardInterrupt:
        print("\n停止監控")
    finally:
        ser.close()

if __name__ == "__main__":
    run_raw_slave()
```

