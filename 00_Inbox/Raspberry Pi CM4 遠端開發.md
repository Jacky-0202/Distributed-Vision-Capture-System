---
tags:
---
## 摘要

紀錄如何從 Ubuntu 本地端，透過 **VS Code Remote - SSH** 完美操控無螢幕的 CM4。

---
## 第一階段：連線驗證與安全設定

先確保你的 Ubuntu 電腦和樹莓派連上**同一個 WiFi**
#### 1. 測試網路發現 (mDNS)

Ubuntu 預設聽不懂 `.local` 這種 mDNS 廣播名稱
安裝 `avahi-daemon` (mDNS 翻譯蒟蒻)：
```bash
sudo apt install avahi-daemon
```

由於你在燒錄時設定了 Hostname，我們可以使用 `.local` 位址：
```bash
ping cm4-master.local
```

> **提示**：如果有回應，代表 `avahi-daemon` 運作正常，你可以不用背 IP 位址了。

#### 2. 設定 SSH 免密碼登入 (核心步驟)

為了讓 VS Code 連線更順暢，我們將 Ubuntu 的公鑰推送到 CM4：

```bash
# 如果你還沒有金鑰對，先產生一組 (一路按 Enter 即可)
ssh-keygen -t ed25519

# 將公鑰複製到 CM4
ssh-copy-id pi@cm4-master.local
```

---
## 第二階段：VS Code 遠端開發環境

#### 1. 安裝套件

1. 打開 **VS Code**。
2. 按下 `Ctrl + Shift + X` 開啟擴充功能商店。
3. 搜尋並安裝 **`Remote - SSH`** (由 Microsoft 發行)。

#### 2. 新增遠端主機

1. 按下 `Ctrl + Shift + P`，輸入 `Remote-SSH: Add New SSH Host...`。
2. 輸入連線指令：`ssh pi@cm4-master.local`。
3. 選擇儲存設定檔的路徑（通常選第一個 `/home/user/.ssh/config`）。

#### 3. 開始開發

1. 點擊 VS Code 左下角的藍色圖標 **`><`**。
2. 選擇 **`Connect to Host...`** -> **`cm4-master.local`**。
3. 第一次連線會詢問平台，選擇 **`Linux`**。
4. **開啟資料夾**：連線成功後，點擊左側「檔案總管」，選擇 `Open Folder`，路徑選 `/home/pi`。

---
## 📦 第三階段：基礎開發環境初始化

連線成功後，直接在 VS Code 內建的終端機 (`Ctrl + ~`) 執行：

```bash
# 更新系統套件庫
sudo apt update

# 安裝 Python 虛擬環境工具
sudo apt install -y python3-venv

# 建立專案資料夾與虛擬環境
mkdir ~/cm4_camera_project && cd ~/cm4_camera_project
python3 -m venv venv

# 啟動虛擬環境 (VS Code 右下角也會提示你切換解譯器)
source venv/bin/activate

# 安裝本專案核心套件
pip install fastapi uvicorn requests httpx python-multipart
```

