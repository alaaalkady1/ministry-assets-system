<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>نظام حصر الأصول - وزارة التربية</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700&display=swap');
        body { font-family: 'Tajawal', sans-serif; background-color: #f5f7fa; }
        .tab-active { border-bottom: 3px solid #1e40af; font-weight: bold; color: #1e40af; }
        .dashboard-card:hover { transform: translateY(-3px); transition: transform 0.3s ease; }
        .fade-in { animation: fadeIn 0.4s ease-in-out; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(5px); } to { opacity: 1; transform: translateY(0); } }
    </style>
</head>
<body class="bg-gray-50 text-gray-800">
    <div class="container mx-auto px-4 py-8 max-w-7xl">
        <!-- Header -->
        <header class="bg-gradient-to-r from-emerald-800 to-teal-900 text-white rounded-2xl shadow-xl p-6 mb-8 border-b-4 border-amber-500">
            <div class="flex flex-col md:flex-row justify-between items-center">
                <div>
                    <h1 class="text-3xl font-extrabold tracking-wide">نظام حصر الأصول والدعم التقني</h1>
                    <p class="mt-2 text-emerald-100 opacity-90 font-medium">وزارة التربية - إدارة النظم الآلية والبنية التحتية (قسم التشغيل والدعم التقني)</p>
                </div>
                <div class="mt-4 md:mt-0 flex space-x-3 space-x-reverse">
                    <button id="clear-all" class="bg-red-600 hover:bg-red-700 text-white px-4 py-2.5 rounded-xl font-medium transition shadow flex items-center">
                        <i class="fas fa-trash-alt ml-2"></i> مسح كافة السجلات
                    </button>
                </div>
            </div>
        </header>

        <!-- Navigation Tabs -->
        <div class="bg-white rounded-2xl shadow-md mb-8 border border-gray-100">
            <div class="flex border-b overflow-x-auto">
                <button id="add-tab" class="tab-btn py-4 px-6 text-lg tab-active whitespace-nowrap flex items-center"><i class="fas fa-plus-circle ml-2"></i> تسجیل عهدة جديدة</button>
                <button id="dashboard-tab" class="tab-btn py-4 px-6 text-lg whitespace-nowrap flex items-center"><i class="fas fa-chart-pie ml-2"></i> لوحة الإحصائيات</button>
                <button id="records-tab" class="tab-btn py-4 px-6 text-lg whitespace-nowrap flex items-center"><i class="fas fa-table ml-2"></i> سجل الأصول (الإجمالي)</button>
            </div>
        </div>

        <!-- Add Asset Section -->
        <section id="add-section" class="tab-content fade-in">
            <div class="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
                <h2 class="text-2xl font-bold text-gray-800 mb-6 pb-3 border-b flex items-center">
                    <i class="fas fa-laptop-code text-emerald-700 ml-3"></i> نموذج إدخال عهدة جهاز وملاحقه
                </h2>
                
                <form id="asset-form">
                    <!-- Location & User Details -->
                    <h3 class="text-lg font-semibold text-emerald-800 mb-4 bg-emerald-50 p-3 rounded-lg border-r-4 border-emerald-600">بيانات الموقع والموظف</h3>
                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                        <div>
                            <label class="block text-gray-700 font-medium mb-2">اسم المبنى</label>
                            <input type="text" id="building-name" value="ديوان الوزارة" class="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-600 focus:outline-none" required>
                        </div>
                        <div>
                            <label class="block text-gray-700 font-medium mb-2">الدور</label>
                            <select id="floor" class="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-600 focus:outline-none">
                                <option value="الدور الأرضي">الدور الأرضي</option>
                                <option value="الأول">الأول</option>
                                <option value="الثاني">الثاني</option>
                                <option value="الثالث">الثالث</option>
                                <option value="الرابع">الرابع</option>
                                <option value="الخامس">الخامس</option>
                                <option value="السادس">السادس</option>
                                <option value="السابع">السابع</option>
                                <option value="الثامن">الثامن</option>
                                <option value="التاسع">التاسع</option>
                                <option value="العاشر">العاشر</option>
                                <option value="الحادي عشر">الحادي عشر</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-gray-700 font-medium mb-2">الإدارة</label>
                            <input type="text" id="department" class="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-600 focus:outline-none" placeholder="مثال: إدارة النظم الآلية" required>
                        </div>
                        <div>
                            <label class="block text-gray-700 font-medium mb-2">القسم</label>
                            <input type="text" id="section" class="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-600 focus:outline-none" placeholder="مثال: التشغيل والدعم التقني">
                        </div>
                        <div class="md:col-span-2">
                            <label class="block text-gray-700 font-medium mb-2">اسم الموظف المسؤول</label>
                            <input type="text" id="employee-name" class="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-600 focus:outline-none" placeholder="الاسم الثلاثي" required>
                        </div>
                    </div>
                    
                    <!-- Hardware Details -->
                    <h3 class="text-lg font-semibold text-emerald-800 mb-4 bg-emerald-50 p-3 rounded-lg border-r-4 border-emerald-600">تفاصيل العهدة والأرقام التسلسلية (Serial Numbers)</h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8 p-4 bg-gray-50 rounded-xl border">
                        <!-- PC -->
                        <div>
                            <label class="block text-gray-700 font-medium mb-2">نوع وموديل الجهاز (PC)</label>
                            <input type="text" id="pc-type" class="w-full p-3 bg-white border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-600 focus:outline-none" placeholder="مثال: Dell OptiPlex 7090">
                        </div>
                        <div>
                            <label class="block text-gray-700 font-medium mb-2">سيريال نمبر الجهاز (PC S/N)</label>
                            <input type="text" id="pc-serial" class="w-full p-3 bg-white border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-600 focus:outline-none" placeholder="S/N">
                        </div>
                        <!-- Monitor -->
                        <div>
                            <label class="block text-gray-700 font-medium mb-2">نوع وحجم الشاشة</label>
                            <input type="text" id="monitor-type" class="w-full p-3 bg-white border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-600 focus:outline-none" placeholder="مثال: Dell 24 inch">
                        </div>
                        <div>
                            <label class="block text-gray-700 font-medium mb-2">سيريال نمبر الشاشة (Monitor S/N)</label>
                            <input type="text" id="monitor-serial" class="w-full p-3 bg-white border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-600 focus:outline-none" placeholder="S/N">
                        </div>
                        <!-- Printer -->
                        <div>
                            <label class="block text-gray-700 font-medium mb-2">نوع الطابعة</label>
                            <input type="text" id="printer-type" class="w-full p-3 bg-white border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-600 focus:outline-none" placeholder="مثال: HP LaserJet Pro">
                        </div>
                        <div>
                            <label class="block text-gray-700 font-medium mb-2">سيريال نمبر الطابعة (Printer S/N)</label>
                            <input type="text" id="printer-serial" class="w-full p-3 bg-white border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-600 focus:outline-none" placeholder="S/N">
                        </div>
                    </div>

                    <!-- Notes -->
                    <div class="mb-6">
                        <label class="block text-gray-700 font-medium mb-2">ملاحظات إضافية</label>
                        <textarea id="notes" class="w-full p-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-emerald-600 focus:outline-none" rows="2" placeholder="أي ملاحظات تخص حالة الجهاز أو الصيانة..."></textarea>
                    </div>
                    
                    <div class="flex justify-end">
                        <button type="submit" class="bg-emerald-700 hover:bg-emerald-800 text-white px-8 py-3.5 rounded-xl font-bold flex items-center shadow-lg transition transform hover:-translate-y-0.5">
                            <i class="fas fa-save ml-2"></i> حفظ في سجل الأصول
                        </button>
                    </div>
                </form>
            </div>
        </section>

        <!-- Dashboard Section -->
        <section id="dashboard-section" class="tab-content hidden fade-in">
            <div class="bg-white rounded-2xl shadow-xl p-8 border border-gray-100 mb-8">
                <h2 class="text-2xl font-bold text-gray-800 mb-6 pb-3 border-b flex items-center">
                    <i class="fas fa-chart-bar text-emerald-700 ml-3"></i> مؤشرات وإحصائيات الحصر الشاملة
                </h2>
                
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    <div class="dashboard-card bg-gradient-to-br from-blue-600 to-indigo-700 text-white rounded-2xl shadow-lg p-6">
                        <div class="flex justify-between items-center">
                            <div>
                                <p class="text-blue-100 font-medium">إجمالي الموظفين المسجلين</p>
                                <p id="stat-records" class="text-4xl font-extrabold mt-2">0</p>
                            </div>
                            <i class="fas fa-users text-4xl text-blue-200 opacity-80"></i>
                        </div>
                    </div>
                    
                    <div class="dashboard-card bg-gradient-to-br from-emerald-600 to-teal-700 text-white rounded-2xl shadow-lg p-6">
                        <div class="flex justify-between items-center">
                            <div>
                                <p class="text-emerald-100 font-medium">إجمالي الأجهزة (PC)</p>
                                <p id="stat-pcs" class="text-4xl font-extrabold mt-2">0</p>
                            </div>
                            <i class="fas fa-desktop text-4xl text-emerald-200 opacity-80"></i>
                        </div>
                    </div>
                    
                    <div class="dashboard-card bg-gradient-to-br from-purple-600 to-pink-700 text-white rounded-2xl shadow-lg p-6">
                        <div class="flex justify-between items-center">
                            <div>
                                <p class="text-purple-100 font-medium">إجمالي الشاشات</p>
                                <p id="stat-monitors" class="text-4xl font-extrabold mt-2">0</p>
                            </div>
                            <i class="fas fa-tv text-4xl text-purple-200 opacity-80"></i>
                        </div>
                    </div>
                    
                    <div class="dashboard-card bg-gradient-to-br from-amber-600 to-orange-700 text-white rounded-2xl shadow-lg p-6">
                        <div class="flex justify-between items-center">
                            <div>
                                <p class="text-amber-100 font-medium">إجمالي الطابعات</p>
                                <p id="stat-printers" class="text-4xl font-extrabold mt-2">0</p>
                            </div>
                            <i class="fas fa-print text-4xl text-amber-200 opacity-80"></i>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Records/Inventory Table Section -->
        <section id="records-section" class="tab-content hidden fade-in">
            <div class="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
                <div class="flex flex-col md:flex-row justify-between items-center mb-6 pb-3 border-b gap-4">
                    <h2 class="text-2xl font-bold text-gray-800 flex items-center">
                        <i class="fas database text-emerald-700 ml-3"></i> سجل عهد ديوان الوزارة والأجهزة
                    </h2>
                    <button id="export-csv" class="bg-emerald-600 hover:bg-emerald-700 text-white px-5 py-2.5 rounded-xl font-medium shadow transition flex items-center">
                        <i class="fas fa-file-excel ml-2"></i> تصدير البيانات إلى Excel / CSV
                    </button>
                </div>
                
                <div class="overflow-x-auto">
                    <table class="w-full border-collapse text-sm">
                        <thead class="bg-gray-100 text-gray-700">
                            <tr>
                                <th class="border p-3">م</th>
                                <th class="border p-3">المبنى والدور</th>
                                <th class="border p-3">الإدارة / القسم</th>
                                <th class="border p-3">اسم الموظف</th>
                                <th class="border p-3">الجهاز (PC & S/N)</th>
                                <th class="border p-3">الشاشة (Monitor & S/N)</th>
                                <th class="border p-3">الطابعة (Printer & S/N)</th>
                                <th class="border p-3">ملاحظات</th>
                                <th class="border p-3 text-center">إجراءات</th>
                            </tr>
                        </thead>
                        <tbody id="inventory-list">
                            <tr>
                                <td colspan="9" class="border p-8 text-center text-gray-500 font-medium">لا توجد أجهزة محفوظة حتى الآن</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </section>
    </div>

    <!-- Script for Application Logic -->
    <script>
        let assets = [];
        try {
            const stored = localStorage.getItem('ministry_assets_v2');
            if (stored) assets = JSON.parse(stored);
        } catch (error) {
            assets = [];
        }

        const tabs = {
            'add': document.getElementById('add-section'),
            'dashboard': document.getElementById('dashboard-section'),
            'records': document.getElementById('records-section')
        };
        const tabBtns = document.querySelectorAll('.tab-btn');

        function switchTab(tabId) {
            Object.values(tabs).forEach(section => section.classList.add('hidden'));
            tabBtns.forEach(btn => btn.classList.remove('tab-active'));
            
            tabs[tabId].classList.remove('hidden');
            document.getElementById(`${tabId}-tab`).classList.add('tab-active');

            if (tabId === 'dashboard') updateDashboard();
            if (tabId === 'records') renderTable();
        }

        document.getElementById('add-tab').addEventListener('click', () => switchTab('add'));
        document.getElementById('dashboard-tab').addEventListener('click', () => switchTab('dashboard'));
        document.getElementById('records-tab').addEventListener('click', () => switchTab('records'));

        document.getElementById('asset-form').addEventListener('submit', function(e) {
            e.preventDefault();
            
            const newAsset = {
                id: Date.now(),
                building: document.getElementById('building-name').value,
                floor: document.getElementById('floor').value,
                department: document.getElementById('department').value,
                section: document.getElementById('section').value,
                employee: document.getElementById('employee-name').value,
                pcType: document.getElementById('pc-type').value,
                pcSerial: document.getElementById('pc-serial').value,
                monitorType: document.getElementById('monitor-type').value,
                monitorSerial: document.getElementById('monitor-serial').value,
                printerType: document.getElementById('printer-type').value,
                printerSerial: document.getElementById('printer-serial').value,
                notes: document.getElementById('notes').value
            };

            assets.push(newAsset);
            localStorage.setItem('ministry_assets_v2', JSON.stringify(assets));
            
            showNotification('تم تسجيل العهدة بنجاح!', 'success');
            
            // Clear input fields for next entry (keeping building/floor for fast entry)
            document.getElementById('employee-name').value = '';
            document.getElementById('department').value = '';
            document.getElementById('section').value = '';
            document.getElementById('pc-type').value = '';
            document.getElementById('pc-serial').value = '';
            document.getElementById('monitor-type').value = '';
            document.getElementById('monitor-serial').value = '';
            document.getElementById('printer-type').value = '';
            document.getElementById('printer-serial').value = '';
            document.getElementById('notes').value = '';
        });

        function renderTable() {
            const list = document.getElementById('inventory-list');
            if (assets.length === 0) {
                list.innerHTML = '<tr><td colspan="9" class="border p-8 text-center text-gray-500 font-medium">لا توجد أجهزة محفوظة حتى الآن</td></tr>';
                return;
            }
            
            list.innerHTML = '';
            assets.forEach((asset, index) => {
                const tr = document.createElement('tr');
                tr.className = 'hover:bg-gray-50 transition';
                tr.innerHTML = `
                    <td class="border p-3 text-center font-bold">${index + 1}</td>
                    <td class="border p-3">${asset.building}<br><span class="text-xs text-blue-600 font-semibold">${asset.floor}</span></td>
                    <td class="border p-3">${asset.department}<br><span class="text-xs text-gray-500">${asset.section || '-'}</span></td>
                    <td class="border p-3 font-bold text-gray-900">${asset.employee}</td>
                    <td class="border p-3">${asset.pcType || '-'}<br><span class="text-xs font-mono text-gray-500">${asset.pcSerial || ''}</span></td>
                    <td class="border p-3">${asset.monitorType || '-'}<br><span class="text-xs font-mono text-gray-500">${asset.monitorSerial || ''}</span></td>
                    <td class="border p-3">${asset.printerType || '-'}<br><span class="text-xs font-mono text-gray-500">${asset.printerSerial || ''}</span></td>
                    <td class="border p-3 text-gray-600 text-xs">${asset.notes || '-'}</td>
                    <td class="border p-3 text-center">
                        <button onclick="deleteAsset(${index})" class="text-red-600 hover:text-red-900 bg-red-50 hover:bg-red-100 p-2 rounded-lg transition" title="حذف السجل">
                            <i class="fas fa-trash-alt"></i>
                        </button>
                    </td>
                `;
                list.appendChild(tr);
            });
        }

        function updateDashboard() {
            document.getElementById('stat-records').textContent = assets.length;
            
            let pcs = 0, monitors = 0, printers = 0;
            assets.forEach(a => {
                if (a.pcType || a.pcSerial) pcs++;
                if (a.monitorType || a.monitorSerial) monitors++;
                if (a.printerType || a.printerSerial) printers++;
            });
            
            document.getElementById('stat-pcs').textContent = pcs;
            document.getElementById('stat-monitors').textContent = monitors;
            document.getElementById('stat-printers').textContent = printers;
        }

        window.deleteAsset = function(index) {
            if (confirm('هل أنت متأكد من رغبتك في حذف هذا السجل نهائياً؟')) {
                assets.splice(index, 1);
                localStorage.setItem('ministry_assets_v2', JSON.stringify(assets));
                renderTable();
                updateDashboard();
                showNotification('تم حذف السجل بنجاح', 'success');
            }
        };

        document.getElementById('clear-all').addEventListener('click', () => {
            if (confirm('تحذير خطير: سيتم مسح كافة سجلات الأصول نهائياً من الذاكرة المحلية. هل أنت متأكد؟')) {
                assets = [];
                localStorage.setItem('ministry_assets_v2', JSON.stringify(assets));
                renderTable();
                updateDashboard();
                showNotification('تم مسح جميع البيانات بنجاح', 'success');
            }
        });

        document.getElementById('export-csv').addEventListener('click', () => {
            if (assets.length === 0) return showNotification('لا توجد بيانات متاحة للتصدير!', 'error');
            
            let csvContent = "\uFEFFم,اسم المبنى,الدور,الإدارة,القسم,اسم الموظف,نوع الجهاز,سيريال الجهاز,نوع الشاشة,سيريال الشاشة,نوع الطابعة,سيريال الطابعة,ملاحظات\n";
            assets.forEach((a, i) => {
                csvContent += `${i+1},"${a.building}","${a.floor}","${a.department}","${a.section}","${a.employee}","${a.pcType}","${a.pcSerial}","${a.monitorType}","${a.monitorSerial}","${a.printerType}","${a.printerSerial}","${a.notes}"\n`;
            });
            
            const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
            const link = document.createElement("a");
            link.href = URL.createObjectURL(blob);
            link.download = "حصر_عهد_وزارة_التربية.csv";
            link.click();
        });

        function showNotification(message, type = 'info') {
            const notification = document.createElement('div');
            notification.className = `fixed top-6 right-6 p-4 rounded-xl shadow-2xl text-white z-50 fade-in flex items-center ${type === 'success' ? 'bg-emerald-600' : 'bg-red-600'}`;
            notification.innerHTML = `<i class="fas ${type === 'success' ? 'fa-check-circle' : 'fa-exclamation-circle'} ml-3 text-lg"></i><span class="font-medium">${message}</span>`;
            document.body.appendChild(notification);
            setTimeout(() => notification.remove(), 3000);
        }
    </script>
</body>
</html>
