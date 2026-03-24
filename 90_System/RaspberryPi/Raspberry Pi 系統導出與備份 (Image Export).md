---
tags: [Pi, Backup, Export]
---
## 🔍 核心邏輯

導出的過程其實就是**燒錄的逆向工程**：將 SD 卡或 eMMC 的內容「讀取」出來，並儲存為電腦中的檔案。

---
## 📂 場景一：標準版 Pi  (SD 卡)

### 🖥️ Windows 環境

推薦工具：**Win32 Disk Imager** (最穩定的讀取工具)。

1. 將 SD 卡插入電腦。
2. 打開 **Win32 Disk Imager**。
3. **Image File**：點擊資料夾圖示，選擇儲存位置並手動輸入檔名（例如 `my_pi_backup.img`）。
4. **Device**：選擇 SD 卡對應的磁碟代號。
5. 點擊 **[Read]**：開始將 SD 卡內容讀出為 `.img` 檔。
    
    > [!warning] 注意 如果你的 SD 卡是 64GB，導出的檔案也會是 64GB，不論裡面放了多少資料。

### 🐧 Linux 環境

使用最強大的 `dd` 指令：

1. 插入 SD 卡並確認掛載路徑（使用 `lsblk`）。假設 SD 卡為 `/dev/sdb`。
2. 執行讀取指令：

```bash
sudo dd if=/dev/sdb of=~/pi_backup.img bs=4M status=progress
```

---
## ⚡ 場景二：CM4 eMMC 版本 (進階)

CM4 eMMC 無法直接讀取，必須先進入「虛擬磁碟模式」。

### 第一階段：掛載 eMMC

1. **硬體設置**：將 CM4 載板上的 **J2 (nRPIBOOT)** 短路。
2. **連線**：用 USB 線連接電腦 Slave 孔與供電。
3. **執行 rpiboot**：
- **Linux**: 
```bash
rpiboot
```

- **Windows**: 執行 `rpiboot.exe` 等待工具跑完，電腦會出現一個「新的磁碟」。

### 第二階段：讀取系統映像

- **Windows**: 使用 **Win32 Disk Imager**，步驟同場景一，點擊 **[Read]**。
    
- **Linux**:
    
    1. 使用 `lsblk` 找到 eMMC 對應的代號（例如 `/dev/sdc`）。
    2. 使用 `dd` 指令導出。

```bash
sudo dd if=/dev/sdb of=~/pi_backup.img bs=4M status=progress
```

---
## ✂️ 必學技巧：映像檔瘦身 (PiShrink)

如果你備份的是 64GB 或 128GB 的卡，導出的 `.img` 會非常巨大。使用 **PiShrink** 可以自動將映像檔壓縮到「僅包含實際資料」的大小。

### 在 Linux 下操作：

1. **下載腳本**：
```bash
# install pishrink（just once）
wget https://raw.githubusercontent.com/Drewsif/PiShrink/master/pishrink.sh
chmod +x pishrink.sh
```
    
2. **執行壓縮**：

```bash
sudo ./pishrink.sh -v ~/pi_backup.img
```
    
> [!success] 優點 壓縮後的 `.img` 不僅體積變小，還會自動開啟「首次開機自動擴展磁區」功能，方便你還原到不同容量的 SD 卡。

