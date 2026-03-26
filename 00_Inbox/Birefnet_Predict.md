---
tags:
---
## 程式碼

```python
import os
import cv2
import torch
import torch.nn.functional as F
from tqdm import tqdm
from PIL import Image
from torchvision import transforms
from models.birefnet import BiRefNet
from utils import check_state_dict

# --- 設定 ---
CKPT_PATH = 'ckpts/BiRefNet-general-epoch_244.pth'
INPUT_DIR = './test_images'
OUTPUT_DIR = './results'
RESOLUTION = (1024, 1024)  # 植物細節建議使用 1024x1024
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

# 1. 初始化模型
model = BiRefNet(bb_pretrained=False)
state_dict = torch.load(CKPT_PATH, map_location='cpu')
model.load_state_dict(check_state_dict(state_dict))
model.to(DEVICE).eval()

# 2. 影像預處理
transform = transforms.Compose([
    transforms.Resize(RESOLUTION),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
])

# 3. 執行推理
os.makedirs(OUTPUT_DIR, exist_ok=True)
images = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(('.png', '.jpg'))]

for img_name in tqdm(images):
    img_path = os.path.join(INPUT_DIR, img_name)
    orig_img = Image.open(img_path).convert('RGB')
    w, h = orig_img.size
    
    input_tensor = transform(orig_img).unsqueeze(0).to(DEVICE)
    
    with torch.no_grad():
        preds = model(input_tensor)[-1]
        preds = F.interpolate(preds, size=(h, w), mode='bilinear', align_corners=True)
        mask = torch.sigmoid(preds).cpu().squeeze().numpy()
        mask = (mask * 255).astype('uint8')
    
    # 儲存黑白遮罩
    cv2.imwrite(os.path.join(OUTPUT_DIR, f"mask_{img_name}"), mask)
```

