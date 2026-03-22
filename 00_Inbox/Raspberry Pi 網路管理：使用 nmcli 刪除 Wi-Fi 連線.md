---
tags: ['RaspberryPi', 'NetworkManager', 'Linux']
---
在較新版本的 Raspberry Pi OS (Bookworm+) 中，系統預設使用 **NetworkManager**。使用 `nmcli` 工具可以快速清理不再需要的網路設定檔。

## 1. 查詢目前的連線清單

在刪除之前，先確認連線的精確名稱（NAME）或 UUID。

```
nmcli connection show
```

_註：如果名稱包含空格，刪除時需使用引號括起來。_

## 2. 刪除指定連線

使用連線名稱（SSID）進行刪除：

```
sudo nmcli connection delete "HiPoint"
```

或是使用該連線的 **UUID**（最精確的方法）：

```
sudo nmcli connection delete 4f12314c-6119-4831-9924-1a947f6be201
```

## 3. 批次刪除多個連線

若要一次清理多個過期的網路設定，可以用空格隔開：

```
sudo nmcli connection delete "HiPoint" "preconfigured"
```

## 4. 驗證是否刪除成功

再次執行顯示指令，確認該連線已不在清單中：

```
nmcli connection show
```