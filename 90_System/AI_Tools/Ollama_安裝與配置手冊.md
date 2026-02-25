---
tags: [AI, System, Installation]
---

## 摘要

利用本地 GPU 算力實現「零隱私洩漏」的筆記自動化。由 Ollama 擔任模型後端，透過 Python 腳本監控 `00_Inbox`，實現檔案的語義分類與自動搬移。

---
## 主機環境安裝 (System Level)

Ollama 是系統級服務，直接與 NVIDIA 驅動溝通，**不需**在 Python 虛擬環境中安裝。

1. **安裝指令**：

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

2. **服務管理**：

- 啟動：
```bash
systemctl start ollama
```

- 狀態：
```bash
systemctl status ollama
```

3. **硬體驗證**：

- Ollama 會自動偵測 CUDA 指令集。對於 **RTX 5070 Ti (16GB)**，建議分配至少 10GB 顯存給模型，剩餘 6GB 留給系統與 GUI。

---
## 模型選擇 (Model Selection)

針對 **The Nexus** 的中文環境與分類精度需求：

|**模型名稱 (系列)**|**邏輯層次**|**顯存佔用 (Q4_K_M)**|**16GB 運行狀態**|**最適合你的場景**|
|---|---|---|---|---|
|**Qwen 2.5 14B**|⭐⭐⭐⭐⭐|**~9.5 GB**|🟢 **極速** (全速加載)|**日常首選**。打標籤、改程式碼、整理筆記。|
|**DeepSeek-R1-Distill-14B**|⭐⭐⭐⭐⭐|**~10.2 GB**|🟢 **流暢** (思考型)|**複雜邏輯**。區分深層樂理與 AI 理論。|
|**Gemma 2 9B**|⭐⭐⭐⭐|**~6.8 GB**|🟢 **秒回** (極輕量)|**快速打標**。不需要太深推理的簡單筆記。|
|**Mistral NeMo 12B**|⭐⭐⭐|**~8.5 GB**|🟢 **流暢** (多語言)|**英文文獻**。如果你有大量國外 AI 論文。|
|**Qwen 2.5 32B**|⭐⭐⭐⭐|**~19.5 GB**|🟡 **略慢** (部分入 RAM)|**高維度分析**。處理極度糾結的知識映射。|

**下載指令**：

```bash
ollama run qwen2.5:14b
```