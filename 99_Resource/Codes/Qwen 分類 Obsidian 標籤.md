---
tags: [Obsidian, AI, Classification]
---
## 摘要

就是...分就對了

## 程式碼-範例

#### 匯入函式庫
```python
import json
import re
from pathlib import Path
import ollama
```

#### 配置
```python
EXECUTE_WRITE = False
VAULT_DIR = Path("/home/tec/Documents/Sheng_Obsidian_Vault")
INBOX_DIR = VAULT_DIR / "00_Inbox"
MODEL_NAME = "qwen2.5:14b-instruct-q4_K_M"
```

#### 讀取 vault 結構
```python
def get_vault_structure(root_path: Path) -> str:
    """
    Scans the actual vault and returns a list of existing directories.
    Excludes hidden folders and the Inbox itself.
    """
    # Get all subdirectories, relative to vault root
    folders = [
        str(p.relative_to(root_path)) 
        for p in root_path.rglob("*") 
        if p.is_dir() and not p.name.startswith(".") and "00_Inbox" not in str(p)
    ]
    return "\n".join(folders)
```

#### 輸入指令
```python
def get_ai_suggestion(filename: str, content: str, folder_list: str) -> dict:
    """Queries AI with dynamic folder context."""
    
    # We inject the REAL folder list into the prompt
    dynamic_prompt = f"""
You are a Linux Systems Architect. Categorize files based on the ACTUAL vault structure.

ACTUAL EXISTING FOLDERS:
{folder_list}

RULES:
1. MAX 3 tags, STRICTLY ENGLISH. No Chinese characters in tags.
2. NO SPACES IN TAGS: Replace all spaces with underscores (e.g., 'Virtual Machine' -> 'Virtual_Machine').
3. Choose the best FOLDER from the list above. If no folder fits, suggest a new one following PARA/Linux patterns.
4. Output ONLY JSON: {{"tags": ["Tag_One", "Tag_Two"], "folder": "90_System/Linux/..."}}
"""

    try:
        response = ollama.generate(
            model=MODEL_NAME,
            system=dynamic_prompt,
            prompt=f"File: {filename}\nContent: {content[:1000]}",
            format='json',
            stream=False,
            options={"temperature": 0.1}
        )
        return json.loads(response['response'])
    except Exception:
        return {"tags": ["Review"], "folder": "90_System/Error"}
```

#### 模型預測
```python
def update_yaml_tags(file_path: Path, tags: list):
    """Inserts or updates YAML frontmatter with tags."""
    content = file_path.read_text(encoding='utf-8')
    tag_line = f"tags: {tags}"
    
    yaml_pattern = re.compile(r'^---\s*\n(.*?)\n---\s*\n', re.DOTALL | re.MULTILINE)
    match = yaml_pattern.match(content)
    
    if match:
        header = match.group(1)
        body = content[match.end():]
        new_header = re.sub(r'^tags:.*$', tag_line, header, flags=re.MULTILINE) if "tags:" in header else f"{header.strip()}\n{tag_line}"
        new_content = f"---\n{new_header.strip()}\n---\n{body}"
    else:
        new_content = f"---\n{tag_line}\n---\n\n{content}"
    
    file_path.write_text(new_content, encoding='utf-8')
```

#### 主程式
```python
def main():
    if not INBOX_DIR.exists(): return

    # Step 1: Scan real folder structure ONCE
    print("[SYSTEM] Scanning vault structure for context...")
    current_folders = get_vault_structure(VAULT_DIR)

    notes = list(INBOX_DIR.glob("*.md"))
    if not notes:
        print("Inbox is empty.")
        return

    mode_label = "[ EXECUTE MODE ]" if EXECUTE_WRITE else "[ PREVIEW MODE ]"
    print(f"\n{mode_label:^100}")
    print(f"{'Filename':<40} | {'Suggested Folder (Dynamic)':<35} | {'English Tags'}")
    print("-" * 115)

    for note_path in notes:
        try:
            content = note_path.read_text(encoding='utf-8')
            # Step 2: Pass the real folder list to the AI
            suggestion = get_ai_suggestion(note_path.name, content, current_folders)
            
            tag_str = ", ".join([f"#{t}" for t in suggestion['tags'][:3]])
            print(f"{note_path.name[:40]:<40} | {suggestion['folder']:<35} | {tag_str}")
            
            if EXECUTE_WRITE:
                update_yaml_tags(note_path, suggestion['tags'])
                
        except Exception as e:
            print(f"Error processing {note_path.name}: {e}")
```

#### 主程式執行
```python
if __name__ == "__main__":
    main()
```
