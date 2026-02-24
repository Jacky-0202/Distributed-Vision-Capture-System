---
tags: [Git, RepositorySetup, WebUi]
---

## 摘要

這是將「本地代碼/筆記」推送到雲端的「容器準備」階段。對於已有本地檔案（如你的 Obsidian Vault）的專案，採取 **「空殼優先」** 原則。

---
## 🛠️ 網頁端 SOP (Web UI)

1. **進入路徑**：GitHub 右上角 **`+`** 號 $\rightarrow$ **`New repository`**。    
2. **命名規範 (Repository name)**：建議與本地資料夾同名（例如 `Sheng_Obsidian`）。
3. **隱私等級 (Public / Private)**：
    
    - **Private**：私人筆記、涉及密鑰的專案（強烈建議）。
    - **Public**：開源專案、教學文件。
        
4. **⛔ 關鍵防坑（請勿勾選）**：
    
    - **不要** 勾選 `Add a README file`。
    - **不要** 勾選 `Add .gitignore`。
    - **不要** 勾選 `Choose a license`。
    
    > **理由**：若在網頁端建立這些檔案，會導致遠端與本地擁有「不相關的歷史紀錄」，造成第一次 Push 失敗。
    
---