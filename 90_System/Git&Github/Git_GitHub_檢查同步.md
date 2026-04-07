---
tags: [Git, FetchStatus, SyncCheck]
---
### 1. 最快的方法：`git status`

這是最常用的指令。它會告訴你目前的本地分支領先（Ahead）或落後（Behind）遠端分支多少個提交（Commit）。

- **前提：** 執行 `git status` 前，建議先執行 `git fetch`。
    
- **為什麼？** `git fetch` 會去雲端抓取最新的狀態資訊，但不會合併檔案，這能確保 `git status` 看到的資訊是最準確的。


```bash
git fetch origin
git status
```

**你會看到的幾種結果：**

- **Your branch is up to date:** 恭喜，兩邊完全同步。
- **Your branch is ahead of 'origin/main' by X commits:** 你有 X 個更新還沒 Push 到雲端。
- **Your branch is behind 'origin/main' by X commits:** 雲端有 X 個更新你還沒 Pull 下來。
- **Your branch and 'origin/main' have diverged:** 兩邊都有新的提交，且路徑分叉了（這通常需要進行 Merge 或 Rebase）。

