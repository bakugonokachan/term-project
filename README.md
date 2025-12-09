# Title

Interactive Projectile Motion Simulator

Term Project – B11504118

## 1.Function and Technical Principles
 本程式實作一套可視覺化拋體運動的互動模擬工具。
模擬同時包含兩種物理模型：

無空氣阻力（理想拋物線）

具線性空氣阻力（阻力與速度成正比）

使用者可透過滑桿即時調整：

初速 
𝑣
0
v
0
	​


發射角度 
𝜃
θ

阻力係數 
𝑘
k

並立即觀察參數變動對軌跡的影響。

1.1 無空氣阻力模型

拋體運動遵循以下基本公式：

𝑥
(
𝑡
)
=
𝑣
0
cos
⁡
𝜃
⋅
𝑡
x(t)=v
0
	​

cosθ⋅t
𝑦
(
𝑡
)
=
𝑣
0
sin
⁡
𝜃
⋅
𝑡
−
1
2
𝑔
𝑡
2
y(t)=v
0
	​

sinθ⋅t−
2
1
	​

gt
2

其中

𝑣
0
v
0
	​

：初速

𝜃
θ：發射角度

𝑔
g：重力加速度

1.2 線性空氣阻力模型

假設阻力形式：

𝐹
=
−
𝑘
𝑣
F=−kv

定義時間常數：

𝜏
=
𝑚
𝑘
τ=
k
m
	​


可得位置解析解：

𝑥
(
𝑡
)
=
𝑣
0
𝑥
𝜏
(
1
−
𝑒
−
𝑡
/
𝜏
)
x(t)=v
0x
	​

τ(1−e
−t/τ
)
𝑦
(
𝑡
)
=
(
𝑣
0
𝑦
+
𝑔
𝜏
)
𝜏
(
1
−
𝑒
−
𝑡
/
𝜏
)
−
𝑔
𝑡
𝜏
y(t)=(v
0y
	​

+gτ)τ(1−e
−t/τ
)−gtτ

此模型反映了空氣阻力對射程、最高點與飛行時間的影響。


## 2.Usage Instructions

2.1 安裝必要套件

若未安裝 Matplotlib，請執行：

pip install matplotlib

2.2 執行程式

python3 B11504118_term\ project.py

2.3 互動操作

執行後會開啟視窗，內含三組滑桿：

| 滑桿         | 說明              |
| ----------- | --------------- |
| v0 (m/s)    | 調整初速（1–100 m/s） |
| Angle (deg) | 調整發射角度（1–89°）   |
| Drag k      | 調整線性空氣阻力（0–1）   |



## 3.Program Structure

├── trajectory_no_drag()
│   └── 計算無空氣阻力情況下的拋體軌跡
│
├── trajectory_linear_drag()
│   └── 計算線性空氣阻力解析解
│
├── interactive_plot()
│   ├── 初始化繪圖介面
│   ├── 建立滑桿
│   ├── 繪製初始軌跡
│   └── update()：更新曲線並重繪
│
└── main entry
    └── 呼叫 interactive_plot()


## 4.Development Process
開發過程主要包含以下階段：

4.1 模型推導與測試

驗證理想拋體運動方程式

整理並實作線性阻力模型的解析解

測試不同參數下是否生成合理軌跡

4.2 圖形繪製

以 Matplotlib 繪製初步軌跡

測試是否會出現 NaN、軌跡斷裂等情況

4.3 互動功能實作

使用 matplotlib.widgets.Slider 建立滑桿

實作更新函式，在參數變動時重新計算軌跡

4.4 邊界與例外處理

當 y(t) < 0（落地）時以 NaN 隱藏後段曲線

使用 ax.relim() 與 ax.autoscale_view() 讓圖形自動調整

4.5 介面與程式整理

調整滑桿位置避免遮擋圖形

加上標題、座標軸標示與圖例

## 5.References
普通物理教科書：拋體運動章節

R. Fitzpatrick, Newtonian Dynamics, University of Texas

Wikipedia: Drag Equation（線性阻力模型部分）

