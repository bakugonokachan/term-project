import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

g = 9.80665      
m = 0.145        # kg（標準棒球約 145 g）

# 無空氣阻力：解析解
def trajectory_no_drag(v0, theta_deg, t):
    th = np.radians(theta_deg)
    x = v0 * np.cos(th) * t
    y = v0 * np.sin(th) * t - 0.5 * g * t**2
    return x, y


# 線性空氣阻力：解析解
def trajectory_linear_drag(v0, theta_deg, k, t):
    th = np.radians(theta_deg)
    v0x = v0 * np.cos(th)
    v0y = v0 * np.sin(th)

    tau = m / k if k != 0 else 1e10

    x = v0x * tau * (1 - np.exp(-t / tau))
    y = (v0y + g * tau) * tau * (1 - np.exp(-t / tau)) - g * t * tau
    return x, y


# 旋轉 + 線性阻力：數值積分
def simulate_linear_drag_with_spin_rk4(v0, theta_deg, k, rpm, C_M,
                                       dt=0.01, t_max=30.0):
    th = np.radians(theta_deg)
    vx = v0 * np.cos(th)
    vy = v0 * np.sin(th)
    x, y = 0.0, 0.0

    omega = rpm * 2*np.pi / 60.0  # rad/s

    xs, ys = [x], [y]
    ts = [0.0]

    def deriv(state):
        x_, y_, vx_, vy_ = state

        ax_drag = -(k/m) * vx_
        ay_drag = -(k/m) * vy_

        ax_mag = (C_M/m) * (-omega * vy_)
        ay_mag = (C_M/m) * ( omega * vx_)

        ax = ax_drag + ax_mag
        ay = ay_drag + ay_mag - g

        return np.array([vx_, vy_, ax, ay], dtype=float)

    t = 0.0
    state = np.array([x, y, vx, vy], dtype=float)

    while t < t_max:
        k1 = deriv(state)
        k2 = deriv(state + 0.5*dt*k1)
        k3 = deriv(state + 0.5*dt*k2)
        k4 = deriv(state + dt*k3)
        state_next = state + (dt/6.0)*(k1 + 2*k2 + 2*k3 + k4)

        t_next = t + dt

        x_next, y_next, vx_next, vy_next = state_next

        xs.append(x_next)
        ys.append(y_next)
        ts.append(t_next)

        state = state_next
        t = t_next
        if y_next < 0:
            x_prev, y_prev = xs[-2], ys[-2]

            frac = y_prev / (y_prev - y_next)   
            x_ground = x_prev + frac * (x_next - x_prev)
            t_ground = ts[-2] + frac * (t_next - ts[-2])

            xs[-1] = x_ground
            ys[-1] = 0.0
            ts[-1] = t_ground
            break


    return np.array(xs), np.array(ys), np.array(ts)



