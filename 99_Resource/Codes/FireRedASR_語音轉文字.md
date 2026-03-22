---
tags:
---
## 程式碼

```python
import os
import time
import torch
import datetime
import argparse

from funasr import AutoModel
from pydub import AudioSegment
from fireredasr.models.fireredasr import FireRedAsr

# Workaround for PyTorch 2.4+ security restrictions on loading untrusted models
_original_load = torch.load
torch.load = lambda *args, **kwargs: _original_load(*args, **{**kwargs, 'weights_only': False})

def main():
    # Setup command line argument parsing
    parser = argparse.ArgumentParser(description="FireRedASR + FunASR VAD Transcription Tool")
    parser.add_argument("input", type=str, help="Path to the input audio file (e.g., church.wav)")
    parser.add_argument("--output", type=str, default=None, help="Specific output filename (optional)")
    parser.add_argument("--beam", type=int, default=15, help="Beam size for ASR decoding (default: 15)")
    args = parser.parse_args()

    # Model directory path
    ASR_DIR = os.path.abspath("pretrained_models/FireRedASR2-AED")
    INPUT_WAV = args.input
    
    # Check if input file exists
    if not os.path.exists(INPUT_WAV):
        print(f"Error: File not found at {INPUT_WAV}")
        return

    # Create 'output' directory if it doesn't exist
    OUTPUT_DIR = "output"
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Determine the output filename
    if args.output:
        # If output filename is provided, ensure it has .txt extension
        filename = args.output if args.output.endswith(".txt") else f"{args.output}.txt"
    else:
        # Default: Use original filename + date
        base_name = os.path.splitext(os.path.basename(INPUT_WAV))[0]
        filename = f"{base_name}_{datetime.date.today()}.txt"

    # Full path to the output file inside the 'output' folder
    OUTPUT_PATH = os.path.join(OUTPUT_DIR, filename)

    # 1. Initialize AI Engines
    print("Initializing ASR and VAD engines on GPU...")
    asr_engine = FireRedAsr.from_pretrained("aed", ASR_DIR)
    vad_engine = AutoModel(model="fsmn-vad", model_revision="v2.0.4")

    # 2. Perform VAD (Voice Activity Detection)
    print(f"Scanning for speech segments in: {INPUT_WAV}")
    res = vad_engine.generate(input=INPUT_WAV, max_single_segment_time=30000)
    speech_chunks = res[0]['value'] 

    # 3. Transcribe speech segments
    audio = AudioSegment.from_wav(INPUT_WAV)
    print(f"VAD complete. Found {len(speech_chunks)} segments. Starting transcription...")

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        # Write header information
        f.write(f"Transcription Record: {os.path.basename(INPUT_WAV)}\n")
        f.write(f"Date: {datetime.date.today()}\n")
        f.write("-" * 50 + "\n\n")
        
        start_time_all = time.time()
        for i, ts in enumerate(speech_chunks):
            start_ms, end_ms = ts[0], ts[1]
            # Extract and export temporary audio segment
            chunk = audio[start_ms : end_ms]
            tmp_wav = f"tmp_segment_{i}.wav"
            chunk.export(tmp_wav, format="wav")
            
            try:
                # Execute ASR transcription
                result = asr_engine.transcribe([f"u_{i}"], [tmp_wav], {"use_gpu": 1, "beam_size": args.beam})
                if result:
                    text = result[0]['text'].strip()
                    
                    # Convert milliseconds to HH:MM:SS format
                    seconds = int(start_ms // 1000)
                    timestamp = "[%02d:%02d:%02d]" % (seconds//3600, (seconds%3600)//60, seconds%60)
                    
                    # Log to console and save to file
                    entry = f"{timestamp} {text}"
                    print(entry)
                    f.write(entry + "\n")
                    f.flush()
            except Exception as e:
                print(f"Warning: Failed to transcribe segment {i}: {e}")
            finally:
                # Cleanup: remove temporary file and clear GPU cache
                if os.path.exists(tmp_wav):
                    os.remove(tmp_wav)
                torch.cuda.empty_cache()

        total_time = time.time() - start_time_all
        print(f"\nProcessing finished in {total_time:.1f} seconds.")
        print(f"Result saved to: {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
```
