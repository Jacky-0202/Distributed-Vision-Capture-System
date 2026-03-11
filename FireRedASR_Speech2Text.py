import os
import torch
import datetime
import time
from pydub import AudioSegment
from funasr import AutoModel 

# 🔑 解決 PyTorch 2.4+ 安全封鎖
_original_load = torch.load
torch.load = lambda *args, **kwargs: _original_load(*args, **{**kwargs, 'weights_only': False})

from fireredasr.models.fireredasr import FireRedAsr

# ================= 參數設定 =================
ASR_DIR = os.path.abspath("pretrained_models/FireRedASR2-AED")
INPUT_WAV = "church_meeting.wav"
OUTPUT_MD = f"Church_Note_{datetime.date.today()}.md"

# 術語校正表 (根據測試結果持續更新)
# NAME_FIXES = {
#     "受刑": "受洗", "壽星": "受洗", "魏武營": "衛武營",
#     "心一": "欣儀", "子陽": "子暘", "力學": "立群"
# }

# ================= 1. 初始化引擎 =================
print(f"🚀 啟動 RTX 5070 Ti 雙引擎模式...")
asr_engine = FireRedAsr.from_pretrained("aed", ASR_DIR)
vad_engine = AutoModel(model="fsmn-vad", model_revision="v2.0.4") 

# ================= 2. VAD 智慧切片 =================
print("🔍 執行 AI VAD 掃描...")
res = vad_engine.generate(input=INPUT_WAV, max_single_segment_time=30000)
speech_chunks = res[0]['value'] 

# ================= 3. 轉錄與 Obsidian 格式化輸出 =================
audio = AudioSegment.from_wav(INPUT_WAV)

with open(OUTPUT_MD, "w", encoding="utf-8") as f:
    f.write(f"---\ntags: [教會紀錄, AI轉錄, FireRedASR]\ndate: {datetime.date.today()}\n---\n\n")
    f.write(f"# 📖 聚會逐字紀錄\n\n")
    f.write("| 時間戳 | 內容紀錄 |\n| :--- | :--- |\n")
    
    for i, ts in enumerate(speech_chunks):
        start_ms, end_ms = ts[0], ts[1]
        chunk = audio[start_ms : end_ms]
        tmp_wav = f"tmp_{i}.wav"
        chunk.export(tmp_wav, format="wav")
        
        try:
            # 💡 5070 Ti 效能全開：Beam Size 設為 15
            result = asr_engine.transcribe([f"u_{i}"], [tmp_wav], {"use_gpu": 1, "beam_size": 15})
            if result:
                text = result[0]['text'].strip()
                # for wrong, right in NAME_FIXES.items(): text = text.replace(wrong, right)
                
                # 時間戳格式化
                sec = int(start_ms // 1000)
                ts_str = "%02d:%02d:%02d" % (sec//3600, (sec%3600)//60, sec%60)
                f.write(f"| `{ts_str}` | {text} |\n")
                f.flush()
        finally:
            if os.path.exists(tmp_wav): os.remove(tmp_wav)
            torch.cuda.empty_cache()

print(f"🎉 任務大功告成！筆記已生成：{OUTPUT_MD}")