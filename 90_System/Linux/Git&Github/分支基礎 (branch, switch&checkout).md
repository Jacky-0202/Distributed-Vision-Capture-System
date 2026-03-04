---
tags: [Git, Branching, SwitchCheckout]
---

## 摘要

分支（Branch）是 Git 用來隔離開發環境的指標。透過切換分支，你可以在同一個專案資料夾中，於不同的功能狀態之間快速跳轉。

---
### 分支操作 (git branch)

- **核心功能**：建立、列出或刪除開發線路。
    
- **常用指令**：
    - `git branch`：列出所有本地分支。
    - `git branch <name>`：建立新分支（但不切換）。
    - **`git branch -M main`**：將目前分支強制更名為 `main`（推送到 GitHub 前的標配動作）。
    - `git branch -d <name>`：刪除已合併的分支。
    - `git branch -D <name>`：強制刪除未合併的分支（危險操作）。

---
## 切換分支 (git switch / checkout)

- **核心功能**：移動 Git 的 `HEAD` 指標，讓工作區的檔案瞬間變成該分支的狀態。
- **常用指令**：
    
    - `git switch <branch-name>`：切換到指定分支（現代建議用法）。
    - `git switch -c <branch-name>`：**常用**。建立新分支並「立即切換」過去。

---
## 操作邏輯

1. **開闢**：當要開發新功能或修 Bug 時，先開一個新分支 `git switch -c feat-login`。
2. **開發**：在該分支上進行多次 `add` 與 `commit`，這不會影響 `main` 主線。
3. **回歸**：功能完成後，切換回主線 `git switch main` 準備進行合併。