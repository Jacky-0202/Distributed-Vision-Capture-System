---
tags: ['Linux', 'Package_Management']

---
# dpkg vs apt

## 核心差異

- **dpkg (Debian Package)**:
    
    - 屬於底層工具。
    - 只能處理「單一檔案」，**不具備**自動下載相依套件的能力。
    - 適合在沒有網路或安裝簡單套件時使用。

- **apt (Advanced Package Tool)**:
    
    - 屬於高階前端工具（底層仍是調用 dpkg）。
    - **具備自動化相依性管理**，會自動從軟體倉庫下載缺少的組件。
    - 現今 Linux 桌面與伺服器維護的標準推薦方式。

## 指令對照表

|**動作**|**dpkg 指令**|**apt 指令**|
|---|---|---|
|**安裝本地檔案**|`sudo dpkg -i <file.deb>`|`sudo apt install ./<file.deb>`|
|**列出已安裝套件**|`dpkg -l`|`apt list --installed`|
|**查詢套件資訊**|`dpkg -s <pkg_name>`|`apt show <pkg_name>`|