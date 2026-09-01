import io
import pandas as pd
import streamlit as st

# -------------------------------------------------------------------------
# 1. إعدادات الصفحة
# -------------------------------------------------------------------------
st.set_page_config(
    page_title="نظام حصر الأصول والدعم التقني", page_icon="💻", layout="wide"
)

# -------------------------------------------------------------------------
# 2. تخصيص التصميم الاحترافي (CSS)
# -------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');

    html, body, [class*="st-"] {
        font-family: 'Cairo', sans-serif !important;
        direction: rtl;
        text-align: right;
    }
    
    [data-testid="stAppViewContainer"] { background-color: #F4F7F6; }

    .stTextInput input, .stSelectbox select, .stMultiSelect div, textarea {
        direction: rtl !important;
        text-align: right !important;
        border-radius: 8px !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: #1E293B !important;
        box-shadow: -2px 0 10px rgba(0,0,0,0.1);
    }
    [data-testid="stSidebar"] * { color: #F8FAFC !important; }

    [data-testid="stSidebar"] .stRadio label {
        font-weight: 600; font-size: 15px !important; padding: 10px 15px;
        border-radius: 8px; transition: all 0.3s ease; margin-bottom: 8px;
        background-color: rgba(255, 255, 255, 0.05);
    }
    [data-testid="stSidebar"] .stRadio label:hover {
        background-color: rgba(255, 255, 255, 0.15); transform: translateX(-5px);
    }
    [data-testid="stSidebar"] div[data-baseweb="radio"] input:checked + div {
        background-color: #3B82F6 !important; border-radius: 8px;
        color: white !important; box-shadow: 0 4px 6px rgba(59, 130, 246, 0.3);
    }

    .stButton>button {
        border-radius: 8px; font-weight: 700; padding: 0.6rem 1.2rem;
        background-color: #2563EB !important; color: white !important;
        border: none; box-shadow: 0 2px 4px rgba(37, 99, 235, 0.2);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #1D4ED8 !important; transform: translateY(-2px);
        box-shadow: 0 4px 10px rgba(37, 99, 235, 0.4);
    }

    div.stDataFrame {
        background-color: white; padding: 15px; border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #E2E8F0;
    }

    .metric-card {
        background-color: #FFFFFF; padding: 20px; border-radius: 12px;
        color: #1E293B; text-align: right; box-shadow: 0 4px 6px rgba(0,0,0,0.04);
        border: 1px solid #E2E8F0; border-right: 5px solid #3B82F6;
        transition: all 0.3s ease; cursor: pointer;
    }
    .metric-card:hover {
        transform: translateY(-4px); box-shadow: 0 10px 15px rgba(0,0,0,0.1);
        border-right-width: 8px;
    }
    .metric-card.alert { border-right: 5px solid #EF4444; }
    .metric-card h3 { margin: 0; font-size: 15px; font-weight: 600; color: #64748B; }
    .metric-card h2 { margin: 10px 0 0 0; font-size: 28px; font-weight: 800; color: #0F172A; }
    
    .main-header {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        padding: 25px; border-radius: 12px; color: white; text-align: center;
        margin-bottom: 25px; box-shadow: 0 10px 20px rgba(30, 58, 138, 0.15);
    }
    .main-header h1 { margin: 0; font-size: 30px; font-weight: 800; }
    .main-header p { margin: 8px 0 0 0; font-size: 16px; opacity: 0.9; }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------------------------------
# 3. تهيئة قواعد البيانات (Session State)
# -------------------------------------------------------------------------
if "users_df" not in st.session_state:
    st.session_state.users_df = pd.DataFrame({
        "اسم المستخدم": ["admin", "mostafa"],
        "كلمة المرور": ["123", "123"],
        "الصلاحية": ["مدير النظام", "فني دعم"],
        "الحالة": ["نشط", "نشط"]
    })

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = ""
    st.session_state.user_role = ""

if "assets_df" not in st.session_state:
    st.session_state.assets_df = pd.DataFrame([
        {
            "المنطقة": "مبنى الوزارة الرئيسي", "المبنى": "المبنى الرئيسي", "الدور": "الأرضي",
            "الإدارة": "إدارة النظم الآلية والبنية التحتية", "القسم": "قسم التشغيل والدعم التقني",
            "اسم الموظف": "أحمد العتيبي", "نوع الجهاز (PC)": "Lenovo M70q", "سيريال الجهاز": "PC-12345",
            "مقاس/نوع الشاشة": "Lenovo 24 inch", "سيريال الشاشة": "MON-123",
            "موديل الطابعة": "Canon MF463dw", "نوع طباعة الطابعة": "أسود وأبيض", "سيريال الطابعة": "PRN-123",
            "حالة العطل": "سليم", "ملاحظات": "تم التسليم"
        },
        {
            "المنطقة": "العاصمة التعليمية", "المبنى": "مدرسة الشويخ", "الدور": "الأول",
            "الإدارة": "الشؤون التعليمية", "القسم": "السكرتارية",
            "اسم الموظف": "خالد الشمري", "نوع الجهاز (PC)": "Dell Optiplex", "سيريال الجهاز": "PC-98765",
            "مقاس/نوع الشاشة": "Dell 27 inch", "سيريال الشاشة": "MON-987",
            "موديل الطابعة": "HP Color LaserJet", "نوع طباعة الطابعة": "ملون", "سيريال الطابعة": "PRN-987",
            "حالة العطل": "عطل في الباور", "ملاحظات": "يحتاج تبديل كابل طاقة"
        }
    ])

# -------------------------------------------------------------------------
# 4. شاشة تسجيل الدخول
# -------------------------------------------------------------------------
if not st.session_state.logged_in:
    st.markdown("""
        <div class="main-header" style="margin-top: 50px;">
            <h1>نظام حصر الأصول والدعم التقني</h1>
            <p>وزارة التربية - إدارة النظم الآلية والبنية التحتية</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown("<h3 style='text-align: center; color: #1E293B;'>تسجيل الدخول</h3>", unsafe_allow_html=True)
        with st.form("login_form"):
            username_input = st.text_input("اسم المستخدم")
            password_input = st.text_input("كلمة المرور", type="password")
            login_submit = st.form_submit_button("دخول", use_container_width=True)

            if login_submit:
                users = st.session_state.users_df
                matched = users[(users["اسم المستخدم"] == username_input) & (users["كلمة المرور"] == password_input)]
                if not matched.empty:
                    if matched.iloc[0]["الحالة"] == "معطل":
                        st.error("الحساب معطل. راجع الإدارة.")
                    else:
                        st.session_state.logged_in = True
                        st.session_state.current_user = username_input
                        st.session_state.user_role = matched.iloc[0]["الصلاحية"]
                        st.rerun()
                else:
                    st.error("بيانات الدخول غير صحيحة.")
    st.stop()

# -------------------------------------------------------------------------
# 5. التوجيه (Navigation) والقائمة الجانبية
# -------------------------------------------------------------------------
if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 الرئيسية وإضافة العهد"

st.sidebar.markdown("<h2 style='text-align: center; color: white;'>لوحة التحكم</h2>", unsafe_allow_html=True)
st.sidebar.markdown(f"""
    <div style='background: rgba(255,255,255,0.1); padding: 15px; border-radius: 8px; margin-bottom: 20px;'>
        <p style='margin: 0; font-size: 14px;'>المستخدم: <b>{st.session_state.current_user}</b></p>
        <p style='margin: 5px 0 0 0; font-size: 13px; color: #94A3B8;'>الصلاحية: {st.session_state.user_role}</p>
    </div>
""", unsafe_allow_html=True)

nav_options = [
    "🏠 الرئيسية وإضافة العهد", "📋 سجل الأصول والبحث", "📊 إحصائيات الموظفين",
    "💻 إحصائيات الأجهزة (PC)", "🖥️ إحصائيات الشاشات", "🖨️ إحصائيات الطابعات",
    "⚠️ الأعطال التقنية والصيانة", "👥 إدارة المستخدمين"
]

selected_nav = st.sidebar.radio("القائمة", nav_options, index=nav_options.index(st.session_state.current_page))
if selected_nav != st.session_state.current_page:
    st.session_state.current_page = selected_nav
    st.rerun()

if st.sidebar.button("🚪 تسجيل الخروج", use_container_width=True):
    st.session_state.logged_in = False
    st.rerun()

# -------------------------------------------------------------------------
# 6. الترويسة الرئيسية والمؤشرات (Metrics)
# -------------------------------------------------------------------------
st.markdown("""
    <div class="main-header">
        <h1>نظام حصر الأصول والدعم التقني</h1>
        <p>وزارة التربية - قسم التشغيل والدعم التقني</p>
    </div>
""", unsafe_allow_html=True)

df = st.session_state.assets_df
total_records = len(df)
total_pcs = df["نوع الجهاز (PC)"].replace("", pd.NA).dropna().count()
total_monitors = df["مقاس/نوع الشاشة"].replace("", pd.NA).dropna().count()
total_printers = df["موديل الطابعة"].replace("", pd.NA).dropna().count()
total_faults = df[df["حالة العطل"] != "سليم"].shape[0]

st.markdown("<p style='color: #64748B; font-weight: 600;'>نظرة عامة (اضغط على التقرير للتفاصيل):</p>", unsafe_allow_html=True)
m1, m2, m3, m4, m5 = st.columns(5)
with m1:
    st.markdown(f'<div class="metric-card"><h3>إجمالي العهد</h3><h2>{total_records}</h2></div>', unsafe_allow_html=True)
with m2:
    st.markdown(f'<div class="metric-card"><h3>أجهزة الكمبيوتر</h3><h2>{total_pcs}</h2></div>', unsafe_allow_html=True)
with m3:
    st.markdown(f'<div class="metric-card"><h3>الشاشات</h3><h2>{total_monitors}</h2></div>', unsafe_allow_html=True)
with m4:
    st.markdown(f'<div class="metric-card"><h3>الطابعات</h3><h2>{total_printers}</h2></div>', unsafe_allow_html=True)
with m5:
    st.markdown(f'<div class="metric-card alert"><h3>أجهزة معطلة</h3><h2>{total_faults}</h2></div>', unsafe_allow_html=True)

st.markdown("<hr style='border-color: #E2E8F0; margin: 20px 0;'>", unsafe_allow_html=True)

# -------------------------------------------------------------------------
# 7. محتوى الصفحات والمنطق البرمجي (Logic)
# -------------------------------------------------------------------------
page = st.session_state.current_page

if page == "🏠 الرئيسية وإضافة العهد":
    st.subheader("📥 إدخال أصول وعهد جديدة")
    
    with st.expander("📁 رفع ملف Excel / CSV شامل", expanded=False):
        uploaded_file = st.file_uploader("اختر ملف البيانات", type=["xlsx", "csv"])
        if uploaded_file:
            try:
                if uploaded_file.name.endswith('.csv'):
                    new_data = pd.read_csv(uploaded_file)
                else:
                    new_data = pd.read_excel(uploaded_file)
                st.session_state.assets_df = pd.concat([st.session_state.assets_df, new_data], ignore_index=True)
                st.success(f"✅ تم استيراد {len(new_data)} سجل بنجاح! قم بتحديث الصفحة.")
            except Exception as e:
                st.error(f"حدث خطأ أثناء قراءة الملف: {e}")

    st.markdown("#### أو إدخال عهدة يدوياً")
    with st.form("add_asset_form"):
        c1, c2, c3 = st.columns(3)
        region = c1.selectbox("المنطقة", ["مبنى الوزارة الرئيسي", "العاصمة التعليمية", "حولي التعليمية", "الفروانية التعليمية", "الأحمدي التعليمية", "مبارك الكبير التعليمية", "الجهراء التعليمية"])
        building = c2.text_input("المبنى / المدرسة")
        floor = c3.text_input("الدور")
        
        c4, c5, c6 = st.columns(3)
        dept = c4.text_input("الإدارة")
        section = c5.text_input("القسم")
        emp = c6.text_input("اسم الموظف")
        
        st.markdown("---")
        st.markdown("**مواصفات الأجهزة**")
        c7, c8, c9 = st.columns(3)
        pc_type = c7.text_input("نوع الجهاز (PC)")
        pc_sn = c8.text_input("سيريال الجهاز (PC)")
        mon_type = c9.text_input("نوع الشاشة ومقاسها")
        
        c10, c11, c12 = st.columns(3)
        mon_sn = c10.text_input("سيريال الشاشة")
        prn_type = c11.text_input("موديل الطابعة")
        prn_color = c12.selectbox("نوع طباعة الطابعة", ["أسود وأبيض", "ملون", "أخرى", "لا يوجد"])
        
        st.markdown("---")
        c13, c14, c15 = st.columns(3)
        prn_sn = c13.text_input("سيريال الطابعة")
        fault = c14.selectbox("حالة العطل", ["سليم", "عطل في الباور", "عطل شاشة", "عطل شبكة", "عطل طابعة", "أخرى"])
        notes = c15.text_area("ملاحظات إضافية")
        
        submit_btn = st.form_submit_button("💾 حفظ العهدة في السجل")
        if submit_btn:
            new_row = pd.DataFrame([{
                "المنطقة": region, "المبنى": building, "الدور": floor,
                "الإدارة": dept, "القسم": section, "اسم الموظف": emp,
                "نوع الجهاز (PC)": pc_type, "سيريال الجهاز": pc_sn,
                "مقاس/نوع الشاشة": mon_type, "سيريال الشاشة": mon_sn,
                "موديل الطابعة": prn_type, "نوع طباعة الطابعة": prn_color,
                "سيريال الطابعة": prn_sn, "حالة العطل": fault, "ملاحظات": notes
            }])
            st.session_state.assets_df = pd.concat([st.session_state.assets_df, new_row], ignore_index=True)
            st.success("✅ تم تسجيل العهدة بنجاح!")

elif page == "📋 سجل الأصول والبحث":
    st.subheader("🔍 البحث المتقدم في السجل")
    df_search = df.copy()
    
    # فلاتر البحث
    col_f1, col_f2, col_f3 = st.columns(3)
    filter_region = col_f1.multiselect("تصفية بالمنطقة", options=df_search["المنطقة"].unique())
    filter_dept = col_f2.multiselect("تصفية بالإدارة", options=df_search["الإدارة"].unique())
    filter_emp = col_f3.text_input("بحث باسم الموظف أو السيريال")

    if filter_region:
        df_search = df_search[df_search["المنطقة"].isin(filter_region)]
    if filter_dept:
        df_search = df_search[df_search["الإدارة"].isin(filter_dept)]
    if filter_emp:
        df_search = df_search[
            df_search["اسم الموظف"].str.contains(filter_emp, case=False, na=False) |
            df_search["سيريال الجهاز"].str.contains(filter_emp, case=False, na=False)
        ]

    st.markdown(f"**عدد النتائج:** {len(df_search)} سجل")
    st.dataframe(df_search, use_container_width=True)

    # زر تصدير البيانات إلى CSV يدعم اللغة العربية
    csv = df_search.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 تصدير النتائج لملف Excel/CSV",
        data=csv,
        file_name='assets_export.csv',
        mime='text/csv'
    )

elif page == "📊 إحصائيات الموظفين":
    st.subheader("📊 إحصائيات توزيع العهد على الموظفين والإدارات")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**عدد الأجهزة لكل إدارة:**")
        dept_counts = df["الإدارة"].value_counts()
        st.bar_chart(dept_counts)
    with col2:
        st.markdown("**تفصيل الموظفين:**")
        emp_counts = df.groupby(["الإدارة", "اسم الموظف"]).size().reset_index(name="عدد العهد")
        st.dataframe(emp_counts, use_container_width=True)

elif page == "💻 إحصائيات الأجهزة (PC)":
    st.subheader("💻 إحصائيات أجهزة الكمبيوتر")
    pc_data = df[df["نوع الجهاز (PC)"].str.strip() != ""]
    st.markdown(f"**إجمالي الأجهزة المسجلة:** {len(pc_data)}")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown("**الأنواع والموديلات:**")
        st.dataframe(pc_data["نوع الجهاز (PC)"].value_counts().reset_index(name="العدد"), use_container_width=True)
    with col2:
        st.bar_chart(pc_data["نوع الجهاز (PC)"].value_counts())

elif page == "🖥️ إحصائيات الشاشات":
    st.subheader("🖥️ إحصائيات الشاشات")
    mon_data = df[df["مقاس/نوع الشاشة"].str.strip() != ""]
    st.markdown(f"**إجمالي الشاشات المسجلة:** {len(mon_data)}")
    
    st.markdown("**الأنواع والمقاسات:**")
    st.bar_chart(mon_data["مقاس/نوع الشاشة"].value_counts())
    st.dataframe(mon_data[["اسم الموظف", "الإدارة", "مقاس/نوع الشاشة", "سيريال الشاشة"]], use_container_width=True)

elif page == "🖨️ إحصائيات الطابعات":
    st.subheader("🖨️ إحصائيات الطابعات")
    prn_data = df[df["موديل الطابعة"].str.strip() != ""]
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**الموديلات:**")
        st.dataframe(prn_data["موديل الطابعة"].value_counts().reset_index(name="العدد"), use_container_width=True)
    with c2:
        st.markdown("**حسب نوع الطباعة (ملون / أسود):**")
        st.bar_chart(prn_data["نوع طباعة الطابعة"].value_counts())

elif page == "⚠️ الأعطال التقنية والصيانة":
    st.subheader("⚠️ سجل الأعطال التقنية والصيانة")
    faults_df = df[df["حالة العطل"] != "سليم"]
    
    if faults_df.empty:
        st.success("🎉 ممتاز! لا توجد أعطال مسجلة حالياً في النظام.")
    else:
        st.error(f"يوجد عدد {len(faults_df)} جهاز/ملحق بحاجة للصيانة.")
        st.dataframe(faults_df[["المنطقة", "الإدارة", "اسم الموظف", "نوع الجهاز (PC)", "حالة العطل", "ملاحظات"]], use_container_width=True)
        st.markdown("**تحليل أنواع الأعطال:**")
        st.bar_chart(faults_df["حالة العطل"].value_counts())

elif page == "👥 إدارة المستخدمين":
    st.subheader("👥 إدارة حسابات النظام")
    
    if st.session_state.user_role != "مدير النظام":
        st.warning("⚠️ عذراً، هذه الصفحة مخصصة لمدراء النظام فقط.")
    else:
        st.dataframe(st.session_state.users_df, use_container_width=True)
        
        st.markdown("#### إضافة مستخدم جديد")
        with st.form("new_user_form"):
            c1, c2 = st.columns(2)
            new_user = c1.text_input("اسم المستخدم")
            new_pass = c2.text_input("كلمة المرور", type="password")
            new_role = c1.selectbox("الصلاحية", ["فني دعم", "مدير النظام", "مراقب"])
            new_status = c2.selectbox("الحالة", ["نشط", "معطل"])
            
            if st.form_submit_button("إضافة مستخدم"):
                if new_user != "":
                    new_u = pd.DataFrame([{"اسم المستخدم": new_user, "كلمة المرور": new_pass, "الصلاحية": new_role, "الحالة": new_status}])
                    st.session_state.users_df = pd.concat([st.session_state.users_df, new_u], ignore_index=True)
                    st.success("تم إضافة المستخدم بنجاح! قم بتحديث الصفحة.")
                else:
                    st.error("يرجى إدخال اسم المستخدم.")
