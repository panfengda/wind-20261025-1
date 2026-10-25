import math
from datetime import datetime

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


st.set_page_config(
    page_title="PFD | 海上风电数字孪生",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Theme
# -----------------------------
st.markdown(
    """
    <style>
    .stApp {
        background: radial-gradient(circle at 50% 0%, #102a3b 0%, #071421 55%, #06111c 100%);
        color: #e6f0f7;
    }
    [data-testid="stSidebar"] {
        background: #0c2030;
        border-right: 1px solid #1b3b50;
    }
    h1, h2, h3, p, label, span, div { }
    h1, h2, h3 { color: #eaf4fb; }
    .pfd-eyebrow {
        color: #55dbe5; font-size: 0.75rem; letter-spacing: .18em;
        font-weight: 800; text-transform: uppercase; margin-bottom: .3rem;
    }
    .pfd-subtitle { color: #93adbd; margin-top: -0.4rem; }
    .metric-card {
        background: linear-gradient(145deg, #142d40, #0d2233);
        border: 1px solid #24465c; border-radius: 15px;
        padding: 17px 18px; min-height: 112px;
    }
    .metric-label { color: #9bb5c5; font-size: .9rem; }
    .metric-value { color: #54dce7; font-size: 1.75rem; font-weight: 800; margin-top: 6px; }
    .metric-note { color: #7895a7; font-size: .75rem; margin-top: 4px; }
    .panel {
        background: rgba(15, 35, 51, .92);
        border: 1px solid #214258; border-radius: 15px; padding: 16px 18px;
    }
    .status-ok {
        background: #10372f; color: #75e5bd; border: 1px solid #1b6657;
        padding: 8px 12px; border-radius: 9px; display: inline-block; font-weight: 700;
    }
    .status-warn {
        background: #3b2c1b; color: #ffc078; border: 1px solid #78522b;
        padding: 8px 12px; border-radius: 9px; display: inline-block; font-weight: 700;
    }
    div[data-testid="stDataFrame"] { border: 1px solid #24465c; border-radius: 10px; }
    .small-muted { color: #8ca5b6; font-size: .8rem; }
    </style>
    """,
    unsafe_allow_html=True,
)


# -----------------------------
# Geometry helpers
# -----------------------------
def make_turbine_figure(rotor_angle_deg, damage_pct, wind_speed, wave_height, show_coating, focus_blade):
    """Create a procedural 3D offshore turbine demo. Geometry and damage are illustrative."""
    fig = go.Figure()

    # Ocean surface with a subtle wave pattern.
    xx = np.linspace(-13, 13, 36)
    yy = np.linspace(-10, 10, 30)
    X, Y = np.meshgrid(xx, yy)
    Z = -0.35 + 0.10 * np.sin(X * 0.45) * np.cos(Y * 0.38) * max(wave_height / 8.0, 0.1)
    fig.add_trace(
        go.Surface(
            x=X, y=Y, z=Z,
            surfacecolor=np.zeros_like(Z),
            colorscale=[[0, "#17657a"], [1, "#17657a"]],
            showscale=False, opacity=0.9, hoverinfo="skip",
            lighting=dict(ambient=0.75, diffuse=0.35, specular=0.1, roughness=0.9),
            name="海面",
        )
    )

    # Tower, slightly tapered.
    tower_z = np.linspace(0.0, 7.9, 24)
    tower_theta = np.linspace(0, 2 * np.pi, 28)
    TT, ZZ = np.meshgrid(tower_theta, tower_z)
    radius = 0.22 - 0.09 * (ZZ / 7.9)
    TX = radius * np.cos(TT)
    TY = radius * np.sin(TT)
    fig.add_trace(
        go.Surface(
            x=TX, y=TY, z=ZZ,
            colorscale=[[0, "#d7e3e9"], [0.45, "#f5f8fa"], [1, "#8ca7b5"]],
            showscale=False, hoverinfo="skip", name="塔筒",
            lighting=dict(ambient=0.55, diffuse=0.8, specular=0.35, roughness=0.45),
        )
    )

    # Simple monopile and splash-zone bands.
    for px, py in [(-0.48, -0.42), (0.48, -0.42), (0, 0.52)]:
        pile_z = np.linspace(-1.15, 0.55, 10)
        pile_t = np.linspace(0, 2 * np.pi, 20)
        PT, PZ = np.meshgrid(pile_t, pile_z)
        r = 0.13
        fig.add_trace(
            go.Surface(
                x=px + r * np.cos(PT), y=py + r * np.sin(PT), z=PZ,
                colorscale=[[0, "#24556a"], [1, "#3c8290"]],
                showscale=False, hoverinfo="skip", name="基础",
            )
        )
        # Yellow cap at sea level
        cap_t = np.linspace(0, 2 * np.pi, 24)
        cap_r = np.linspace(0.0, r * 1.08, 3)
        CT, CR = np.meshgrid(cap_t, cap_r)
        fig.add_trace(
            go.Surface(
                x=px + CR * np.cos(CT), y=py + CR * np.sin(CT),
                z=np.full_like(CR, 0.55),
                colorscale=[[0, "#e5c56b"], [1, "#e5c56b"]],
                showscale=False, hoverinfo="skip", name="基础顶盖",
            )
        )

    # Nacelle and hub.
    fig.add_trace(
        go.Mesh3d(
            x=[-0.35, 0.55, 0.55, -0.35, -0.35, 0.55, 0.55, -0.35],
            y=[-0.22, -0.22, 0.22, 0.22, -0.22, -0.22, 0.22, 0.22],
            z=[7.82, 7.82, 7.82, 7.82, 8.18, 8.18, 8.18, 8.18],
            i=[0, 0, 0, 1, 4, 4, 2, 3, 6, 5, 1, 2],
            j=[1, 2, 3, 2, 5, 6, 6, 7, 7, 6, 5, 6],
            k=[2, 3, 0, 6, 6, 7, 7, 4, 4, 1, 6, 3],
            color="#d9e5eb", opacity=1, flatshading=True, name="机舱",
            hoverinfo="skip",
        )
    )
    hub = go.Scatter3d(
        x=[0.0], y=[0.0], z=[8.0], mode="markers",
        marker=dict(size=11, color="#edf6fb", line=dict(color="#7f9cac", width=2)),
        name="轮毂", hovertemplate="轮毂<extra></extra>",
    )
    fig.add_trace(hub)

    # Rotor blades. Rotor plane is approximately the X-Z plane.
    base_angles = [0, 120, 240]
    blade_names = ["A", "B", "C"]
    palette = [[0.0, "#25b8c5"], [0.25, "#a8e7d0"], [0.5, "#f7d76a"], [0.75, "#ff944d"], [1.0, "#f0445f"]]
    damage_level = float(np.clip(damage_pct / 100.0, 0, 1))
    env_factor = np.clip((wind_speed - 8) / 25, 0, 1) * 0.45 + np.clip(wave_height / 12, 0, 1) * 0.25
    for idx, base in enumerate(base_angles):
        angle = math.radians(base + rotor_angle_deg)
        direction = np.array([math.cos(angle), 0.0, math.sin(angle)])
        width_direction = np.array([-math.sin(angle), 0.0, math.cos(angle)])
        span = np.linspace(0.35, 4.65, 42)
        # Tapered blade width; widest close to the root, narrowing toward the tip.
        widths = 0.36 * (1 - (span / 5.2) ** 1.15) + 0.025
        center = np.array([0.0, 0.0, 8.0])[:, None] + direction[:, None] * span[None, :]
        left = center + width_direction[:, None] * widths[None, :] / 2
        right = center - width_direction[:, None] * widths[None, :] / 2
        # Give blade a slight chordwise sweep.
        sweep = (span / span.max()) ** 2 * 0.18
        left[1, :] += sweep
        right[1, :] += sweep

        vertices = np.concatenate([left.T, right.T], axis=0)
        n = len(span)
        ii, jj, kk = [], [], []
        for k in range(n - 1):
            ii.extend([k, k + 1])
            jj.extend([k + 1, n + k + 1])
            kk.extend([n + k, n + k])
        # Damage concentrates toward the leading edge and outer span.
        radial = np.repeat((span / span.max()), 2)
        edge = np.tile(np.array([0.92, 0.12]), n)
        blade_damage = np.clip(damage_level * (0.20 + 0.80 * radial ** 1.5) * (0.55 + 0.45 * edge) + env_factor * 0.18 * radial, 0, 1)
        if not show_coating:
            blade_damage = np.full_like(blade_damage, 0.08)
        # Emphasize selected blade; retain other blades for context.
        opacity = 1.0 if (focus_blade == blade_names[idx] or focus_blade == "全部") else 0.48
        fig.add_trace(
            go.Mesh3d(
                x=vertices[:, 0], y=vertices[:, 1], z=vertices[:, 2],
                i=ii, j=jj, k=kk,
                intensity=blade_damage,
                intensitymode="vertex",
                colorscale=palette,
                cmin=0, cmax=1,
                showscale=(idx == 0 and show_coating),
                colorbar=dict(
                    title=dict(text="损伤程度", font=dict(color="#d9eaf2", size=12)),
                    tickfont=dict(color="#d9eaf2", size=10),
                    tickvals=[0, 0.25, 0.5, 0.75, 1],
                    ticktext=["0%", "25%", "50%", "75%", "100%"],
                    bgcolor="rgba(8, 24, 37, 0.88)",
                    outlinecolor="#31546a",
                    thickness=14,
                    len=0.58,
                ),
                opacity=opacity,
                flatshading=False,
                name=f"叶片 {blade_names[idx]}",
                hovertemplate=f"叶片 {blade_names[idx]}<br>展向位置: %{{x:.2f}}<br>示意损伤指数: %{{intensity:.0%}}<extra></extra>",
                lighting=dict(ambient=0.55, diffuse=0.8, specular=0.25, roughness=0.5),
            )
        )

    # Distant turbines, intentionally simplified contextual silhouettes.
    for dx, dy, scale in [(-7.2, 3.5, 0.62), (7.8, 4.0, 0.72), (9.5, -3.8, 0.55)]:
        h = 5.0 * scale
        fig.add_trace(go.Scatter3d(
            x=[dx, dx], y=[dy, dy], z=[0, h],
            mode="lines", line=dict(color="#b7cbd5", width=5), showlegend=False,
            hoverinfo="skip",
        ))
        for b in range(3):
            a = math.radians(b * 120 + rotor_angle_deg * 0.3)
            fig.add_trace(go.Scatter3d(
                x=[dx, dx + 1.8 * scale * math.cos(a)],
                y=[dy, dy],
                z=[h, h + 1.8 * scale * math.sin(a)],
                mode="lines", line=dict(color="#e4edf1", width=4), showlegend=False,
                hoverinfo="skip",
            ))

    fig.update_layout(
        height=650,
        margin=dict(l=0, r=0, t=8, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Arial, Microsoft YaHei, sans-serif", color="#dbeaf2", size=12),
        scene=dict(
            bgcolor="#b0d0d8",
            xaxis=dict(visible=False, range=[-12, 12]),
            yaxis=dict(visible=False, range=[-9, 9]),
            zaxis=dict(visible=False, range=[-1.5, 13]),
            aspectmode="manual",
            aspectratio=dict(x=1.25, y=1.0, z=0.9),
            camera=dict(eye=dict(x=1.55, y=1.65, z=1.05)),
            dragmode="orbit",
        ),
        showlegend=False,
    )
    return fig


# -----------------------------
# Sidebar controls
# -----------------------------
with st.sidebar:
    st.markdown('<div class="pfd-eyebrow">PFD / WIND ENERGY RESEARCH TWIN</div>', unsafe_allow_html=True)
    st.title("运行控制")
    st.caption("交互式研究原型 · 非实时SCADA")
    rotor_rpm = st.slider("叶轮转速 (rpm)", min_value=0, max_value=24, value=12, step=1)
    rotor_angle = st.slider("叶轮旋转角度 (°)", min_value=0, max_value=359, value=35, step=5)
    wind = st.slider("风速 (m/s)", min_value=0.0, max_value=35.0, value=12.3, step=0.5)
    wave = st.slider("有效波高 (m)", min_value=0.0, max_value=15.0, value=2.1, step=0.1)
    temperature = st.slider("环境温度 (°C)", min_value=-15.0, max_value=40.0, value=16.6, step=0.5)
    damage = st.slider("叶片损伤演示值 (%)", min_value=0, max_value=100, value=28, step=1)
    focus_blade = st.selectbox("重点叶片", ["全部", "A", "B", "C"], index=0)
    show_coating = st.toggle("显示涂层损伤热图", value=True)
    st.divider()
    st.markdown(
        '<div class="small-muted">注意：当前为程序生成的示意几何与演示损伤指数，不代表现场测量、经验证的物理仿真或剩余寿命预测。</div>',
        unsafe_allow_html=True,
    )


# -----------------------------
# Main page
# -----------------------------
st.markdown('<div class="pfd-eyebrow">OFFSHORE WIND · DIGITAL TWIN</div>', unsafe_allow_html=True)
title_col, status_col = st.columns([4, 1])
with title_col:
    st.title("PFD 海上风电数字孪生")
    st.markdown('<div class="pfd-subtitle">双馈风电机组 · 叶片涂层状态与环境驱动研究原型</div>', unsafe_allow_html=True)
with status_col:
    st.markdown("<div style='text-align:right;padding-top:16px'><span class='status-ok'>● 演示运行中</span></div>", unsafe_allow_html=True)
    st.caption(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

m1, m2, m3, m4 = st.columns(4)
metrics = [
    ("叶轮转速", f"{rotor_rpm} rpm", "用户可调演示参数"),
    ("风速", f"{wind:.1f} m/s", "环境输入 / 非现场传感器"),
    ("有效波高", f"{wave:.1f} m", "海况情景输入"),
    ("损伤演示值", f"{damage}%", "未由真实损伤数据校准"),
]
for col, (label, value, note) in zip([m1, m2, m3, m4], metrics):
    with col:
        st.markdown(
            f"<div class='metric-card'><div class='metric-label'>{label}</div>"
            f"<div class='metric-value'>{value}</div><div class='metric-note'>{note}</div></div>",
            unsafe_allow_html=True,
        )

st.write("")
left, right = st.columns([2.15, 1], gap="large")
with left:
    st.markdown("### 三维风机与叶片涂层状态")
    st.caption("拖动可旋转视角，滚轮可缩放；通过左侧参数改变转子姿态与热图演示值。")
    fig = make_turbine_figure(rotor_angle, damage, wind, wave, show_coating, focus_blade)
    st.plotly_chart(fig, use_container_width=True, config={"displaylogo": False, "scrollZoom": True})
with right:
    st.markdown("### 叶片状态评估")
    if damage >= 70:
        st.markdown("<div class='status-warn'>重点复核 · 高损伤演示情景</div>", unsafe_allow_html=True)
        advice = "建议检查叶片前缘、涂层连续性与局部侵蚀；此提示仅由演示阈值触发。"
    elif damage >= 35:
        st.markdown("<div class='status-warn'>建议检查 · 中等损伤演示情景</div>", unsafe_allow_html=True)
        advice = "建议结合现场巡检、无人机图像或材料试验确认损伤，不应仅依据此页面做维护决策。"
    else:
        st.markdown("<div class='status-ok'>常规观察 · 低损伤演示情景</div>", unsafe_allow_html=True)
        advice = "当前演示损伤值较低；这不代表真实叶片已通过安全评估。"
    st.write(advice)
    st.divider()
    st.markdown("### 环境参数")
    env_df = pd.DataFrame({
        "参数": ["风速", "有效波高", "环境温度", "叶轮转速", "损伤演示值"],
        "当前值": [f"{wind:.1f} m/s", f"{wave:.1f} m", f"{temperature:.1f} °C", f"{rotor_rpm} rpm", f"{damage}%"],
        "数据类型": ["用户输入演示值"] * 5,
    })
    st.dataframe(env_df, hide_index=True, use_container_width=True)
    st.markdown("### 研究边界")
    st.caption("此版本用于展示界面交互与数据流设计。没有连接真实SCADA、叶片传感器或经验证的损伤演化模型。")

st.divider()
st.markdown("### 当前演示数据")
positions = np.arange(1, 13)
rng = np.random.default_rng(20261025)
demo_index = np.clip(damage * (0.25 + 0.75 * positions / 12) + rng.normal(0, 3, 12), 0, 100)
zones = pd.DataFrame({
    "叶片分区": [f"S{i:02d}" for i in positions],
    "展向位置（示意）": [f"{(i-1)*8.0:.0f}–{i*8.0:.0f} m" for i in positions],
    "损伤指数（演示）": np.round(demo_index, 1),
    "质量标记": ["SIMULATED_DEMO"] * len(positions),
})
st.dataframe(zones, hide_index=True, use_container_width=True)
csv = zones.to_csv(index=False).encode("utf-8-sig")
st.download_button("下载演示分区 CSV", data=csv, file_name="pfd_blade_demo_zones.csv", mime="text/csv")

with st.expander("数据来源与免责声明"):
    st.write(
        "本页面的风机几何由代码程序生成；风速、波高、温度、转速和损伤值为用户调节的演示参数；"
        "分区损伤指数为展示交互而生成的模拟数据。它们不是实时天气、现场传感器或实验测量结果。"
        "本应用不提供经验证的剩余寿命预测，也不能替代风机运维工程师的安全判断。"
    )
