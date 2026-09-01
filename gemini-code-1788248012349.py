import pandas as pd
import streamlit as st
import io

# إعدادات الصفحة
st.set_page_config(
    page_title="نظام حصر الأصول - وزارة التربية", page_icon="💻", layout="wide"
)

# تخصيص التصميم ليدعم اللغة العربية والاتجاه من اليمين لليسار
st.markdown(
    """
    <style>
    body, [data-testid="stAppViewContainer"] {
        direction: rtl;
        text-align: right;
        font-family: 'Tajawal', sans-serif;
    }
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        font-weight: bold;
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
            "ملاحظات",
        ]
    )

# القوائم الجانبية أو التبويبات الرئيسية
tab1, tab2, tab3 = st.tabs(
    ["📥 تسجيل عهدة / رفع ملف Excel", "📊 لوحة الإحصائيات", "📋 سجل الأصول"]
)

with tab1:
  st.subheader("استيراد البيانات الضخمة عبر ملف Excel / CSV")
  st.write(
    "قم برفع ملف إكسيل جاهز يحتوي على الأعمدة بالترتيب الصحيح لتحديث السجلات"
    " دفعة واحدة."
  )

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
        # دمج البيانات الجديدة مع البيانات الحالية
        st.session_state.assets_df = pd.concat(
            [st.session_state.assets_df, df_imported], ignore_index=True
        )
        st.success(
            f"تم استيراد {len(df_imported)} سجلاً بنجاح إلى قاعدة البيانات!"
        )
    except Exception as e:
      st.error(f"حدث خطأ أثناء قراءة الملف: {e}")

  st.markdown("---")
  st.subheader("أو الإدخال اليدوي الفردي")

  with st.form("manual_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
      building = st.text_input("اسم المبنى", "ديوان الوزارة")
    with col2:
      floor = st.selectbox(
          "الدور",
          [
              "الدور الأرضي",
              "الأول",
              "الثاني",
              "الثالث",
              "الرابع",
              "الخامس",
              "السادس",
              "السابع",
              "الثامن",
              "التاسع",
              "العاشر",
          ],
      )
    with col3:
      department = st.text_input("الإدارة", placeholder="مثال: إدارة النظم الآلية")

    col4, col5 = st.columns(2)
    with col4:
      section = st.text_input("القسم", placeholder="التشغيل والدعم التقني")
    with col5:
      employee = st.text_input("اسم الموظف المسؤول")

    st.markdown("#### تفاصيل العهدة والأرقام التسلسلية")
    col6, col7 = st.columns(2)
    with col6:
      pc_type = st.text_input("نوع وموديل الجهاز (PC)")
      monitor_type = st.text_input("نوع وحجم الشاشة")
      printer_type = st.text_input("نوع الطابعة")
    with col7:
      pc_serial = st.text_input("سيريال نمبر الجهاز (PC S/N)")
      monitor_serial = st.text_input("سيريال نمبر الشاشة")
      printer_serial = st.text_input("سيريال نمبر الطابعة")

    notes = st.text_area("ملاحظات إضافية")

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

with tab2:
  st.subheader("مؤشرات وإحصائيات الحصر الشاملة")
  df = st.session_state.assets_df

  total_records = len(df)
  total_pcs = df["نوع الجهاز (PC)"].astype(bool).sum() if total_records > 0 else 0
  total_monitors = (
      df["نوع الشاشة"].astype(bool).sum() if total_records > 0 else 0
  )
  total_printers = (
      df["نوع الطابعة"].astype(bool).sum() if total_records > 0 else 0
  )

  mcol1, mcol2, mcol3, mcol4 = st.columns(4)
  mcol1.metric("إجمالي الموظفين", total_records)
  mcol2.metric("إجمالي الأجهزة (PC)", total_pcs)
  mcol3.metric("إجمالي الشاشات", total_monitors)
  mcol4.metric("إجمالي الطابعات", total_printers)

with tab3:
  st.subheader("سجل عهد ديوان الوزارة والأجهزة")
  df = st.session_state.assets_df

  if len(df) > 0:
    st.dataframe(df, use_container_width=True)

    # زر مسح أو حذف الكل
    if st.button("مسح كافة السجلات"):
      st.session_state.assets_df = pd.DataFrame(columns=df.columns)
      st.rerun()
  else:
    st.info("لا توجد أجهزة محفوظة حتى الآن. أضف بيانات يدوياً أو ارفع ملف إكسيل.")
