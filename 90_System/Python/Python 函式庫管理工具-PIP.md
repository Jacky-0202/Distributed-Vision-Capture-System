---
tags:
- requirements-management
- pip
- Python
---

## **安裝 pip**

在 **一般環境** 或 **虛擬環境** 中都可以使用 `pip` 來管理 Python 套件。若系統尚未安裝 `pip`，可以使用以下方式安裝：

#### Windows/Linux

- 確保 `Python` 已安裝：
```bash
python --version
```
	請看 [[Python 安裝]]

- 更新 `pip`：

linux:
```bash
pip install --upgrade pip
```
windows:
```bash
python.exe -m pip install --upgrade pip
```

---
## 一般環境中使用 pip

當沒有啟動虛擬環境時，`pip` 會直接影響系統的全域 Python 環境

- 安裝套件
	```bash
	pip install package_name
	```

- 安裝特定版本的套件
	```bash
	pip install package_name==版本號
	```

- 更新已安裝的套件
	```bash
	pip install --upgrade package_name
	```

- 移除套件
	```bash
	pip uninstall package_name
	```

- 查看套件版本
	```bash
	pip show PySide6

	#or linux
	pip show matplotlib | grep ^Version
	```

---
## 在虛擬環境中使用 pip

當進入 **虛擬環境** 後，`pip` 會在該環境內運行，不會影響全域 Python 安裝

- 啟動虛擬環境
	請看 [[Python 虛擬環境]]

- 虛擬環境中使用 pip
	虛擬環境中的 `pip` 使用方式與一般環境相同

---
## 導出必要套件

- 導出 `requirements.txt`
	`requirements.txt` 是 Python 環境中的 **依賴管理文件**，通常用於記錄與安裝專案所需的所有套件
```bash
pip freeze > requirements.txt
```

- 安裝 `requirements.txt`
	當我們需要在新環境中安裝相同的依賴時，可以執行：
```bash
pip install -r requirements.txt
```

---
## 還原環境

```bash
pip freeze > temp_requirements.txt && pip uninstall -r temp_requirements.txt -y
```