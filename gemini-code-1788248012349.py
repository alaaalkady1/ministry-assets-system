import streamlit as st
import pandas as pd

st.set_page_config(page_title="نظام إدارة العهد", page_icon="💼", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;900&display=swap');
    html, body, [class*="css"] { font-family: 'Tajawal', sans-serif; direction: rtl; text-align: right; }
    .main-header { background: #f1f5f9; color: #1e293b; padding: 20px; border-radius: 6px; border-right: 5px solid #0f172a; margin-bottom: 20px; }
</style>
""", unsafe_allow_html=True)

if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'assets_df' not in st.session_state:
    st.session_state.assets_df = pd.DataFrame({
        "الممنطقة": ["مبنى وزارة التربية", "حولي"], "اسم الموظف": ["ساره خالد", "خالد بدر"],
        "رقم الباركود": ["BAR-003", "BAR-004"], "الحالة": ["يعمل", "قيد الصيانة"]
    })

if not st.session_state.logged_in:
    st.markdown("<div class='main-header'><h2>نظام عهد الدعم التقني</h2><p>التصميم البسيط والفاخر</p></div>", unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        with st.form("l"):
            u = st.text_input("اسم المستخدم")
            p = st.text_input("كلمة المرور", type="password")
            if st.form_submit_button("دخول", use_container_width=True):
                if u == "admin" and p == "123": st.session_state.logged_in = True; st.rerun()
                else: st.error("خطأ (admin / 123)")
    st.stop()

st.sidebar.title("الخيارات")
if st.sidebar.button("خروج"): st.session_state.logged_in = False; st.rerun()
st.markdown("<div class='main-header'><h2>سجل الأجهزة والعهد</h2></div>", unsafe_allow_html=True)
st.dataframe(st.session_state.assets_df, use_container_width=True)
