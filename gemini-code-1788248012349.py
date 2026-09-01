import io
import pandas as pd
import streamlit as st

# إعدادات الصفحة
st.set_page_config(
    page_title="نظام حصر الأصول والدعم التقني", page_icon="💻", layout="wide"
)

# تخصيص التصميم ليدعم اللغة العربية والاتجاه من اليمين لليسار
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

# تهيئة الذاكرة المؤقتة للبيانات
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
          "مقاس/نوع الشاشة",
          "سيريال الشاشة",
          "موديل الطابعة",
          "نوع طباعة الطابعة",
          "سيريال الطابعة",
          "حالة العطل",
          "ملاحظات",
      ]
  )

# القائمة الجانبية للتنقل بين الصفحات والصفحات الخاصة للإحصائيات
st.sidebar.title("🧭 تنقل النظام")
page = st.sidebar.radio(
    "اختر الصفحة:",
    [
        "🏠 الرئيسية واللوحة الشاملة",
        "📥 تسجيل عهدة جديدة / رفع ملف",
        "📋 سجل الأصول والبحث المتقدم",
        "📊 تفاصيل إحصائيات الموظفين",
        "💻 تفاصيل إحصائيات الأجهزة (PC)",
        "🖥️ تفاصيل إحصائيات الشاشات",
        "🖨️ تفاصيل إحصائيات الطابعات (ملون / أبيض وأسود)",
        "⚠️ تفاصيل الأعطال التقنية",
    ],
)

# العنوان الثابت
st.markdown(
    """
    <div style="background: linear-gradient(to right, #065f46, #0f766e); padding: 20px; border-radius: 15px; color: white; text-align: center; margin-bottom: 20px;">
        <h1 style="margin: 0; font-size: 28px;">نظام حصر الأصول والدعم التقني</h1>
        <p style="margin: 5px 0 0 0; opacity: 0.9;">وزارة التربية - إدارة النظم الآلية والبنية التحتية (قسم التشغيل والدعم التقني)</p>
    </div>
""",
    unsafe_allow_html=True,
)

df = st.session_state.assets_df
total_records = len(df)

# --- 1. الصفحة الرئيسية واللوحة الشاملة ---
if page == "🏠 الرئيسية واللوحة الشاملة":
  st.subheader("📊 لوحة المؤشرات والإحصائيات الشاملة")

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

  col1, col2, col3, col4, col5 = st.columns(5)
  with col1:
    if st.metric("إجمالي الموظفين", total_records):
      pass
  with col2:
    if st.metric("إجمالي الأجهزة", total_pcs):
      pass
  with col3:
    if st.metric("إجمالي الشاشات", total_monitors):
      pass
  with col4:
    if st.metric("إجمالي الطابعات", total_printers):
      pass
  with col5:
    if st.metric("الأجهزة المعطلة", total_faults):
      pass

  st.info(
      "💡 يمكنك الانتقال إلى أي إحصائية تفصيلية عبر القائمة الجانبية للتحكم في"
      " عرض البيانات ومعاينة التصنيفات والألوان."
  )

  if total_records > 0:
    st.markdown("### 📋 معاينة سريعة لأحدث السجلات")
    st.dataframe(df.tail(5), use_container_width=True)

