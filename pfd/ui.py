import streamlit as st

def apply_theme():
    st.markdown("""
    <style>
    :root { color-scheme: dark; }
    .stApp {background:linear-gradient(180deg,#071522 0%,#091b2a 48%,#071522 100%);color:#eaf4fb}
    [data-testid="stSidebar"] {background:#0b1d2c;border-right:1px solid #203e51}
    .block-container {max-width:1680px;padding-top:1.15rem;padding-bottom:2.5rem}
    header[data-testid="stHeader"] {background:rgba(5,17,28,.88)}
    h1,h2,h3 {color:#eff8fc !important; letter-spacing:-.02em}
    p,li,label,.stMarkdown {color:#c8d9e4}
    .pfd-topbar {display:flex;align-items:center;justify-content:space-between;gap:18px;padding:12px 2px 20px;border-bottom:1px solid #1c3b4d;margin-bottom:20px}
    .pfd-brand {display:flex;align-items:center;gap:13px}
    .pfd-logo {display:flex;align-items:center;justify-content:center;width:48px;height:48px;border:1px solid #35d2dc;border-radius:12px;background:#103344;color:#62e7ee;font-weight:900;letter-spacing:1px;font-size:17px}
    .pfd-brand b {display:block;color:#e9f6fb;font-size:14px;letter-spacing:1.6px}
    .pfd-brand small {display:block;color:#7f9cac;font-size:12px;margin-top:4px}
    .pfd-live {border:1px solid #176454;background:#0b332f;color:#70e0bd;padding:8px 13px;border-radius:9px;font-size:12px;font-weight:700;white-space:nowrap}
    .pulse {display:inline-block;width:7px;height:7px;background:#51dfb4;border-radius:50%;margin-right:6px;box-shadow:0 0 9px #51dfb4}
    .pfd-title {padding:6px 0 20px}
    .pfd-kicker,.section-label {font-size:11px;letter-spacing:2px;font-weight:800;color:#50dbe5}
    .pfd-title h1 {font-size:clamp(1.65rem,3vw,2.45rem);margin:.55rem 0 .4rem}
    .pfd-title p {color:#8faabb;font-size:15px;margin:0}
    .section-label {margin:8px 0}
    div[data-testid="stMetric"] {background:linear-gradient(145deg,#112c40,#0d2233);border:1px solid #23465a;padding:15px 16px;border-radius:13px;min-height:104px}
    div[data-testid="stMetricLabel"] {color:#8faabd !important;font-size:13px}
    div[data-testid="stMetricValue"] {color:#58dce7 !important;font-size:1.7rem;font-weight:750}
    div[data-testid="stMetricDelta"] {font-size:11px}
    .status-card {padding:18px;border:1px solid #27475a;background:linear-gradient(145deg,#122c3e,#0c2030);border-radius:14px;margin-bottom:16px}
    .status-kicker {font-size:10px;letter-spacing:1.6px;color:#7896a8;font-weight:800}
    .status-value {font-size:28px;font-weight:800;margin:8px 0}
    .status-card p {font-size:13px;line-height:1.7;color:#a9bfcd;margin-bottom:0}
    .data-row {display:flex;justify-content:space-between;gap:12px;padding:12px 2px;border-bottom:1px solid #1e3a4c;font-size:13px}
    .data-row span {color:#8ea8b8}.data-row b {color:#e3f3f8}
    div.stButton > button, div.stDownloadButton > button, a[data-testid="stPageLink"] {border-radius:9px}
    div.stButton > button[kind="primary"] {background:#159e9a;border-color:#159e9a}
    [data-testid="stAlert"] {border-radius:11px}
    [data-testid="stDataFrame"] {border:1px solid #214256;border-radius:10px;overflow:hidden}
    footer {visibility:hidden}
    </style>
    """, unsafe_allow_html=True)
