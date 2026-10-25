import hmac
import os
import streamlit as st


def require_login():
    """Optional shared-password gate. Set APP_PASSWORD in Streamlit Secrets."""
    try:
        expected = str(st.secrets.get("APP_PASSWORD", "")).strip()
    except Exception:
        expected = os.environ.get("APP_PASSWORD", "").strip()

    if not expected:
        st.sidebar.warning("未配置 APP_PASSWORD：当前为开发模式，无密码保护。部署公开前请配置 Secrets。")
        return

    if "pfd_authenticated" not in st.session_state:
        st.session_state.pfd_authenticated = False

    if st.session_state.pfd_authenticated:
        with st.sidebar:
            st.success("团队访问已验证")
            if st.button("退出登录", use_container_width=True):
                st.session_state.pfd_authenticated = False
                st.rerun()
        return

    st.title("PFD 研究平台登录")
    st.caption("请输入团队共享访问密码")
    supplied = st.text_input("访问密码", type="password")
    if st.button("登录", type="primary"):
        if hmac.compare_digest(supplied, expected):
            st.session_state.pfd_authenticated = True
            st.rerun()
        else:
            st.error("密码不正确。")
    st.stop()
