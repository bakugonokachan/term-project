import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# 物理參數
g = 9.80665      # 重力加速度
m = 1.0          # 質量 (線性阻力要用到) 


# 無空氣阻力：
def trajectory_no_drag(v0, theta, t):
    theta_rad = np.radians(theta)
    x = v0 * np.cos(theta_rad) * t
    y = v0 * np.sin(theta_rad) * t - 0.5 * g * t**2
    return x, y

# 線性空氣阻力：
def trajectory_linear_drag(v0, theta, k, t):
    theta_rad = np.radians(theta)
    v0x = v0 * np.cos(theta_rad)
    v0y = v0 * np.sin(theta_rad)

    # 時間常數 (避免 k = 0 時除以 0)
    tau = m / k if k != 0 else 1e10

    # 位置解析解
    x = v0x * tau * (1 - np.exp(-t / tau))
    y = (v0y + g * tau) * tau * (1 - np.exp(-t / tau)) - g * t * tau
    return x, y



# 互動式繪圖函數
def interactive_plot():
    t = np.linspace(0, 30, 800)

    v0_init = 50
    theta_init = 45
    k_init = 0.2

    x_no, y_no = trajectory_no_drag(v0_init, theta_init, t)
    x_drag, y_drag = trajectory_linear_drag(v0_init, theta_init, k_init, t)

    y_no = np.where(y_no >= 0, y_no, np.nan)
    y_drag = np.where(y_drag >= 0, y_drag, np.nan)

    fig, ax = plt.subplots(figsize=(8, 5))
    plt.subplots_adjust(left=0.12, bottom=0.30)

    line_no, = ax.plot(x_no, y_no, label="No Drag", linewidth=2)
    line_drag, = ax.plot(x_drag, y_drag, label="Linear Drag", linewidth=2)

    ax.set_xlabel("Horizontal Distance (m)")
    ax.set_ylabel("Height (m)")
    ax.set_title("Projectile Motion: With & Without Linear Drag")
    ax.grid(True)
    ax.legend()
    text_info = ax.text(
    0.05, 0.99, "",
    transform=ax.transAxes,
    fontsize=9,
    verticalalignment="top",
    zorder=999,
    bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3', alpha=0.8)
)


    # Slider 區域
    ax_v0 = plt.axes([0.15, 0.18, 0.7, 0.03])
    ax_theta = plt.axes([0.15, 0.12, 0.7, 0.03])
    ax_k = plt.axes([0.15, 0.06, 0.7, 0.03])

    slider_v0 = Slider(ax_v0, "v0 (m/s)", 1, 100, valinit=v0_init)
    slider_theta = Slider(ax_theta, "Angle (deg)", 1, 89, valinit=theta_init)
    slider_k = Slider(ax_k, "Drag k", 0.0, 1.0, valinit=k_init)

    def update(val):
        v0 = slider_v0.val
        theta = slider_theta.val
        k = slider_k.val
        theta_rad = np.radians(theta)
        t_f_no_drag = (2 * v0 * np.sin(theta_rad)) / g
        h_max_no_drag = (v0 * np.sin(theta_rad))**2 / (2 * g)
        range_no_drag = v0**2 * np.sin(2 * theta_rad) / g

        x1, y1 = trajectory_no_drag(v0, theta, t)
        x2, y2 = trajectory_linear_drag(v0, theta, k, t)

        y1 = np.where(y1 >= 0, y1, np.nan)
        y2 = np.where(y2 >= 0, y2, np.nan)

        line_no.set_xdata(x1)
        line_no.set_ydata(y1)
        line_drag.set_xdata(x2)
        line_drag.set_ydata(y2)

        text_info.set_text(
            f"Range (no drag): {range_no_drag:.2f} m\n"
            f"Max height (no drag): {h_max_no_drag:.2f} m\n"
            f"Flight time (no drag): {t_f_no_drag:.2f} s"
        )


        ax.relim()
        ax.autoscale_view()
        fig.canvas.draw_idle()

    slider_v0.on_changed(update)
    slider_theta.on_changed(update)
    slider_k.on_changed(update)

    plt.show()


# 程式入口點
if __name__ == "__main__":
    interactive_plot()
