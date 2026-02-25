---
tags: [Obsidian, AI, Classification]
---
## 摘要



## 程式碼-範例

```python
import os
import json
import ollama

# 配置路徑
VAULT_PATH = "/home/tec/Documents/Sheng_Obsidian_Vault"
INBOX_PATH = os.path.join(VAULT_PATH, "00_Inbox")

# 強化後的 AI 指令集
SYSTEM_PROMPT = """
You are an expert Obsidian vault organizer. Your task is to categorize notes based on their filenames and content.

STRICT CLASSIFICATION RULES:
1. 20_Knowledge: Abstract theories, concepts, and methodologies (e.g., "Eisenhower Matrix", "Music Theory", "AI Theory/Math").
2. 90_System: System-level management and hardware. (e.g., "Linux commands", "Raspberry Pi setup", "Automation scripts").
3. 30_Praxis: Hands-on tutorials, step-by-step guides (e.g., "How to upload to Git").
4. 10_Atlas: Maps of Content (MOC).

TAGGING RULES:
- Max 3 tags.
- MUST be in ENGLISH (e.g., #Productivity, #Linux, #NeuralNetwork).

OUTPUT FORMAT:
Return ONLY a JSON object:
{"tags": ["Tag1", "Tag2"], "target_folder": "90_System/Linux"}
"""

def get_ai_decision(filename):
    # 這裡我們傳入檔名讓 AI 判斷，若檔名不明確，後續可改為傳入檔案前 500 字
    response = ollama.generate(
        model='qwen2.5:14b',
        system=SYSTEM_PROMPT,
        prompt=f"File Name: {filename}",
        format='json',
        stream=False
    )
    return json.loads(response['response'])

def preview_all_files():
    if not os.path.exists(INBOX_PATH):
        print("Error: Inbox path not found.")
        return

    files = [f for f in os.listdir(INBOX_PATH) if f.endswith(".md")]
    
    print(f"{'Original File':<40} | {'Target Folder':<25} | {'English Tags'}")
    print("-" * 100)

    for filename in files:
        try:
            result = get_ai_decision(filename)
            tags = " ".join([f"#{t}" for t in result['tags']])
            folder = result['target_folder']
            print(f"{filename[:40]:<40} | {folder:<25} | {tags}")
        except Exception as e:
            print(f"Error processing {filename}: {e}")

if __name__ == "__main__":
    preview_all_files()
```
