---
tags:
---
### IMX 系列參數設定

- 編輯設定檔：
```bash
sudo nano /boot/firmware/config.txt
```

- 單一相機 (IMX708)
```ini
dtoverlay=imx708
```

- 64MP 相機 (OV64A40)
```ini
camera_auto_detect=0
dtoverlay=ov64a40,cam0
```

- 雙相機 (例：IMX708 + IMX219)
```ini
camera_auto_detect=0
dtoverlay=imx708,cam0
dtoverlay=imx219,cam1.
```

> 注意：必須關閉自動偵測 `camera_auto_detect=0`

- 重啟套用設定
```bash
sudo reboot
```

---
### 查看是否讀取到相機

- 顯示當前連線的相機裝置
```bash
libcamera-hello --list-cameras
```

範例輸出：
```
tec@cm4:~ $ libcamera-hello --list-cameras
Available cameras
-----------------
0 : imx219 [3280x2464 10-bit RGGB] (/base/soc/i2c0mux/i2c@1/imx219@10)
    Modes: 'SRGGB10_CSI2P' : 640x480 [103.33 fps - (1000, 752)/1280x960 crop]
                             1640x1232 [41.85 fps - (0, 0)/3280x2464 crop]
                             1920x1080 [47.57 fps - (680, 152)/1920x2160 crop]
                             3280x2464 [21.19 fps - (0, 0)/3280x2464 crop]
           'SRGGB8' : 640x480 [103.33 fps - (1000, 752)/1280x960 crop]
                      1640x1232 [41.85 fps - (0, 0)/3280x2464 crop]
                      1920x1080 [47.57 fps - (680, 152)/1920x2160 crop]
                      3280x2464 [21.19 fps - (0, 0)/3280x2464 crop]

```