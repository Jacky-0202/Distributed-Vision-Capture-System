---
tags: [Linux, Chmod, Permissions]
---
## 👤 1. chown (Change Owner) —— 「這是誰的？」

當你從 `rpiboot` 導出映像檔或是從 root 帳號建立檔案時，普通使用者（如 `pi`）可能無法讀寫，這時就需要更改擁有者。

### 基本語法

```bash
sudo chown [使用者]:[群組] [檔案路徑]
```

### 常用範例

- **更改擁有者**：將 `data.img` 的擁有者改為 `tec`。
   
```bash
sudo chown tec pi_backup.img
```
    
- **更改擁有者與群組**：同時將擁有者與群組都改為 `tec`。

```bash
sudo chown tec:tec pi_backup.img
```

- **遞迴更改 (資料夾)**：將整個目錄及其下的所有檔案都改給 `tec`。

```bash
sudo chown -R tec:tec  /home/pi/my_project
```

---
## 🔑 2. chmod (Change Mode) —— 「能對它做什麼？」

如果你想控制檔案是否可以被 **讀取 (r)**、**寫入 (w)** 或 **執行 (x)**，就要用 `chmod`。

### 數字表示法 (最常用)

權限由三個數字組成，分別代表：**擁有者 (User)** / **群組 (Group)** / **其他人 (Others)**。

- **4**: Read (讀)
- **2**: Write (寫)
- **1**: Execute (執行)
- **0**: 無權限

|**數字**|**權限 (rwx)**|**說明**|
|---|---|---|
|**7**|`rwx`|全部權限 (4+2+1)|
|**6**|`rw-`|可讀寫，不可執行 (4+2)|
|**5**|`r-x`|可讀與執行 (4+1)|
|**4**|`r--`|只讀|

#### 範例：

- **設定為最高權限 (不安全，慎用)**：
```bash
chmod 777 script.sh
```
    
- **標準設定 (擁有者全開，其他人唯讀)**：

```bash
chmod 755 script.sh
```