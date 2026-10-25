import streamlit as st
import pandas as pd
from pfd.auth import require_login
from pfd.ui import apply_theme
from pfd.weather import UNITS, quality_check, analysis_copy

st.set_page_config(page_title="数据质量与来源 | PFD", layout="wide")
apply_theme()
require_login()
st.title("数据质量、来源与可追溯性")
df = st.session_state.get("pfd_weather_df")
if df is None:
    st.info("请先获取历史天气数据。")
    st.stop()
a,b,c = st.columns(3)
a.metric("原始记录数", f"{len(df):,}")
b.metric("质量标记记录", f"{(df.quality_status != 'range_checks_passed').sum():,}")
c.metric("重复时间记录", f"{df.duplicated(['site_id','timestamp_utc'], keep=False).sum():,}")
st.subheader("数据字典")
dict_rows = [
    ("timestamp_utc","UTC 时间戳","时间索引"),
    ("site_id","候选场址名称","场址标识"),
    ("source_type","reanalysis","来源类别，不是现场实测"),
    ("source_name","Open-Meteo / ERA5-family reanalysis","数据来源"),
    ("retrieved_at_utc","API 获取时间","抓取时间"),
    ("api_response_sha256","响应 JSON 的 SHA-256","用于审计响应内容是否一致"),
    ("quality_flags","缺失、范围异常、重复记录标记","质量审计"),
]
dict_rows += [(k, v, "单位："+UNITS.get(k,"—")) for k,v in UNITS.items()]
st.dataframe(pd.DataFrame(dict_rows, columns=["字段","说明","用途/单位"]), use_container_width=True, hide_index=True)
st.subheader("来源分布")
st.dataframe(df.groupby(["source_name","source_type","quality_status"], dropna=False).size().reset_index(name="记录数"),
             use_container_width=True, hide_index=True)
st.caption("质量检查是基本范围检查，不代表气象数据已经过现场校准。重复记录在原始表中保留；分析副本才执行去重。")
st.download_button("导出质量审计 CSV", df.to_csv(index=False).encode("utf-8-sig"),
                   "pfd_data_quality_audit.csv", "text/csv")