# --- 2. صفحة تسجيل عهدة جديدة / رفع ملف ---
elif page == "📥 تسجيل عهدة جديدة / رفع ملف":
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
  st.subheader(
      "الإدخال اليدوي مع قوائم الاختيارات المباشرة (المبنى مكون من 11 دور)"
  )

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

    st.markdown("#### تفاصيل العهدة والموديلات (اختيار من القوائم)")
    col6, col7 = st.columns(2)
    with col6:
      pc_type = st.text_input(
          "نوع وموديل الجهاز (PC)", placeholder="مثال: Dell OptiPlex 7090"
      )

      # قائمة اختيار مقاسات الشاشة
      monitor_options = [
          "غير موجود",
          "شاشة 19 بوصة",
          "شاشة 22 بوصة",
          "شاشة 24 بوصة",
          "شاشة 27 بوصة",
          "أخرى",
      ]
      monitor_type = st.selectbox("مقاس / نوع الشاشة", monitor_options)

      # قائمة اختيار موديلات الطابعات
      printer_options = [
          "غير موجود",
          "HP LaserJet Pro (أبيض وأسود)",
          "HP Color LaserJet (ملون)",
          "Canon imageRUNNER (أبيض وأسود)",
          "Brother HL Series (أبيض وأسود)",
          "Epson EcoTank (ملون)",
          "أخرى",
      ]
      printer_model = st.selectbox("موديل الطابعة", printer_options)

      # تحديد تلقائي أو يدوي لنوع الطابعة (ملون / أبيض وأسود)
      if "ملون" in printer_model:
        printer_color_type = "ملون"
      elif "أبيض وأسود" in printer_model:
        printer_color_type = "أبيض وأسود"
      else:
        printer_color_type = st.selectbox(
            "نوع طباعة الطابعة", ["غير محدد", "أبيض وأسود", "ملون"]
        )

    with col7:
      pc_serial = st.text_input("سيريال نمبر الجهاز (PC S/N)")
      monitor_serial = st.text_input("سيريال نمبر الشاشة")
      printer_serial = st.text_input("سيريال نمبر الطابعة")

    col_fault, col_notes = st.columns(2)
    with col_fault:
      fault_status = st.text_input(
          "خانة تسجيل العطل",
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

# --- 3. سجل الأصول والبحث المتقدم ---
elif page == "📋 سجل الأصول والبحث المتقدم":
  st.subheader("سجل الأصول والبحث الفوري")
  if len(df) > 0:
    search_query = st.text_input(
        "🔍 ابحث في السجلات (بالاسم، السيريال، الإدارة، الدور، أو العطل)...", ""
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

# --- 4. صفحة تفاصيل إحصائيات الموظفين ---
elif page == "📊 تفاصيل إحصائيات الموظفين":
  st.subheader("📊 الصفحة الخاصة بإحصائيات وتوزيع الموظفين والأقسام")
  if total_records > 0:
    col1, col2 = st.columns(2)
    with col1:
      st.metric("إجمالي الموظفين المسجلين", total_records)
    with col2:
      st.metric("عدد الإدارات المختلفة", df["الإدارة"].nunique())

    st.markdown("### توزيع الموظفين حسب الأدوار في المبنى:")
    floor_counts = df["الدور"].value_counts().reset_index()
    floor_counts.columns = ["الدور", "عدد الموظفين"]
    st.dataframe(floor_counts, use_container_width=True)
  else:
    st.info("لا توجد بيانات كافية لعرض الإحصائيات.")

# --- 5. صفحة تفاصيل إحصائيات الأجهزة (PC) ---
elif page == "💻 تفاصيل إحصائيات الأجهزة (PC)":
  st.subheader("💻 الصفحة الخاصة بإحصائيات أجهزة الحاسب الآلي (PC)")
  if total_records > 0:
    pcs_df = df[df["نوع الجهاز (PC)"].astype(bool)]
    st.metric("إجمالي أجهزة الحاسب الآلي", len(pcs_df))

    st.markdown("### تفاصيل موديلات الأجهزة المسجلة:")
    if len(pcs_df) > 0:
      pc_counts = pcs_df["نوع الجهاز (PC)"].value_counts().reset_index()
      pc_counts.columns = ["موديل الجهاز", "العدد"]
      st.dataframe(pc_counts, use_container_width=True)
    else:
      st.write("لا توجد أجهزة حاسب مسجلة.")
  else:
    st.info("لا توجد بيانات مسجلة.")

# --- 6. صفحة تفاصيل إحصائيات الشاشات ---
elif page == "🖥️ تفاصيل إحصائيات الشاشات":
  st.subheader("🖥️ الصفحة الخاصة بإحصائيات الشاشات ومقاساتها")
  if total_records > 0:
    mon_df = df[
        (df["مقاس/نوع الشاشة"].astype(bool))
        & (df["مقاس/نوع الشاشة"] != "غير موجود")
    ]
    st.metric("إجمالي الشاشات الفعالة", len(mon_df))

    st.markdown("### توزيع الشاشات حسب المقاسات:")
    if len(mon_df) > 0:
      mon_counts = mon_df["مقاس/نوع الشاشة"].value_counts().reset_index()
      mon_counts.columns = ["مقاس الشاشة", "العدد"]
      st.dataframe(mon_counts, use_container_width=True)
    else:
      st.write("لا توجد شاشات مسجلة.")
  else:
    st.info("لا توجد بيانات مسجلة.")

# --- 7. صفحة تفاصيل إحصائيات الطابعات (ملون / أبيض وأسود) ---
elif page == "🖨️ تفاصيل إحصائيات الطابعات (ملون / أبيض وأسود)":
  st.subheader("🖨️ الصفحة الخاصة بإحصائيات الطابعات وتصنيفاتها")
  if total_records > 0:
    print_df = df[
        (df["موديل الطابعة"].astype(bool))
        & (df["موديل الطابعة"] != "غير موجود")
    ]

    total_p = len(print_df)
    color_p = len(
        print_df[print_df["نوع طباعة الطابعة"].str.contains("ملون", na=False)]
    )
    bw_p = len(
        print_df[
            print_df["نوع طباعة الطابعة"].str.contains("أبيض وأسود", na=False)
        ]
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("إجمالي الطابعات", total_p)
    c2.metric("🖨️ طابعات أبيض وأسود", bw_p)
    c3.metric("🎨 طابعات ملونة", color_p)

    st.markdown("### تفاصيل موديلات الطابعات وتصنيفاتها:")
    if total_p > 0:
      p_counts = (
          print_df[["موديل الطابعة", "نوع طباعة الطابعة"]]
          .value_counts()
          .reset_index()
      )
      p_counts.columns = ["موديل الطابعة", "نوع الطباعة (ملون/أسود)", "العدد"]
      st.dataframe(p_counts, use_container_width=True)
    else:
      st.write("لا توجد طابعات مسجلة.")
  else:
    st.info("لا توجد بيانات مسجلة.")

# --- 8. صفحة تفاصيل الأعطال التقنية ---
elif page == "⚠️ تفاصيل الأعطال التقنية":
  st.subheader("⚠️ الصفحة الخاصة بمتابعة الأعطال التقنية والأجهزة المعطلة")
  if total_records > 0:
    faults_df = df[df["حالة العطل"] != "سليم"]
    st.metric("إجمالي الأجهزة التي بها أعطال", len(faults_df))

    if len(faults_df) > 0:
      st.markdown("### قائمة الأجهزة المعطلة وتفاصيل الأعطال:")
      st.dataframe(
          faults_df[
              [
                  "المبنى",
                  "الدور",
                  "الإدارة",
                  "اسم الموظف",
                  "حالة العطل",
                  "ملاحظات",
              ]
          ],
          use_container_width=True,
      )
    else:
      st.success("ممتاز! لا توجد أي أعطال مسجلة حالياً، كافة الأجهزة سليمة.")
  else:
    st.info("لا توجد بيانات مسجلة.")
