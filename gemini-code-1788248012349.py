import io
import pandas as pd
import streamlit as st

# -------------------------------------------------------------------------
# 1. إعدادات الصفحة
# -------------------------------------------------------------------------
st.set_page_config(
    page_title="نظام حصر الأصول والدعم التقني - وزارة التربية",
    page_icon="💻",
    layout="wide",
)

# -------------------------------------------------------------------------
# 2. تخصيص التصميم الاحترافي (UI/UX - RTL & Custom Theme)
# -------------------------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800&display=swap');

    /* التوجيه والخط العام */
    html, body, [class*="st-"] {
        font-family: 'Cairo', sans-serif !important;
        direction: rtl;
        text-align: right;
    }
    
    [data-testid="stAppViewContainer"] {
        background-color: #0F172A; /* خلفية داكنة احترافية للأنظمة */
        color: #F8FAFC;
    }

    /* محاذاة حقول الإدخال */
    .stTextInput input, .stSelectbox select, .stMultiSelect div, textarea, 
    [data-baseweb="select"] span, [data-baseweb="input"] input {
        direction: rtl !important;
        text-align: right !important;
        border-radius: 8px !important;
        background-color: #1E293B !important;
        color: white !important;
    }
    
    /* إخفاء تعليمات الإدخال المزعجة */
    [data-testid="InputInstructions"] {
        display: none !important;
    }

    /* القائمة الجانبية */
    [data-testid="stSidebar"] {
        background-color: #1E293B !important;
        box-shadow: -2px 0 15px rgba(0,0,0,0.3);
        border-left: 1px solid #334155;
    }
    [data-testid="stSidebar"] * { color: #F8FAFC !important; }

    /* الأزرار في القائمة الجانبية والصفحة */
    .stButton>button {
        border-radius: 8px;
        font-weight: 700;
        padding: 0.6rem 1.2rem;
        background-color: #3B82F6 !important;
        color: white !important;
        border: none;
        box-shadow: 0 4px 6px rgba(59, 130, 246, 0.3);
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #2563EB !important;
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(59, 130, 246, 0.5);
    }

    /* بطاقات الإحصائيات التفاعلية */
    .metric-card {
        background: linear-gradient(135deg, #1E293B 0%, #334155 100%);
        padding: 22px;
        border-radius: 12px;
        color: white;
        text-align: right;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        border: 1px solid #475569;
        border-right: 6px solid #3B82F6;
        transition: all 0.3s ease;
        cursor: pointer;
        margin-bottom: 10px;
    }
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(59, 130, 246, 0.4);
        border-right-color: #F59E0B;
        background: linear-gradient(135deg, #334155 0%, #1E293B 100%);
    }
    .metric-card.alert {
        border-right-color: #EF4444;
    }
    .metric-card h3 {
        margin: 0;
        font-size: 16px;
        font-weight: 600;
        color: #94A3B8;
    }
    .metric-card h2 {
        margin: 12px 0 0 0;
        font-size: 32px;
        font-weight: 800;
        color: #F8FAFC;
    }

    /* الترويسة الرئيسية */
    .main-header {
        background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 100%);
        padding: 25px;
        border-radius: 12px;
        color: white;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 10px 25px rgba(37, 99, 235, 0.25);
    }
    .main-header h1 {
        margin: 0;
        font-size: 32px;
        font-weight: 800;
    }
    .main-header p {
        margin: 8px 0 0 0;
        font-size: 17px;
        opacity: 0.95;
    }
    
    /* الجداول */
    div.stDataFrame {
        background-color: #1E293B;
        padding: 15px;
        border-radius: 12px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        border: 1px solid #334155;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -------------------------------------------------------------------------
# 3. تهيئة البيانات وقواعد البيانات التجريبية (Session State)
# -------------------------------------------------------------------------
if "users_df" not in st.session_state:
    st.session_state.users_df = pd.DataFrame(
        {
            "اسم المستخدم": ["admin", "mostafa", "support1"],
            "كلمة المرور": ["123", "123", "123"],
            "الصلاحية": ["مدير النظام", "مدير النظام", "فني دعم"],
            "الحالة": ["نشط", "نشط", "نشط"],
        }
    )

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.current_user = ""
    st.session_state.user_role = ""

if "assets_df" not in st.session_state:
    # البيانات التجريبية الشاملة بالترتيب المطلوب: المنطقة -> المبنى -> الدور -> اسم الموظف -> الجهاز -> الشاشة -> الطابعة -> الباركود -> الحالة -> ملاحظات
    st.session_state.assets_df = pd.DataFrame(
        [
            {
                "المنطقة": "مبنى وزارة التربية",
                "المبنى": "المبنى الرئيسي",
                "الدور": "الدور الثالث",
                "اسم الموظف": "مصطفى أحمد",
                "نوع الجهاز (PC)": "Lenovo M70q (Type A)",
                "سيريال الجهاز": "PC-998811",
                "مقاس/نوع الشاشة": "Lenovo 24 inch",
                "سيريال الشاشة": "MON-1122",
                "موديل الطابعة": "Canon MF463dw (Black)",
                "سيريال الطابعة": "PRN-5544",
                "الباركود": "BAR-882210",
                "حالة العطل": "سليم",
                "ملاحظات": "تم التسليم بحالة ممتازة",
            },
            {
                "المنطقة": "العاصمة التعليمية",
                "المبنى": "مدرسة الشويخ الثانوية",
                "الدور": "الدور الأول",
                "اسم الموظف": "خالد العتيبي",
                "نوع الجهاز (PC)": "Lenovo M90t (Type C)",
                "سيريال الجهاز": "PC-774412",
                "مقاس/نوع الشاشة": "Lenovo 27 inch",
                "سيريال الشاشة": "MON-3344",
                "موديل الطابعة": "Canon MF754Cdw (Color)",
                "سيريال الطابعة": "PRN-8877",
                "الباركود": "BAR-991122",
                "حالة العطل": "عطل في الباور",
                "ملاحظات": "يحتاج فحص مصدر الطاقة",
            },
            {
                "المنطقة": "حولي التعليمية",
                "المبنى": "مدرسة ابن خلدون",
                "الدور": "الدور الأرضي",
                "اسم الموظف": "سعد الشمري",
                "نوع الجهاز (PC)": "laptop",
                "سيريال الجهاز": "LAP-556677",
                "مقاس/نوع الشاشة": "لا يوجد / مدمج",
                "سيريال الشاشة": "N/A",
                "موديل الطابعة": "Label Printer",
                "سيريال الطابعة": "PRN-1122",
                "الباركود": "BAR-334455",
                "حالة العطل": "سليم",
                "ملاحظات": "جهاز محمول خاص بالتنقل",
            },
        ]
    )

# -------------------------------------------------------------------------
# 4. شاشة تسجيل الدخول
# -------------------------------------------------------------------------
if not st.session_state.logged_in:
    st.markdown(
        """
        <div class="main-header" style="margin-top: 40px;">
            <h1>نظام حصر الأصول والدعم التقني</h1>
            <p>وزارة التربية - إدارة النظم الآلية والبنية التحتية</p>
        </div>
    """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown(
            "<h3 style='text-align: center; color: #F8FAFC;'>تسجيل الدخول إلى النظام</h3>",
            unsafe_allow_html=True,
        )
        with st.form("login_form"):
            username_input = st.text_input("اسم المستخدم")
            password_input = st.text_input("كلمة المرور", type="password")
            login_submit = st.form_submit_button("دخول", use_container_width=True)

            if login_submit:
                users = st.session_state.users_df
                matched = users[
                    (users["اسم المستخدم"] == username_input)
                    & (users["كلمة المرور"] == password_input)
                ]
                if not matched.empty:
                    if matched.iloc[0]["الحالة"] == "معطل":
                        st.error("عذراً، هذا الحساب معطل.")
                    else:
                        st.session_state.logged_in = True
                        st.session_state.current_user = username_input
                        st.session_state.user_role = matched.iloc[0]["الصلاحية"]
                        st.rerun()
                else:
                    st.error("اسم المستخدم أو كلمة المرور غير صحيحة.")
    st.stop()

# -------------------------------------------------------------------------
# 5. القائمة الجانبية الثابتة والتنقل
# -------------------------------------------------------------------------
if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 الرئيسية وإضافة العهد"

st.sidebar.markdown(
    "<h2 style='text-align: center; color: white;'>لوحة التحكم</h2>",
    unsafe_allow_html=True,
)
st.sidebar.markdown(
    f"""
    <div style='background: rgba(255,255,255,0.05); padding: 15px; border-radius: 8px; margin-bottom: 20px; border: 1px solid #334155;'>
        <p style='margin: 0; font-size: 14px;'>المستخدم: <b>{st.session_state.current_user}</b></p>
        <p style='margin: 5px 0 0 0; font-size: 13px; color: #94A3B8;'>الصلاحية: {st.session_state.user_role}</p>
    </div>
""",
    unsafe_allow_html=True,
)

nav_options = [
    "🏠 الرئيسية وإضافة العهد",
    "📋 سجل الأصول والبحث والتعديل",
    "📊 إحصائيات الموظفين",
    "💻 إحصائيات أجهزة (PC)",
    "🖥️ إحصائيات الشاشات",
    "🖨️ إحصائيات الطابعات",
    "⚠️ الأعطال التقنية والصيانة",
    "👥 إدارة المستخدمين",
]

selected_nav = st.sidebar.radio(
    "التنقل بين الصفحات",
    nav_options,
    index=nav_options.index(st.session_state.current_page)
    if st.session_state.current_page in nav_options
    else 0,
)
if selected_nav != st.session_state.current_page:
    st.session_state.current_page = selected_nav
    st.rerun()

st.sidebar.markdown("<br>", unsafe_allow_html=True)
if st.sidebar.button("🚪 تسجيل الخروج", use_container_width=True):
    st.session_state.logged_in = False
    st.rerun()

# -------------------------------------------------------------------------
# 6. الترويسة الرئيسية الثابتة
# -------------------------------------------------------------------------
st.markdown(
    """
    <div class="main-header">
        <h1>نظام حصر الأصول والدعم التقني</h1>
        <p>وزارة التربية - إدارة النظم الآلية والبنية التحتية (قسم التشغيل والدعم التقني)</p>
    </div>
""",
    unsafe_allow_html=True,
)

# حساب الإحصائيات السريعة بطريقة آمنة
df = st.session_state.assets_df
total_records = len(df)
total_pcs = len(df[df["نوع الجهاز (PC)"].str.strip() != ""])
total_monitors = len(
    df[~df["مقاس/نوع الشاشة"].isin(["لا يوجد / مدمج", "N/A", ""])]
)
total_printers = len(df[~df["موديل الطابعة"].isin(["لا يوجد", ""])])
total_faults = len(df[df["حالة العطل"] != "سليم"])

# عرض أزرار / بطاقات الإحصائيات التفاعلية في الأعلى (تنتقل للصفحات عند الضغط عليها)
st.markdown(
    "<p style='color: #94A3B8; font-weight: 600; margin-bottom: 12px;'>📊 نظرة عامة سريعة (اضغط على البطاقة للانتقال للتقرير التفصيلي):</p>",
    unsafe_allow_html=True,
)
m1, m2, m3, m4, m5 = st.columns(5)

with m1:
    st.markdown(
        f'<div class="metric-card"><h3>إجمالي العهد</h3><h2>{total_records}</h2></div>',
        unsafe_allow_html=True,
    )
    if st.button("عرض سجل الأصول", key="btn_all", use_container_width=True):
        st.session_state.current_page = "📋 سجل الأصول والبحث والتعديل"
        st.rerun()

with m2:
    st.markdown(
        f'<div class="metric-card"><h3>أجهزة (PC)</h3><h2>{total_pcs}</h2></div>',
        unsafe_allow_html=True,
    )
    if st.button("تقرير الأجهزة", key="btn_pc", use_container_width=True):
        st.session_state.current_page = "💻 إحصائيات أجهزة (PC)"
        st.rerun()

with m3:
    st.markdown(
        f'<div class="metric-card"><h3>الشاشات</h3><h2>{total_monitors}</h2></div>',
        unsafe_allow_html=True,
    )
    if st.button("تقرير الشاشات", key="btn_mon", use_container_width=True):
        st.session_state.current_page = "🖥️ إحصائيات الشاشات"
        st.rerun()

with m4:
    st.markdown(
        f'<div class="metric-card"><h3>الطابعات</h3><h2>{total_printers}</h2></div>',
        unsafe_allow_html=True,
    )
    if st.button("تقرير الطابعات", key="btn_prn", use_container_width=True):
        st.session_state.current_page = "🖨️ إحصائيات الطابعات"
        st.rerun()

with m5:
    st.markdown(
        f'<div class="metric-card alert"><h3>الأعطال والصيانة</h3><h2>{total_faults}</h2></div>',
        unsafe_allow_html=True,
    )
    if st.button("متابعة الأعطال", key="btn_flt", use_container_width=True):
        st.session_state.current_page = "⚠️ الأعطال التقنية والصيانة"
        st.rerun()

st.markdown(
    "<hr style='border-color: #334155; margin: 30px 0;'>", unsafe_allow_html=True
)

# -------------------------------------------------------------------------
# 7. الصفحات والوظائف البرمجية الكاملة
# -------------------------------------------------------------------------
page = st.session_state.current_page

if page == "🏠 الرئيسية وإضافة العهد":
    st.subheader("📥 إضافة عهدة جديدة أو رفع ملف (Excel / CSV)")

    # خيار رفع الملفات
    with st.expander(
        "📁 استيراد جماعي عبر ملف Excel أو CSV (متوافق مع ترتيب الشيت)",
        expanded=False,
    ):
        uploaded_file = st.file_uploader(
            "اختر ملف البيانات", type=["xlsx", "csv"]
        )
        if uploaded_file:
            try:
                if uploaded_file.name.endswith(".csv"):
                    new_data = pd.read_csv(uploaded_file)
                else:
                    new_data = pd.read_excel(uploaded_file)
                st.session_state.assets_df = pd.concat(
                    [st.session_state.assets_df, new_data], ignore_index=True
                )
                st.success(
                    f"✅ تم دمج واستيراد {len(new_data)} سجل بنجاح مع الاحتفاظ بالبيانات الأصلية!"
                )
            except Exception as e:
                st.error(f"حدث خطأ أثناء قراءة الملف: {e}")

    st.markdown("#### نموذج إدخال عهدة جديدة يدوياً")
    with st.form("add_asset_form"):
        col1, col2, col3 = st.columns(3)

        # المناطق الست + مبنى الوزارة الرئيسي
        regions_list = [
            "مبنى وزارة التربية",
            "العاصمة التعليمية",
            "حولي التعليمية",
            "مبارك الكبير التعليمية",
            "الفروانية التعليمية",
            "الجهراء التعليمية",
            "الأحمدي التعليمية",
        ]
        region = col1.selectbox("المنطقة / الجهة", regions_list)

        building = col2.text_input("اسم المبنى / المدرسة")

        # حقل الدور (للمبنى الرئيسي 11 دور أو كتابة حرة للمدارس والمباني الأخرى)
        floor_options = [
            "الدور الأرضي",
            "الدور الأول",
            "الدور الثاني",
            "الدور الثالث",
            "الدور الرابع",
            "الدور الخامس",
            "الدور السادس",
            "الدور السابع",
            "الدور الثامن",
            "الدور التاسع",
            "الدور العاشر",
            "الدور الحادي عشر",
            "أخرى",
        ]
        floor = col3.selectbox("الدور", floor_options)

        col4, col5, col6 = st.columns(3)
        emp_name = col4.text_input("اسم الموظف المسؤول")
        barcode = col5.text_input("حقل الباركود (Barcode)")

        pc_types = [
            "Lenovo M70q (Type A)",
            "Lenovo M70q (Type B)",
            "Lenovo M90t (Type C)",
            "laptop",
        ]
        pc_type = col6.selectbox("نوع الجهاز (PC)", pc_types)

        col7, col8, col9 = st.columns(3)
        pc_sn = col7.text_input("سيريال الجهاز (PC SN)")

        monitor_options = ["Lenovo 24 inch", "Lenovo 27 inch", "لا يوجد / مدمج"]
        monitor_type = col8.selectbox("مقاس / نوع الشاشة", monitor_options)
        monitor_sn = col9.text_input("سيريال الشاشة")

        col10, col11, col12 = st.columns(3)
        printer_models = [
            "Canon MF463dw (Black)",
            "Canon MF754Cdw (Color)",
            "Label Printer",
            "لا يوجد",
        ]
        printer_type = col10.selectbox("موديل الطابعة", printer_models)
        printer_sn = col11.text_input("سيريال الطابعة")
        fault_status = col12.selectbox(
            "حالة العطل", ["سليم", "عطل في الباور", "عطل شاشة", "عطل شبكة", "أخرى"]
        )

        notes = st.text_area("ملاحظات إضافية")

        submit_btn = st.form_submit_button(
            "💾 حفظ وتسجيل العهدة في قاعدة البيانات"
        )
        if submit_btn:
            new_row = pd.DataFrame(
                [
                    {
                        "المنطقة": region,
                        "المبنى": building,
                        "الدور": floor,
                        "اسم الموظف": emp_name,
                        "نوع الجهاز (PC)": pc_type,
                        "سيريال الجهاز": pc_sn,
                        "مقاس/نوع الشاشة": monitor_type,
                        "سيريال الشاشة": monitor_sn,
                        "موديل الطابعة": printer_type,
                        "سيريال الطابعة": printer_sn,
                        "الباركود": barcode,
                        "حالة العطل": fault_status,
                        "ملاحظات": notes,
                    }
                ]
            )
            st.session_state.assets_df = pd.concat(
                [st.session_state.assets_df, new_row], ignore_index=True
            )
            st.success("✅ تم حفظ العهدة الجديدة بنجاح وإضافتها للسجل!")

elif page == "📋 سجل الأصول والبحث والتعديل":
    st.subheader("📋 سجل الأصول والعهد (بحث، تعديل، وحذف)")

    search_query = st.text_input(
        "🔍 ابحث برقم الباركود، اسم الموظف، أو السيريال:"
    )
    df_display = st.session_state.assets_df.copy()

    if search_query:
        df_display = df_display[
            df_display["اسم الموظف"].str.contains(
                search_query, case=False, na=False
            )
            | df_display["سيريال الجهاز"].str.contains(
                search_query, case=False, na=False
            )
            | df_display["الباركود"].str.contains(
                search_query, case=False, na=False
            )
        ]

    st.markdown(f"**عدد السجلات المعروضة:** {len(df_display)}")
    st.dataframe(df_display, use_container_width=True)

    csv_data = df_display.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        label="📥 تحميل السجل الحالي كملف Excel/CSV",
        data=csv_data,
        file_name="ministry_assets_report.csv",
        mime="text/csv",
    )

    st.markdown("---")
    st.markdown("#### 🛠️ تعديل أو حذف عهدة / تصليح جهاز")
    if not df_display.empty:
        record_indices = df_display.index.tolist()
        selected_idx = st.selectbox(
            "اختر رقم السجل (Index) لتعديله أو حذفها:", record_indices
        )

        if selected_idx is not None:
            current_row = st.session_state.assets_df.loc[selected_idx]
            with st.form("edit_record_form"):
                e_region = st.text_input("المنطقة", value=current_row["المنطقة"])
                e_building = st.text_input(
                    "المبنى", value=current_row["المبنى"]
                )
                e_floor = st.text_input("الدور", value=current_row["الدور"])
                e_emp = st.text_input(
                    "اسم الموظف", value=current_row["اسم الموظف"]
                )
                e_barcode = st.text_input(
                    "الباركود", value=current_row["الباركود"]
                )
                e_fault = st.selectbox(
                    "حالة العطل (حدد 'سليم' عند الإصلاح والتصليح)",
                    ["سليم", "عطل في الباور", "عطل شاشة", "عطل شبكة", "أخرى"],
                    index=0
                    if current_row["حالة العطل"] == "سليم"
                    else 1,
                )
                e_notes = st.text_area(
                    "ملاحظات", value=current_row["ملاحظات"]
                )

                col_upd, col_del = st.columns(2)
                update_btn = col_upd.form_submit_button(
                    "💾 تحديث البيانات وحالة الإصلاح"
                )
                delete_btn = col_del.form_submit_button(
                    "🗑️ حذف هذه العهدة نهائياً"
                )

                if update_btn:
                    st.session_state.assets_df.loc[selected_idx, "المنطقة"] = (
                        e_region
                    )
                    st.session_state.assets_df.loc[selected_idx, "المبنى"] = (
                        e_building
                    )
                    st.session_state.assets_df.loc[selected_idx, "الدور"] = (
                        e_floor
                    )
                    st.session_state.assets_df.loc[selected_idx, "اسم الموظف"] = (
                        e_emp
                    )
                    st.session_state.assets_df.loc[selected_idx, "الباركود"] = (
                        e_barcode
                    )
                    st.session_state.assets_df.loc[selected_idx, "حالة العطل"] = (
                        e_fault
                    )
                    st.session_state.assets_df.loc[selected_idx, "ملاحظات"] = (
                        e_notes
                    )
                    st.success("✅ تم تحديث بيانات العهدة بنجاح!")
                    st.rerun()

                if delete_btn:
                    st.session_state.assets_df = (
                        st.session_state.assets_df.drop(selected_idx)
                        .reset_index(drop=True)
                    )
                    st.warning("⚠️ تم حذف العهدة بنجاح.")
                    st.rerun()

elif page == "📊 إحصائيات الموظفين":
    st.subheader("📊 تقرير توزيع العهد والموظفين حسب المنطقة والإدارة")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**التوزيع حسب المنطقة / الجهة:**")
        reg_counts = df["المنطقة"].value_counts()
        st.bar_chart(reg_counts)
    with col2:
        st.markdown("**تفصيل الموظفين والعهد:**")
        st.dataframe(
            df[["المنطقة", "المبنى", "اسم الموظف", "سيريال الجهاز"]],
            use_container_width=True,
        )

elif page == "💻 إحصائيات أجهزة (PC)":
    st.subheader("💻 تفصيل ومواصفات أجهزة الكمبيوتر (PC & Laptops)")
    pc_data = df[df["نوع الجهاز (PC)"].str.strip() != ""]
    st.markdown(f"**إجمالي الأجهزة المسجلة:** {len(pc_data)}")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**توزيع الأنواع والموديلات:**")
        pc_counts = pc_data["نوع الجهاز (PC)"].value_counts()
        st.bar_chart(pc_counts)
    with col2:
        st.dataframe(
            pc_counts.reset_index().rename(
                columns={"index": "نوع الجهاز", "count": "العدد"}
            ),
            use_container_width=True,
        )

elif page == "🖥️ إحصائيات الشاشات":
    st.subheader("🖥️ إحصائيات الشاشات (مقاسات 24 و 27 بوصة)")
    mon_data = df[~df["مقاس/نوع الشاشة"].isin(["لا يوجد / مدمج", "N/A", ""])]
    st.markdown(f"**إجمالي الشاشات الخارجية المسجلة:** {len(mon_data)}")

    st.bar_chart(mon_data["مقاس/نوع الشاشة"].value_counts())
    st.dataframe(
        mon_data[["المنطقة", "اسم الموظف", "مقاس/نوع الشاشة", "سيريال الشاشة"]],
        use_container_width=True,
    )

elif page == "🖨️ إحصائيات الطابعات":
    st.subheader("🖨️ تفصيل الطابعات (أسود وأبيض، ملون، وملصقات)")
    prn_data = df[~df["موديل الطابعة"].isin(["لا يوجد", ""])]
    st.markdown(f"**إجمالي الطابعات المسجلة:** {len(prn_data)}")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**تفصيل الطابعات (الألوان، الأسود والأبيض، والملصقات):**")
        prn_counts = prn_data["موديل الطابعة"].value_counts()
        st.bar_chart(prn_counts)
    with c2:
        st.dataframe(
            prn_counts.reset_index().rename(
                columns={"index": "موديل الطابعة", "count": "العدد"}
            ),
            use_container_width=True,
        )

elif page == "⚠️ الأعطال التقنية والصيانة":
    st.subheader("⚠️ متابعة الأعطال التقنية وإصلاح الأجهزة")
    faults_df = df[df["حالة العطل"] != "سليم"]

    if faults_df.empty:
        st.success(
            "🎉 ممتاز جداً! لا توجد أي أعطال مسجلة حالياً، جميع الأجهزة سليمة وتعمل بكفاءة."
        )
    else:
        num_faults = len(faults_df)
        st.error(
            f"⚠️ يوجد عدد ({num_faults}) جهاز بحاجة للصيانة والمتابعة الفورية."
        )
        st.dataframe(
            faults_df[
                [
                    "المنطقة",
                    "المبنى",
                    "اسم الموظف",
                    "نوع الجهاز (PC)",
                    "حالة العطل",
                    "ملاحظات",
                ]
            ],
            use_container_width=True,
        )
        st.markdown("**توزيع أنواع الأعطال:**")
        st.bar_chart(faults_df["حالة العطل"].value_counts())

elif page == "👥 إدارة المستخدمين":
    st.subheader("👥 إدارة حسابات المستخدمين والصلاحيات")

    if st.session_state.user_role != "مدير النظام":
        st.warning(
            "⚠️ عذراً، هذه الصفحة مخصصة لمدراء النظام فقط للتحكم في الحسابات والصلاحيات."
        )
    else:
        st.dataframe(st.session_state.users_df, use_container_width=True)

        st.markdown("#### إضافة مستخدم جديد للنظام")
        with st.form("new_user_form"):
            c1, c2 = st.columns(2)
            new_user = c1.text_input("اسم المستخدم الجديد")
            new_pass = c2.text_input("كلمة المرور", type="password")
            new_role = c1.selectbox("الصلاحية", ["فني دعم", "مدير النظام"])
            new_status = c2.selectbox("حالة الحساب", ["نشط", "معطل"])

            if st.form_submit_button("إضافة المستخدم"):
                if new_user:
                    new_u = pd.DataFrame(
                        [
                            {
                                "اسم المستخدم": new_user,
                                "كلمة المرور": new_pass,
                                "الصلاحية": new_role,
                                "الحالة": new_status,
                            }
                        ]
                    )
                    st.session_state.users_df = pd.concat(
                        [st.session_state.users_df, new_u], ignore_index=True
                    )
                    st.success("✅ تم إضافة المستخدم بنجاح!")
                    st.rerun()
                else:
                    st.error("يرجى إدخال اسم المستخدم.")
