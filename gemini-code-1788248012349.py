import streamlit as st
import pandas as pd
from datetime import datetime
import io

st.set_page_config(page_title="نظام إدارة العهد - وزارة التربية", page_icon="🖥️", layout="wide", initial_sidebar_state="expanded")

# Custom Styling - Corporate Navy Theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Tajawal', sans-serif; direction: rtl; text-align: right; background-color: #0f172a; color: #f8fafc; }
    .main-header { background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); color: #38bdf8; padding: 25px; border-radius: 12px; margin-bottom: 25px; text-align: center; border: 1px solid #334155; box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.2); }
    .stSidebar { background-color: #1e293b !important; }
</style>
""", unsafe_allow_html=True)

# Session State & Data Setup
if 'users' not in st.session_state:
    st.session_state.users = {"admin": {"password": "123", "role": "مدير النظام", "region": "الكل"}}
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'assets_df' not in st.session_state:
    st.session_state.assets_df = pd.DataFrame({
        "الممنطقة": ["مبنى وزارة التربية", "العاصمة", "حولي"],
        "اسم الموظف": ["أحمد محمد", "فهد عبد الله", "ساره خالد"],
        "رقم الباركود": ["BAR-001", "BAR-002", "BAR-003"],
        "رقم ونوع الجهاز": ["DELL-5090 i7", "HP-ProDesk i5", "DELL-OptiPlex"],
        "رقم وحجم الشاشة": ["DELL-24 inch", "HP-22 inch", "DELL-27 inch"],
        "رقم ونوع الطابعة": ["HP LaserJet", "Canon", "Brother"],
        "الحالة": ["يعمل", "يعمل", "قيد الصيانة"]
    })

if not st.session_state.logged_in:
    st.markdown("<div class='main-header'><h1>نظام إدارة العهد التقنية</h1><p>قسم التشغيل والدعم التقني - الثيم التقني المودرن</p></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        with st.form("l"):
            u = st.text_input("اسم المستخدم")
            p = st.text_input("كلمة المرور", type="password")
            if st.form_submit_button("دخول", use_container_width=True):
                if u == "admin" and p == "123":
                    st.session_state.logged_in = True
                    st.rerun()
                else:
                    st.error("خطأ في البيانات (admin / 123)")
    st.stop()

st.sidebar.title("لوحة التحكم")
if st.sidebar.button("خروج"): st.session_state.logged_in = False; st.rerun()
st.markdown("<div class='main-header'><h1>نظام إدارة العهد والأجهزة التقنية</h1></div>", unsafe_allow_html=True)
st.dataframe(st.session_state.assets_df, use_container_width=True)
