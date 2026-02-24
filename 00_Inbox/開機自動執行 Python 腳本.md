---
tags: [Pi, Systemd, StartupScript]
---
## 1. 核心元件：systemd 服務檔案

`systemd` 是 Linux 的總指揮官。我們建立一個「劇本」(Service file)，告訴它該怎麼做。

**劇本位置：** `/etc/systemd/system/pds.service`
**建立指令：** 
```bash
sudo nano /etc/systemd/system/pds.service
```

**劇本內容 (pds.service)：**
```ini
[Unit]
Description=PDS Upload Script
# 🔥 關鍵：告訴 systemd 等到網路 100% 連線後才啟動
After=network-online.target
Wants=network-online.target

[Service]
# 1. 執行這個服務的使用者 (非 root，更安全)
User=pi
Group=pi


# 2. 腳本的工作目錄 (它才能找到 upload_files)
WorkingDirectory=/home/pi

# 3. 這裡修改：指定工作目錄為你的專案資料夾
WorkingDirectory=/home/pi/rpi405x/Common_WSN

# 4. 執行
ExecStart=/usr/bin/python3 /home/pi/rpi405x/Common_WSN/WISN_V7.py

# 5. 執行完就結束，不要重啟
Restart=no

[Install]
WantedBy=multi-user.target
```

---

## 2. 核心元件：Sudo 權限 (Visudo)

**問題：** `main.py` 腳本中的 `os.system("sudo shutdown -h now")` 需要 `sudo` 權限，但 `systemd` 是以普通使用者 `hipoint` 的身分執行的。

**解法：** 我們必須明確地「只」授權 `hipoint` 可以「免密碼」執行 `shutdown` 這**一個**指令。

**編輯指令：** (這是唯一安全的方式，不要直接編輯檔案)
```bash
sudo visudo
```

**在檔案最底部加入這行：**
```ini
# 格式：[使用者] [在哪台主機]=(可切換成誰) NOPASSWD: [完整的指令路徑]
pi ALL=(ALL) NOPASSWD: /usr/sbin/shutdown
```

- **注意：** 必須是 `/usr/sbin/shutdown` 這個**完整路徑**，不能只是 `shutdown`。

---
## 3. 部署與監控 (驗收流程)

#### 3.1. 部署指令 (三部曲)

```bash
# 1. 通知 systemd 總指揮官：「嘿！我有新劇本 (pds.service) 了！」
sudo systemctl daemon-reload

# 2. 設定「開機自動啟動」 (Enable)
# (這會建立一個連結，讓 Pi 未來每次開機都自動執行)
sudo systemctl enable pds.service

# 3. 立刻試跑一次 (Start) (可選，用來測試)
sudo systemctl start pds.service
```

- 立刻停止
```bash
sudo systemctl stop pds.service
```

- 取消開機自動啟動
```bash
sudo systemctl disable pds.service
```

#### 3.2. 🔥 監控執行狀況 (看 Log)

這是你的「控制室」。這個指令可以**即時查看** `main.py` 裡面所有的 `print` 訊息。
```bash
journalctl -u pds.service -f
```
- `-u pds.service`：只看 (unit) `pds.service` 服務的日誌。
- `-f`：(Follow) 跟隨模式，像看直播一樣即時顯示最新訊息。