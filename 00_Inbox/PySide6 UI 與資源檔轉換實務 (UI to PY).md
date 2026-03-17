---
tags:
---
## 摘要

記錄如何將 Qt Designer 產出的 `.ui` 與 `.qrc` 檔案轉換為 Python 模組，並解決轉換後的檔案路徑與匯入問題。

---

### 1. 核心轉換指令

在終端機進入專案目錄後執行：

- **UI 檔案轉換**
```
pyside6-uic main_window.ui -o ui_main_window.py
```

- **資源檔 (圖片/圖示) 轉換**
```
pyside6-rcc resource.qrc -o resource_rc.py
```

---
### 2. 檔案放置與 Import 的大坑

轉換後，最常見的錯誤是 `ModuleNotFoundError: No module named 'resource_rc'`。

#### 🚩 問題成因

當你在 Qt Designer 中使用資源檔時，轉出來的 `ui_main_window.py` 最後幾行通常會自動加上：

```python
import resource_rc
```

如果你把 `ui_main_window.py` 放在子資料夾（例如 `ui/`），而 `resource_rc.py` 放在根目錄，Python 就會找不到它。
加上 ui 即可:
```python
import ui.resource_rc
```

#### ✅ 建議配置架構

建議將 UI 相關檔案統一管理：

```
Project/
├── main.py              # 主程式
├── ui/                  # UI 資料夾
│   ├── main_window.ui
│   ├── resource.qrc
│   ├── ui_main_window.py # 轉換出的檔案
│   └── resource_rc.py    # 轉換出的檔案
└── images/              # 原始圖片
```

#### 🛠️ 修正方式

1. **同目錄法（最簡單）**：確保 `.ui` 轉出的 `py` 與 `_rc.py` 放在同一個資料夾。
2. **自動修正指令**：在轉換時加上 `--from-imports` 參數（若你在做套件開發）：
```
pyside6-uic main_window.ui -o ui_main_window.py --from-imports
```
