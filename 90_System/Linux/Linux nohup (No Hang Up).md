---
tags: ['Linux', 'Scripting', 'Background_Jobs']
---
## 摘要

`nohup` 是 "No Hang Up" 的縮寫。
它的作用是讓提交的指令在用戶 **登出 (Logout)** 或 **關閉終端機 (SSH 斷線)** 後，依然能在背景繼續執行。

---
## 基本用法

最標準的執行方式是在指令最後加上 `&`，將程式丟入背景。
```bash
nohup [指令] &
```

範例：執行一個 Python 腳本
```bash
nohup python3 main.py &
```

執行後，系統會回傳一個 **PID (Process ID)**，你可以用這個 ID 來追蹤程式。

---
## 輸出處理 (Output Redirection)

預設情況下，`nohup` 會將原本顯示在螢幕上的所有訊息（標準輸出與錯誤訊息）存到當前目錄下的 `nohup.out` 檔案中。

#### 1. 自定義輸出檔案

如果你想指定輸出的 log 檔名：
```bash
nohup [指令] > my_api.log &
```

#### 2. 結合「錯誤訊息」重新導向 (推薦做法)

為了確保完整記錄（包含錯誤訊息），通常會搭配 `2>&1`：
```bash
nohup python3 main.py > output.log 2>&1 &
```

- `>` : 將標準輸出 (stdout) 導向到檔案。
- `2>&1` : 將標準錯誤 (stderr) 也導向到標準輸出（也就是同一個檔案）。

---
## 管理背景程式

程式執行後，因為你看不到它在跑，需要透過以下指令來管理：

#### 1. 查看程式是否還在跑

```bash
# 透過關鍵字搜尋
ps aux | grep [指令關鍵字]

# 例如：
ps aux | grep main
```

#### 2. 停止 (結束) 程式

找到 **PID** 後，使用 `kill` 指令：
```bash
kill [PID]

# 如果程式沒反應，強制關閉：
kill -9 [PID]
```

#### 3. 即時監看日誌內容

```bash
tail -f output.log
```
