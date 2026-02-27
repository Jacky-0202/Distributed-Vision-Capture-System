---
tags:
---
## 1. 樹莓派端 (Server) 準備

在連線之前，必須確保 CM4 的 VNC 服務已開啟：

- **指令路徑**：`sudo raspi-config` -> `Interface Options` -> `VNC` -> `Yes`。
- **顯示架構確認**：若為最新版 OS (Bookworm)，建議維持 `Wayland` 開啟（若 RealVNC 連線黑屏，才考慮切換回 `X11`）。

---
## 2. Ubuntu 端 (Client) 安裝

在你的開發主機（Ubuntu）上安裝 RealVNC Viewer：

- **下載位址**：[RealVNC 官網](https://www.realvnc.com/en/connect/download/?lai_sr=0-4&lai_sl=l&lai_p=1&lai_na=6113&lai_vid=pXDqWaWNGFj2X)。
- **安裝指令** (假設下載的是 .deb 檔)：
```bash
sudo dpkg -i <下載的檔案名稱>.deb
```


---
## 3. 建立連線

1. **取得 IP**：在 CM4 終端機輸入 `hostname -I`（目前確認為 `192.168.34.144`）。
    
2. **開啟連線**：
    
    - 啟動 Ubuntu 的 RealVNC Viewer。
    - 在上方網址列輸入 CM4 的 IP 位址並按回車。
    - **認證**：輸入 Raspberry Pi Imager 設定的 `Username` (預設為 `pi`) 與 `Password`。

> 要付費才有遠端傳輸檔案的功能...當然 scp 也可以實現功能但就不純粹了...