---
tags:
---
## 1. 核心機制：mDNS (Avahi/Bonjour)

要在區域網路內透過名稱尋找裝置，目標裝置（CM4/Pi）必須運行 **Avahi** 服務。

- **檢查裝置名稱 (Hostname)**： 在裝置端輸入 `hostname`。根據你的日誌顯示，目前的名稱應為 `PDS24B313`。
- **確認 Avahi 是否運行**： 樹莓派通常預設已安裝。若連不上，請手動安裝：

```bash
sudo apt update && sudo apt install avahi-daemon -y
```

---
## 2. 操作流程：從 IP 切換到 .local

#### 第一步：確認名稱是否可解析

在你的 Ubuntu 主機（連線發起端）執行：
```bash
ping pds24b313.local
```

>[!NOTE]
>- 如果 ping 得通，代表 mDNS 運作正常。
>- 名稱不分大小寫（pds24b313.local 或 PDS24B313.local 皆可）。

#### 第二步：直接登入

```bash
ssh pi@pds24b313.local
```

