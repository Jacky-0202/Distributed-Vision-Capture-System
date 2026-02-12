---
tags:
---
## 遠端下載與複製 (Clone)

將遠端（GitHub）上的整個儲存庫完整複製一份到本地電腦。

#### 核心指令：git clone

- **動作**：`git clone <遠端網址>`
- **效果**：
    
    - 會建立一個新資料夾。
    - 下載所有的檔案、所有的分支以及完整的歷史紀錄（log）。
    - **自動建立連結**：會自動執行 `remote add`，將該網址設定為預設的 `origin`。

#### 操作邏輯

1. **取得網址**：在 GitHub 專案頁面點擊綠色的 **"Code"** 按鈕，複製 SSH 網址（例如 `git@github.com:user/repo.git`）。
2. **執行複製**：在終端機輸入 `git clone git@github.com:user/repo.git`。
3. **進入專案**：`cd repo`。
4. **開始工作**：此時你已經擁有完整的 Git 環境，可以直接進行 `git status` 或 `git log`。

---
## 遠端更新同步 (Syncing Remotes)

#### 快速同步 (git pull) —— 最常用

如果你想**直接**把雲端的內容抓下來並更新你現在的檔案：

- **指令**：`git pull origin main` (假設主分支叫 main)
- **背後邏輯**：它是 `fetch` + `merge` 的連續動作。
- **適用時機**：你確定雲端的更動沒問題，且你想立刻讓本地檔案變成最新狀態。

#### 安全檢查同步 (git fetch + merge) —— 推薦專業用法

如果你不確定別人的更新會不會弄壞你的程式碼，想先「看看」：

1. **抓取資訊**：`git fetch origin`
    
    - 這時你的檔案**完全不會變動**，Git 只是把雲端的紀錄抓到本地的「隱藏區」。
        
2. **比對差異**：`git log main..origin/main`
    
    - 查看雲端比你多了哪些 Commit。
        
3. **手動合併**：`git merge origin/main`
    
    - 確認沒問題後，才把雲端紀錄併入你的檔案。