---
tags: [Git, Remote, Manage]
---

## 摘要

`Remote` 是本地儲存庫與遠端伺服器（如 GitHub）之間的連結。它就像是通訊錄裡的聯絡人名稱，代表一個特定的遠端地址。

---
## 核心指令

- **查看連結**：`git remote -v`
    
    - 顯示目前已設定的所有遠端地址及其對應的簡稱。
    
- **新增連結**：`git remote add <簡稱> <URL>`
    
    - 最常用的簡稱是 `origin`。
    - 例如：
```bash
git remote add origin git@github.com:tecjacky/my-project.git
```

- **移除連結**：`git remote remove <簡稱>`
    
    - 刪除與遠端的關聯，不會刪除本地或雲端的檔案，只是「斷開連結」。

---
## 操作邏輯

1. **建立雲端倉庫**：先在 GitHub 網頁上點擊 `New repository`。
2. **複製地址**：選擇 SSH 格式的網址（如 `git@github.com:...`）。
3. **本地關聯**：回到電腦終端機，執行 `git remote add origin [複製的網址]`。
4. **確認**：執行 `git remote -v` 確保 `(fetch)` 與 `(push)` 的地址都正確指向 GitHub。