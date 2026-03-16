---
tags:
---
## 🗑 使用 `dd` 永久清除磁碟

⚠ **此操作會完全刪除磁碟資料且無法復原，務必先確認磁碟名稱！**

#### 1. 確認磁碟名稱

```bash
lsblk
```

找到目標磁碟，例如 `/dev/sdb`。

#### 2. 用零覆寫磁碟

```bash
sudo umount /dev/sdb
sudo dd if=/dev/zero of=/dev/sdX bs=1M status=progress
```

- `umount /dev/sdb` →  卸載分割區
- `if=/dev/zero` → 使用零填充磁碟
- `of=/dev/sdX` → 目標磁碟（如 `/dev/sdb`）
- `bs=1M` → 每次寫入 1MB
- `status=progress` → 顯示進度

#### 3. 用隨機數據覆寫（更安全）

```bash
sudo dd if=/dev/urandom of=/dev/sdb1 bs=1M status=progress
```