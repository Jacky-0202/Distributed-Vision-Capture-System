---
tags:
---
## 1. 環境配置 (Setup)

首先建立專屬的虛擬環境，避免套件衝突。

```bash
# 建立並進入環境
conda create -n birefnet python=3.11 -y
conda activate birefnet
```

複製倉庫與安裝依賴:

```bash
git clone https://github.com/zhengpeng7/birefnet.git
cd birefnet
pip install -r requirements.txt
```

> 注意 cuda 版本
```bash
pip uninstall torch torchvision
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu124
```

---
## 2. 權重與目錄準備

將模型權重放置於專案根目錄下的 `ckpts` 資料夾。

- **官方權重**：`BiRefNet-general-epoch_244.pth`
- **目錄結構**：
```
birefnet/
├── ckpts/
│   └── BiRefNet-general-epoch_244.pth
├── test_images/      # 存放待處理的植物原圖
└── results/          # 存放輸出的遮罩圖 (Mask)
```

> [Github](https://github.com/zhengpeng7/birefnet)

---
## 3. 無 GT 快速推理腳本 (`predict.py`)

這份腳本專門用於「生產環境」，不需要標註圖 (Ground Truth)，直接對圖片進行去背。

[[Birefnet_Predict]]
