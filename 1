import math
import streamlit as st
import plotly.graph_objects as go
import numpy as np
from pfd.auth import require_login
from pfd.ui import apply_theme

st.set_page_config(page_title="PFD | 海上风电数字孪生", page_icon="🌊", layout="wide")
apply_theme()
require_login()

# ---- State ----
defaults = {
    "pfd_rotor_rpm": 12,
    "pfd_wind_speed": 12.3,
    "pfd_wave_height": 2.1,
    "pfd_damage": 28,
    "pfd_rotor_angle": 0,
    "pfd_rotation_on": False,
    "pfd_show_coating": True,
    "pfd_selected_blade": "A",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

try:
    from streamlit_autorefresh import st_autorefresh
    if st.session_state.pfd_rotation_on:
        tick = st_autorefresh(interval=700, key="pfd_rotation_tick")
        st.session_state.pfd_rotor_angle = (tick * st.session_state.pfd_rotor_rpm * 360 / 60 * 0.7) % 360
except Exception:
    pass

def blade_color(value):
    # Discrete, high-contrast coating condition colors
    if value < 20: return "#21b8a6"
    if value < 40: return "#b7d94b"
    if value < 60: return "#ffbd4a"
    if value < 80: return "#ff784f"
    return "#ff3d62"

def make_turbine_figure(angle_deg, damage, wind_speed, wave_height, show_coating=True):
    fig = go.Figure()
    # Ocean surface, subtle grid-like wave texture
    xs = np.linspace(-95, 95, 24)
    ys = np.linspace(-95, 95, 24)
    X, Y = np.meshgrid(xs, ys)
    Z = -2.5 + 0.45*np.sin(X/13.0)*np.cos(Y/17.0) + 0.12*np.sin((X+Y)/5.0)
    fig.add_trace(go.Surface(
        x=X, y=Y, z=Z, showscale=False, opacity=0.92,
        colorscale=[[0,"#0c536a"],[0.45,"#126d82"],[1,"#238a9b"]],
        lighting=dict(ambient=0.72, diffuse=0.35, roughness=0.9, specular=0.1),
        hoverinfo="skip", name="海面"
    ))
    # Horizon/sky background is conveyed through scene background and ocean.
    # Monopile / tower
    fig.add_trace(go.Scatter3d(
        x=[0,0,0,0], y=[0,0,0,0], z=[-2,18,52,94],
        mode="lines", line=dict(color="#e6f2f6", width=13),
        hoverinfo="skip", name="塔筒"
    ))
    # Tower base / transition piece
    fig.add_trace(go.Scatter3d(
        x=[0,0], y=[0,0], z=[-2,5], mode="lines",
        line=dict(color="#a9c2ce", width=20), hoverinfo="skip", name="基础"
    ))
    # Three simple floating foundation columns
    for phi in (0, 120, 240):
        rad = math.radians(phi)
        bx, by = 5.5*math.cos(rad), 5.5*math.sin(rad)
        fig.add_trace(go.Scatter3d(
            x=[bx,bx], y=[by,by], z=[-12,-1],
            mode="lines", line=dict(color="#4c8794", width=15),
            hoverinfo="skip", showlegend=False
        ))
        fig.add_trace(go.Scatter3d(
            x=[bx,bx], y=[by,by], z=[-1.2,0],
            mode="lines", line=dict(color="#e5c96a", width=16),
            hoverinfo="skip", showlegend=False
        ))
    # Nacelle and hub
    fig.add_trace(go.Scatter3d(
        x=[-4,4], y=[0,0], z=[94,94], mode="lines",
        line=dict(color="#e8f1f5", width=19), hoverinfo="skip", name="机舱"
    ))
    fig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[94], mode="markers",
        marker=dict(size=9, color="#f5fbff", line=dict(color="#5d8291",width=2)),
        hovertemplate="轮毂<extra></extra>", name="轮毂"
    ))
    # Blade polygons. Each span segment has a distinct coating/damage color.
    base_angle = math.radians(angle_deg)
    blade_names = ["A", "B", "C"]
    for bi, name in enumerate(blade_names):
        theta = base_angle + math.radians(bi*120)
        radial = np.array([math.cos(theta), math.sin(theta)])  # y,z plane
        perp = np.array([-math.sin(theta), math.cos(theta)])
        span_edges = np.linspace(5.5, 61, 11)
        for si in range(len(span_edges)-1):
            r0, r1 = span_edges[si], span_edges[si+1]
            # Tapered chord, with a subtle swept leading edge.
            c0 = 4.8*(1-r0/72)+0.55
            c1 = 4.8*(1-r1/72)+0.55
            sweep0, sweep1 = 0.35*math.sin(r0/13), 0.35*math.sin(r1/13)
            # Blade lies mostly in rotor plane; small x-offset gives depth.
            p0 = np.array([sweep0, 0, 0])
            p1 = np.array([sweep1, 0, 0])
            def point(r, chord_sign, sweep):
                yz = radial*r + perp*(chord_sign*(4.8*(1-r/72)+0.55)/2)
                return [sweep, yz[0], 94+yz[1]]
            verts = [point(r0,-1,sweep0), point(r0,1,sweep0),
                     point(r1,1,sweep1), point(r1,-1,sweep1)]
            # Outer span has higher rain-erosion exposure; a local hotspot is visible.
            span_fraction = (r0+r1)/(2*61)
            hotspot = math.exp(-((span_fraction-0.78)/0.13)**2)
            blade_factor = 1.0 if name == st.session_state.pfd_selected_blade else 0.78
            local_damage = max(0, min(100, damage*blade_factor*(0.18+0.55*span_fraction+0.72*hotspot)))
            if not show_coating:
                col = "#dce8ee"
            else:
                col = blade_color(local_damage)
            fig.add_trace(go.Mesh3d(
                x=[v[0] for v in verts], y=[v[1] for v in verts], z=[v[2] for v in verts],
                i=[0,0], j=[1,2], k=[2,3],
                color=col, opacity=1, flatshading=True, lighting=dict(ambient=0.9,diffuse=0.45,specular=0.12,roughness=0.75),
                hovertemplate=f"叶片 {name}<br>分区 S{si+1:02d}<br>模拟损伤暴露值 {local_damage:.1f}%<extra></extra>",
                name=f"叶片{name}·S{si+1:02d}", showlegend=False
            ))
    # Far turbines for context
    for tx, ty, scale in [(-55,-28,0.68), (60,-25,0.55), (-48,42,0.48)]:
        hubz=94*scale
        fig.add_trace(go.Scatter3d(
            x=[tx,tx], y=[ty,ty], z=[-1,hubz],
            mode="lines", line=dict(color="#a7c5d0",width=5), opacity=0.72,
            hoverinfo="skip", showlegend=False
        ))
        fig.add_trace(go.Scatter3d(
            x=[tx], y=[ty], z=[hubz], mode="markers",
            marker=dict(size=4,color="#eaf5f8"), hoverinfo="skip", showlegend=False
        ))
        for bj in range(3):
            th=math.radians(angle_deg*0.55+bj*120)
            rr=22*scale
            fig.add_trace(go.Scatter3d(
                x=[tx,tx], y=[ty,ty+rr*math.cos(th)],
                z=[hubz,hubz+rr*math.sin(th)], mode="lines",
                line=dict(color="#d8e6ec",width=5), opacity=0.72,
                hoverinfo="skip", showlegend=False
            ))
    # Overlay legend for heatmap
    fig.add_trace(go.Scatter3d(
        x=[None], y=[None], z=[None], mode="markers",
        marker=dict(size=8, color=["#21b8a6","#b7d94b","#ffbd4a","#ff784f","#ff3d62"],
                    cmin=0,cmax=100,colorscale=[[0,"#21b8a6"],[0.25,"#b7d94b"],[0.5,"#ffbd4a"],[0.75,"#ff784f"],[1,"#ff3d62"]],
                    showscale=True, colorbar=dict(title="损伤暴露<br>示意值 (%)",tickfont=dict(color="#c4d7e2"),titlefont=dict(color="#c4d7e2"),bgcolor="rgba(9,24,38,.6)",outlinewidth=0,thickness=12,len=0.55)),
        showlegend=False, hoverinfo="skip"
    ))
    fig.update_layout(
        height=650, margin=dict(l=0,r=0,t=0,b=0),
        paper_bgcolor="#0a1724", plot_bgcolor="#0a1724",
        font=dict(family="Arial, Microsoft YaHei", color="#d8e8f0"),
        scene=dict(
            bgcolor="#0a1724",
            xaxis=dict(visible=False, range=[-95,95], showbackground=False),
            yaxis=dict(visible=False, range=[-95,95], showbackground=False),
            zaxis=dict(visible=False, range=[-18,175], showbackground=False),
            aspectmode="manual", aspectratio=dict(x=1.1,y=1.1,z=0.9),
            camera=dict(eye=dict(x=1.55,y=1.65,z=1.1))
        ),
        showlegend=False
    )
    return fig

