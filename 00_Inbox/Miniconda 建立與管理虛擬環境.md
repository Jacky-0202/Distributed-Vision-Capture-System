---
tags:
---
## 1. 建立環境

使用以下指令建立一個全新的環境。建議在建立時就指定 **Python 版本**，這能避免後續出現不相容的問題。

```bash
conda create --name <環境名稱> python=3.10
```

- **`<環境名稱>`**：建議使用跟專案相關的英文名稱（例如 `my_web_app` 或 `data_test`）。
- **`python=3.10`**：指定你需要的 Python 版本（例如 3.9, 3.11 等）。

## 2. 啟動環境

環境建立好之後，必須「進入」該環境才能開始工作：

```bash
conda activate <環境名稱>
```

啟動成功後，你的終端機提示字元前方應該會從 `(base)` 變成你的 `(環境名稱)`。

## 3. 在環境中安裝套件

進入環境後，你安裝的所有套件都會被限制在這個專屬空間內。你可以使用 `conda` 或 `pip` 安裝：

```bash
conda install numpy
# 或者
pip install requests
```

## 4. 退出環境

當你完成工作或想切換到其他專案時，可以退出目前環境：

```bash
conda deactivate
```

---

### 常用管理指令清單

|**功能**|**指令**|
|---|---|
|**列出所有已建立的環境**|`conda env list`|
|**查看當前環境安裝了哪些套件**|`conda list`|
|**刪除整個環境**|`conda remove --name <環境名稱> --all`|
|**複製現有的環境**|`conda create --name <新環境> --clone <舊環境>`|