---
tags: ['Machine_Learning', 'Data_Science', 'Training']
---
## 1. 資料集目錄規範

為了符合 BiRefNet 內部路徑拼接邏輯（`root/task/dataset/train/im`），建議採用的結構如下：

```
~/Desktop/Project/Datasets/Matte/
└── General/              # 對應 config.task
    └── Plant/            # 你的資料集名稱
        ├── train/        # 訓練集 (至少 3000+ images/masks)
        │   ├── im/       # 原始圖 (.jpg/.png)
        │   └── gt/       # 標註圖 (必須為 .png)
        └── val/          # 驗證集
            ├── im/
            └── gt/
```

>[!TIP] 
>自動切分建議 如果只有 `train` 資料夾，請務必隨機抽樣 10% 建立 `val` 資料夾，模型才能在訓練過程中評估精準度。

---
## 2. 關鍵檔案修改 (Hack & Fix)

### A. `config.py` 設定

修改 `config.py` 確保模型能正確找到路徑並發揮 H200 效能：
```python
# 1. 系統路徑與任務
self.sys_home_dir = os.path.expanduser('~')
self.data_root_dir = os.path.join(self.sys_home_dir, 'Desktop/Project/Datasets/Matte')
self.task = 'General'

# 2. 指定資料夾名稱 (不含 /train 或 /val)
self.training_set = {'General': 'Plant'}
self.testsets = {'General': 'Plant'}

# 3. 效能最佳化
self.batch_size = 8         # H200 建議設為 8 或以上
self.size = (1024, 1024)    # 維持高解析度以捕捉植物細節
self.mixed_precision = 'bf16' # H200 強烈建議使用 bf16
```

### B. `train.py` 繞過 Backbone 下載錯誤

為了避免程式去抓取不存在的原始 Swin-L 權重（`/home/tec/weights/cv/...`），請修改 `train.py` 第 110 行：
```python
# 修改前：model = BiRefNet(bb_pretrained=True and ...)
# 修改後：
model = BiRefNet(bb_pretrained=False) # 因為稍後會載入完整權重，故此處設為 False
```

---
## 3. 啟動訓練指令

在 `birefnet` 根目錄下執行。請務必區分「讀取權重路徑」與「輸出資料夾」。
```bash
python train.py \
  --ckpt ckpts/BiRefNet-general-epoch_244.pth \
  --ckpt_dir ckpts/plant_finetune_v1 \
  --epochs 100
```

>[!IMPORTANT] 參數說明
>`--ckpt`: 起始點，載入官方預訓練權重。

