from datetime import date, timedelta
import pandas as pd
import streamlit as st
import plotly.express as px
from pfd.auth import require_login
from pfd.ui import apply_theme
from pfd.weather import SITES, fetch_archive, quality_check, save_dataset, analysis_copy

st.set_page_config(page_title="历史天气与场址 | PFD", layout="wide")
apply_theme()
require_login()
st.title("历史天气与多场址对比")
st.caption("数据源：Open-Meteo Historical Weather API。历史再分析估计，不是现场传感器实测。")
st.markdown("[API 文档](https://open-meteo.com/en/docs/historical-weather-api) · [数据与许可说明](https://open-meteo.com/en/terms)")

with st.sidebar:
    st.subheader("查询设置")
    selected = st.multiselect("候选场址", list(SITES), default=list(SITES))
    end_default = date.today() - timedelta(days=7)
    end = st.date_input("结束日期（UTC）", end_default, max_value=end_default)
    start = st.date_input("开始日期（UTC）", end - timedelta(days=13), max_value=end)
    go = st.button("获取历史天气", type="primary", use_container_width=True)

if "pfd_weather_df" not in st.session_state:
    st.session_state.pfd_weather_df = None
if go:
    if not selected:
        st.error("至少选择一个场址。")
        st.stop()
    if start >= end:
        st.error("开始日期必须早于结束日期。")
        st.stop()
    if (end - start).days > 31:
        st.error("单次最多查询 31 天，避免长时间请求和页面负载。")
        st.stop()
    frames, errors = [], []
    with st.spinner("正在获取历史再分析数据……"):
        for name in selected:
            try:
                df, _ = fetch_archive(name, SITES[name], start.isoformat(), end.isoformat())
                frames.append(df)
            except Exception as exc:
                errors.append(f"{name}: {type(exc).__name__}: {exc}")
    if frames:
        raw = pd.concat(frames, ignore_index=True)
        checked = quality_check(raw)
        st.session_state.pfd_weather_df = checked
        st.session_state.pfd_weather_query = {"start": start.isoformat(), "end": end.isoformat(), "sites": selected}
        raw_path, checked_path = save_dataset(raw)
        st.success(f"已保存原始数据：{raw_path}；质量标记数据：{checked_path}")
    for error in errors:
        st.error(error)
    if not frames:
        st.warning("未获取到数据。请检查网络或缩短日期范围；本页面不会悄悄用模拟数据替代真实数据。")

df = st.session_state.pfd_weather_df
if df is None:
    st.info("选择场址和日期后点击“获取历史天气”。")
    st.stop()

clean = analysis_copy(df)
a,b,c,d = st.columns(4)
a.metric("记录数（含原始重复项）", f"{len(df):,}")
b.metric("分析记录数（去重副本）", f"{len(clean):,}")
c.metric("标记记录", f"{(df.quality_status != 'range_checks_passed').sum():,}")
d.metric("场址数", f"{clean.site_id.nunique()}")

summary = clean.groupby(["site_id","site_type"], as_index=False).agg(
    平均风速100m=("wind_speed_100m","mean"),
    平均风速10m=("wind_speed_10m","mean"),
    最大阵风=("wind_gusts_10m","max"),
    累计降雨=("rain","sum"),
    平均温度=("temperature_2m","mean"),
    平均湿度=("relative_humidity_2m","mean"),
)
st.subheader("场址汇总")
st.dataframe(summary.round(3), use_container_width=True, hide_index=True)
var = st.selectbox("绘图变量", {
    "100 m 风速 (m/s)":"wind_speed_100m",
    "10 m 风速 (m/s)":"wind_speed_10m",
    "阵风 (m/s)":"wind_gusts_10m",
    "降雨 (mm/hour)":"rain",
    "气温 (°C)":"temperature_2m",
    "相对湿度 (%)":"relative_humidity_2m",
})
fig = px.line(clean, x="timestamp_utc", y=var, color="site_id", title=f"{var} · 历史时序")
fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig, use_container_width=True)
st.download_button("下载当前分析数据 CSV", clean.to_csv(index=False).encode("utf-8-sig"),
                   "pfd_weather_analysis.csv", "text/csv")
st.download_button("下载带质量标记的原始记录 CSV", df.to_csv(index=False).encode("utf-8-sig"),
                   "pfd_weather_raw_with_quality_flags.csv", "text/csv")
with st.expander("查看质量问题记录"):
    issues = df[df.quality_status != "range_checks_passed"]
    st.dataframe(issues, use_container_width=True, hide_index=True)
