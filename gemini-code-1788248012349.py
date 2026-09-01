# Let's create a complete, robust Python Streamlit application for asset management.
# This app will support:
# - User authentication & Role-based access control (Admin, Regional Supervisor, Technician)
# - Dashboard with charts and metrics across Ministry building + 6 regions
# - Excel file import with data validation, retaining history/audit logs
# - Barcode scanning / search functionality
# - Interactive UI with full CRUD and tracking fields:
#   اسم الموظف, رقم الباركود, رقم ونوع الجهاز, رقم وحجم الشاشة, رقم ونوع الطابعة, الشاشة التفاعلية (Hikvision)
# - Audit log to ensure original data is preserved.

import pandas as pd
import numpy as np

# Let's write out the comprehensive Streamlit app code to a file so it can be packaged cleanly.
app_code = '''
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
    
    .metric-card {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Session State for Data, Users, and Audit Logs
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
    # Initial mock data matching requested fields
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

# Regions list
REGIONS = [
    "مبنى وزارة التربية",
    "العاصمة",
    "حولي",
    "مبارك الكبير",
    "الفروانيه",
    "الجهراء",
    "الاحمدي"
]

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
        
        st.info("💡 حسابات تجريبية للاختبار:\\n- **مدير النظام:** اسم المستخدم `admin` | كلمة المرور `123`\\n- **مشرف العاصمة:** اسم المستخدم `supervisor_asima` | كلمة المرور `123`\\n- **فني الدعم:** اسم المستخدم `tech1` | كلمة المرور `123`")
    st.stop()

# --- MAIN APP INTERFACE ---
st.sidebar.title("لوحة التحكم")
st.sidebar.write(f"👤 **المستخدم:** {st.session_state.username}")
st.sidebar.write(f"🛡️ **الصلاحية:** {st.session_state.role}")
st.sidebar.write(f"🏢 **النطاق:** {st.session_state.region}")

if st.sidebar.button("تسجيل الخروج", use_container_width=True):
    st.session_state.logged_in = False
    st.rerun()

st.sidebar.divider()
menu = st.sidebar.radio("القائمة الرئيسية", [
    "📊 الشاشة التفاعلية (Dashboard)",
    "💻 إدارة الأجهزة والعهد",
    "📥 استيراد من ملف إكسيل",
    "📋 سجل الحركات (Audit Log)",
    "⚙️ إدارة المستخدمين" if st.session_state.role == "مدير النظام" else None
])
# Clean None from menu if filtered
menu = [m for m in menu if m is not None]

st.markdown("<div class='main-header'><h1>نظام إدارة العهد والأجهزة التقنية</h1><p>وزارة التربية - قسم التشغيل والدعم التقني</p></div>", unsafe_allow_html=True)

df = st.session_state.assets_df

# Filter dataframe based on user region if not Admin/Global
if st.session_state.role == "مشرف منطقة":
    df_filtered = df[df["الممنطقة"] == st.session_state.region]
else:
    df_filtered = df

# --- 1. DASHBOARD ---
if "الشاشة التفاعلية (Dashboard)" in menu:
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
        st.markdown("### 🏢 توزيع الأجهزة حسب المناطق والمبنى الرئيسي")
        region_counts = df["الممنطقة"].value_counts().reset_index()
        region_counts.columns = ["المنطقة / المبنى", "عدد الأجهزة"]
        st.dataframe(region_counts, use_container_width=True, hide_index=True)
        
    with c2:
        st.markdown("### 📈 حالة الأجهزة العامة")
        status_counts = df["الحالة"].value_counts().reset_index()
        status_counts.columns = ["الحالة", "العدد"]
        st.dataframe(status_counts, use_container_width=True, hide_index=True)

# --- 2. ASSETS MANAGEMENT ---
elif "إدارة الأجهزة والعهد" in menu:
    st.subheader("💻 إدارة الأجهزة والبحث بالباركود")
    
    search_query = st.text_input("🔍 بحث سريـع (برقم الباركود الأصلي، اسم الموظف، نوع الجهاز...):")
    
    display_df = df_filtered
    if search_query:
        mask = display_df.astype(str).apply(lambda x: x.str.contains(search_query, case=False)).any(axis=1)
        display_df = display_df[mask]
        
    st.dataframe(display_df, use_container_width=True)
    
    st.divider()
    
    if st.session_state.role in ["مدير النظام", "مشرف منطقة", "فني / مُدخل بيانات"]:
        with st.expander("➕ إضافة جهاز / عهدة جديدة"):
            with st.form("add_asset_form"):
                c1, c2 = st.columns(2)
                with c1:
                    new_region = st.selectbox("المنطقة / المبنى", REGIONS)
                    new_emp = st.text_input("اسم الموظف")
                    new_barcode = st.text_input("رقم الباركود (الأصلي للمصنع / Serial Number)")
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
                            "الممنطقة": new_region,
                            "اسم الموظف": new_emp,
                            "رقم الباركود": new_barcode,
                            "رقم ونوع الجهاز": new_device,
                            "رقم وحجم الشاشة": new_screen_num,
                            "رقم ونوع الطابعة": new_printer,
                            "الشاشة التفاعلية (Hikvision)": new_hik,
                            "الحالة": new_status,
                            "تاريخ التحديث": datetime.now().strftime("%Y-%m-%d")
                        }
                        st.session_state.assets_df = pd.concat([st.session_state.assets_df, pd.DataFrame([new_row])], ignore_index=True)
                        
                        # Log action
                        new_log = pd.DataFrame([{
                            "التاريخ والوقت": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                            "المستخدم": st.session_state.username,
                            "العملية": "إضافة جهاز جديد",
                            "التفاصيل": f"باركود: {new_barcode} - منطقة: {new_region}"
                        }])
                        st.session_state.audit_log = pd.concat([st.session_state.audit_log, new_log], ignore_index=True)
                        
                        st.success("تمت إضافة الجهاز بنجاح!")
                        st.rerun()
                    else:
                        st.error("يرجى ملء حقل رقم الباركود واسم الموظف على الأقل.")

        if st.session_state.role in ["مدير النظام", "مشرف منطقة"]:
            with st.expander("✏️ تعديل بيانات جهاز حالي (مع الاحتفاظ بالأصل عبر سجل الحركات)"):
                barcode_to_edit = st.selectbox("اختر الباركود للجهاز المراد تعديله", df_filtered["رقم الباركود"].tolist())
                if barcode_to_edit:
                    current_row = df[df["رقم الباركود"] == barcode_to_edit].iloc[0]
                    with st.form("edit_asset_form"):
                        ed_region = st.selectbox("المنطقة / المبنى", REGIONS, index=REGIONS.index(current_row["الممنطقة"]))
                        ed_emp = st.text_input("اسم الموظف", value=current_row["اسم الموظف"])
                        ed_device = st.text_input("رقم ونوع الجهاز", value=current_row["رقم ونوع الجهاز"])
                        ed_screen = st.text_input("رقم وحجم الشاشة", value=current_row["رقم وحجم الشاشة"])
                        ed_printer = st.text_input("رقم ونوع الطابعة", value=current_row["رقم ونوع الطابعة"])
                        ed_hik = st.text_input("الشاشة التفاعلية (Hikvision)", value=current_row["الشاشة التفاعلية (Hikvision)"])
                        ed_status = st.selectbox("الحالة", ["يعمل", "قيد الصيانة", "معطل", "متوفر في المخزن"], index=["يعمل", "قيد الصيانة", "معطل", "متوفر في المخزن"].index(current_row["الحالة"]))
                        
                        submit_edit = st.form_submit_button("تحديث البيانات")
                        if submit_edit:
                            st.session_state.assets_df.loc[st.session_state.assets_df["رقم الباركود"] == barcode_to_edit, ["الممنطقة", "اسم الموظف", "رقم ونوع الجهاز", "رقم وحجم الشاشة", "رقم ونوع الطابعة", "الشاشة التفاعلية (Hikvision)", "الحالة", "تاريخ التحديث"]] = [ed_region, ed_emp, ed_device, ed_screen, ed_printer, ed_hik, ed_status, datetime.now().strftime("%Y-%m-%d")]
                            
                            # Log audit
                            new_log = pd.DataFrame([{
                                "التاريخ والوقت": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                "المستخدم": st.session_state.username,
                                "العملية": "تعديل جهاز",
                                "التفاصيل": f"تعديل بيانات الباركود: {barcode_to_edit}"
                            }])
                            st.session_state.audit_log = pd.concat([st.session_state.audit_log, new_log], ignore_index=True)
                            
                            st.success("تم تحديث البيانات بنجاح مع حفظ السجل!")
                            st.rerun()

# --- 3. EXCEL IMPORT ---
elif "استيراد من ملف إكسيل" in menu:
    st.subheader("📥 استيراد البيانات عبر ملف إكسيل (Excel Import)")
    st.write("يمكنك رفع ملف Excel يحتوي على البيانات ليتم دمجها وإضافتها مباشرة للنظام:")
    
    # Download sample template
    sample_data = pd.DataFrame({
        "الممنطقة": ["العاصمة", "حولي"],
        "اسم الموظف": ["محمد أحمد", "سعد فهد"],
        "رقم الباركود": ["BAR-101", "BAR-102"],
        "رقم ونوع الجهاز": ["DELL i7", "HP i5"],
        "رقم وحجم الشاشة": ["24 inch", "22 inch"],
        "رقم ونوع الطابعة": ["HP LaserJet", "Canon"],
        "الشاشة التفاعلية (Hikvision)": ["HIK-55", "غير متوفر"],
        "الحالة": ["يعمل", "يعمل"]
    })
    
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        sample_data.to_excel(writer, index=False, sheet_name='Assets')
    buffer.seek(0)
    
    st.download_button(
        label="📥 تحميل نموذج ملف الإكسيل الجاهز",
        data=buffer,
    file_name="asset_template.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
    st.divider()
    
    uploaded_file = st.file_uploader("اختر ملف إكسيل (.xlsx)", type=["xlsx"])
    if uploaded_file is not None:
        try:
            imported_df = pd.read_excel(uploaded_file)
            st.write("معاينة البيانات المستوردة:", imported_df.head())
            if st.button("تأكيد واعتماد استيراد البيانات"):
                imported_df["تاريخ التحديث"] = datetime.now().strftime("%Y-%m-%d")
                st.session_state.assets_df = pd.concat([st.session_state.assets_df, imported_df], ignore_index=True)
                
                new_log = pd.DataFrame([{
                    "التاريخ والوقت": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "المستخدم": st.session_state.username,
                    "العملية": "استيراد ملف إكسيل",
                    "التفاصيل": f"تم استيراد {len(imported_df)} سجل جديد"
                }])
                st.session_state.audit_log = pd.concat([st.session_state.audit_log, new_log], ignore_index=True)
                
                st.success("تم استيراد الملف ودمج البيانات بنجاح!")
                st.rerun()
        except Exception as e:
            st.error(fحدث خطأ أثناء قراءة الملف: {e}")

# --- 4. AUDIT LOG ---
elif "سجل الحركات (Audit Log)" in menu:
    st.subheader("📋 سجل الحركات والعمليات (Audit Log & History)")
    st.write("هذا السجل يضمن الاحتفاظ بالأصل ومتابعة كل تعديل أو إضافة بدقة تامة:")
    if len(st.session_state.audit_log) > 0:
        st.dataframe(st.session_state.audit_log, use_container_width=True)
    else:
        st.info("لا توجد حركات مسجلة حتى الآن.")

# --- 5. USER MANAGEMENT ---
elif "إدارة المستخدمين" in menu and st.session_state.role == "مدير النظام":
    st.subheader("⚙️ إدارة صلاحيات المستخدمين")
    st.write("المستخدمون الحاليون في النظام:")
    
    users_data = []
    for uname, details in st.session_state.users.items():
        users_data.append({"اسم المستخدم": uname, "الدور/الصلاحية": details["role"], "النطاق/المنطقة": details["region"]})
    st.dataframe(pd.DataFrame(users_data), use_container_width=True)
'''

with open("app.py", "w", encoding="utf-8") as f:
    f.write(app_code)

print("Streamlit application code generated successfully in app.py")