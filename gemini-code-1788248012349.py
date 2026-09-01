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

# تهيئة الذاكرة المؤقتة للبيانات بالترتيب الجديد المطلوب
if "assets_df" not in st.session_state:
  st.session_state.assets_df = pd.DataFrame(
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
      ]
  )

# القائمة الجانبية للتنقل بين الصفحات والإحصائيات
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
        "🖨️ تفاصيل إحصائيات الطابعات (ملون / أسود / ملصقات)",
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

# --- 1. الرئيسية واللوحة الشاملة ---
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
    st.metric("إجمالي الموظفين", total_records)
  with col2:
    st.metric("إجمالي الأجهزة", total_pcs)
  with col3:
    st.metric("إجمالي الشاشات", total_monitors)
  with col4:
    st.metric("إجمالي الطابعات", total_printers)
  with col5:
    st.metric("الأجهزة المعطلة", total_faults)

  st.info(
      "💡 يمكنك الانتقال إلى أي إحصائية تفصيلية عبر القائمة الجانبية لمعاينة"
      " التصنيفات بدقة."
  )

  if total_records > 0:
    st.markdown("### 📋 معاينة سريعة لأحدث السجلات")
    st.dataframe(df.tail(5), use_container_width=True)

# --- 2. تسجيل عهدة جديدة / رفع ملف ---
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
  st.subheader("الإدخال اليدوي مع القوائم والمحددات الجديدة")

  with st.form("manual_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
      # اختيار المنطقة (6 مناطق)
      regions = [
          "منطقة العاصمة التعليمية",
          "منطقة حولي التعليمية",
          "منطقة الفروانية التعليمية",
          "منطقة الأحمدي التعليمية",
          "منطقة الجهراء التعليمية",
          "منطقة مبارك الكبير التعليمية",
      ]
      region = st.selectbox("المنطقة", regions)
    with col2:
      building = st.text_input(
          "اسم المبنى", placeholder="أدخل اسم أو رقم المبنى"
      )
    with col3:
      # 11 دور + الدور الأرضي
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

    col4, col5, col6 = st.columns(3)
    with col4:
      department = st.text_input("الإدارة", placeholder="مثال: إدارة النظم الآلية")
    with col5:
      section = st.text_input("القسم", placeholder="التشغيل والدعم التقني")
    with col6:
      employee = st.text_input("اسم الموظف المسؤول")

    st.markdown(
        "#### تفاصيل الأجهزة، الشاشات، والطابعات (حسب الخيارات المحددة)"
    )
    col7, col8 = st.columns(2)
    with col7:
      # أنواع الأجهزة المطلوبة
      pc_options = [
          "غير موجود",
          "Lenovo M70q (Type B)",
          "Lenovo M70q (Type A)",
          "Lenovo M90t (Type C)",
          "laptop",
      ]
      pc_type = st.selectbox("نوع الجهاز (PC)", pc_options)

      # الشاشات (تظهر فقط إذا لم يكن الجهاز Laptop)
      if pc_type != "laptop":
        monitor_options = [
            "غير موجود",
            "Lenovo 24 inch",
            "Lenovo 27 inch",
        ]
        monitor_type = st.selectbox("مقاس / نوع الشاشة", monitor_options)
      else:
        monitor_type = "لابتوب (شاشة مدمجة)"
        st.info("تم تخطي اختيار الشاشة لأن الجهاز Laptop.")

      # موديلات الطابعات المطلوبة
      printer_options = [
          "غير موجود",
          "Canon MF463dw (Black)",
          "Canon MF754Cdw (Color)",
          "Label Printer",
      ]
      printer_model = st.selectbox("موديل الطابعة", printer_options)

      # تحديد نوع الطباعة تلقائياً بناءً على اختيار الطابعة
      if printer_model == "Canon MF463dw (Black)":
        printer_color_type = "أسود وأبيض"
      elif printer_model == "Canon MF754Cdw (Color)":
        printer_color_type = "ملون"
      elif printer_model == "Label Printer":
        printer_color_type = "ملصقات"
      else:
        printer_color_type = "غير محدد"

    with col8:
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

# --- 3. سجل الأصول والبحث المتقدم ---
elif page == "📋 سجل الأصول والبحث المتقدم":
  st.subheader("سجل الأصول والبحث الفوري (مرتب حسب المنطقة والمبنى والدور)")
  if len(df) > 0:
    search_query = st.text_input(
        "🔍 ابحث في السجلات (بالمنطقة، الاسم، السيريال، الإدارة، أو الدور)...",
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

# --- 4. تفاصيل إحصائيات الموظفين ---
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
  else:
    st.info("لا توجد بيانات كافية لعرض الإحصائيات.")

# --- 5. تفاصيل إحصائيات الأجهزة (PC) ---
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
    else:
      st.write("لا توجد أجهزة مسجلة.")
  else:
    st.info("لا توجد بيانات مسجلة.")

# --- 6. تفاصيل إحصائيات الشاشات ---
elif page == "🖥️ تفاصيل إحصائيات الشاشات":
  st.subheader("🖥️ تفصيل الشاشات حسب المقاسات")
  if total_records > 0:
    mon_df = df[
        (df["مقاس/نوع الشاشة"].astype(bool))
        & (~df["مقاس/نوع الشاشة"].isin(["غير موجود", "لابتوب (شاشة مدمجة)"]))
    ]
    st.metric("إجمالي الشاشات الخارجية", len(mon_df))

    if len(mon_df) > 0:
      mon_counts = mon_df["مقاس/نوع الشاشة"].value_counts().reset_index()
      mon_counts.columns = ["مقاس الشاشة", "العدد"]
      st.dataframe(mon_counts, use_container_width=True)
    else:
      st.write("لا توجد شاشات خارجية مسجلة.")
  else:
    st.info("لا توجد بيانات مسجلة.")

# --- 7. تفاصيل إحصائيات الطابعات ---
elif page == "🖨️ تفاصيل إحصائيات الطابعات (ملون / أسود / ملصقات)":
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
    else:
      st.write("لا توجد طابعات مسجلة.")
  else:
    st.info("لا توجد بيانات مسجلة.")

# --- 8. تفاصيل الأعطال التقنية ---
elif page == "⚠️ تفاصيل الأعطال التقنية":
  st.subheader("⚠️ متابعة الأعطال التقنية والأجهزة المعطلة")
  if total_records > 0:
    faults_df = df[df["حالة العطل"] != "سليم"]
    st.metric("إجمالي الأجهزة التي بها أعطال", len(faults_df))

    if len(faults_df) > 0:
      st.dataframe(
          faults_df[
              [
                  "المنطقة",
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
