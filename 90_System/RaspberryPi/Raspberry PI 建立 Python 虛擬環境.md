---
tags: [Pi, Python, VirtualEnv]
---
## 很簡單所以不囉唆

- **建立目錄**：
```bash
mkdir ~/project && cd ~/project
```
- **建立環境**：
```bash
python3 -m venv --system-site-packages .venv
```

> 在樹莓派 CM4 上，為了能同時使用 `pip` 安裝套件並存取系統硬體 API (如相機)，建議使用 `--system-site-packages`

- **啟動環境**：
```bash
source .venv/bin/activate
```
- **安裝套件**：
```bash
pip install fastapi uvicorn
```
