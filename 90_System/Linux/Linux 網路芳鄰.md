---
tags: ['Linux', 'Networking', 'Samba']
---
## 摘要

將 Ubuntu 的某個資料夾（如 `~/Desktop/Common`）設為網路芳鄰 (Samba) 共享，讓 Windows 等設備可以「免密碼」存取。

---
### 1. 🧩 安裝 Samba

```bash
sudo apt update
sudo apt install samba
```

### 2. 📁 建立並設定共享資料夾

```bash
# 建立資料夾
mkdir -p ~/Desktop/Common

# [推薦] 設定安全權限 (775)，取代 777
# 775 = 擁有者(rwx), 群組(rwx), 其他人(r-x)
chmod 775 ~/Desktop/Common

# [推薦] 確保資料夾擁有者是你的帳號 (例如 tec)
sudo chown tec:tec ~/Desktop/Common
```

替換 `tec` 為你的 Ubuntu 使用者帳號


### 3. ⚙️ 編輯 Samba 設定檔

```bash
sudo nano /etc/samba/smb.conf
```

在檔案**最下方**加入以下區塊：

```ini
[Common]
    # 共享的名稱 (Windows 會看到的名字)
    comment = Ubuntu Common Share
    
    # 實際的資料夾路徑 (請填寫你的絕對路徑)
    path = /home/tec/Desktop/Common
    
    # [關鍵] 允許訪客 (免密碼)
    guest ok = yes
    
    # [關鍵] 所有訪客的讀寫操作，都強制以 'tec'  user 的身份執行
    # 這就是為什麼我們上一步要讓 'tec' 擁有資料夾權限
    force user = tec

    # 可被瀏覽 (在網路芳鄰列表看得到)
    browseable = yes
    
    # 允許寫入 (no = 唯讀)
    read only = no
```

### 4. ⚙️ Global 全域設定 (確保 Guest 生效)

> **重要：** 某些新版 Samba 需要這一步，`guest ok` 才會生效。

編輯 `smb.conf`，找到 `[global]` 區塊，在**底下**加入：

```ini
[global]
    # ... (原本的設定) ...
    
    # 當登入失敗或使用者不存在時，將其對應為 "訪客"
    map to guest = Bad User
    
    # 指定訪客帳號為 'nobody'
    guest account = nobody
```

### 5. 🧪 檢查設定檔並重啟

```bash
# 檢查 smb.conf 語法有沒有打錯
sudo testparm

# 重新啟動 Samba 服務 (smbd 是主要的)
sudo systemctl restart smbd
```

### 6. 🔥 開啟防火牆 (如有啟用 UFW)


```bash
sudo ufw allow samba
```

### 7. 🖥️ 在 Windows 連線

1. 開啟「檔案總管」
2. 在上方路徑列輸入 `\\Ubuntu的IP位址\Common`
3. 例如：`\\192.168.31.19\Common`
4. 用來分享的主機之帳號密碼輸入即可

### 8. 🧪 (Ubuntu 本機) 檢查分享是否成功

```bash
# -L 列出本機上的分享清單
# -U% 代表使用匿名/訪客身份
smbclient -L localhost -U%
```