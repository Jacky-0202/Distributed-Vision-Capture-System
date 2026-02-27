---
tags:
---

---
## 安裝 RustDesk

- 官方下載網址 ： [RustDesk GitHub Releases](https://github.com/rustdesk/rustdesk)

#### 安裝方式

```bash
# 方式一（需再補依賴）
sudo dpkg -i rustdesk-1.4.0-aarch64.deb
sudo apt --fix-broken install

# 方式二（推薦，會自動處理依賴）
sudo apt install ./rustdesk-1.4.0-aarch64.deb
```

---
#### 無螢幕 (Headless) 顯示修復

**目的**：讓 CM4 在未接實體螢幕時，仍能強制啟動 GPU 渲染並提供 1080p 畫面。

#### Step A: 系統層級設定 (raspi-config)

```bash
sudo raspi-config
```

1. **切換顯示架構**：`6 Advanced Options` -> `A6 Wayland` -> 選擇 **`W1 X11`**。
2. **開啟 VNC 服務**：`3 Interface Options` -> `I3 VNC` -> **`Yes`**。

#### Step B: 硬體訊號欺騙 (config.txt)

```bash
sudo nano /boot/firmware/config.txt
```

在檔案末尾加入：

```plaintext
# 強制偵測 HDMI (騙硬體通電)
hdmi_force_hotplug=1
```

#### Step C: 內核強制渲染 (cmdline.txt)

```bash
sudo nano /boot/firmware/cmdline.txt
```

在原本內容的**同一行末尾**，加入一格空格後貼上：

```plaintext
video=HDMI-A-1:1920x1080M@60D
```

> **注意**：必須保持在同一行，不可換行。

#### Step D: 重開機

---
## 重置 RustDesk ID

#### 1. 重置 Linux 系統身分 (Machine ID)

```bash
# 1. 刪除現有的 machine-id
sudo rm -f /etc/machine-id /var/lib/dbus/machine-id

# 2. 重新產生新的 machine-id
sudo dbus-uuidgen --ensure=/etc/machine-id
sudo cp /etc/machine-id /var/lib/dbus/machine-id

# 3. 檢查一下新的 ID 是否產生了
cat /etc/machine-id
```

#### 2. 徹底清除 RustDesk 殘留

```bash
sudo systemctl stop rustdesk
sudo rm -rf /etc/rustdesk
sudo rm -rf /var/lib/rustdesk
sudo rm -rf /root/.config/rustdesk
rm -rf ~/.config/rustdesk
```

#### 3. 啟動 RustDesk 服務：

```bash
sudo systemctl start rustdesk
```
