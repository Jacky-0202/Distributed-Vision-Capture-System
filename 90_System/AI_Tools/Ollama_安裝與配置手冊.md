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

|**模型名稱**|**推薦程度**|**顯存佔用**|**優點**|
|---|---|---|---|
|**Qwen 2.5 14B**|⭐⭐⭐⭐⭐|~9.5 GB|**首選**。中文語境最強，邏輯推演精密，16GB 顯存完美運行。|
|**Llama 3.1 8B**|⭐⭐⭐|~5.2 GB|速度極快，適合簡單的標籤生成，但中文理解略遜。|

**下載指令**：

```bash
ollama run qwen2.5:14b
```