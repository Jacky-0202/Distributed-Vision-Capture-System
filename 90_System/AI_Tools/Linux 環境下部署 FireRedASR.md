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
git clone https://github.com/FireRedTeam/FireRedASR.git
cd FireRedASR
```

---
## 第二步：建立純淨的開發環境 (Python 3.10)

參考：[[Miniconda 建立與管理虛擬環境]]
官網：[github](https://github.com/FireRedTeam/FireRedASR)

要檢查 cuda version
```bash
pip3 install torch torchvision --index-url https://download.pytorch.org/whl/cu124
```

Set up Linux PATH and PYTHONPATH
```bash
export PATH=$PWD/fireredasr/:$PWD/fireredasr/utils/:$PATH
export PYTHONPATH=$PWD/:$PYTHONPATH
```

---
## 第四步：模型下載

#### AED
Download model files from [huggingface](https://huggingface.co/fireredteam) and place them in the folder `pretrained_models`.

OR:
```bash
git clone https://huggingface.co/FireRedTeam/FireRedASR2-AED
```
模型要重新下載，git 只把目錄結構載下來而已

#### VAD

```bash
pip install silero-vad pydub
```

---
## 第五步：轉檔與執行

1. m4a to wav
```bash
ffmpeg -i examples/wav/input.mp3 -ar 16000 -ac 1 -acodec pcm_s16le -f wav examples/wav/output.wav
```
pyt
2.  執行
```bash
python main.py
```

[[FireRedASR_語音轉文字_程式碼]]
