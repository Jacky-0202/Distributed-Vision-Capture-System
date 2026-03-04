---
tags: [Pi, Burn, Emmc]
---
## 🛠️ 事前準備

### 1. 硬體

- **MicroSD 卡 & 讀卡機**：標準版 Pi 或 CM4 Lite 使用。
- **USB 數據線**：CM4 eMMC 版專用（連接電腦與載板的 Micro-USB/USB-C Slave 孔）。
- **跳線 (Jumper)**：用於短路 CM4 載板上的 **nRPIBOOT (J2)** 腳位。

### 2. 軟體 (Linux / Windows)

- **Raspberry Pi Imager**：
    
    - **Windows**: [官網下載](https://www.raspberrypi.com/software/)
    - **Linux (Debian/Ubuntu)**:

```bash
sudo apt update
sudo apt install rpi-imager
```
        
- **usbboot (rpiboot)**：
    
    - **Windows**: 下載安裝檔。
    - **Linux**: 需手動編譯（詳見下方 CM4 章節）。

---
## 📂 場景一：標準版 Pi / CM4 Lite (SD 卡)

1. **啟動 Imager**：
    
    - Linux 終端機輸入
```bash
rpi-imager
```    

2. **選擇裝置 (Choose Device)**：選取你的 Pi 型號（如 Pi 4 或 CM4）。
3. **選擇 OS**：推薦 _Raspberry Pi OS (64-bit)_。
4. **選擇儲存卡**：選取你的 MicroSD 卡。
5. **進階設定 (必做)**：

    * **Hostname**：`pi` (Imager 會自動加上 `.local`)。
    * **Enable SSH**：✅ (勾選)，並選擇 "Use password authentication"。
    * **Set username and password**：
        * Username: `???`
        * Password: `???`
    * **Configure wireless LAN**：✅ (勾選)
        * SSID: `???`
        * Password: `???`
    * **Country**：`TW`
    * **Time zone** ： `Asia/Taipei`

---

## ⚡ 場景二：CM4 eMMC 版本 (Linux 詳解)

當 CM4 使用內建 eMMC 時，Linux 電腦需要透過 `usbboot` 工具才能將其掛載。

### 第一階段：在 Linux 安裝 rpiboot 工具

若你使用 Linux，建議直接編譯官方工具：
```bash
# 安裝依賴環境
sudo apt install git libusb-1.0-0-dev pkg-config build-essential

# 下載並編譯 usbboot
git clone --depth=1 https://github.com/raspberrypi/usbboot
cd usbboot
make

# 編譯完成後會產生 rpiboot 執行檔
```

### 第二階段：讓電腦識別 eMMC

1. **硬體設置**：將 CM4 IO Board 上的 **J2 (disable eMMC Boot)** 用跳線短路。
2. **連接**：用 USB 線連接電腦與 IO Board 的 Slave 孔。
3. **供電**：插上電源。
4. **執行工具**：
```bash
rpiboot
```

>[!note] 說明 執行後，畫面上會顯示正在載入驅動。成功後，系統會自動將 eMMC 掛載為一個新的磁碟（通常在 `/dev/sdX`）。


### 第三階段：燒錄與恢復

1. **燒錄**：儲存裝置選擇剛出現的 eMMC 磁區。
```bash
rpi-imager
```

2. **斷電**：燒錄完成後，**關閉電源**。
3. **切換模式**：**務必移除 J2 的跳線**，否則會一直卡在燒錄模式。
4. **重啟**：重新上電，系統即從 eMMC 啟動。


