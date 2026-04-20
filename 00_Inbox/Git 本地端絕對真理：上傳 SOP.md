---
tags:
---
## 📑 核心哲學 (Philosophy)

- **目標**：GitHub（雲端）的內容必須與電腦 A（本機）**完全同步**。
- **包含**：本機新增的要上傳、修改的要覆寫、**本機刪除的在雲端也要跟著消失**。
- **策略**：無視雲端的所有紀錄與衝突，直接以本機狀態強制定義 GitHub。

---
## 🚀 執行步驟 (在電腦 A 執行)

這套指令比一般的 `git push` 更霸道且有效，能解決所有「拒絕推送」的問題：

### 第一步：封存本地所有狀態

先將本機目前所有新增、修改、刪除的動作打包成一個提交紀錄。

```bash
git add -A
git commit -m "Local truth: Overwrite remote with local state"
```

> [!TIP] `git add -A` 與 `git add .` 的差別
> 
> `-A` (All) 會更精確地處理「檔案刪除」的動作，確保雲端也會同步刪除你本機不要的檔案。

### 第二步：強勢定義雲端 (核心指令)

使用強制推送，這會直接把 GitHub 的指針拉到跟你本機一模一樣的位置，無視任何雲端的更新。

```bash
git push origin main --force
```

_或是更安全的寫法：_ `git push origin main --force-with-lease`

### 第三步：驗證雲端狀態 (選用)

打開 GitHub 網頁版，你會發現它的檔案清單、最後更新時間與 Commit 訊息已經變得跟本機完全同步。

---

## 🛠️ 為什麼普通的 `git push` 不夠？

|**情況**|**git push 的反應**|**push --force 的反應**|
|---|---|---|
|**雲端有我不想要的檔案**|報錯 (Rejected)，要求你先 `pull`。|**直接覆蓋**，以本機為準。|
|**我刪除了歷史紀錄**|報錯 (non-fast-forward)。|**強行洗掉** 雲端的歷史紀錄。|
|**兩邊歷史對不起來**|報錯 (unrelated histories)。|**暴力對齊**，GitHub 必須聽我的。|