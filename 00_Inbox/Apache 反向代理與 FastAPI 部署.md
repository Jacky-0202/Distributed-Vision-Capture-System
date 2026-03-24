---
tags: ['Linux', 'WebServer', 'FastAPI']
---
## 系統架構圖

- **Client (邊緣端)**: 存取 `http://newpds.twhipoint.com/path`
- **Server A (Apache Proxy)**: 接收請求並根據路徑轉發。
- **Server B (FastAPI Backend)**: 處理運算邏輯 (`192.168.31.68:8000`)。

---
## 部署邏輯清單

## 步驟一：Server B 建立 FastAPI 測試服務

####  1-1. 安裝依賴（如果還沒安裝）：

```bash
pip install fastapi uvicorn
```

#### 1-2. 建立 `main.py`

```python
# main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/inference")
def get_inference():
    return {"msg": "Hello from Server B via Apache Proxy"}
```

#### 1-3. 啟動 FastAPI 伺服器：

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

（`--host 0.0.0.0` 是為了讓內網的 Server A 可以連進來）

---
## 步驟二：Server A 設定 Apache Proxy

#### 2-1. 啟用 Apache 模組

請先執行以下指令安裝 Apache 及其相關工具：
```
sudo apt update
sudo apt install apache2 -y
```

```bash
sudo a2enmod proxy
sudo a2enmod proxy_http
```

####  2-2. 編輯 Apache 設定檔（以 `000-default.conf` 為例）：

```bash
sudo nano /etc/apache2/sites-available/000-default.conf
```

在 `<VirtualHost *:80>` 區塊內加入以下內容：

```apache
ProxyPreserveHost On

# 將 /inference 導向 Server B
ProxyPass /inference http://192.168.35.250:8000/inference
ProxyPassReverse /inference http://192.168.35.250:8000/inference
```

> ⚠️ IP `192.168.35.250` 請改成你實際的 Server B 內網位址

告訴 Apache 「去守住這個號碼的門」。

1. 編輯埠口設定檔： `sudo nano /etc/apache2/ports.conf`
2. 在 `Listen 80` 下方增加你想要的埠口：
```
Listen 80
Listen 8000
Listen 8080  # 如果你想再增加一個 8080 埠口
```

#### 2-3. 重啟 Apache：

```bash
sudo systemctl restart apache2
```

---
##  步驟三：測試流程（邊緣端／其他機器執行）

####  在任一可以上網的電腦執行：

```bash
curl http://59.125.195.194/inference
```

應得到以下回應（代表轉發成功）：

```json
{"msg": "Hello from Server B via Apache Proxy"}
```

---

### 補充工具：Apache Logs

如果遇到錯誤，你可以查看以下 log：

```bash
# Apache 存取紀錄
sudo tail -f /var/log/apache2/access.log

# Apache 錯誤紀錄
sudo tail -f /var/log/apache2/error.log
```

---

### 成功後你就能做到：

- 邊緣設備 → 固定 IP 傳送 `/inference`
- Server A（Apache）→ 反向代理給 Server B（FastAPI）
- Server B 處理後返回 JSON 結果