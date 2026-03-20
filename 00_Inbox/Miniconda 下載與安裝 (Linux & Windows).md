---
tags:
---
## 🐧 Linux 安裝步驟

在 Linux (如 Ubuntu, Raspberry Pi OS) 中，通常建議使用終端機（Terminal）進行腳本安裝，這最為高效。

### 1. 下載安裝腳本

打開終端機，使用 `wget` 下載最新的 Miniconda 安裝檔：

```bash
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
```

> [!NOTE] 提示 如果你的裝置是 Raspberry Pi (ARM 架構)，請將檔名改為 `Miniconda3-latest-Linux-aarch64.sh`。

### 2. 執行安裝程式

使用 `bash` 執行下載好的檔案：

```bash
bash Miniconda3-latest-Linux-x86_64.sh
```

- **閱讀條款**：按住 `Enter` 捲動，直到看到問你是否接受條款，輸入 `yes`。
- **安裝路徑**：預設通常在 `~/miniconda3`，直接按 `Enter` 即可。
- **初始化**：最後會問是否要執行 `conda init`，請輸入 **`yes`**。

### 3. 套用變更

安裝完成後，執行以下指令讓環境變數立即生效：

```bash
source ~/.bashrc
```

---

## 🪟 Windows 安裝步驟

Windows 使用圖形化安裝程式（GUI），操作相對直覺。

### 1. 下載安裝檔

前往 [Miniconda 官網下載頁面](https://docs.conda.io/en/latest/miniconda.html)，選擇 **Windows 64-bit** 的 `.exe` 檔案。

### 2. 執行安裝精靈

雙擊執行的 `.exe` 檔，並注意以下設定：

- **Select Installation Type**：建議選 **Just Me (recommended)**。
- **Choose Install Location**：預設路徑即可（路徑中盡量不要有空格或中文字）。
- **Advanced Installation Options** (關鍵！)：
    
    - **不要** 勾選 "Add Miniconda3 to my PATH" (避免跟系統其他 Python 衝突)。
    - **勾選** "Register Miniconda3 as my default Python"。

### 3. 如何啟動

安裝完後，請在 Windows 開始功能表搜尋並開啟 **「Anaconda Prompt (miniconda3)」**，這是一個已經設定好 Conda 環境的特殊命令提示字元。

---
## ✅ 安裝後的驗證與基礎設定

無論在哪個系統，安裝完後請先執行以下指令確保一切正常：

1. **檢查版本**：
```
conda --version
```

2. **更新 Conda 本體**：
```
conda update conda
```

3. **防止啟動終端機就自動進入 base 環境** (選配)： 如果你不希望每次打開終端機都看到 `(base)` 字樣，可以關閉自動啟動：
```
conda config --set auto_activate_base false
```

