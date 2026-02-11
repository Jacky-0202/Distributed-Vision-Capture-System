---
tags:
- Obsidian
- Git
- Version-Control
---

## STEP1. 建立過濾器 (`.gitignore`)

通常只要過濾此檔案
```bash
.obsidian/workspace.json
```

參考：[[忽略規則設定 (.gitignore)]]

---
## STEP2. 本地倉庫初始化 (Terminal)

參考：[[環境配置與初始化 (init, config)]]

---
## STEP3. 紀錄到儲存庫

參考：[[變更紀錄的藝術 (add, commit)]]

---
## STEP4. 建立 GitHub 遠端倉庫

參考：[[GitHub_建立遠端倉庫流程]]

---
## STEP5. 推送到雲端

```bash
git branch -M main
git remote add origin https://github.com/Jacky-0202/Sheng_Obsidian_Vault.git
git push -u origin main
```

參考：[[遠端倉庫管理 (remote)]]
參考：[[分支基礎 (branch, switch&checkout)]]
參考：[[數據傳輸三劍客 (push, pull, fetch)]]