# Header
st.markdown("""
<div class="pfd-topbar">
  <div class="pfd-brand"><span class="pfd-logo">PFD</span><div><b>OFFSHORE WIND · DIGITAL TWIN</b><small>海上风电机组状态监测与叶片涂层损伤演化研究</small></div></div>
  <div class="pfd-live"><span class="pulse"></span> 研究演示模式</div>
</div>
""", unsafe_allow_html=True)
st.markdown("""
<div class="pfd-title">
  <div class="pfd-kicker">WIND TURBINE · BLADE INTEGRITY · ENVIRONMENTAL EXPOSURE</div>
  <h1>海上风电数字孪生控制中心</h1>
  <p>环境变化 → 叶片分区暴露 → 状态评估 → 数据验证</p>
</div>
""", unsafe_allow_html=True)

# Controls sidebar
with st.sidebar:
    st.markdown("### 运行控制")
    st.session_state.pfd_rotor_rpm = st.slider("叶轮转速 (rpm)", 0, 24, int(st.session_state.pfd_rotor_rpm))
    st.session_state.pfd_wind_speed = st.slider("风速 (m/s)", 0.0, 35.0, float(st.session_state.pfd_wind_speed), 0.5)
    st.session_state.pfd_wave_height = st.slider("有效波高 (m)", 0.0, 15.0, float(st.session_state.pfd_wave_height), 0.1)
    st.session_state.pfd_damage = st.slider("叶片损伤暴露演示值 (%)", 0, 100, int(st.session_state.pfd_damage))
    st.session_state.pfd_selected_blade = st.selectbox("重点叶片", ["A","B","C"], index=["A","B","C"].index(st.session_state.pfd_selected_blade))
    st.session_state.pfd_show_coating = st.toggle("显示涂层损伤热图", value=st.session_state.pfd_show_coating)
    a,b = st.columns(2)
    if a.button("▶ 启动旋转", use_container_width=True):
        st.session_state.pfd_rotation_on = True
        st.rerun()
    if b.button("Ⅱ 暂停", use_container_width=True):
        st.session_state.pfd_rotation_on = False
        st.rerun()
    if st.button("↻ 叶轮转过 15°", use_container_width=True):
        st.session_state.pfd_rotation_on = False
        st.session_state.pfd_rotor_angle = (st.session_state.pfd_rotor_angle + 15) % 360
        st.rerun()
    st.caption("环境和损伤滑块仅用于交互演示，不代表现场传感器值或真实损伤测量。")

