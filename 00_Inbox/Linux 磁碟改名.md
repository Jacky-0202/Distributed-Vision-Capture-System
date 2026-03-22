---
tags: ['Linux', 'Disk_Management']

---
### 1. 核心流程：看、卸、改

改名三部曲：**看**清格式與路徑 $\rightarrow$ **卸**載掛載點 $\rightarrow$ 執行**改**名指令。

```bash
# 1. 看：確認 FSTYPE 與 NAME (路徑)
lsblk -f

# 2. 卸：若已掛載 (MOUNTPOINT 有路徑)，必須先卸載
sudo umount /dev/sdxY
```

### 2. 各格式指令對照表

依據 `lsblk` 查到的 **FSTYPE** 選擇對應工具：

|**檔案系統**|**改名指令 (需 sudo)**|**長度上限**|**備註**|
|---|---|---|---|
|**ext2/3/4**|`e2label /dev/sdxY [新名稱]`|16 字元|最常用|
|**XFS**|`xfs_admin -L [新名稱] /dev/sdxY`|12 字元||
|**exFAT**|`exfatlabel /dev/sdxY [新名稱]`|15 字元|需 `exfatprogs`|
|**NTFS**|`ntfslabel /dev/sdxY [新名稱]`|32 字元||
|**FAT32**|`fatlabel /dev/sdxY [新名稱]`|11 字元|需 `dosfstools`|

### 3. 避坑指南

- **驗證結果**：改完後再次執行 `lsblk -f` 或 `blkid` 確認 LABEL 是否更新。
- **字元規範**：嚴禁 `/`，建議只用英數與底線 `_`，避免在不同系統間產生亂碼或掛載錯誤。
- **系統分區**：若要改 `/` 或 `/home`，請進 Live USB 操作，不要在系統運行時強行挑戰。