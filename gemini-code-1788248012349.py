import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="نظام إدارة العهد - وزارة التربية", page_icon="🛡️", layout="wide")

# Custom Styling - Official Emerald Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Tajawal', sans-serif; direction: rtl; text-align: right; }
    .main-header { background: linear-gradient(135deg, #1b4d3e 0%, #2c6b56 100%); color: white; padding: 25px; border-radius: 8px; margin-bottom: 20px; text-align: center; }
</style>
""", unsafe_allow_html=True)

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'assets_df' not in st.session_state:
    st.session_state.assets_df = pd.DataFrame({
        "الممنطقة": ["مبنى وزارة التربية", "العاصمة"], "اسم الموظف": ["أحمد محمد", "فهد عبد الله"],
        "رقم الباركود": ["BAR-001", "BAR-002"], "رقم ونوع الجهاز": ["DELL-5090", "HP-ProDesk"], "الحالة": ["يعمل", "يعمل"]
    })

if not st.session_state.logged_in:
    st.markdown("<div class='main-header'><h1>نظام إدارة العهد والأجهزة التقنية</h1><p>وزارة التربية - قسم التشغيل والدعم التقني</p></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        with st.form("login"):
            u = st.text_input("اسم المستخدم")
            p = st.text_input("كلمة المرور", type="password")
            if st.form_submit_button("تسجيل الدخول", use_container_width=True):
                if u == "admin" and p == "123": st.session_state.logged_in = True; st.rerun()
                else: st.error("بيانات غير صحيحة (admin / 123)")
    st.stop()

st.sidebar.title("لوحة التحكم")
if st.sidebar.button("خروج"): st.session_state.logged_in = False; st.rerun()
st.markdown("<div class='main-header'><h1>لوحة عهد وزارة التربية</h1></div>", unsafe_allow_html=True)
st.dataframe(st.session_state.assets_df, use_container_width=True)
