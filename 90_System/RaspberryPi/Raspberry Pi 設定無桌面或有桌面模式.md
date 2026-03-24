---
tags: [Pi, Setup, BootOptions]
---
### 1. 進入設定選單

在終端機輸入：
```bash
sudo raspi-config
```

### 2. 選單操作流程

1. 選擇 **1 System Options**。
2. 選擇 **S5 Boot / Auto Login**。
3. 在此處你可以看到四個選項：
    
    - **B1 Console**：無介面 (CLI)，需輸入帳密。
    - **B2 Console Autologin**：無介面 (CLI)，自動登入（**建議邊緣端使用**）。
    - **B3 Desktop**：有介面 (GUI)，需輸入帳密。
    - **B4 Desktop Autologin**：有介面 (GUI)，自動進入桌面。

### 3. 套用並重啟

選擇完畢後，按 `Tab` 鍵選擇 **<Finish>**，系統會詢問是否要現在重開機 (Would you like to reboot now?)，請選擇 **<Yes>**。
