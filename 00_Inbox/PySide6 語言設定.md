---
tags:
---
## 摘要

本筆記記錄了如何將 PySide6 專案轉換為中英雙語界面，並實現重啟後自動載入上一次語言設定的功能。

## 1. 翻譯工具鏈工作流 (Workflow)

開發時建議 **「原始碼用英文，介面轉中文」**。

### A. 擷取文字 (lupdate)
掃描 `main.py` 與 `ui/main_window.ui`，將 `self.tr()` 標記的文字與 UI 標籤抓取至翻譯源檔。
```bash
pyside6-lupdate main.py ui/main_window.ui -ts ui/zh_TW.ts ui/en_US.ts -target-language zh_TW
```

### B. 圖形化翻譯 (Linguist)

使用官方工具進行人工翻譯。

```bash
pyside6-linguist ui/zh_TW.ts
```

- **重點**：完成翻譯後需點擊「藍色勾勾」確認，否則編譯時會被忽略。
    

### C. 發佈二進位檔 (lrelease)

將 XML 格式的 `.ts` 編譯為程式讀取的 `.qm`。

```bash
pyside6-lrelease ui/zh_TW.ts ui/en_US.ts
```
