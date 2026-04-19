---
tags: ['Git', 'Workflow']
---
## 📑 核心哲學 (Philosophy)

- **遠端 (GitHub) = 主 (Master)**：雲端儲存的版本才是「最終真理」。
- **本機 (Local) = 從 (Slave)**：本機的修改只是暫時的，若與雲端衝突，直接服從雲端。
- **策略：** 接受雲端的所有更新。若同一個檔案在兩邊都被修改，**自動放棄本機版本，強制保留雲端內容**。

---
## 📥 操作情境：以雲端為主進行合併

當你想更新筆記，且希望在衝突發生時，直接讓 GitHub 的內容覆蓋掉這台電腦的修改。

## 核心指令

```bash
# 1. Stage local changes
git add .
# 2. Commit local work
git commit -m "Save local before syncing with remote truth"
# 3. Pull using 'theirs' strategy
git pull origin main -X theirs --no-edit
```

### 動作拆解

1. **`git add .` & `commit`**: 雖然我們要以雲端為主，但 Git 要求必須先 Commit 本地修改才能進行合併。
2. **`-X theirs`**: **關鍵參數**。告訴 Git：「如果發生衝突，請無條件選擇 **他們的（theirs/遠端）** 版本」。
3. **`--no-edit`**: 自動產生合併紀錄，不彈出 Vim 視窗。

---
## 📤 既然「遠端是真理」，那上傳時該怎麼做？

如果遠端才是真理，你通常不需要「強制上傳」。
你應該先執行上述的 **下載並以雲端為主**，合併完後再推上去：

```bash
# 確保本機已經吸收了雲端的「真理」，再把剩下的部分推上去
git push origin main
```

---
## 🛠️ 與其他模式的對照表

|**模式**|**核心參數**|**發生衝突時誰贏？**|
|---|---|---|
|**本機優先**|`-X ours`|**這台電腦** 的內容保留，雲端衝突部分被捨棄。|
|**雲端優先**|`-X theirs`|**GitHub** 的內容保留，這台電腦衝突部分被捨棄。|
|**暴力同步**|`reset --hard`|**本機所有未推修內容直接消失**，完全變成雲端的形狀。|