# KPI row
damage = st.session_state.pfd_damage
wind = st.session_state.pfd_wind_speed
wave = st.session_state.pfd_wave_height
rpm = st.session_state.pfd_rotor_rpm
k1,k2,k3,k4 = st.columns(4)
k1.metric("叶轮转速", f"{rpm} rpm", "交互设定")
k2.metric("环境风速", f"{wind:.1f} m/s", "演示输入")
k3.metric("有效波高", f"{wave:.1f} m", "演示输入")
k4.metric("损伤暴露演示值", f"{damage}%", "非实测损伤")

left, right = st.columns([2.2,1], gap="large")
with left:
    st.markdown('<div class="section-label">01 / 3D ASSET & ENVIRONMENT</div>', unsafe_allow_html=True)
    st.markdown("### 海上风机与叶片分区热图")
    fig = make_turbine_figure(st.session_state.pfd_rotor_angle, damage, wind, wave, st.session_state.pfd_show_coating)
    st.plotly_chart(fig, use_container_width=True, config={"displaylogo":False,"scrollZoom":True})
    st.caption("三维风机为程序生成的交互式示意几何；颜色用于演示分区暴露差异，不是经验证的涂层损伤场。可拖动旋转视角、滚轮缩放。")
with right:
    st.markdown('<div class="section-label">02 / BLADE INTEGRITY</div>', unsafe_allow_html=True)
    st.markdown("### 叶片状态")
    if damage >= 75:
        status, color, advice = "重点复核", "#ff5876", "演示暴露值较高。建议结合检查记录与材料试验数据核实。"
    elif damage >= 40:
        status, color, advice = "计划检查", "#ffbd4a", "建议重点检查前缘外段与雨蚀敏感区域。"
    else:
        status, color, advice = "持续观察", "#48d8bd", "当前演示值较低，仍需依靠真实检查数据判断。"
    st.markdown(f"""
    <div class="status-card"><div class="status-kicker">SIMULATED STATUS</div>
    <div class="status-value" style="color:{color}">{status}</div>
    <p>{advice}</p></div>
    """, unsafe_allow_html=True)
    st.markdown("#### 环境输入")
    st.markdown(f"""
    <div class="data-row"><span>风速</span><b>{wind:.1f} m/s</b></div>
    <div class="data-row"><span>有效波高</span><b>{wave:.1f} m</b></div>
    <div class="data-row"><span>重点叶片</span><b>{st.session_state.pfd_selected_blade}</b></div>
    <div class="data-row"><span>转子角度</span><b>{st.session_state.pfd_rotor_angle:.0f}°</b></div>
    """, unsafe_allow_html=True)
    st.markdown("#### 研究边界")
    st.info("本页为可交互的数字孪生展示原型。环境参数可手动调节；损伤热图是可视化演示值，尚未由真实叶片损伤数据校准。")

st.markdown("---")
st.markdown("### 研究工作流")
w1,w2,w3,w4 = st.columns(4)
w1.markdown("**01 历史天气**\n\n查询公开历史再分析数据。")
w2.markdown("**02 数据审计**\n\n检查缺失、重复和异常记录。")
w3.markdown("**03 暴露分析**\n\n计算透明的环境暴露代理指标。")
w4.markdown("**04 独立验证**\n\n与公开图谱、试验或检查记录比较。")
st.warning("科研声明：天气再分析不是风场现场实测；三维风机和损伤热图为演示模型；本项目不输出经过验证的剩余寿命预测。")
st.markdown("### 快速入口")
q1,q2,q3,q4 = st.columns(4)
q1.page_link("pages/1_历史天气与场址.py", label="历史天气与场址", icon="🌦️")
q2.page_link("pages/2_雨蚀暴露分析.py", label="雨蚀暴露分析", icon="📈")
q3.page_link("pages/3_数据质量与来源.py", label="数据质量与来源", icon="🧪")
q4.page_link("pages/4_验证与研究记录.py", label="验证与研究记录", icon="📚")
