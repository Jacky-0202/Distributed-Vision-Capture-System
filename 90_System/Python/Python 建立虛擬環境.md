---
tags:
- Virtual-Environment
- Project-Setup
- Python
---

## 進入專案目錄

```
cd /path/to/your/project
```

請先切換至你欲建立虛擬環境的專案資料夾

---
## 建立虛擬環境

```bash
python3 -m venv .venv
```

- `env` 為虛擬環境名稱，可自訂為 `venv`, `env310`, `project_env` 等
- 建立後目錄結構如下：
```
env/
├── bin/           # 執行虛擬環境的腳本（Linux 執行啟動用）
├── include/       # C headers（for native 模組）
├── lib/           # Python 安裝與套件
└── pyvenv.cfg     # 環境組態檔案
```

---
## 啟動與停用虛擬環境

#### 啟動虛擬環境

linux:
```bash
source .venv/bin/activate
```

windows:
```bash
.venv\Scripts\activate
```

啟動後，你會在終端機提示前方看到類似：

```bash
(env) user@hostname:/path/to/project$
```

代表虛擬環境已成功啟用。

參考：[[Python 函式庫管理工具-PIP]]

#### 停用虛擬環境

```bash
deactivate
```
執行後將會離開虛擬環境，回到系統預設的 Python 解譯器。