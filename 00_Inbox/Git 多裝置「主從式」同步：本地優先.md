---
tags: ['Git', 'VersionControl']
---
## 📑 核心哲學 (Philosophy)

- **本機 (Local) = 主 (Master)**：目前操作的裝置擁有最高決策權。
- **遠端 (GitHub) = 從 (Slave)**：僅作為儲存與中繼站。
- **策略：** 接受遠端的新檔案（新增的筆記），但若同一個檔案在兩邊都被修改，**強制保留本機版本**。

---
## 📥 情境一：從雲端下載 (下載並解決衝突)

當你在別台裝置改了筆記，現在回到這台電腦，想把更新抓下來，但怕洗掉這台電腦剛寫好的內容。

### 核心指令

```
git add .
git commit -m "Save local before pull"
git pull origin main -X ours --no-edit
```

### 動作拆解

1. `git add .` & `commit`: Git 要求在合併前必須先提交本地修改。
2. `-X ours`: 這是關鍵參數。如果雲端與本地衝突，Git 會自動選擇「我們的（本機）」版本，略過雲端的修改。
3. `--no-edit`: 自動跳過合併訊息的 Vim 視窗。