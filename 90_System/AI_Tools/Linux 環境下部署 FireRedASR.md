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
## 第二步：建立純淨的開發環境 (Python 3.10)

參考：[[Miniconda 建立與管理虛擬環境]]
官網：[github](https://github.com/FireRedTeam/FireRedASR)

---
## 第四步：模型下載 (AED 或 LLM)

Download model files from [huggingface](https://huggingface.co/fireredteam) and place them in the folder `pretrained_models`.

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

[[FireRedASR_語音轉文字_程式碼]]
