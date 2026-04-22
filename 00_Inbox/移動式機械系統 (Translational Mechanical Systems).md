---
tags:
---
## 1. 機械系統的三大基本零件

在 $s$ 領域中，我們同樣把這些物理特性看成是「阻礙運動」的比例關係：

|**零件**|**物理意義**|**時間域方程 (F=)**|**s 領域阻抗 (Z)**|**類比電路零件**|
|---|---|---|---|---|
|**質量 (M)**|慣性 (對抗加速度)|$M \frac{d^2x}{dt^2}$|**$Ms^2$**|電感 ($Ls^2$ ?) 其實類比 $L$|
|**阻尼 (B)**|摩擦 (對抗速度)|$B \frac{dx}{dt}$|**$Bs$**|電阻 ($R$)|
|**彈簧 (K)**|彈性 (對抗位移)|$Kx$|**$K$**|電容之倒數 ($1/C$)|

---
## 2. 建立運動方程 (Newton's Second Law)

想像一個質量為 $M$ 的方塊，受外力 $f(t)$ 推動，同時受到彈簧 $K$ 和阻尼 $B$ 的拉扯。根據牛頓第二運動定律：

$$\sum F = Ma$$

外力 $-$ 彈簧力 $-$ 阻尼力 $=$ 質量 $\times$ 加速度

$$f(t) - Kx(t) - B\frac{dx(t)}{dt} = M\frac{d^2x(t)}{dt^2}$$

整理成標準的微分方程形式：

$$M\frac{d^2x(t)}{dt^2} + B\frac{dx(t)}{dt} + Kx(t) = f(t)$$
![[移動式機械系統 (Translational Mechanical Systems)_20260422155620.png|400]]

---
## 3. 求轉移函數 $G(s) = \frac{X(s)}{F(s)}$

我們再次使出那招「假設初始條件為 0」的全面拉氏轉換：

1. $M\frac{d^2x}{dt^2} \longrightarrow M[s^2X(s)]$
2. $B\frac{dx}{dt} \longrightarrow B[sX(s)]$
3. $Kx \longrightarrow KX(s)$
4. $f(t) \longrightarrow F(s)$

**代數合併：**

$$(Ms^2 + Bs + K)X(s) = F(s)$$

**求比例（輸出位移 / 輸入力）：**

$$G(s) = \frac{X(s)}{F(s)} = \frac{1}{Ms^2 + Bs + K}$$