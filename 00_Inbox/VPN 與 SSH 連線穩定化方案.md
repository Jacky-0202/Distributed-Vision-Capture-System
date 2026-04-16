---
tags:
---
## 1. SSH 維持連線 (Keep-Alive)

這是解決連線「自動跳掉」最有效的方法，透過定時發送心跳包防止連線被伺服器或防火牆中斷。

### 設定步驟

1. 在本地端終端機執行：
    
    `mkdir -p ~/.ssh && nano ~/.ssh/config`
    
2. 貼入以下設定：


```plaintext
Host 192.168.68.10
    HostName 192.168.68.10
    User hipoint
    ServerAliveInterval 60
    ServerAliveCountMax 10
```

3. 儲存離開後，設定正確權限：
    
    `chmod 600 ~/.ssh/config`
    

> [!SUCCESS] 優點
> 
> 設定後只需輸入 `ssh 192.168.68.10` 即可連線，且長時間不操作也不易中斷。

---
## 2. VPN (L2TP/IPsec) 優化設定

如果 SSH 設定後仍會斷線，通常是 VPN 本身的封裝問題。

### A. 解決 IPsec Rekeying 失敗

在連線一段時間後（通常是 1 小時）會觸發金鑰更新，若失敗則會斷線。

- **調整位置**：`Settings` > `Network` > `VPN (H200 VPN)` > `IPsec Settings`    
- **建議勾選**：
    
    - `Enable IPsec tunnel to L2TP host`
    - `Force UDP encapsulation` (穿透防火牆)

### B. MTU 數值調整 (防止封包過大)

L2TP 協議會增加封包標頭大小，若超過網路限制會導致連線不穩。

- **手動指令** (連線後執行)：


    ```bash
    # 查詢 VPN 網卡名稱 (通常為 ppp0)
    ip addr | grep ppp
    # 將 MTU 調低至 1200 或 1300
    sudo ifconfig ppp0 mtu 1200
    ```

---
## 3. 故障排除工具 (Debug)

當連線斷開時，可查看系統日誌找出具體原因：

| **指令**                            | **目的**             |
| --------------------------------- | ------------------ |
| `journalctl -u NetworkManager -f` | 即時監看 VPN 連線狀態與錯誤訊息 |
| `ssh -v hipoint@192.168.68.10`    | 以偵錯模式啟動 SSH，查看中斷原因 |

---
## 補充

### 設定步驟

1. **Settings** > **Network** > **VPN (H200 VPN)** > 點擊齒輪圖示。
2. 切換至 **IPv4** 分頁。
3. **勾選**：`Use this connection only for resources on its network` (僅將此連線用於其網路上的資源)。
4. 儲存並重新啟動 VPN。