---
tags:
---
## 1. 刪除軟體 (Removal)

在使用刪除指令前，請先確認 **套件名稱** (Package Name)，例如 Chrome 的名稱通常是 `google-chrome-stable`（而非檔案名）。

### 使用 apt 刪除 (推薦)

- **一般刪除**：保留設定檔，僅移除程式主體。
```
sudo apt remove <package_name>
```

- **徹底清除 (Purge)**：同時移除程式與相關設定檔。
```
sudo apt purge <package_name>
```

- **自動清理**：刪除不再被需要的相依套件。
```
sudo apt autoremove
```

### 使用 dpkg 刪除

- **一般刪除**：
```
sudo dpkg -r <package_name>
```

- **徹底清除**：
```
sudo dpkg -P <package_name>
```

## 2. 更新軟體 (Update)

- **更新軟體清單**：從伺服器獲取最新的套件資訊。
```
sudo apt update
```

- **升級軟體**：根據清單將過時的軟體升級到最新版。
```
sudo apt upgrade
```

> **註記**：像 Chrome 這種軟體，安裝後會自動加入 Google 的 Repo，因此之後只需跑 `apt upgrade` 即可自動更新，不需手動下載新的 `.deb`。