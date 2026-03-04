---
tags:
---
## 摘要

在同時連接 **有線網路 (eth0)** 與 **無線網路 (wlan0)** 的情況下，強制系統優先使用 Wi-Fi 進行數據傳輸（如影像上傳），並將有線網路設為備援。

---
## 1. 核心觀念：躍點數 (Metric)

Linux 路由表使用 **Metric** 值來決定優先順序：

- **規則**：Metric 數值 **越小**，優先權 **越高**。
- **現況**：預設情況下，有線網路 (100) 通常小於無線網路 (600)，因此有線會被優先使用。

---

## 2. 調整流程

### 第一步：檢查目前狀態

執行以下指令查看目前的路由表與 Metric：

```bash
ip route
```

> 你會看到類似 `default via ... dev eth0 ... metric 100` 的資訊。

### 第二步：修改設定 

#### 使用 nmcli (推薦，適用於現代 OS)

1. **找出連線名稱**：
```bash
nmcli connection show
```

2. **調低 Wi-Fi Metric (提高優先權)**：
```bash
sudo nmcli connection modify "你的_WIFI_名稱" ipv4.route-metric 50
```

3. **調高有線 Metric (降低優先權)**：
```bash
sudo nmcli connection modify "你的_有線_名稱" ipv4.route-metric 1000
```

4. **立即生效**： 
```bash
sudo systemctl restart NetworkManager
```
