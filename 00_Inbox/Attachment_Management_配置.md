---
tags:
---
## 摘要

本設定旨在達成附件「自動歸位、邏輯命名、嚴格兩層扁平化」，確保系統在搜尋的高效性。

---
## ⚙️ 核心全域設定 (主要針對圖片)

進入 Settings -> Attachment Management，依序設定：

1. **Root Path to Save New Attachments**: 選擇 `In the folder specified below`
2. **Root Folder**: 輸入 `90_System/Images`
3. **Attachment Path**: 輸入 `.` (一個點，代表不額外增設子資料夾)
4. **Attachment Format**: 輸入 `${notename}_${date}`
5. **Auto Rename Attachment**: `開啟 (Enable)`

---
## 📑 副檔名覆蓋設定 (針對 PDF 等非圖片檔案)

為了保持 `PDFs` 與 `Images` 獨立，請在 **Extension Override** 區塊點擊 **Add**：

- **Extension**: `pdf`
- **Root Path to Save New Attachments**: `In the folder specified below`
- **Root Folder**: `90_System/PDFs`
- **Attachment Path**: `.`
- **Attachment Format**: `${notename}_${index}`

*(註：若有 Word 或 PPT 需求，可比照辦理，將路徑指向 90_System/PDFs 或另設資料夾。)*
