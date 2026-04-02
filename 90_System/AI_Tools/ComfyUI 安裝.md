---
tags: ['ComfyUI', 'Installation', 'Linux']
---
## 🛠️ Step 1. 下載核心程式 (Core)

你可以選擇直接下載 Release 版本或是透過 Git 進行管理。

### 方式 A：GitHub 直接下載

- **網址：** [ComfyUI Releases](https://github.com/comfyanonymous/ComfyUI/releases)
- **說明：** 下載對應作業系統（Windows/Linux）的壓縮檔並解壓縮。

### 方式 B：Git 複製倉庫 (推薦)

透過終端機執行以下指令，方便未來使用 `git pull` 快速更新：

```bash
mkdir ComfyUI
git clone https://github.com/comfyanonymous/ComfyUI.git
cd ComfyUI
```

---

## 🐍 Step 2. 環境配置與 Manager 安裝

建議建立 **Python 虛擬環境 (venv)** 以保持系統乾淨。

參考：[[Miniconda 建立與管理虛擬環境]]

### 1. 安裝 ComfyUI-Manager (擴充管理工具)

這是一個必裝的擴充功能，用於自動安裝缺失的節點。

```bash
cd custom_nodes
git clone https://github.com/ltdrdata/ComfyUI-Manager.git comfyui-manager
cd ..
```

### 2. 安裝必要套件 (Dependencies)

> [!IMPORTANT] **注意 CUDA 版本：** 如果你有 NVIDIA 顯卡，請務必根據你的 CUDA 版本安裝對應的 PyTorch。

```bash
# 安裝基礎必要套件
pip install -r requirements.txt

# 安裝 ComfyUI-Manager 的必要套件
pip install -r custom_nodes/comfyui-manager/requirements.txt

# 安裝 PyTorch (範例為 CUDA 13.0 版本)
pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu130
```

---

## 🚀 Step 3. 啟動 ComfyUI

啟動後即可在瀏覽器中操作介面。

- **標準啟動指令：**

    ```bash
    python main.py
    ```
    
- **預設網址：** `http://127.0.0.1:8188`
> [!TIP] **如何確認 Manager 是否成功啟動？** 啟動時請確認終端機是否有載入 `ComfyUI-Manager` 的字樣。進入網頁後，右下角選單若出現 **「Manager」** 按鈕即表示成功。