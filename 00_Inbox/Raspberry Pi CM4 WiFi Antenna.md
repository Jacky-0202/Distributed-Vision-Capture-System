---
tags:
---
## 摘要

- Raspberry Pi Compute Module 4 (CM4) **有兩個天線選擇**：
  1. **內建 PCB 天線**（預設，Antenna 1）
  2. **外接天線**（透過 U.FL 接頭，Antenna 2）

- 要切換到外接天線，需在設定中啟用：
```ini
dtparam=ant2
```

`dtparam=ant2` 的作用

- **ant1**：使用板載 PCB 天線（預設值）。
- **ant2**：切換到 **U.FL 外接天線**。
    
若你的 CM4 板上有 **U.FL 接頭並接上外部天線**，就需要啟用 `dtparam=ant2`。  
否則開啟 `ant2` 而沒有天線，會導致 WiFi 訊號極差或完全無法連線。

---
### 設定方式

##### 1. 編輯設定檔：
```bash
sudo nano /boot/firmware/config.txt
```

##### 2. 在合適位置加入：
```ini
dtparam=ant2
```

建議放在其他 `dtparam` 區塊附近，方便管理

##### 3. 儲存並重啟：
```
sudo reboot
```

---
## 實測對比

重啟後，觀察 `level` 的變化：

```bash
watch -n 1 cat /proc/net/wireless
```

**紀錄：**

| **測試項目**         | **內建天線 (Ant 1)** | **外接天線 (Ant 2)** | **效能提升** |
| ---------------- | ---------------- | ---------------- | -------- |
| **訊號強度 (Level)** | -60 dBm          | **-54 dBm**      | 提升 6 dBm |
| **連線品質 (Link)**  | 50 / 70          | **56 / 70**      | 提升 12%   |
| **重傳次數 (Retry)** | 12               | **0**            | **穩定**   |
| **雜訊 (Noise)**   | -256             | -256             | 無顯著差異    |
