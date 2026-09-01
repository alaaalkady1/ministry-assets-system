import io
import pandas as pd
import streamlit as st

# إعدادات الصفحة
st.set_page_config(
    page_title="نظام حصر الأصول والدعم التقني", page_icon="💻", layout="wide"
)

# تخصيص التصميم ليدعم اللغة العربية والاتجاه من اليمين لليسار بالكامل
st.markdown(
    """
    <style>
    body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {
        direction: rtl;
        text-align: right;
        font-family: 'Tajawal', sans-serif;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        font-weight: bold;
    }
    div.stDataFrame {
        direction: rtl;
        text-align: right;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# العنوان الرئيسي
st.markdown(
    """
    <div style="background: linear-gradient(to right, #065f46, #0f766e); padding: 20px; border-radius: 15px; color: white; text-align: center; margin-bottom: 20px;">
        <h1 style="margin: 0; font-size: 28px;">نظام حصر الأصول والدعم التقني</h1>
        <p style="margin: 5px 0 0 0; opacity: 0.9;">وزارة التربية - إدارة النظم الآلية والبنية التحتية (قسم التشغيل والدعم التقني)</p>
    </div>
""",
    unsafe_allow_html=True,
)

# تهيئة الذاكرة المؤقتة للبيانات (Session State)
if "assets_df" not in st.session_state:
  st.session_state.assets_df = pd.DataFrame(
      columns=[
          "المبنى",
          "الدور",
          "الإدارة",
          "القسم",
          "اسم الموظف",
          "نوع الجهاز (PC)",
          "سيريال الجهاز",
          "نوع الشاشة",
          "سيريال الشاشة",
          "نوع الطابعة",
          "سيريال الطابعة",
          "حالة العطل",
          "ملاحظات",
      ]
  )

# --- 1. لوحة الإحصائيات في الواجهة الرئيسية بشكل دائم ---
st.subheader("📊 مؤشرات وإحصائيات الحصر الشاملة")
df_stats = st.session_state.assets_df

total_records = len(df_stats)
total_pcs = (
    df_stats["نوع الجهاز (PC)"].astype(bool).sum() if total_records > 0 else 0
)
total_monitors = (
    df_stats["نوع الشاشة"].astype(bool).sum() if total_records > 0 else 0
)
total_printers = (
    df_stats["نوع الطابعة"].astype(bool).sum() if total_records > 0 else 0
)
total_faults = (
    df_stats[df_stats["حالة العطل"] != "سليم"]["حالة العطل"].count()
    if total_records > 0
    else 0
)

mcol1, mcol2, mcol3, mcol4, mcol5 = st.columns(5)
mcol1.metric("إجمالي الموظفين", total_records)
mcol2.metric("إجمالي الأجهزة", total_pcs)
mcol3.metric("إجمالي الشاشات", total_monitors)
mcol4.metric("إجمالي الطابعات", total_printers)
mcol5.metric("الأجهزة المعطلة", total_faults)

st.markdown("---")

# القوائم الرئيسية (تبويبان فقط للعمليات والسجلات)
tab1, tab2 = st.tabs(["📥 تسجيل عهدة / رفع ملف Excel", "📋 سجل الأصول والبحث المتقدم"])

with tab1:
  st.subheader("استيراد البيانات الضخمة عبر ملف Excel / CSV")
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

  st.markdown("---")
  st.subheader("الإدخال اليدوي الفردي (المبنى الرئيسي - 11 دور)")

  with st.form("manual_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
      building = st.text_input("اسم المبنى", "المبنى الرئيسي")
    with col2:
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
      ]
      floor = st.selectbox("الدور", floor_options)
    with col3:
      department = st.text_input("الإدارة", placeholder="مثال: إدارة النظم الآلية")

    col4, col5 = st.columns(2)
    with col4:
      section = st.text_input("القسم", placeholder="التشغيل والدعم التقني")
    with col5:
      employee = st.text_input("اسم الموظف المسؤول")

    st.markdown("#### تفاصيل العهدة والأرقام التسلسلية والأعطال")
    col6, col7 = st.columns(2)
    with col6:
      pc_type = st.text_input("نوع وموديل الجهاز (PC)")
      monitor_type = st.text_input("نوع وحجم الشاشة")
      printer_type = st.text_input("نوع الطابعة")
    with col7:
      pc_serial = st.text_input("سيريال نمبر الجهاز (PC S/N)")
      monitor_serial = st.text_input("سيريال نمبر الشاشة")
      printer_serial = st.text_input("سيريال نمبر الطابعة")

    col_fault, col_notes = st.columns(2)
    with col_fault:
      fault_status = st.text_input(
          "خانة تسجيل العطل (إن وجدت)",
          placeholder="مثال: سليم / عطل في الباور / لا يتصل بالشبكة",
      )
    with col_notes:
      notes = st.text_input("ملاحظات إضافية")

    submitted = st.form_submit_button("حفظ في سجل الأصول")
    if submitted:
      if not employee or not department:
        st.warning("الرجاء إدخال اسم الموظف وإدارة العمل على الأقل.")
      else:
        new_row = {
            "المبنى": building,
            "الدور": floor,
            "الإدارة": department,
            "القسم": section,
            "اسم الموظف": employee,
            "نوع الجهاز (PC)": pc_type,
            "سيريال الجهاز": pc_serial,
            "نوع الشاشة": monitor_type,
            "سيريال الشاشة": monitor_serial,
            "نوع الطابعة": printer_type,
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

with tab2:
  st.subheader("سجل الأصول والبحث المتقدم")
  df = st.session_state.assets_df

  if len(df) > 0:
    # خانة البحث الفوري
    search_query = st.text_input(
        "🔍 ابحث في السجلات (بالاسم، السيريال، الإدارة، الدور، أو حالة العطل)...",
        "",
    )

    if search_query:
      mask = df.astype(str).apply(
          lambda x: x.str.contains(search_query, case=False, na=False)
      ).any(axis=1)
      filtered_df = df[mask]
    else:
      filtered_df = df

    st.dataframe(filtered_df, use_container_width=True)

    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
      buffer = io.BytesIO()
      with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df.to_excel(writer, sheet_name="الأصول", index=False)
      buffer.seek(0)
      st.download_button(
          label="📥 تحميل السجلات كملف Excel",
          data=buffer,
          file_name="ministry_assets.xlsx",
          mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
      )

    with col_btn2:
      if st.button("مسح كافة السجلات نهائياً"):
        st.session_state.assets_df = pd.DataFrame(columns=df.columns)
        st.rerun()
  else:
    st.info("لا توجد أجهزة محفوظة حتى الآن. أضف بيانات يدوياً أو ارفع ملف إكسيل.")
