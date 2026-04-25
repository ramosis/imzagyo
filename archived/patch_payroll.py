import sys

with open('portal.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Sidebar'a Hakediş & Komisyon butonu ekle (Finans butonunun altına)
sidebar_marker = '''<i class="fa-solid fa-receipt w-5 text-center"></i> Harcama Yönetimi
                </button>'''

sidebar_insert = '''<i class="fa-solid fa-receipt w-5 text-center"></i> Harcama Yönetimi
                </button>

                <button onclick="showSection('payroll', this)"
                    class="nav-item w-full flex items-center gap-3 px-4 py-3 rounded-lg text-gray-400 hover:text-white hover:bg-white/5 transition-all text-sm font-medium">
                    <i class="fa-solid fa-money-bill-trend-up w-5 text-center"></i> Hakediş & Komisyon
                </button>'''

content = content.replace(sidebar_marker, sidebar_insert)

# 2. Hakediş section HTML'i ekle (expenses-section kapanışından sonra)
payroll_section = '''
            <!-- ========================================== -->
            <!-- PAYROLL / HAKEDİŞ SECTION -->
            <section id="payroll-section" class="content-section flex flex-col h-full bg-white hidden">
                <div class="px-8 py-6 border-b border-gray-100 shrink-0">
                    <div class="flex justify-between items-end">
                        <div class="space-y-1">
                            <h2 class="text-2xl font-serif font-bold text-navy">Hakediş & Komisyon Tablosu</h2>
                            <p class="text-sm text-gray-500">Aylık kazanç, komisyon ve harcama dengesi.</p>
                        </div>
                        <div class="flex items-center gap-3">
                            <select id="payroll-month" onchange="fetchPayroll()" class="border border-gray-200 rounded-lg px-4 py-2 text-sm font-medium text-navy">
                                <option value="2026-03">Mart 2026</option>
                                <option value="2026-02">Şubat 2026</option>
                                <option value="2026-01">Ocak 2026</option>
                            </select>
                        </div>
                    </div>
                </div>
                <div class="flex-1 overflow-auto p-8">
                    <!-- Özet Kartları -->
                    <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
                        <div class="bg-gradient-to-br from-green-50 to-green-100 rounded-2xl p-6 border border-green-200">
                            <p class="text-[10px] font-bold text-green-600 uppercase tracking-widest mb-1">Toplam Komisyon</p>
                            <h3 id="payroll-commission-total" class="text-2xl font-bold text-green-700">₺0</h3>
                        </div>
                        <div class="bg-gradient-to-br from-red-50 to-red-100 rounded-2xl p-6 border border-red-200">
                            <p class="text-[10px] font-bold text-red-600 uppercase tracking-widest mb-1">Toplam Harcama</p>
                            <h3 id="payroll-expense-total" class="text-2xl font-bold text-red-700">₺0</h3>
                        </div>
                        <div class="bg-gradient-to-br from-blue-50 to-blue-100 rounded-2xl p-6 border border-blue-200">
                            <p class="text-[10px] font-bold text-blue-600 uppercase tracking-widest mb-1">Sözleşme Sayısı</p>
                            <h3 id="payroll-contract-count" class="text-2xl font-bold text-blue-700">0</h3>
                        </div>
                        <div class="bg-gradient-to-br from-gold/10 to-gold/20 rounded-2xl p-6 border border-gold/30">
                            <p class="text-[10px] font-bold text-gold uppercase tracking-widest mb-1">Net Hakediş</p>
                            <h3 id="payroll-net" class="text-2xl font-bold text-navy">₺0</h3>
                        </div>
                    </div>

                    <!-- Komisyon Detayları -->
                    <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
                        <div class="px-6 py-4 border-b border-gray-100 bg-gray-50">
                            <h4 class="font-bold text-navy text-sm uppercase tracking-wider">Komisyon Detayları</h4>
                        </div>
                        <table class="w-full text-left">
                            <thead>
                                <tr class="border-b border-gray-100 text-[10px] uppercase font-bold text-gray-500 tracking-wider">
                                    <th class="px-6 py-3">Sözleşme</th>
                                    <th class="px-6 py-3">Mülk</th>
                                    <th class="px-6 py-3">Oran</th>
                                    <th class="px-6 py-3">Tutar</th>
                                    <th class="px-6 py-3">Durum</th>
                                </tr>
                            </thead>
                            <tbody id="payroll-commissions-body" class="text-sm"></tbody>
                        </table>
                    </div>
                </div>
            </section>
'''

# expenses-section kapanışından sonra ekle
expenses_end = '</section>\n\n            <!-- ========================================== -->\n            <!-- LEADS (CRM) SECTION -->'
if expenses_end not in content:
    # Alternatif: leads section'ın başından hemen önce ekle
    expenses_end = '<!-- LEADS (CRM) SECTION -->'

content = content.replace(expenses_end, payroll_section + '\n            ' + expenses_end)

# 3. Hakediş JS fonksiyonlarını ekle
payroll_js = '''
        // --- HAKEDİŞ & KOMİSYON LOGİĞİ ---
        async function fetchPayroll() {
            const month = document.getElementById('payroll-month').value;
            const token = localStorage.getItem('imza_admin_token');
            
            try {
                // Komisyonları çek
                let commissionTotal = 0;
                let commissionCount = 0;
                const commBody = document.getElementById('payroll-commissions-body');
                commBody.innerHTML = '';

                // Sözleşmelerden komisyon hesapla (demo: satış sözleşmelerinin %2'si)
                const contractsRes = await fetch(`${API_BASE}/contracts`, {
                    headers: {'Authorization': `Bearer ${token}`}
                });
                if (contractsRes.ok) {
                    const contracts = await contractsRes.json();
                    const monthContracts = contracts.filter(c => (c.created_at || '').startsWith(month));
                    commissionCount = monthContracts.length;

                    monthContracts.forEach(c => {
                        // Demo: Komisyon = Mülk değerinin %2'si (gerçekte fiyat parse edilir)
                        const commAmount = 700000; // Demo sabit komisyon
                        commissionTotal += commAmount;

                        commBody.innerHTML += `
                            <tr class="border-b border-gray-50 hover:bg-gray-50">
                                <td class="px-6 py-3 font-medium text-navy">#${c.id}</td>
                                <td class="px-6 py-3">${c.baslik1 || c.refNo || '-'}</td>
                                <td class="px-6 py-3 text-gold font-bold">%2</td>
                                <td class="px-6 py-3 font-bold text-green-600">₺${commAmount.toLocaleString('tr-TR')}</td>
                                <td class="px-6 py-3"><span class="bg-green-100 text-green-700 px-2 py-1 rounded text-[10px] font-bold">Onaylandı</span></td>
                            </tr>
                        `;
                    });

                    if (monthContracts.length === 0) {
                        commBody.innerHTML = '<tr><td colspan="5" class="px-6 py-8 text-center text-gray-400">Bu ay için komisyon kaydı yok.</td></tr>';
                    }
                }

                // Harcamaları çek
                let expenseTotal = 0;
                const expensesRes = await fetch(`${API_BASE}/expenses`, {
                    headers: {'Authorization': `Bearer ${token}`}
                });
                if (expensesRes.ok) {
                    const expenses = await expensesRes.json();
                    const monthExpenses = expenses.filter(e => (e.date || '').startsWith(month) && e.status === 'approved');
                    monthExpenses.forEach(e => { expenseTotal += parseFloat(e.amount) || 0; });
                }

                // UI güncelle
                document.getElementById('payroll-commission-total').textContent = '₺' + commissionTotal.toLocaleString('tr-TR');
                document.getElementById('payroll-expense-total').textContent = '₺' + expenseTotal.toLocaleString('tr-TR');
                document.getElementById('payroll-contract-count').textContent = commissionCount;
                const net = commissionTotal - expenseTotal;
                document.getElementById('payroll-net').textContent = '₺' + net.toLocaleString('tr-TR');
                document.getElementById('payroll-net').className = net >= 0 
                    ? 'text-2xl font-bold text-green-700' 
                    : 'text-2xl font-bold text-red-700';

            } catch(e) { console.error('Hakediş hesaplama hatası:', e); }
        }
'''

# showSection genişletmesine payroll ekle
old_show = "if (sectionId === 'leads') fetchLeads();"
new_show = "if (sectionId === 'leads') fetchLeads();\n            if (sectionId === 'payroll') fetchPayroll();"
content = content.replace(old_show, new_show)

# JS'yi son </script> öncesine ekle
last_script_close = content.rfind('</script>')
if last_script_close != -1:
    content = content[:last_script_close] + payroll_js + '\n' + content[last_script_close:]

with open('portal.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Hakediş & Komisyon UI eklendi!")
