---
tags: ['Linux_Tools', 'Screenshot']
---
## 🛠️ 如何下載與安裝

在 Ubuntu 上，你有幾種安裝方式，建議優先使用 `apt` 進行安裝：

### 1. 使用官方套件庫 (推薦)

這是最穩定且整合度最高的方式：

```bash
sudo apt update
sudo apt install flameshot
```

### 2. 使用 Snap 或 Flatpak (若需要最新版本)

如果你想要使用最新發佈的功能，可以使用以下指令：

- **Snap:** `sudo snap install flameshot`
- **Flatpak:** `flatpak install flathub org.flameshot.Flameshot`

### 3. 其他系統 (Windows / macOS)

可以前往 [Flameshot GitHub Releases](https://github.com/flameshot-org/flameshot/releases) 頁面下載 `.exe` 或 `.dmg` 安裝檔。

---
## ⌨️ 核心快捷鍵與操作

當你啟動 Flameshot 進入截圖模式後（通常指令是 `flameshot gui`），可以使用以下快捷鍵快速操作：

### 基礎操作

|**快捷鍵**|**功能說明**|
|---|---|
|**Enter / Ctrl + C**|儲存截圖至剪貼簿|
|**Ctrl + S**|儲存截圖為檔案|
|**Esc**|退出截圖模式|
|**Ctrl + Z**|復原上一個標註動作|
|**右鍵點擊**|隱藏/顯示側邊設定面板（可調整線條粗細、顏色等）|

---
## 💡 進階技巧：設定系統快捷鍵

在 Ubuntu 中，預設按 `PrtSc` 會啟動系統內建截圖。若要讓它啟動 Flameshot，請依照以下步驟設定：

1. 開啟 **Settings (設定)** -> **Keyboard (鍵盤)** -> **Keyboard Shortcuts (鍵盤快捷鍵)**。
2. 點擊 **View and Customize Shortcuts** -> **Custom Shortcuts (自訂快捷鍵)**。
3. 點擊 **+** 號新增：
    
    - **Name**: `Flameshot GUI`
    - **Command**: `flameshot gui`
    - **Shortcut**: 設定為 `PrtSc` (或你喜歡的組合鍵)。
        
4. 系統可能會提示該鍵已在使用中，選擇「Replace」即可。