# 互動式頁面程式
def interactive_plot():
    t = np.linspace(0, 30, 800)

    v0_init = 50
    theta_init = 45
    k_init = 0.2

    rpm_init = 1500     
    CM_init = 1.2e-4   

    x_no, y_no = trajectory_no_drag(v0_init, theta_init, t)
    x_lin, y_lin = trajectory_linear_drag(v0_init, theta_init, k_init, t)

    x_sp, y_sp, _ = simulate_linear_drag_with_spin_rk4(
        v0_init, theta_init, k_init, rpm_init, CM_init, dt=0.01, t_max=30.0
    )

    y_no = np.where(y_no >= 0, y_no, np.nan)
    y_lin = np.where(y_lin >= 0, y_lin, np.nan)
    y_sp_plot = np.where(y_sp >= 0, y_sp, np.nan)

    fig, ax = plt.subplots(figsize=(9, 5.6))
    plt.subplots_adjust(left=0.12, bottom=0.33)

    line_no, = ax.plot(x_no, y_no, label="No Drag", linewidth=2)
    line_lin, = ax.plot(x_lin, y_lin, label="Linear Drag (Analytic)", linewidth=2)
    line_sp, = ax.plot(x_sp, y_sp_plot, label="Linear Drag + Spin (RK4)", linewidth=2)

    ax.set_xlabel("Horizontal Distance (m)")
    ax.set_ylabel("Height (m)")
    ax.set_title("Projectile Motion: No Drag vs Linear Drag vs Spin (Magnus)")
    ax.grid(True)
    ax.legend()

    text_info = ax.text(
        0.02, 0.98, "",
        transform=ax.transAxes,
        fontsize=9,
        verticalalignment="top",
        zorder=999,
        bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3', alpha=0.85)
    )


    # Slider
    ax_v0    = plt.axes([0.15, 0.23, 0.72, 0.03])
    ax_theta = plt.axes([0.15, 0.17, 0.72, 0.03])
    ax_k     = plt.axes([0.15, 0.11, 0.72, 0.03])
    ax_rpm   = plt.axes([0.15, 0.05, 0.72, 0.03])

    slider_v0 = Slider(ax_v0, "v0 (m/s)", 1, 100, valinit=v0_init)
    slider_th = Slider(ax_theta, "Angle (deg)", 1, 89, valinit=theta_init)
    slider_k  = Slider(ax_k, "Drag k (kg/s)", 0.0, 1.0, valinit=k_init)
    slider_r  = Slider(ax_rpm, "Spin (rpm)", 0, 3000, valinit=rpm_init)


    def compute_metrics_from_xy(x_arr, y_arr):
        mask = np.isfinite(y_arr)
        if not np.any(mask):
            return np.nan, np.nan
        x_eff = x_arr[mask]
        y_eff = y_arr[mask]
        return np.nanmax(y_eff), x_eff[-1] 
    def update(val):
        v0 = slider_v0.val
        th = slider_th.val
        k  = slider_k.val
        rpm = slider_r.val
        C_M = CM_init  

        th_rad = np.radians(th)
        t_f_no = (2 * v0 * np.sin(th_rad)) / g
        h_no   = (v0 * np.sin(th_rad))**2 / (2 * g)
        r_no   = (v0**2) * np.sin(2 * th_rad) / g

        x1, y1 = trajectory_no_drag(v0, th, t)
        x2, y2 = trajectory_linear_drag(v0, th, k, t)

        x3, y3, ts3 = simulate_linear_drag_with_spin_rk4(
            v0, th, k, rpm, C_M, dt=0.01, t_max=30.0
        )

        y1 = np.where(y1 >= 0, y1, np.nan)
        y2 = np.where(y2 >= 0, y2, np.nan)
        y3p = np.where(y3 >= 0, y3, np.nan)

        line_no.set_data(x1, y1)
        line_lin.set_data(x2, y2)
        line_sp.set_data(x3, y3p)

        h_lin, r_lin = compute_metrics_from_xy(x2, y2)
        h_sp,  r_sp  = compute_metrics_from_xy(x3, y3p)
        t_sp = ts3[-1] if len(ts3) > 0 else np.nan

        text_info.set_text(
            f"[No Drag]\n"
            f"Range: {r_no:.2f} m | Max height: {h_no:.2f} m | Flight time: {t_f_no:.2f} s\n\n"
            f"[Linear Drag]\n"
            f"Range≈ {r_lin:.2f} m | Max height≈ {h_lin:.2f} m\n\n"
            f"[Linear Drag + Spin]\n"
            f"Spin: {rpm:.0f} rpm | Range≈ {r_sp:.2f} m | Max height≈ {h_sp:.2f} m | Time≈ {t_sp:.2f} s"
        )

        ax.relim()
        ax.autoscale_view()
        fig.canvas.draw_idle()

    slider_v0.on_changed(update)
    slider_th.on_changed(update)
    slider_k.on_changed(update)
    slider_r.on_changed(update)
   
    update(None)

    plt.show()


if __name__ == "__main__":
    interactive_plot()
