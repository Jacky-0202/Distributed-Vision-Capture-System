---
tags: [Obsidian, Attachment, Configuration]
---

## 摘要

本設定旨在達成附件「自動歸位、邏輯命名、嚴格兩層扁平化」，確保系統在搜尋的高效性。

---
## ⚙️ 核心全域設定

進入 Settings -> Attachment Management，依序設定：

1. **Root Path to Save New Attachments**: 選擇 `In the folder specified below`
2. **Root Folder**: 輸入 `99_Resource`
3. **Attachment Path**: 輸入 `.` (一個點，代表不額外增設子資料夾)
4. **Attachment Format**: 輸入 `${notename}_${date}`
5. **Auto Rename Attachment**: `開啟 (Enable)`

---
## 分類設定

#### 1. 建立擴展名規則

在插件設定的 **"Extension Metadata Setting"** 區塊：

- 在 `Extension` 欄位輸入：`png|jpg|jpeg`
- 點擊右側的 **「+ Add」** 按鈕。
- **關鍵動作**：點擊該行右側出現的 **「編輯（鉛筆圖示）」** 進入進階設定。

---

### 2. 編輯規則內容 (Edit Metadata)

進入編輯視窗後，請按照以下邏輯修改（以圖片為例）：

- **Root path**: 選擇 `Folder specified by below`。
- **Root folder**: 輸入 `99_Resource`。
- **Attachment path**: 輸入 `Images`。
- **Attachment format**: 建議輸入 `${notename}_${date}` (這樣圖片檔名會跟著筆記走)。

> [!NOTE] PDF 同理 請重複以上步驟處理 `pdf`，並將 **Attachment path** 改為 `PDFs`。