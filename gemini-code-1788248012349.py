import streamlit as st

# إعداد صفحة ستريمليت لتكون بعرض واسع واتجاه من اليمين لليسار (RTL)
st.set_page_config(
    page_title="لوحة التحكم - إدارة الأصول المالية",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تخصيص التصميم والخطوط والألوان عبر CSS لتتناسب مع طلبك (خطوط بيضاء وأزرار تفاعلية)
st.markdown("""
    <style>
        /* اتجاه الموقع من اليمين لليسار ودعم اللغة العربية */
        html, body, [class*="css"] {
            direction: rtl;
            text-align: right;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        /* تكبير الخطوط وجعلها بيضاء واضحة */
        h1, h2, h3, p, span, div, label {
            color: #ffffff !important;
        }

        /* تنسيق الكروت والإحصائيات */
        .metric-card {
            background-color: #1e293b;
            border: 1px solid #334155;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s;
        }
        .metric-card:hover {
            border-color: #3b82f6;
            transform: translateY(-3px);
        }
    </style>
""", unsafe_allow_html=True)

# إدارة حالة التنقل بين الصفحات في الجلسة (Session State)
if 'current_page' not in st.session_state:
    st.session_state.current_page = "الرئيسية"

# القائمة الجانبية (الأزرار الثابتة في جميع الصفحات)
st.sidebar.markdown("<h2 style='text-align: center;'>إدارة الأصول المالية</h2>", unsafe_allow_html=True)
st.sidebar.markdown("---")

# استخدام أزرار القائمة الجانبية للتنقل
if st.sidebar.button("الرئيسية", use_container_width=True):
    st.session_state.current_page = "الرئيسية"
if st.sidebar.button("الإحصائيات", use_container_width=True):
    st.session_state.current_page = "الإحصائيات"
if st.sidebar.button("الأصول", use_container_width=True):
    st.session_state.current_page = "الأصول"
if st.sidebar.button("التقارير", use_container_width=True):
    st.session_state.current_page = "التقارير"
if st.sidebar.button("الإعدادات", use_container_width=True):
    st.session_state.current_page = "الإعدادات"

# عرض المحتوى بناءً على الصفحة المختار
if st.session_state.current_page == "الرئيسية":
    st.markdown("<h2>الرئيسية</h2>", unsafe_allow_html=True)
    st.write("")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # جعل بطاقة الإحصائيات قابلة للضغط للانتقال المباشر لصفحة الإحصائيات
        if st.button("📊 إجمالي الإحصائيات\n\n 1,280", use_container_width=True):
            st.session_state.current_page = "الإحصائيات"
            st.rerun()
            
    with col2:
        st.markdown("""
            <div class="metric-card">
                <h3>الأصول النشطة</h3>
                <h2 style="color: #3b82f6 !important;">940</h2>
            </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
            <div class="metric-card">
                <h3>قيد الصيانة</h3>
                <h2 style="color: #ef4444 !important;">45</h2>
            </div>
        """, unsafe_allow_html=True)

elif st.session_state.current_page == "الإحصائيات":
    st.markdown("<h2>صفحة الإحصائيات الشاملة</h2>", unsafe_allow_html=True)
    st.write("هنا يتم عرض كافة الأرقام والبيانات الإحصائية الخاصة بالنظام بشكل تفصيلي.")

elif st.session_state.current_page == "الأصول":
    st.markdown("<h2>إدارة الأصول</h2>", unsafe_allow_html=True)
    st.write("قائمة الأصول والوحدات المتاحة في النظام.")

elif st.session_state.current_page == "Reports" or st.session_state.current_page == "التقارير":
    st.markdown("<h2>التقارير المالية</h2>", unsafe_allow_html=True)
    st.write("استخراج وعرض التقارير التفصيلية.")

elif st.session_state.current_page == "الإعدادات":
    st.markdown("<h2>الإعدادات</h2>", unsafe_allow_html=True)
    st.write("تخصيص إعدادات النظام وتفضيلات الحساب.")
