---
tags: ['Python', 'Linux', 'RaspberryPi']
---
## 摘要

本文記錄如何在 Python 環境中安裝 PySide6，並啟動內建的圖形化介面設計工具 Qt Designer，特別收錄了樹莓派 (Raspberry Pi) 的環境補丁。

---
### 1. 前置準備 (Installation)

PySide6 安裝後會自動包含 **Qt Designer**。

- **安裝指令：**
```
pip install PySide6
```
    
- **核心檔案位置：** 安裝完成後，在 Python 目錄下的 `Scripts` 資料夾內可以找到：

    - `designer.exe`：Qt Designer 主程式。
    - `pyside6-uic`：將 `.ui` 檔案轉換為 `.py` 程式碼的工具。

---
### 2. 啟動 Qt Designer

#### 方法一：終端機直接執行 (推薦)

在已安裝 PySide6 的環境下，直接輸入：
```bash
pyside6-designer
```

#### 方法二：手動尋找執行檔

若命令列失效，可前往 Python 的 `site-packages` 路徑尋找： `.../site-packages/PySide6/designer.exe`

---
### 3. 樹梅派 (Raspberry Pi) 環境補丁

> [!warning] 必備依賴 在 Raspberry Pi 或 Linux 環境下啟動 Designer 時，若遇到庫文件缺失（如 `xcb` 錯誤），須執行以下指令安裝必要的系統依賴：

```bash
sudo apt update
sudo apt install -y \
  libxcb-cursor0 \
  libxkbcommon-x11-0 \
  libxcb-icccm4 \
  libxcb-image0 \
  libxcb-keysyms1 \
  libxcb-render-util0 \
  libxcb-xinerama0 \
  libxcb-xfixes0
```

