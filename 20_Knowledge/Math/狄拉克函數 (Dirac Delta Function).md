---
tags: ['Math', 'Calculus']
---
## 1. 核心定義 (Core Definition)

$\delta(t)$ 並不是傳統意義上的函數，而是一種「廣義函數（或分佈）」。
它描述了一個**無限短、無限高、但總能量有限**的物理現象。

- **數學特性：**
    
    1. 當 $t \neq 0$ 時，$\delta(t) = 0$。
    2. 在 $t = 0$ 時，高度趨近於 $\infty$。
    3. **全時域積分為 1：**
        $$\int_{-\infty}^{\infty} \delta(t) \, dt = 1$$

---
## 2. 幾何直覺：極限的產物

想像一個面積為 $1$ 的長方形，寬度為 $\epsilon$，高度為 $1/\epsilon$。

![[狄拉克函數 (Dirac Delta Function)_20260418220435.gif]]

當我們讓寬度 $\epsilon \to 0$ 時：

- 它變得極窄（瞬間發生）。
- 它變得極高（強度極大）。    
- **但它的面積（總衝量）永遠保持為 $1$。**

---
## 積分不變性

我們先定義一個函數序列 $d_\epsilon(t)$：

$$d_\epsilon(t) =

\begin{cases}

\frac{1}{\epsilon}, & \text{if } -\frac{\epsilon}{2} < t < \frac{\epsilon}{2} \

0, & \text{otherwise}

\end{cases}$$

**證明積分值：**

我們對這個函數進行全時域積分：

$$\int_{-\infty}^{\infty} d_\epsilon(t) \, dt = \int_{-\epsilon/2}^{\epsilon/2} \frac{1}{\epsilon} \, dt$$

執行積分：

$$\left[ \frac{1}{\epsilon} \cdot t \right]_{-\epsilon/2}^{\epsilon/2} = \frac{1}{\epsilon} \left( \frac{\epsilon}{2} - \left( -\frac{\epsilon}{2} \right) \right) = \frac{1}{\epsilon} (\epsilon) = 1$$

**結論：** 無論 $\epsilon$ 變得多小（寬度趨近於 0），只要高度維持 $1/\epsilon$，這個積分的結果**永遠等於 1**。當 $\epsilon \to 0$ 時，這個極限就是 $\delta(t)$。