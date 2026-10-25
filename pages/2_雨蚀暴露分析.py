import streamlit as st
import plotly.express as px
from pfd.auth import require_login
from pfd.ui import apply_theme
from pfd.erosion import add_exposure_proxy, aggregate_site_exposure, DISCLAIMER

st.set_page_config(page_title="雨蚀暴露分析 | PFD", layout="wide")
apply_theme()
require_login()
st.title("叶片前缘雨蚀：环境暴露筛查")
st.warning(DISCLAIMER)
st.markdown("""
该指标只用于演示如何把风与雨的历史时序转成可解释的场址筛查变量。它没有使用雨滴粒径分布、叶片相对速度、涂层材料性能、雨蚀试验曲线或现场损伤标签，因此**不是物理雨蚀模型，也不是经过训练的 AI 预测器**。
""")
df = st.session_state.get("pfd_weather_df")
if df is None:
    st.info("请先进入“历史天气与场址”页面获取数据。")
    st.stop()
out = add_exposure_proxy(df)
clean = out.sort_values(["site_id","timestamp_utc"]).drop_duplicates(["site_id","timestamp_utc"])
summary = aggregate_site_exposure(clean)
st.subheader("场址暴露指标汇总（无量纲）")
st.dataframe(summary.round(3), use_container_width=True, hide_index=True)
fig = px.line(clean, x="timestamp_utc", y="lee_exposure_proxy_0_100", color="site_id",
              title="LEE 环境暴露代理指标（0–100，不是损伤百分比）")
fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
st.plotly_chart(fig, use_container_width=True)
st.download_button("下载暴露分析 CSV", clean.to_csv(index=False).encode("utf-8-sig"),
                   "pfd_lee_exposure_proxy.csv", "text/csv")
with st.expander("查看模型假设与适用边界"):
    st.write(clean[["site_id","timestamp_utc","lee_exposure_proxy_0_100","model_status","model_assumptions"]].head(100))
