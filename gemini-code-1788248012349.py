import streamlit as st
import pandas as pd
from datetime import datetime
import io

st.set_page_config(
    page_title="نظام إدارة العهد والأجهزة - وزارة التربية",
    page_icon="🖥️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling & RTL support
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@400;500;700;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Tajawal', sans-serif;
        direction: rtl;
        text-align: right;
    }
    
    .main-header {
        background: linear-gradient(135deg, #1b4d3e 0%, #2c6b56 100%);
        color: white;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State
if 'users' not in st.session_state:
    st.session_state.users = {
        "admin": {"password": "123", "role": "مدير النظام", "region": "الكل"},
        "supervisor_asima": {"password": "123", "role": "مشرف منطقة", "region": "العاصمة"},
        "tech1": {"password": "123", "role": "فني / مُدخل بيانات", "region": "مبنى وزارة التربية"}
    }

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.role = ""
    st.session_state.region = ""

if 'assets_df' not in st.session_state:
    data = {
        "الممنطقة": ["مبنى وزارة التربية", "العاصمة", "حولي", "مبارك الكبير", "الفروانيه", "الجهراء", "الاحمدي"],
        "اسم الموظف": ["أحمد محمد", "فهد عبد الله", "ساره خالد", "خالد بدر", "نورة علي", "محمد العتيبي", "ناصر الصباح"],
        "رقم الباركود": ["BAR-001", "BAR-002", "BAR-003", "BAR-004", "BAR-005", "BAR-006", "BAR-007"],
        "رقم ونوع الجهاز": ["DELL-5090 i7", "HP-ProDesk i5", "DELL-OptiPlex", "HP-EliteDesk", "DELL-5090 i5", "HP-ProDesk i7", "DELL-OptiPlex i5"],
        "رقم وحجم الشاشة": ["DELL-24 inch", "HP-22 inch", "DELL-27 inch", "SAMSUNG-24 inch", "HP-24 inch", "DELL-22 inch", "LG-24 inch"],
        "رقم ونوع الطابعة": ["HP LaserJet M404", "Canon LBP6030", "Brother HL-L2350", "HP LaserJet Pro", "Canon i-SENSYS", "Epson L3210", "HP LaserJet M404"],
        "الشاشة التفاعلية (Hikvision)": ["HIK-DS-55", "HIK-DS-65", "غير متوفر", "HIK-DS-75", "HIK-DS-55", "غير متوفر", "HIK-DS-65"],
        "الحالة": ["يعمل", "يعمل", "قيد الصيانة", "يعمل", "يعمل", "معطل", "يعمل"],
        "تاريخ التحديث": [datetime.now().strftime("%Y-%m-%d")] * 7
    }
    st.session_state.assets_df = pd.DataFrame(data)

if 'audit_log' not in st.session_state:
    st.session_state.audit_log = pd.DataFrame(columns=["التاريخ والوقت", "المستخدم", "العملية", "التفاصيل"])

REGIONS = ["مبنى وزارة التربية", "العاصمة", "حولي", "مبارك الكبير", "الفروانيه", "الجهراء", "الاحمدي"]

# --- LOGIN SCREEN ---
if not st.session_state.logged_in:
    st.markdown("<div class='main-header'><h1>نظام إدارة العهد والأجهزة التقنية</h1><p>قسم التشغيل والدعم التقني - وزارة التربية (الكويت)</p></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.subheader("تسجيل الدخول للنظام")
        with st.form("login_form"):
            username_input = st.text_input("اسم المستخدم")
            password_input = st.text_input("كلمة المرور", type="password")
            submit_login = st.form_submit_button("دخول", use_container_width=True)
            
            if submit_login:
                if username_input in st.session_state.users and st.session_state.users[username_input]["password"] == password_input:
                    st.session_state.logged_in = True
                    st.session_state.username = username_input
                    st.session_state.role = st.session_state.users[username_input]["role"]
                    st.session_state.region = st.session_state.users[username_input]["region"]
                    st.success("تم تسجيل الدخول بنجاح!")
                    st.rerun()
                else:
                    st.error("اسم المستخدم أو كلمة المرور غير صحيحة.")
        
        st.info("💡 بيانات الدخول للاختبار:\n- **مدير النظام:** `admin` | كلمة المرور: `123`\n- **فني الدعم:** `tech1` | كلمة المرور: `123`")
    st.stop()

# --- MAIN APP INTERFACE ---
st.sidebar.title("لوحة التحكم")
st.sidebar.write(f"👤 **المستخدم:** {st.session_state.username}")
st.sidebar.write(f"🛡️ **الصلاحية:** {st.session_state.role}")

if st.sidebar.button("تسجيل الخروج", use_container_width=True):
    st.session_state.logged_in = False
    st.rerun()

st.sidebar.divider()
menu = st.sidebar.radio("القائمة الرئيسية", [
    "📊 الشاشة التفاعلية (Dashboard)",
    "💻 إدارة الأجهزة والعهد",
    "📥 استيراد من ملف إكسيل",
    "📋 سجل الحركات (Audit Log)"
])

st.markdown("<div class='main-header'><h1>نظام إدارة العهد والأجهزة التقنية</h1><p>وزارة التربية - قسم التشغيل والدعم التقني</p></div>", unsafe_allow_html=True)

df = st.session_state.assets_df

if st.session_state.role == "مشرف منطقة":
    df_filtered = df[df["الممنطقة"] == st.session_state.region]
else:
    df_filtered = df

# 1. DASHBOARD
if menu == "📊 الشاشة التفاعلية (Dashboard)":
    st.subheader("📊 لوحة المؤشرات والإحصائيات التفاعلية")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="إجمالي الأجهزة والعهد", value=len(df))
    with col2:
        st.metric(label="الأجهزة العاملة", value=len(df[df["الحالة"] == "يعمل"]))
    with col3:
        st.metric(label="قيد الصيانة / معطلة", value=len(df[df["الحالة"].isin(["قيد الصيانة", "معطل"])]))
    with col4:
        st.metric(label="المناطق والمباني", value=len(REGIONS))
        
    st.divider()
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("### 🏢 توزيع الأجهزة حسب المناطق")
        st.dataframe(df["الممنطقة"].value_counts().reset_index(), use_container_width=True, hide_index=True)
    with c2:
        st.markdown("### 📈 حالة الأجهزة العامة")
        st.dataframe(df["الحالة"].value_counts().reset_index(), use_container_width=True, hide_index=True)

# 2. ASSETS MANAGEMENT
elif menu == "💻 إدارة الأجهزة والعهد":
    st.subheader("💻 إدارة الأجهزة والبحث بالباركود")
    search_query = st.text_input("🔍 بحث سريـع (برقم الباركود الأصلي، اسم الموظف، نوع الجهاز...):")
    
    display_df = df_filtered
    if search_query:
        mask = display_df.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)
        display_df = display_df[mask]
        
    st.dataframe(display_df, use_container_width=True)
    
    st.divider()
    with st.expander("➕ إضافة جهاز / عهدة جديدة"):
        with st.form("add_asset_form"):
            c1, c2 = st.columns(2)
            with c1:
                new_region = st.selectbox("المنطقة / المبنى", REGIONS)
                new_emp = st.text_input("اسم الموظف")
                new_barcode = st.text_input("رقم الباركود (Serial Number)")
                new_device = st.text_input("رقم ونوع الجهاز")
            with c2:
                new_screen_num = st.text_input("رقم وحجم الشاشة")
                new_printer = st.text_input("رقم ونوع الطابعة")
                new_hik = st.text_input("الشاشة التفاعلية (Hikvision)")
                new_status = st.selectbox("الحالة", ["يعمل", "قيد الصيانة", "معطل", "متوفر في المخزن"])
                
            submit_add = st.form_submit_button("حفظ وإضافة الجهاز")
            if submit_add:
                if new_barcode and new_emp:
                    new_row = {
                        "الممنطقة": new_region, "اسم الموظف": new_emp, "رقم الباركود": new_barcode,
                        "رقم ونوع الجهاز": new_device, "رقم وحجم الشاشة": new_screen_num,
                        "رقم ونوع الطابعة": new_printer, "الشاشة التفاعلية (Hikvision)": new_hik,
                        "الحالة": new_status, "تاريخ التحديث": datetime.now().strftime("%Y-%m-%d")
                    }
                    st.session_state.assets_df = pd.concat([st.session_state.assets_df, pd.DataFrame([new_row])], ignore_index=True)
                    
                    new_log = pd.DataFrame([{
                        "التاريخ والوقت": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "المستخدم": st.session_state.username,
                        "العملية": "إضافة جهاز جديد",
                        "التفاصيل": f"باركود: {new_barcode}"
                    }])
                    st.session_state.audit_log = pd.concat([st.session_state.audit_log, new_log], ignore_index=True)
                    st.success("تمت إضافة الجهاز بنجاح!")
                    st.rerun()
                else:
                    st.error("يرجى ملء حقل رقم الباركود واسم الموظف.")

# 3. EXCEL IMPORT
elif menu == "📥 استيراد من ملف إكسيل":
    st.subheader("📥 استيراد البيانات عبر ملف إكسيل")
    sample_data = pd.DataFrame({
        "الممنطقة": ["العاصمة"], "اسم الموظف": ["محمد أحمد"], "رقم الباركود": ["BAR-101"],
        "رقم ونوع الجهاز": ["DELL i7"], "رقم وحجم الشاشة": ["24 inch"], "رقم ونوع الطابعة": ["HP LaserJet"],
        "الشاشة التفاعلية (Hikvision)": ["HIK-55"], "الحالة": ["يعمل"]
    })
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        sample_data.to_excel(writer, index=False, sheet_name='Assets')
    buffer.seek(0)
    
    st.download_button("📥 تحميل نموذج ملف الإكسيل الجاهز", data=buffer, file_name="asset_template.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    
    uploaded_file = st.file_uploader("اختر ملف إكسيل (.xlsx)", type=["xlsx"])
    if uploaded_file is not None:
        try:
            imported_df = pd.read_excel(uploaded_file)
            st.write("معاينة البيانات المستوردة:", imported_df.head())
            if st.button("تأكيد واعتماد استيراد البيانات"):
                imported_df["تاريخ التحديث"] = datetime.now().strftime("%Y-%m-%d")
                st.session_state.assets_df = pd.concat([st.session_state.assets_df, imported_df], ignore_index=True)
                st.success("تم استيراد الملف ودمج البيانات بنجاح!")
                st.rerun()
        except Exception as e:
            st.error(f"خطأ: {e}")

# 4. AUDIT LOG
elif menu == "📋 سجل الحركات (Audit Log)":
    st.subheader("📋 سجل الحركات والعمليات (Audit Log & History)")
    if len(st.session_state.audit_log) > 0:
        st.dataframe(st.session_state.audit_log, use_container_width=True)
    else:
        st.info("لا توجد حركات مسجلة حتى الآن.")
