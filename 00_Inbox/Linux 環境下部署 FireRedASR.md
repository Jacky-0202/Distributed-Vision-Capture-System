---
tags: ['Linux', 'Deployment', 'ASR']
---
## 第一步：系統層級的準備 (OS Level)

在 Linux (Ubuntu) 環境下，我們先確保最底層的工具都已安裝。

1. **安裝 FFmpeg** (用於音訊數位淨化與轉檔)：

```bash
sudo apt update && sudo apt install ffmpeg git -y
```

2. **建立專案根目錄**：

```bash
cd ~/Desktop/Project
git clone https://github.com/FireRedTeam/FireRedASR.git
cd FireRedASR
```

---
## 第二步：建立純淨的開發環境 (Python 3.11)

我們避開 3.12 可能的相容性問題，直接使用最穩定的 3.11。

1. **建立虛擬環境**：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
```

2. **安裝核心套件**：

```
pip install --upgrade pip
pip install -r requirements.txt
pip install funasr modelscope pydub torchaudio
```

### FireRedASR 原始碼修正 (必要)

由於官方模型權重包含訓練用的 CTC 參數，在載入時必須忽略這些不匹配的 Key 。

- **檔案路徑**：`fireredasr/models/fireredasr.py`
- **修改位置**：約第 **113 行**。    
- **修改內容**：將 `strict=True` 改為 `False`。

```python
# 修正後內容
model.load_state_dict(package["model_state_dict"], strict=False)
```

參考：[[Python 建立虛擬環境]]
參考：[[Python 函式庫管理工具-PIP]]

3.  Set up Linux PATH and PYTHONPATH

```bash
export PATH=$PWD/fireredasr/:$PWD/fireredasr/utils/:$PATH
export PYTHONPATH=$PWD/:$PYTHONPATH
```

---
## 第四步：模型下載 (AED 或 LLM)

Download model files from [huggingface](https://huggingface.co/fireredteam) and place them in the folder `pretrained_models`.

If you want to use `FireRedASR-LLM-L`, you also need to download [Qwen2-7B-Instruct](https://huggingface.co/Qwen/Qwen2-7B-Instruct) and place it in the folder `pretrained_models`. Then, go to folder `FireRedASR-LLM-L` and run `$ ln -s ../Qwen2-7B-Instruct`

---
## 第五步：轉檔與執行

1. m4a to wav
```bash
ffmpeg -i examples/wav/20260307_123655.m4a \
  -ar 16000 -ac 1 -acodec pcm_s16le examples/wav/church.wav
```

2.  執行
```bash
python FireRedASR_Speech2Text.py
```

[[FireRedASR_語音轉文字]]
