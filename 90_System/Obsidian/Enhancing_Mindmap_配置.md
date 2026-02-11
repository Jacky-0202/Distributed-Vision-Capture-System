---
tags:
- Mindmap
- ObsidianPlugin
- Configuration
---

## 摘要

本指南旨在發揮 Enhancing Mindmap 「圖文一體」的特性，
確保心智圖與你的原子筆記、兩層扁平化系統完美兼容。

---
## ⚙️ 核心全域設定 (Settings)

進入 `Settings` -> `Enhancing Mindmap`，調整以下參數：

1. **預設視圖 (Default View)**：`Markdown` (確保檔案本質是文字)。
2. **節點樣式 (Node Style)**：`Line` (直線) —— _最適合工程架構，視覺最乾淨。_
3. **連接線風格 (Link Line)**：`Sharp` (直角) 或 `Curve` (曲線)。
4. **標題建立節點上限 (Max level to create a node)**：`0` 或 `1`。

---
## 🔐 觸發密碼 (The YAML)

為了讓 Obsidian 自動辨識心智圖模式，請在筆記最上方加入：
```yaml
---
mindmap-plugin: mindmap
---
```

---
## ⌨️ 效率快捷鍵 (Mindmap Mode)

- **Mindmap Layout (佈局)**：
    
    - 建議：`right` (向右增長) 或 `map` (放射狀)。
    - _工程師推薦選 `right`，這樣結構會像目錄一樣整齊排列。_
        
- **Max level of node to create a Heading**：
    
    - 設定值：`0`
    - _用意：強制所有節點在 Markdown 中僅以清單 `-` 形式存在，不自動生成 `#` 標題。_
        
- **Stroke array (線條樣式)**：
    
    - 設定值：`(留白)`
    - _用意：保持實線連線，視覺最不干擾。_

---
## 🔗 連結與導航規範

為了維持地圖整潔，建議根據需求使用不同的連結方式：

1. **Wiki-link (快速)**：`[[檔案名稱|顯示名稱]]`
    
    - 優點：自動更新路徑，輸入 `[[` 即可自動完成。
        
2. **Markdown-link (精確)**：`[顯示名稱](20_Knowledge/檔案名稱.md)`
    
    - 優點：節點顯示極度簡潔，可自定義任何文字。

---
## 🚀 雙視窗工作流 (Dual-Window)

這是在 Ubuntu 環境下最強大的使用方式：

1. **左側 (Source)**：編輯 Markdown 原始碼。負責精確調整路徑 `[ ]( )` 與文字描述。
2. **右側 (View)**：開啟 `Open as mindmap`。負責全局導航。