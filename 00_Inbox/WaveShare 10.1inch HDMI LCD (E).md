---
tags:
---
## 摘要

本筆記彙整了樹莓派操作介面優化及 WaveShare 10.1 吋觸控螢幕（E 型號）的校正設定。
參考網址
1. [微雪官網](https://www.waveshare.com/10.1inch-hdmi-lcd-e.htm?srsltid=AfmBOorqqgbz2dv8IW_p7-iXy28kUPVqWyvWyAWYaiD1d4WuZWRB1nVH)
2. [wiki](https://www.waveshare.com/wiki/10.1inch_HDMI_LCD_(E))

## 1. 操作界面縮放 (UI Scaling)
若覺得開始功能表或工作列圖示太小，可依序調整：

#### 工作列與圖示
1. **右鍵點擊**工作列 -> **Panel Settings** (面板設定)。
2. **Geometry** (幾何圖形) 分頁：調整 **Height** (高度) 為 `48` 或 `64`。
3. **Appearance** (外觀) 分頁：確保 **Icon size** 隨之調整。

#### 系統全域縮放 (高解析度建議)
- **Menu** -> **Preferences** -> **Screen Configuration**。
- 對著顯示器點擊右鍵 -> **Scale** -> 選擇 `1.5x` 或 `2x`。

---
## 2. 螢幕硬體解析度配置
確保 `/boot/config.txt` (或 `/boot/firmware/config.txt`) 已宣告正確解析度，避免觸控偏移。

```text
# 穩定觸控晶片供電
max_usb_current=1
hdmi_force_hotplug=1
config_hdmi_boost=10

# 強制 1024x600 解析度設定
hdmi_group=2
hdmi_mode=87
hdmi_cvt 1024 600 60 6 0 0 0
hdmi_drive=1
```

---
## 3. 觸控坐標校正 (Libinput Matrix)

針對 `WaveShare WS170120` 在 X11 環境下的校正，由於系統預設使用 `libinput` 驅動，需使用矩陣 (Matrix) 設定。

在進行校正前，需安裝相關驅動與校正工具 :
```bash
# 安裝 X11 驅動（雖然系統可能預設使用 libinput，但校正工具依賴此驅動）
sudo apt-get update
sudo apt-get install xserver-xorg-input-evdev

# 安裝觸控校正工具
sudo apt-get install xinput-calibrator
```

#### 執行校正：
在桌面環境的終端機輸入 `xinput_calibrator`

#### 設定檔路徑

`/etc/X11/xorg.conf.d/99-calibration.conf`

#### 設定內容

```
Section "InputClass"
	Identifier	"calibration"
	MatchProduct	"WaveShare WS170120"
	# 由 MinX=1051, MaxX=64324, MinY=2221, MaxY=63969 計算而來
	Option	"CalibrationMatrix"	"1.0357 0.0000 -0.0166 0.0000 1.0613 -0.0359 0.0000 0.0000 1.0000"
EndSection
```

#### 重開機
```bash
sudo reboot
```

---
## 4. 常用檢查指令

- **確認驅動屬性**：
    ```
    xinput list-props "WaveShare WS170120"
    ```
    
- **檢查 Xorg 日誌**（確認設定檔是否載入）：
    ```
    grep -E "Using config|calibration" /var/log/Xorg.0.log
    ```
    
- **查看目前 Session 類型** (X11 或 Wayland)：
    ```
    echo $XDG_SESSION_TYPE
    ```

>備註
>若未來將螢幕旋轉，觸控矩陣需重新計算或調整 `SwapXY` / `Invert` 參數。  
>此校正僅對應當前 1024x768 解析度配置。