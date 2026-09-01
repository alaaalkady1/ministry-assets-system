<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>لوحة التحكم - إدارة الأصول المالية</title>
    <style>
        :root {
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --text-color: #ffffff;
            --text-muted: #cbd5e1;
            --accent-blue: #3b82f6;
            --accent-hover: #2563eb;
            --border-color: #334155;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-color);
            display: flex;
            height: 100vh;
            overflow: hidden;
        }

        /* القائمة الجانبية أو الشريط الثابت للأزرار */
        .sidebar {
            width: 260px;
            background-color: var(--card-bg);
            border-left: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
            padding: 20px;
        }

        .logo {
            font-size: 20px;
            font-weight: bold;
            color: var(--text-color);
            margin-bottom: 30px;
            text-align: center;
        }

        .nav-links {
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 12px;
        }

        .nav-links li a {
            display: block;
            padding: 14px 18px;
            color: var(--text-muted);
            background-color: transparent;
            text-decoration: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 500;
            transition: all 0.3s ease;
            cursor: pointer;
        }

        .nav-links li a:hover {
            background-color: rgba(59, 130, 246, 0.1);
            color: var(--text-color);
        }

        /* التبويب النشط يتغير لونه إلى الأزرق ونصوص بيضاء واضحة */
        .nav-links li a.active {
            background-color: var(--accent-blue);
            color: var(--text-color);
            font-weight: bold;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
        }

        /* المحتوى الرئيسي */
        .main-content {
            flex: 1;
            padding: 30px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 25px;
        }

        .header-title {
            font-size: 24px;
            font-weight: bold;
            color: var(--text-color);
        }

        .cards-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
            gap: 20px;
        }

        .card {
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            padding: 25px;
            border-radius: 12px;
            text-align: center;
            transition: transform 0.2s ease, border-color 0.2s ease;
        }

        .card h3 {
            font-size: 18px;
            color: var(--text-muted);
            margin-bottom: 10px;
        }

        .card .number {
            font-size: 28px;
            font-weight: bold;
            color: var(--text-color);
        }

        /* جعل بطاقة الإحصائيات قابلة للضغط للانتقال للصفحة */
        .card.clickable-stat {
            cursor: pointer;
        }

        .card.clickable-stat:hover {
            border-color: var(--accent-blue);
            transform: translateY(-3px);
        }

        .page-section {
            display: none;
        }

        .page-section.active-section {
            display: block;
        }
    </style>
</head>
<body>

    <!-- الشريط الجانبي الثابت للأزرار في جميع الصفحات -->
    <div class="sidebar">
        <div class="logo">إدارة الأصول المالية</div>
        <ul class="nav-links">
            <li><a href="#" class="nav-btn active" onclick="switchPage('home', this)">الرئيسية</a></li>
            <li><a href="#" class="nav-btn" onclick="switchPage('statistics', this)">الإحصائيات</a></li>
            <li><a href="#" class="nav-btn" onclick="switchPage('assets', this)">الأصول</a></li>
            <li><a href="#" class="nav-btn" onclick="switchPage('reports', this)">التقارير</a></li>
            <li><a href="#" class="nav-btn" onclick="switchPage('settings', this)">الإعدادات</a></li>
        </ul>
    </div>

    <!-- محتوى الصفحات -->
    <div class="main-content">
        
        <!-- صفحة الرئيسية -->
        <div id="home" class="page-section active-section">
            <h2 class="header-title" style="margin-bottom: 20px;">الرئيسية</h2>
            <div class="cards-grid">
                <!-- بطاقة الإحصائيات تضغط عليها تنقلك لصفحة الإحصائيات مباشرة -->
                <div class="card clickable-stat" onclick="navigateToStat()">
                    <h3>إجمالي الإحصائيات</h3>
                    <div class="number">1,280</div>
                </div>
                <div class="card">
                    <h3>الأصول النشطة</h3>
                    <div class="number">940</div>
                </div>
                <div class="card">
                    <h3>قيد الصيانة</h3>
                    <div class="number">45</div>
                </div>
            </div>
        </div>

        <!-- صفحة الإحصائيات -->
        <div id="statistics" class="page-section">
            <h2 class="header-title">صفحة الإحصائيات الشاملة</h2>
            <p style="color: var(--text-muted); margin-top: 10px; font-size: 16px;">هنا يتم عرض كافة الأرقام والبيانات الإحصائية الخاصة بالنظام.</p>
        </div>

        <!-- صفحة الأصول -->
        <div id="assets" class="page-section">
            <h2 class="header-title">إدارة الأصول</h2>
            <p style="color: var(--text-muted); margin-top: 10px; font-size: 16px;">قائمة الأصول والوحدات المتاحة.</p>
        </div>

        <!-- صفحة التقارير -->
        <div id="reports" class="page-section">
            <h2 class="header-title">التقارير المالية</h2>
            <p style="color: var(--text-muted); margin-top: 10px; font-size: 16px;">استخراج وعرض التقارير التفصيلية.</p>
        </div>

        <!-- صفحة الإعدادات -->
        <div id="settings" class="page-section">
            <h2 class="header-title">الإعدادات</h2>
            <p style="color: var(--text-muted); margin-top: 10px; font-size: 16px;">تخصيص إعدادات النظام.</p>
        </div>

    </div>

    <script>
        // دالة التنقل بين التبويبات وتغيير اللون (Active State)
        function switchPage(pageId, element) {
            // إخفاء كل الصفحات
            const sections = document.querySelectorAll('.page-section');
            sections.forEach(sec => sec.classList.remove('active-section'));

            // إظهار الصفحة المطلوبة
            document.getElementById(pageId).classList.add('active-section');

            // إزالة التحديد عن كل الأزرار
            const buttons = document.querySelectorAll('.nav-btn');
            buttons.buttonList = buttons.forEach(btn => btn.classList.remove('active'));

            // إضافة التحديد للزر المضغط
            element.classList.add('active');
        }

        // دالة الضغط على بطاقة الإحصائيات لتنقلك مباشرة لصفحة الإحصائيات وتفعل زرها
        function navigateToStat() {
            const statBtn = document.querySelector('.nav-links li:nth-child(2) a');
            switchPage('statistics', statBtn);
        }
    </script>
</body>
</html>
