import io
import pandas as pd
import streamlit as st

# إعدادات الصفحة
st.set_page_config(
    page_title="نظام حصر الأصول والدعم التقني", page_icon="💻", layout="wide"
)

# تخصيص التصميم الاحترافي (تنسيق RTL + تغيير اللون العام إلى الذهبي الفاخر + إبراز الأزرار الجانبية بوضوح تام)
st.markdown(
    """
    <style>
    body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
        direction: rtl;
        text-align: right;
        font-family: 'Tajawal', sans-serif;
        background-color: #fdfbf7;
    }
    
    /* تصميم القائمة الجانبية باللون الذهبي الداكن الفاخر وتأمين وضوح النص الأبيض */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #78350f 0%, #92400e 50%, #b45309 100%);
        color: #ffffff;
    }
    [data-testid="stSidebar"] .stRadio label {
        color: #ffffff !important;
        font-weight: 600;
        font-size: 15px;
        padding: 10px 14px;
        border-radius: 8px;
        transition: all 0.2s ease-in-out;
        margin-bottom: 4px;
        background-color: rgba(0, 0, 0, 0.15);
    }
    [data-testid="stSidebar"] .stRadio label:hover {
        background-color: rgba(255, 255, 255, 0.25);
        cursor: pointer;
    }
    [data-testid="stSidebar"] hr {
        border-color: rgba(255, 255, 255, 0.3);
    }
    [data-testid="stSidebar"] .stButton>button {
        background-color: rgba(239, 68, 68, 0.9);
        color: white;
        border: none;
        border-radius: 8px;
        font-weight: bold;
        transition: all 0.2s;
    }
    [data-testid="stSidebar"] .stButton>button:hover {
        background-color: #dc2626;
    }

    /* تحسين الأزرار العامة في التطبيق بلون منسجم مع الهوية الذهبية */
    .stButton>button {
        border-radius: 8px;
        font-weight: bold;
        padding: 0.5rem 1rem;
        background-color: #d97706;
        color: white;
        border: none;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        transition: all 0.2s ease;
    }
    .stButton>button:hover {
        background-color: #b45309;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        color: white;
    }

    div.stDataFrame {
        direction: rtl;
        text-align: right;
        background-color: white;
        padding: 10px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    [data-testid="InputInstructions"] {
        display: none !important;
    }

    /* تصميم بطاقات الإحصائيات التفاعلية بدرجات الذهبي الفاخر */
    .metric-card {
        background: linear-gradient(135deg, #b45309 0%, #d97706 100%);
        padding: 20px;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.08);
        transition: all 0.3s ease-in-out;
        cursor: pointer;
        margin-bottom: 10px;
    }
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.15);
        background: linear-gradient(135deg, #92400e 0%, #b45309 100%);
    }
    .metric-card h3 {
        margin: 0;
        font-size: 15px;
        opacity: 0.95;
    }
    .metric-card h2 {
        margin: 8px 0 0 0;
        font-size: 26px;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# 1. تهيئة المستخدمين الافتراضيين
if "users_df" not in st.session_state:
  st.session_state.users_df = pd.DataFrame(
      {
          "اسم المستخدم": ["admin", "support1"],
          "كلمة المرور": ["123456", "111111"],
          "الصلاحية": ["مدير النظام", "فني دعم"],
          "الحالة": ["نشط", "نشط"],
      }
  )

# 2. تهيئة حالة تسجيل الدخول
if "logged_in" not in st.session_state:
  st.session_state.logged_in = False
  st.session_state.current_user = ""
  st.session_state.user_role = ""

# 3. تهيئة البيانات التجريبية الشاملة للعهد
if "assets_df" not in st.session_state:
  st.session_state.assets_df = pd.DataFrame(
      [
          {
              "المنطقة": "مبنى الوزارة الرئيسي",
              "المبنى": "المبنى الرئيسي - الدور الأرضي",
              "الدور": "الدور الأرضي",
              "الإدارة": "إدارة النظم الآلية والبنية التحتية",
              "القسم": "قسم التشغيل والدعم التقني",
              "اسم الموظف": "محمد عبد الله",
              "نوع الجهاز (PC)": "Lenovo M70q (Type A)",
              "سيريال الجهاز": "PC-9882103",
              "مقاس/نوع الشاشة": "Lenovo 24 inch",
              "سيريال الشاشة": "MON-554120",
              "موديل الطابعة": "Canon MF463dw (Black)",
              "نوع طباعة الطابعة": "أسود وأبيض",
              "سيريال الطابعة": "PRN-778812",
              "حالة العطل": "سليم",
              "ملاحظات": "تم التسليم بحالة جيدة",
          },
          {
              "المنطقة": "منطقة العاصمة التعليمية",
              "المبنى": "مدرسة ثانوية الشويخ",
              "الدور": "الدور الأول",
              "الإدارة": "مراقبة التقنيات التربوية",
              "القسم": "قسم الدعم الفني",
              "اسم الموظف": "أحمد العتيبي",
              "نوع الجهاز (PC)": "Lenovo M90t (Type C)",
              "سيريال الجهاز": "PC-4412903",
              "مقاس/نوع الشاشة": "Lenovo 27 inch",
              "سيريال الشاشة": "MON-998231",
              "موديل الطابعة": "Canon MF754Cdw (Color)",
              "نوع طباعة الطابعة": "ملون",
              "سيريال الطابعة": "PRN-332145",
              "حالة العطل": "بطء في التشغيل يحتاج فحص الباور",
              "ملاحظات": "جهاز خاص بغرفة الإدارة",
          },
          {
              "المنطقة": "منطقة حولي التعليمية",
              "المبنى": "مدرسة ابن خلدون المتوسطة",
              "الدور": "الدور الثاني",
              "الإدارة": "الشؤون التعليمية",
              "القسم": "مختبر الحاسب الآلي",
              "اسم الموظف": "خالد الشمري",
              "نوع الجهاز (PC)": "laptop",
              "سيريال الجهاز": "LAP-112233",
              "مقاس/نوع الشاشة": "لابتوب (شاشة مدمجة)",
              "سيريال الشاشة": "N/A",
              "موديل الطابعة": "Label Printer",
              "نوع طباعة الطابعة": "ملصقات",
              "سيريال الطابعة": "PRN-998877",
              "حالة العطل": "سليم",
              "ملاحظات": "جهاز محمول خاص بالتنقل والمتابعة",
          },
          {
              "المنطقة": "منطقة الفروانية التعليمية",
              "المبنى": "مدرسة العارضية الابتدائية",
              "الدور": "الدور الأرضي",
              "الإدارة": "السكرتارية",
              "القسم": "قسم الإدارة",
              "اسم الموظف": "فهد المطيري",
              "نوع الجهاز (PC)": "Lenovo M70q (Type B)",
              "سيريال الجهاز": "PC-665544",
              "مقاس/نوع الشاشة": "Lenovo 24 inch",
              "سيريال الشاشة": "MON-112233",
              "موديل الطابعة": "غير موجود",
              "نوع طباعة الطابعة": "",
              "سيريال الطابعة": "",
              "حالة العطل": "لا يعمل - مشكلة في اللوحة الأم",
              "ملاحظات": "بانتظار قطع الغيار للصيانة",
          },
      ],
      columns=[
          "المنطقة",
          "المبنى",
          "الدور",
          "الإدارة",
          "القسم",
          "اسم الموظف",
          "نوع الجهاز (PC)",
          "سيريال الجهاز",
          "مقاس/نوع الشاشة",
          "سيريال الشاشة",
          "موديل الطابعة",
          "نوع طباعة الطابعة",
          "سيريال الطابعة",
          "حالة العطل",
          "ملاحظات",
      ],
  )

# --- شاشة تسجيل الدخول ---
if not st.session_state.logged_in:
  st.markdown(
      """
        <div style="background: linear-gradient(135deg, #78350f, #b45309); padding: 40px; border-radius: 16px; color: white; text-align: center; margin-bottom: 30px; box-shadow: 0 10px 25px rgba(0,0,0,0.1);">
            <h1 style="margin: 0; font-size: 32px;">نظام حصر الأصول والدعم التقني</h1>
            <p style="margin: 10px 0 0 0; opacity: 0.95; font-size: 18px;">وزارة التربية - إدارة النظم الآلية والبنية التحتية</p>
        </div>
    """,
      unsafe_allow_html=True,
  )

  col1, col2, col3 = st.columns([1, 1.5, 1])
  with col2:
    st.markdown("### تسجيل الدخول للنظام")
    with st.form("login_form"):
      username_input = st.text_input("اسم المستخدم", value="")
      password_input = st.text_input(
          "كلمة المرور", type="password", value=""
      )
      login_submit = st.form_submit_button("دخول النظام")

      if login_submit:
        users = st.session_state.users_df
        matched = users[
            (users["اسم المستخدم"] == username_input)
            & (users["كلمة المرور"] == password_input)
        ]
        if not matched.empty:
          user_status = matched.iloc[0]["الحالة"]
          if user_status == "معطل":
            st.error(
                "عذراً، هذا الحساب معطل حالياً. يرجى مراجعة مدير النظام."
            )
          else:
            st.session_state.logged_in = True
            st.session_state.current_user = username_input
            st.session_state.user_role = matched.iloc[0]["الصلاحية"]
            st.success("تم تسجيل الدخول بنجاح!")
            st.rerun()
        else:
          st.error("اسم المستخدم أو كلمة المرور غير صحيحة.")
  st.stop()

# تهيئة التنقل بعد تسجيل الدخول
if "current_page" not in st.session_state:
  st.session_state.current_page = "🏠 الرئيسية وإضافة العهد"

# القائمة الجانبية للتنقل
st.sidebar.title("🧭 تنقل النظام")
st.sidebar.markdown(
    f"<p style='color: #fef3c7; font-size: 14px;'>المستخدم: <b>{st.session_state.current_user}</b><br>الصلاحية: {st.session_state.user_role}</p>",
    unsafe_allow_html=True,
)
st.sidebar.markdown("---")

nav_options = [
    "🏠 الرئيسية وإضافة العهد",
    "📋 سجل الأصول والبحث المتقدم",
    "📊 تفاصيل إحصائيات الموظفين",
    "💻 تفاصيل إحصائيات الأجهزة (PC)",
    "🖥️ تفاصيل إحصائيات الشاشات",
    "🖨️ تفاصيل إحصائيات الطابعات",
    "⚠️ تفاصيل الأعطال التقنية والصيانة",
    "👥 إدارة المستخدمين",
]

selected_nav = st.sidebar.radio(
    "الانتقال السريع:",
    nav_options,
    index=nav_options.index(st.session_state.current_page)
    if st.session_state.current_page in nav_options
    else 0,
    label_visibility="collapsed",
)
if selected_nav != st.session_state.current_page:
  st.session_state.current_page = selected_nav
  st.rerun()

st.sidebar.markdown("---")
if st.sidebar.button("🚪 تسجيل الخروج"):
  st.session_state.logged_in = False
  st.session_state.current_user = ""
  st.session_state.user_role = ""
  st.rerun()

# العنوان الثابت
st.markdown(
    """
    <div style="background: linear-gradient(135deg, #78350f, #b45309); padding: 20px; border-radius: 12px; color: white; text-align: center; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
        <h1 style="margin: 0; font-size: 26px;">نظام حصر الأصول والدعم التقني</h1>
        <p style="margin: 5px 0 0 0; opacity: 0.95; font-size: 14px;">وزارة التربية - إدارة النظم الآلية والبنية التحتية (قسم التشغيل والدعم التقني)</p>
    </div>
""",
    unsafe_allow_html=True,
)

df = st.session_state.assets_df
total_records = len(df)

total_pcs = (
    df["نوع الجهاز (PC)"].astype(bool).sum() if total_records > 0 else 0
)
total_monitors = (
    df["مقاس/نوع الشاشة"].astype(bool).sum() if total_records > 0 else 0
)
total_printers = (
    df["موديل الطابعة"].astype(bool).sum() if total_records > 0 else 0
)
total_faults = (
    df[df["حالة العطل"] != "سليم"]["حالة العطل"].count()
    if total_records > 0
    else 0
)

page = st.session_state.current_page

# --- 1. الرئيسية وإضافة العهد ---
if page == "🏠 الرئيسية وإضافة العهد":
  st.subheader("📊 لوحة المؤشرات التفاعلية")
  st.markdown(
      "<p style='color: gray;'>اضغط على أي بطاقة أدناه للانتقال الفوري للتقرير"
      " الخاص به:</p>",
      unsafe_allow_html=True,
  )

  dcol1, dcol2, dcol3, dcol4, dcol5 = st.columns(5)

  with dcol1:
    st.markdown(
        f"""
        <div class="metric-card">
            <h3>إجمالي الموظفين</h3>
            <h2>{total_records}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("عرض تقرير الموظفين", key="btn_emp"):
      st.session_state.current_page = "📊 تفاصيل إحصائيات الموظفين"
      st.rerun()

  with dcol2:
    st.markdown(
        f"""
        <div class="metric-card">
            <h3>إجمالي الأجهزة</h3>
            <h2>{total_pcs}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("عرض تقرير الأجهزة", key="btn_pc"):
      st.session_state.current_page = "💻 تفاصيل إحصائيات الأجهزة (PC)"
      st.rerun()

  with dcol3:
    st.markdown(
        f"""
        <div class="metric-card">
            <h3>إجمالي الشاشات</h3>
            <h2>{total_monitors}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("عرض تقرير الشاشات", key="btn_mon"):
      st.session_state.current_page = "🖥️ تفاصيل إحصائيات الشاشات"
      st.rerun()

  with dcol4:
    st.markdown(
        f"""
        <div class="metric-card">
            <h3>إجمالي الطابعات</h3>
            <h2>{total_printers}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("عرض تقرير الطابعات", key="btn_prn"):
      st.session_state.current_page = "🖨️ تفاصيل إحصائيات الطابعات"
      st.rerun()

  with dcol5:
    st.markdown(
        f"""
        <div class="metric-card" style="background: linear-gradient(135deg, #991b1b 0%, #b91c1c 100%);">
            <h3>الأجهزة المعطلة</h3>
            <h2>{total_faults}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )
    if st.button("عرض تقرير الأعطال", key="btn_flt"):
      st.session_state.current_page = "⚠️ تفاصيل الأعطال التقنية والصيانة"
      st.rerun()

  st.markdown("---")

  st.subheader("📥 استيراد البيانات (Excel / CSV) أو الإدخال اليدوي")

  with st.expander("📁 اضغط هنا لرفع ملف إكسيل جماعي", expanded=False):
    uploaded_file = st.file_uploader(
        "اختر ملف Excel أو CSV", type=["xlsx", "xls", "csv"]
    )
    if uploaded_file is not None:
      try:
        if uploaded_file.name.endswith(".csv"):
          df_imported = pd.read_csv(uploaded_file)
        else:
          df_imported = pd.read_excel(uploaded_file)

        if st.button("معالجة وإضافة البيانات المرفوعة"):
          st.session_state.assets_df = pd.concat(
              [st.session_state.assets_df, df_imported], ignore_index=True
          )
          st.success(
              f"تم استيراد {len(df_imported)} سجلاً بنجاح إلى قاعدة البيانات!"
          )
          st.rerun()
      except Exception as e:
        st.error(f"حدث خطأ أثناء قراءة الملف: {e}")

  st.markdown("#### نموذج تسجيل عهدة جديدة")
  with st.form("manual_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
      regions = [
          "",
          "مبنى الوزارة الرئيسي",
          "منطقة العاصمة التعليمية",
          "منطقة حولي التعليمية",
          "منطقة الفروانية التعليمية",
          "منطقة الأحمدي التعليمية",
          "منطقة الجهراء التعليمية",
          "منطقة مبارك الكبير التعليمية",
      ]
      region = st.selectbox("المنطقة", regions)
    with col2:
      building = st.text_input("اسم المبنى", value="")
    with col3:
      floor_options = [
          "",
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
      ]
      floor = st.selectbox("الدور", floor_options)

    col4, col5, col6 = st.columns(3)
    with col4:
      department = st.text_input("الإدارة", value="")
    with col5:
      section = st.text_input("القسم", value="")
    with col6:
      employee = st.text_input("اسم الموظف المسؤول", value="")

    st.markdown("#### تفاصيل الأجهزة، الشاشات، والطابعات")
    col7, col8 = st.columns(2)
    with col7:
      pc_options = [
          "",
          "Lenovo M70q (Type B)",
          "Lenovo M70q (Type A)",
          "Lenovo M90t (Type C)",
          "laptop",
      ]
      pc_type = st.selectbox("نوع الجهاز (PC)", pc_options)

      if pc_type and pc_type != "laptop":
        monitor_options = ["", "Lenovo 24 inch", "Lenovo 27 inch"]
        monitor_type = st.selectbox("مقاس / نوع الشاشة", monitor_options)
      else:
        monitor_type = (
            "لابتوب (شاشة مدمجة)" if pc_type == "laptop" else ""
        )
        if pc_type == "laptop":
          st.info("تم تحديد شاشة مدمجة تلقائياً لأن الجهاز Laptop.")

      printer_options = [
          "",
          "Canon MF463dw (Black)",
          "Canon MF754Cdw (Color)",
          "Label Printer",
          "غير موجود",
      ]
      printer_model = st.selectbox("موديل الطابعة", printer_options)

      if printer_model == "Canon MF463dw (Black)":
        printer_color_type = "أسود وأبيض"
      elif printer_model == "Canon MF754Cdw (Color)":
        printer_color_type = "ملون"
      elif printer_model == "Label Printer":
        printer_color_type = "ملصقات"
      else:
        printer_color_type = ""

    with col8:
      pc_serial = st.text_input("سيريال نمبر الجهاز (PC S/N)", value="")
      monitor_serial = st.text_input("سيريال نمبر الشاشة", value="")
      printer_serial = st.text_input("سيريال نمبر الطابعة", value="")

    col_fault, col_notes = st.columns(2)
    with col_fault:
      fault_status = st.text_input("خانة تسجيل العطل", value="")
    with col_notes:
      notes = st.text_input("ملاحظات إضافية", value="")

    submitted = st.form_submit_button("حفظ في سجل الأصول")
    if submitted:
      if not employee or not department:
        st.warning("الرجاء إدخال اسم الموظف وإدارة العمل على الأقل.")
      else:
        new_row = {
            "المنطقة": region,
            "المبنى": building,
            "الدور": floor,
            "الإدارة": department,
            "القسم": section,
            "اسم الموظف": employee,
            "نوع الجهاز (PC)": pc_type,
            "سيريال الجهاز": pc_serial,
            "مقاس/نوع الشاشة": monitor_type,
            "سيريال الشاشة": monitor_serial,
            "موديل الطابعة": printer_model,
            "نوع طباعة الطابعة": printer_color_type,
            "سيريال الطابعة": printer_serial,
            "حالة العطل": fault_status if fault_status else "سليم",
            "ملاحظات": notes,
        }
        st.session_state.assets_df = pd.concat(
            [
                st.session_state.assets_df,
                pd.DataFrame([new_row], columns=st.session_state.assets_df.columns),
            ],
            ignore_index=True,
        )
        st.success("تم تسجيل العهدة بنجاح!")
        st.rerun()

# --- 2. سجل الأصول والبحث المتقدم وإمكانية الحذف ---
elif page == "📋 سجل الأصول والبحث المتقدم":
  st.subheader("📋 سجل الأصول، إدارة الموظفين، والبحث المتقدم")
  if len(df) > 0:
    search_query = st.text_input(
        "🔍 ابحث في السجلات (بالاسم، السيريال، الإدارة...):", value=""
    )
    if search_query:
      mask = df.astype(str).apply(
          lambda x: x.str.contains(search_query, case=False, na=False)
      ).any(axis=1)
      filtered_df = df[mask]
    else:
      filtered_df = df

    st.dataframe(filtered_df, use_container_width=True)

    st.markdown("---")
    st.markdown("#### 🗑️ حذف عهدة أو موظف من السجلات")
    emp_list_to_delete = df["اسم الموظف"].tolist()
    selected_emp_to_delete = st.selectbox(
        "اختر الموظف المراد حذف سجله وعهدته:", [""] + emp_list_to_delete
    )

    if st.button("حذف السجل المحدد"):
      if selected_emp_to_delete:
        st.session_state.assets_df = df[
            df["اسم الموظف"] != selected_emp_to_delete
        ].reset_index(drop=True)
        st.success(
            f"تم حذف سجل الموظف ({selected_emp_to_delete}) والعهد الخاصة به بنجاح!"
        )
        st.rerun()
      else:
        st.warning("الرجاء اختيار موظف للحذف.")

    st.markdown("---")
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
      buffer = io.BytesIO()
      with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df.to_excel(writer, sheet_name="الأصول", index=False)
      buffer.seek(0)
      st.download_button(
          label="📥 تحميل كافة السجلات كملف Excel",
          data=buffer,
          file_name="ministry_assets.xlsx",
          mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      )
    with col_btn2:
      if st.button("مسح كافة السجلات نهائياً"):
        st.session_state.assets_df = pd.DataFrame(columns=df.columns)
        st.rerun()
  else:
    st.info("لا توجد بيانات مسجلة حتى الآن.")

# --- 3. تفاصيل إحصائيات الموظفين ---
elif page == "📊 تفاصيل إحصائيات الموظفين":
  st.subheader("📊 إحصائيات توزيع الموظفين حسب المناطق والمباني")
  if total_records > 0:
    col1, col2 = st.columns(2)
    with col1:
      st.metric("إجمالي الموظفين المسجلين", total_records)
    with col2:
      st.metric("عدد المناطق المغطاة", df["المنطقة"].nunique())

    st.markdown("### التوزيع حسب المنطقة:")
    region_counts = df["المنطقة"].value_counts().reset_index()
    region_counts.columns = ["المنطقة", "عدد السجلات"]
    st.dataframe(region_counts, use_container_width=True)

    st.markdown("### قائمة الموظفين التفصيلية:")
    st.dataframe(
        df[["اسم الموظف", "المنطقة", "المبنى", "الإدارة", "القسم"]],
        use_container_width=True,
    )
  else:
    st.info("لا توجد بيانات كافية لعرض الإحصائيات.")

# --- 4. تفاصيل إحصائيات الأجهزة (PC) ---
elif page == "💻 تفاصيل إحصائيات الأجهزة (PC)":
  st.subheader("💻 تفصيل أجهزة الحاسب الآلي واللابتوب")
  if total_records > 0:
    pcs_df = df[
        (df["نوع الجهاز (PC)"].astype(bool))
        & (df["نوع الجهاز (PC)"] != "غير موجود")
    ]
    st.metric("إجمالي الأجهزة المسجلة", len(pcs_df))

    if len(pcs_df) > 0:
      pc_counts = pcs_df["نوع الجهاز (PC)"].value_counts().reset_index()
      pc_counts.columns = ["نوع الجهاز", "العدد"]
      st.dataframe(pc_counts, use_container_width=True)

      st.markdown("### تفاصيل أجهزة الموظفين والسيريال:")
      st.dataframe(
          pcs_df[
              [
                  "اسم الموظف",
                  "المنطقة",
                  "الإدارة",
                  "نوع الجهاز (PC)",
                  "سيريال الجهاز",
              ]
          ],
          use_container_width=True,
      )
    else:
      st.write("لا توجد أجهزة مسجلة.")
  else:
    st.info("لا توجد بيانات مسجلة.")

# --- 5. تفاصيل إحصائيات الشاشات ---
elif page == "🖥️ تفاصيل إحصائيات الشاشات":
  st.subheader("🖥️ تفصيل الشاشات حسب المقاسات والأنواع")
  if total_records > 0:
    mon_df = df[
        (df["مقاس/نوع الشاشة"].astype(bool))
        & (~df["مقاس/نوع الشاشة"].isin(["غير موجود"]))
    ]
    st.metric("إجمالي الشاشات المسجلة", len(mon_df))

    if len(mon_df) > 0:
      mon_counts = mon_df["مقاس/نوع الشاشة"].value_counts().reset_index()
      mon_counts.columns = ["مقاس/نوع الشاشة", "العدد"]
      st.dataframe(mon_counts, use_container_width=True)

      st.markdown("### تفاصيل الشاشات والسيريال المرتبط بها:")
      st.dataframe(
          mon_df[
              [
                  "اسم الموظف",
                  "المنطقة",
                  "المبنى",
                  "مقاس/نوع الشاشة",
                  "سيريال الشاشة",
              ]
          ],
          use_container_width=True,
      )
    else:
      st.write("لا توجد شاشات مسجلة.")
  else:
    st.info("لا توجد بيانات مسجلة.")

# --- 6. تفاصيل إحصائيات الطابعات ---
elif page == "🖨️ تفاصيل إحصائيات الطابعات":
  st.subheader("🖨️ التقرير التفصيلي للطابعات (ملون، أسود وأبيض، وملصقات)")
  if total_records > 0:
    print_df = df[
        (df["موديل الطابعة"].astype(bool))
        & (df["موديل الطابعة"] != "غير موجود")
    ]

    total_p = len(print_df)
    color_p = len(print_df[print_df["نوع طباعة الطابعة"] == "ملون"])
    bw_p = len(print_df[print_df["نوع طباعة الطابعة"] == "أسود وأبيض"])
    label_p = len(print_df[print_df["نوع طباعة الطابعة"] == "ملصقات"])

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("إجمالي الطابعات", total_p)
    c2.metric("🖨️ أسود وأبيض", bw_p)
    c3.metric("🎨 ملون", color_p)
    c4.metric("🏷️ ملصقات (Label)", label_p)

    st.markdown("### تفصيل الموديلات والأنواع:", unsafe_allow_html=True)
    if total_p > 0:
      p_counts = (
          print_df[["موديل الطابعة", "نوع طباعة الطابعة"]]
          .value_counts()
          .reset_index()
      )
      p_counts.columns = ["موديل الطابعة", "نوع الطباعة", "العدد"]
      st.dataframe(p_counts, use_container_width=True)

      st.markdown("### تفاصيل عهد الطابعات للموظفين:")
      st.dataframe(
          print_df[
              [
                  "اسم الموظف",
                  "المنطقة",
                  "المبنى",
                  "موديل الطابعة",
                  "نوع طباعة الطابعة",
                  "سيريال الطابعة",
              ]
          ],
          use_container_width=True,
      )
    else:
      st.write("لا توجد طابعات مسجلة.")
  else:
    st.info("لا توجد بيانات مسجلة.")

# --- 7. تفاصيل الأعطال التقنية والصيانة ---
elif page == "⚠️ تفاصيل الأعطال التقنية والصيانة":
  st.subheader("⚠️ متابعة الأعطال التقنية وتحديث حالة الأجهزة إلى (عمل / سليم)")
  if total_records > 0:
    faults_df = df[df["حالة العطل"] != "سليم"]
    st.metric("إجمالي الأجهزة التي بها أعطال أو قيد الصيانة", len(faults_df))

    if len(faults_df) > 0:
      st.markdown("#### الأجهزة المعطلة حالياً:")
      st.dataframe(
          faults_df[
              [
                  "المنطقة",
                  "المبنى",
                  "الإدارة",
                  "اسم الموظف",
                  "نوع الجهاز (PC)",
                  "سيريال الجهاز",
                  "حالة العطل",
                  "ملاحظات",
              ]
          ],
          use_container_width=True,
      )

      st.markdown("---")
      st.markdown("#### 🛠️ تحديث حالة جهاز معطل وإرجاعه إلى (يعمل / سليم)")

      faulty_serials = faults_df["سيريال الجهاز"].tolist()
      selected_serial_to_fix = st.selectbox(
          "اختر سيريال الجهاز الذي تم إصلاحه:", [""] + faulty_serials
      )

      if st.button("تحديث الحالة إلى (يعمل وجاهز)"):
        if selected_serial_to_fix:
          st.session_state.assets_df.loc[
              st.session_state.assets_df["سيريال الجهاز"]
              == selected_serial_to_fix,
              "حالة العطل",
          ] = "سليم"
          st.success(
              f"تم تحديث الجهاز ذو السيريال ({selected_serial_to_fix}) إلى حالة"
              " (سليم ويعمل) بنجاح!"
          )
          st.rerun()
        else:
          st.warning("الرجاء اختيار جهاز للتحديث.")

    else:
      st.success(
          "ممتاز! لا توجد أي أعطال مسجلة حالياً، كافة الأجهزة سليمة وتعمل"
          " بكفاءة."
      )
  else:
    st.info("لا توجد بيانات مسجلة.")

# --- 8. إدارة المستخدمين ---
elif page == "👥 إدارة المستخدمين":
  st.subheader("👥 إدارة مستخدمي النظام والصلاحيات")

  if st.session_state.user_role != "مدير النظام":
    st.warning(
        "عذراً، هذه الصفحة خاصة بمدير النظام فقط ولا تمتلك صلاحية التعديل عليها."
    )
    st.dataframe(st.session_state.users_df, use_container_width=True)
  else:
    # 1. إضافة مستخدم جديد
    st.markdown("#### ➕ إضافة مستخدم جديد")
    with st.form("new_user_form"):
      ncol1, ncol2, ncol3 = st.columns(3)
      with ncol1:
        new_username = st.text_input("اسم المستخدم الجديد", value="")
      with ncol2:
        new_password = st.text_input(
            "كلمة المرور", type="password", value=""
        )
      with ncol3:
        new_role = st.selectbox(
            "الصلاحية", ["مدير النظام", "فني دعم", "مستخدم عارض"]
        )

      add_user_btn = st.form_submit_button("إضافة المستخدم")
      if add_user_btn:
        if not new_username or not new_password:
          st.warning("الرجاء إدخال اسم المستخدم وكلمة المرور.")
        elif new_username in st.session_state.users_df["اسم المستخدم"].values:
          st.error("اسم المستخدم موجود مسبقاً، اختر اسمًا آخر.")
        else:
          new_u_row = pd.DataFrame(
              {
                  "اسم المستخدم": [new_username],
                  "كلمة المرور": [new_password],
                  "الصلاحية": [new_role],
                  "الحالة": ["نشط"],
              }
          )
          st.session_state.users_df = pd.concat(
              [st.session_state.users_df, new_u_row], ignore_index=True
          )
          st.success(f"تم إضافة المستخدم {new_username} بنجاح!")
          st.rerun()

    st.markdown("---")

    # 2. تعديل كلمة المرور أو الحالة أو الحذف للمستخدمين الحاليين
    st.markdown("#### ⚙️ تعديل أو تعطيل أو حذف المستخدمين")
    users_list = st.session_state.users_df["اسم المستخدم"].tolist()
    selected_target_user = st.selectbox(
        "اختر اسم المستخدم للتعديل أو الإدارة:", [""] + users_list
    )

    if selected_target_user:
      current_user_data = st.session_state.users_df[
          st.session_state.users_df["اسم المستخدم"] == selected_target_user
      ].iloc[0]

      with st.form("edit_user_form"):
        ecol1, ecol2, ecol3 = st.columns(3)
        with ecol1:
          new_pass_edit = st.text_input(
              "تعديل كلمة المرور (اتركها فارغة لعدم التغيير)",
              type="password",
              value="",
          )
        with ecol2:
          current_status_idx = (
              0 if current_user_data["الحالة"] == "نشط" else 1
          )
          new_status_edit = st.selectbox(
              "حالة الحساب", ["نشط", "معطل"], index=current_status_idx
          )
        with ecol3:
          current_role_options = ["مدير النظام", "فني دعم", "مستخدم عارض"]
          curr_role_idx = (
              current_role_options.index(current_user_data["الصلاحية"])
              if current_user_data["الصلاحية"] in current_role_options
              else 0
          )
          new_role_edit = st.selectbox(
              "الصلاحية", current_role_options, index=curr_role_idx
          )

        update_user_btn = st.form_submit_button("حفظ التعديلات على المستخدم")
        if update_user_btn:
          idx = st.session_state.users_df[
              st.session_state.users_df["اسم المستخدم"] == selected_target_user
          ].index[0]
          if new_pass_edit.strip() != "":
            st.session_state.users_df.at[idx, "كلمة المرور"] = new_pass_edit
          st.session_state.users_df.at[idx, "الحالة"] = new_status_edit
          st.session_state.users_df.at[idx, "الصلاحية"] = new_role_edit
          st.success(f"تم تحديث بيانات المستخدم ({selected_target_user}) بنجاح!")
          st.rerun()

      if st.button("🗑️ حذف هذا المستخدم نهائياً"):
        if selected_target_user == "admin":
          st.error("لا يمكن حذف حساب مدير النظام الأساسي (admin).")
        else:
          st.session_state.users_df = st.session_state.users_df[
              st.session_state.users_df["اسم المستخدم"] != selected_target_user
          ].reset_index(drop=True)
          st.success(f"تم حذف المستخدم ({selected_target_user}) بنجاح!")
          st.rerun()

    st.markdown("---")
    st.markdown("#### 📋 قائمة المستخدمين الحاليين بالنظام")
    st.dataframe(st.session_state.users_df, use_container_width=True)

# زر العودة للرئيسية إذا كان المستخدم في صفحة فرعية
if page != "🏠 الرئيسية وإضافة العهد":
  st.markdown("---")
  if st.button("⬅️ العودة إلى الرئيسية ولوحة المؤشرات"):
    st.session_state.current_page = "🏠 الرئيسية وإضافة العهد"
    st.rerun()
