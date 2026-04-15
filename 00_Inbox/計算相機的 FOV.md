---
tags:
---

---
# FOV\_H 推導公式

## 1. 幾何模型假設
- **θ_H**：水平視角（Horizontal Field of View, HFOV），
	是影像最左與最右光線在相機光心形成的夾角。
- **d**：相機到拍攝平面的垂直距離（mm）。
- **FOV_H**：該距離下，拍攝平面上的實際水平寬度（mm）。
- 使用**理想針孔相機模型**，不考慮鏡頭畸變。

---

## 2. 三角形關係

![[計算相機的 FOV_20260415150109.png]]

將水平視角分成左右對稱的兩部分，每邊的角度為：

$$
\frac{\theta_h}{2}
$$

形成的直角三角形中：
- 鄰邊長：d
- 對邊長：$\frac{FOV_H}{2}$

根據正切函數定義：

$$
\tan\left(\frac{\theta_h}{2}\right) = \frac{\frac{FOV_h}{2}}{d}
$$

---

## 3. 推導公式
由上式可得：

$$
\frac{FOV_h}{2} = d \cdot \tan\left(\frac{\theta_h}{2}\right)
$$

兩邊同乘 2：

$$
FOV_h = 2d \cdot \tan\left(\frac{\theta_h}{2}\right)
$$

---

## 4. 範例說明

- **鏡頭型號**：Arducam 12MP IMX708 Fixed-Focus HDR High SNR Camera Module  
- **水平視野（Field of View, HFOV）**：（對角 75°、水平 66°、垂直 41°）
- **距離（d）**：相機與被測物之間的垂直距離 — 例如：150 mm（15 cm）

$$
FOV_H = 2 × 150\ \text{mm} × \tan(33°) ≈ 300 × 0.6494 ≈ \mathbf{194.8\ mm} \quad (\approx 19.5\ cm)
$$
$$
\text{FOV}_V = 2 \times 150\ \text{mm} \cdot \tan\left(\frac{41^\circ}{2}\right) \approx 112.17\ \text{mm} \ (\approx 11.22\ \text{cm})
$$