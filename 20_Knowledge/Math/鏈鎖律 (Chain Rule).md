---
tags: [AI, Math, Backpropagation]
---
## 摘要

**核心定義**：微積分中求「複合函數」導數的公式。它允許我們將一個複雜的變化率，拆解成多個簡單變化率的**乘積**。

**三個關鍵價值**：

1. **分解複雜度**：將深層網路的巨大運算，拆成每一層內的小運算。
2. **誤差傳遞**：它是誤差訊號從輸出層「流回」輸入層的物理通道。
3. **局部計算**：每一層神經元只需要關心自己與鄰居的變化，不需要知道整張地圖。

---
## 數學公式

假設你有一個複合函數 $y = f(g(x))$。如果你想知道 $x$ 的微小變動會對 $y$ 造成多大影響（即 $\frac{dy}{dx}$）：

$$\frac{dy}{dx} = \frac{dy}{du} \cdot \frac{du}{dx}$$

_(其中 $u = g(x)$)_

### 在神經網路中的樣子：

為了算出權重 $w$ 對損失 $L$ 的影響，我們層層拆解：

$$\frac{\partial L}{\partial w} = \underbrace{\frac{\partial L}{\partial a}}_{\text{結果對輸出的影響}} \times \underbrace{\frac{\partial a}{\partial z}}_{\text{輸出對激勵的影響}} \times \underbrace{\frac{\partial z}{\partial w}}_{\text{激勵對權重的影響}}$$