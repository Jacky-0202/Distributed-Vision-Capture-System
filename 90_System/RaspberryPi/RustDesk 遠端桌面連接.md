---
tags: [Pi, Setup, Headless]
---
# Remote Desktop (RustDesk) & Headless Setup Guide

## 1. RustDesk 安裝 (Linux 通用)

> [!TIP] 官方下載位址 [RustDesk GitHub Releases](https://github.com/rustdesk/rustdesk/releases) (請根據架構選擇 `.deb` 檔，如 `x86_64` 或 `aarch64`)

### 安裝方式

建議使用 **方式二**，因為它能自動處理依賴問題。

```bash
# 推薦方式：自動處理依賴
sudo apt update
sudo apt install ./rustdesk-1.4.0-<arch>.deb

# 備用方式：手動修復依賴
# sudo dpkg -i rustdesk-1.4.0-<arch>.deb
# sudo apt --fix-broken install
```

---

## 2. Headless 無螢幕顯示優化 (Raspberry Pi CM4 專用)

> [!WARNING] 注意事項 以下設定僅適用於使用 **Ubuntu for Raspberry Pi** 的 CM4 裝置。普通 PC 系統不適用 `config.txt` 調整。

### Step A: 系統層級設定 (raspi-config)

```bash
sudo raspi-config
```

1. **切換顯示架構**：`6 Advanced Options` -> `A6 Wayland` -> 選擇 `W1 X11`。    
2. **開啟 VNC 服務**：`3 Interface Options` -> `I3 VNC` -> `Yes`。

### Step B: 硬體訊號欺騙 (config.txt)

```bash
sudo nano /boot/firmware/config.txt
```

在檔案末尾加入：

```plaintext
# 強制偵測 HDMI (騙硬體通電，確保 GPU 啟動)
hdmi_force_hotplug=1
```

### Step C: 內核強制渲染 (cmdline.txt)

```bash
sudo nano /boot/firmware/cmdline.txt
```

在原本內容的 **同一行末尾**，加入一格空格後貼上：

```plaintext
video=HDMI-A-1:1920x1080M@60D
```

### Step D: 重啟生效

```bash
sudo reboot
```

> 如果要插入欺騙器，記得把畫面驅動改成 X11

---

## 3. 重置 RustDesk ID (複製系統後必做)

當你透過映像檔（Image）複製系統到另一台電腦時，必須重置 ID 避免衝突。

### 第一步：重置 Linux 系統身分 (Machine ID)

```bash
# 1. 刪除現有的 machine-id
sudo rm -f /etc/machine-id /var/lib/dbus/machine-id

# 2. 重新產生新的 machine-id
sudo dbus-uuidgen --ensure=/etc/machine-id
sudo cp /etc/machine-id /var/lib/dbus/machine-id

# 3. 確認 ID 已變更
cat /etc/machine-id
```

### 第二步：徹底清除 RustDesk 殘留設定

```bash
sudo systemctl stop rustdesk

# 刪除設定檔目錄
sudo rm -rf /etc/rustdesk
sudo rm -rf /var/lib/rustdesk
sudo rm -rf /root/.config/rustdesk
rm -rf ~/.config/rustdesk

# 重新啟動服務以產生新 ID
sudo systemctl start rustdesk
```

---