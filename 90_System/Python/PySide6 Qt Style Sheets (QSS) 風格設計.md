---
tags: ['Python', 'Qt', 'UI']
---
## 摘要

本文冊整合了 Qt Designer 的預覽技巧與 QSS (Qt Style Sheets) 的美化參數，旨在幫助開發者快速從佈局階段過渡到視覺美化階段。

---
## 1. 啟動預覽模式 (Preview Mode)

在套用任何樣式後，應先在 Designer 中檢視效果，無需重啟 Python 程式。

- **快速鍵啟動：**
    
    - **Windows / Linux:** `Ctrl + R`
    - **macOS:** `Cmd + R`
        
- **查看生成代碼：** 按下 `Ctrl + U` 可即時查看當前 UI 的 Python 原始碼，確認元件名稱。
- **佈局測試：** 在預覽視窗中拖動邊框，確認元件是否隨 Layout 自動縮放。

---
## 2. 常用顏色與色票 (Color Palette)

定義 16 進位 (HEX) 色票，確保介面視覺統一。

|**顏色用途**|**HEX 碼**|**英文備註**|
|---|---|---|
|**主要背景**|`#FFFFFF`|Background (White)|
|**主要邊框**|`#000000`|Border (Black)|
|**懸停狀態**|`#000000`|Hover Background|
|**按下狀態**|`#333333`|Pressed Background (Dark Gray)|

---
## 3. 元件風格設定範例 (QSS Examples)

#### 🖼️ QFrame (容器/區塊)

```css
/* Container box styling */
QFrame {
  background-color: #FFFFFF;    /* White fill */
  border: 2px solid #000000;    /* Thick black border */
  border-radius: 12px;          /* Smooth rounded corners */
  padding: 6px;                 /* Spacing inside the frame */
}
```

#### 🖱️ QPushButton (互動按鈕)

```css
/* Default state */
QPushButton {
  color: #000000;               /* Black text */
  background-color: #FFFFFF;    /* White background */
  border: 2px solid #000000;    /* Black outline */
  border-radius: 8px;           /* Rounded corners */
  padding: 6px 14px;
}

/* Hover effect */
QPushButton:hover {
  color: #FFFFFF;               /* Flip to white text */
  background-color: #000000;    /* Flip to black background */
}

/* Pressed effect */
QPushButton:pressed {
  background-color: #333333;    /* Feedback for click */
}
```

---