# Interactive Projectile Motion Simulator  
**Term Project – B11504118**
 
---

## 1. 程式功能與技術原理（Function and Technical Principles）

本程式實作可視覺化拋體運動的互動模擬工具，包含：

1. 無空氣阻力模型（理想拋物線）  
2. 線性空氣阻力模型（阻力 ∝ 速度）
3. 考慮旋轉效應模型

使用者可透過滑桿調整：

- 初速 \(v_0\)
- 發射角度 \(\theta\)
- 阻力係數 \(k\)
- 角速度 \(rpm\)

並即時觀察軌跡變化。

---
1.1 無空氣阻力模型
拋體運動方程式如下：

<p align="center">
  <img src="img/formula_01.svg" width="300px">
</p>

<p align="center">
  <img src="img/formula_02.svg" width="300px">
</p>

其中：
- \(v_0\)：初速度  
- \(\theta\)：發射角度  
- \(g\)：重力加速度  
---
1.2 線性空氣阻力模型
假設阻力與速度成正比：

<p align="center">
  <img src="img/formula_03.svg" width="300px">
</p>

定義時間常數：

<p align="center">
  <img src="img/formula_04.svg" width="300px">
</p>

其解析解如下：

<p align="center">
  <img src="img/formula_05.svg" width="300px">
</p>

<p align="center">
  <img src="img/formula_06.svg" width="300px">
</p>

1.3 旋轉效應（Magnus Effect，棒球背旋情境）
在球類運動（例如棒球）中，球體常伴隨旋轉。當球體具有背旋（backspin）時，因流體繞流導致球體上下表面流速分佈不同，進而產生垂直於速度方向的升力，使球的飛行時間延長、最高點上升，軌跡也可能出現更明顯的「上飄」現象，這種效應稱為 **Magnus effect**。

本程式將旋轉效應以附加力項納入運動方程，並以轉速（rpm）作為可調參數。概念上，Magnus 力可寫成與角速度及速度相關的形式，


<p align="center">
  <img src="img/formula_07svg" width="300px">
</p>

由於加入旋轉後，速度分量之間會產生耦合，無法維持和前兩種模型同樣簡潔的解析解形式，因此本程式使用 **RK4（四階 Runge–Kutta）數值積分**來模擬「線性阻力 + 旋轉」情境，並以 \(y<0\) 作為落地停止條件，確保模擬結果穩定且直觀。

---

## 2. 使用方式（Usage Instructions）

2.1 安裝必要套件

若未安裝 Matplotlib，請執行：
```
pip install matplotlib
```
2.2 執行程式
```
python3 B11504118_term\ project.py
```
2.3 互動操作

執行後會開啟視窗，內含三組滑桿：

| 滑桿         | 說明              |
| ----------- | --------------- |
| v0 (m/s)    | 調整初速（1–100 m/s） |
| Angle (deg) | 調整發射角度（1–89°）   |
| Drag k      | 調整線性空氣阻力（0–1）   |
| rpm         | 調整角速度   |


## 3.Program Structure

```
trajectory_no_drag()：計算無空氣阻力情況的拋體軌跡
                    ↓

trajectory_linear_drag()：計算線性空氣阻力解析解
                    ↓

interactive_plot()：建立主介面、滑桿與更新函式
                    ↓

simulate_linear_drag_with_spin_rk4()：計算線性阻力 + 旋轉（Magnus effect）的拋體軌跡（RK4 數值積分）
                    ↓

main entry：呼叫 interactive_plot()
                  
```



## 4.Development Process
開發過程主要包含以下階段：
```
1. 模型推導與測試

驗證理想拋體運動方程式

整理並實作線性阻力模型的解析解

測試不同參數下是否生成合理軌跡

加入旋轉模型（Magnus effect）

依教授建議，以球類情境為延伸方向，新增旋轉參數（rpm）

因旋轉導致速度分量耦合，改用 RK4 進行數值積分求解軌跡

測試不同轉速下的軌跡是否呈現合理的上飄／落點變化

2. 圖形繪製

以 Matplotlib 繪製初步軌跡

測試是否會出現 NaN、軌跡斷裂等情況

3. 互動功能實作

使用 matplotlib.widgets.Slider 建立滑桿

實作更新函式，在參數變動時重新計算軌跡

4. 邊界與例外處理

當 y(t) < 0（落地）時以 NaN 隱藏後段曲線

使用 ax.relim() 與 ax.autoscale_view() 讓圖形自動調整

5. 介面與程式整理

調整滑桿位置避免遮擋圖形

加上標題、座標軸標示與圖例
```

## 5.References
普通物理教科書：拋體運動章節

R. Fitzpatrick, Newtonian Dynamics, University of Texas

Wikipedia: Drag Equation（線性阻力模型部分）

