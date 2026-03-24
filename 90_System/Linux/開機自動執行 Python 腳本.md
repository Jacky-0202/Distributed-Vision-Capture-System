---
tags: [Pi, Systemd, StartupScript]
---
## 摘要

讓任何 Linux 設備（樹莓派、PC、伺服器）開機後自動進入專案目錄，使用虛擬環境執行 Python 腳本，
並在執行完成後自動關機，同時支援開發者遠端監控日誌。

---
## 🛠️ 步驟 1：建立 Systemd 服務檔案

`systemd` 是 Linux 的總指揮官。我們需要建立一個 `.service` 檔案來定義自動化動作。

1. **開啟編輯器**： 
```bash
sudo nano /etc/systemd/system/pds.service
```

2. **貼入以下通用內容**（請根據實際路徑修改 `{{...}}` 處）：

```ini
[Unit]
Description=PDS Universal Auto-Run Service
After=network-online.target
Wants=network-online.target

[Service]
# 1. 執行的使用者與工作目錄
User=pi
Group=pi
WorkingDirectory=/home/pi/Documents/PDS_RaspberryPI4_IOT

# 2. 關鍵：Python 執行檔
# ExecStart=/home/pi/your_project_folder/.venv/bin/python3 main.py # 指定虛擬環境中
ExecStart=/usr/bin/python3 /home/pi/Documents/PDS_RaspberryPI4_IOT/main.py

# 3. 確保 print 訊息能即時顯示在日誌中
Environment=PYTHONUNBUFFERED=1

# 4. 執行完畢不重啟
Restart=no

[Install]
WantedBy=multi-user.target
```

---
## 🛠️ 步驟 2：授權免密碼關機 (Visudo)

為了讓 Python 腳本中的 `sudo shutdown` 能順利執行而不被密碼卡住，必須設定權限。

1. **進入權限編輯器**： `sudo visudo`
2. **在檔案最底部加入這行**： `pi ALL=(ALL) NOPASSWD: /usr/sbin/shutdown`
    
    > **注意**：若使用 `systemctl poweroff`，路徑通常為 `/usr/bin/systemctl`。

---

## 🛠️ 步驟 3：部署與啟動

完成設定後，通知系統載入並執行。

1. **重新載入配置**：
```bash
sudo systemctl daemon-reload
```

2. **設定開機自啟**：
```bash
sudo systemctl enable pds.service
```

3. **立刻手動試跑**：
```bash
sudo systemctl start pds.service
```

---
## 🛠️ 步驟 4：監控與偵錯 (Log 檢視)

這是開發者最重要的「控制室」，用來確認 `print` 訊息與報錯。

- **即時監控（直播模式）**： 
```bash
journalctl -u pds.service -f
```

- **停止服務**：
```bash
sudo systemctl stop pds.service
```
    
- **取消開機自啟**：
```bash
sudo systemctl disable pds.service
```