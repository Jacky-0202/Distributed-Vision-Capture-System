---
tags:
- Git
- Version-Control
---

## 摘要

在使用 Git 記錄專案前，必須完成的身分設定與倉庫啟動動作。

---
## 身分配置 (git config)

Git 要求每一次的提交都必須綁定「作者」，以便追蹤是誰做了變動。

- **設定姓名**：
```bash
git config --global user.name "你的名字"
```

- **設定信箱**：
```bash
git config --global user.name "你的信箱"
```

- **查看配置**：
```bash
git config --list
```

> **注意**：`--global` 代表這台電腦上所有的專案都會預設使用這個身分。

---
## 初始化倉庫 (git init)

將一個普通的資料夾轉變為「Git 儲存庫」的指令。

- **指令**：

```bash
git init
```

- **背後原理**：執行後，資料夾內會出現一個隱藏的 `.git` 資料夾。這個資料夾就是「儲存庫 (Repository)」本體，所有的歷史紀錄、暫存區資訊都存在這裡。

> **注意**：如果刪除 `.git` 資料夾，該專案的所有版本歷史將會消失，變回普通資料夾。