---
tags: ['Linux', 'Networking', 'SSH']
---
## 一、 環境準備與套件安裝

#### 系統說明
- H200 (Virgo) 位於私有網路環境  
- 外部無法直接存取，**必須先連線 VPN**
- VPN 成功後，才能透過 **SSH** 進入內部主機

在發起連線的端點（如您的 Gateway 或跳板伺服器）安裝 L2TP VPN 所需的工具：

```bash
sudo apt update 
sudo apt install network-manager-l2tp network-manager-l2tp-gnome
# 安裝後重啟網路管理服務
sudo systemctl restart NetworkManager
```

---
## 二、 設定 VPN 連線資訊


- 進入 **Settings (設定)** > **Network (網路)** > **VPN** > 按下 **+** 新增。
- 選擇 **Layer 2 Tunneling Protocol (L2TP)**。
    
- **填入以下資訊**：
    
    - **Name**: H200 VPN (自訂名稱)
    - **Gateway (閘道器)**: `140.127.155.41`
    - **User name (使用者名稱)**: `hipoint`
    - **Password (密碼)**: `8885@Hpt#%^` (注意：這組 VPN 密碼是統一管理的，使用者**不可**更改 )
        
- **IPsec 設定** (點擊 "IPsec Settings..." 按鈕)：
    
    - 勾選 "Enable IPsec tunnel to L2TP host"。
    - **Pre-shared key (預先共用金鑰)**: `bigdata91201` (對應文件中的 IPsec public key) 。[沒用到]
        
- 儲存並開啟 VPN 開關。如果連線成功，右上角會有 VPN 圖示。

---

## 三、VPN 連線驗證

VPN 連線成功後，您就可以存取內網 IP `192.168.68.10` 。

1. **開啟終端機執行 SSH**：

```bash
ssh hipoint@192.168.68.10
```
    
2. **輸入密碼**：
    
    - 預設密碼：
```
8885@Hpt#%^
```

3. **位置：**
```
cd /mnt/nas/hipoint
```

---

## 四、H200 (Virgo) 主機資訊

| 項目 | 資訊 |
|---|---|
| 內部 IP | 192.168.68.10 |
| 使用者 | hipoint |
| 連線方式 | SSH |

---

## 五、Docker 與 GPU 驗證

```bash
docker run -it --gpus all \
  nvidia/cuda:12.8.0-runtime-ubuntu24.04 bash
```

---

## 八、儲存空間使用規範

### /scratch
- 臨時高速空間
- 30 天自動刪除

### /mnt/nas
- 長期資料儲存

### /data
- 權限限制目錄

---

## 九、公用 nas

```
https://140.127.155.115:5001/
```

帳號密碼與VPN相同。
連結到 H200  /mnt/nas