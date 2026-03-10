import re

with open('portal.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. ADD MISSING JS FUNCTIONS
missing_js = """
        // ==========================================
        // LEADS (MÜŞTERİ ADAYLARI) JS MANTIĞI
        // ==========================================
        async function fetchLeads() {
            const token = localStorage.getItem('imza_admin_token');
            if(!token) return;
            try {
                const res = await fetch(`${API_BASE}/leads`, {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                if (res.ok) {
                    const data = await res.json();
                    const tbody = document.getElementById('leads-table-body');
                    if (!tbody) return;
                    tbody.innerHTML = '';
                    if (data.length === 0) {
                        tbody.innerHTML = '<tr><td colspan="6" class="p-8 text-center text-gray-400">Henüz müşteri adayı bulunmuyor.</td></tr>';
                        return;
                    }
                    data.forEach(l => {
                        const statusColor = l.status === 'new' ? 'bg-blue-100 text-blue-700' : 'bg-gray-100 text-gray-700';
                        const tr = document.createElement('tr');
                        tr.className = 'border-b border-gray-100/50 hover:bg-gray-50';
                        tr.innerHTML = `
                            <td class="px-6 py-4 font-bold text-navy">${l.score || '0'}</td>
                            <td class="px-6 py-4 font-medium text-navy">${l.name}</td>
                            <td class="px-6 py-4 text-gray-500">${l.phone || l.email || '-'}</td>
                            <td class="px-6 py-4 text-gray-500 max-w-[200px] truncate" title="${l.property_interest}">${l.property_interest || '-'}</td>
                            <td class="px-6 py-4"><span class="${statusColor} px-2 py-1 rounded text-xs font-bold uppercase">${l.status}</span></td>
                            <td class="px-6 py-4 text-right">
                                <button class="text-navy hover:text-gold transition-colors p-2"><i class="fa-solid fa-eye"></i></button>
                            </td>
                        `;
                        tbody.appendChild(tr);
                    });
                }
            } catch (err) { console.error(err); }
        }

        // ==========================================
        // EXPENSES (HARCAMALAR) JS MANTIĞI
        // ==========================================
        async function fetchExpenses() {
            const token = localStorage.getItem('imza_admin_token');
            if(!token) return;
            try {
                const res = await fetch(`${API_BASE}/expenses`, {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                if (res.ok) {
                    const data = await res.json();
                    const tbody = document.getElementById('expenses-table-body');
                    if (!tbody) return;
                    tbody.innerHTML = '';
                    if (data.length === 0) {
                        tbody.innerHTML = '<tr><td colspan="7" class="p-8 text-center text-gray-400">Henüz harcama kaydı bulunmuyor.</td></tr>';
                        return;
                    }
                    data.forEach(e => {
                        const statusColor = e.status === 'approved' ? 'bg-green-100 text-green-700' : (e.status === 'pending' ? 'bg-yellow-100 text-yellow-700' : 'bg-red-100 text-red-700');
                        const tr = document.createElement('tr');
                        tr.className = 'border-b border-gray-100/50 hover:bg-gray-50';
                        tr.innerHTML = `
                            <td class="px-6 py-4 font-medium text-navy">#${e.id}</td>
                            <td class="px-6 py-4 font-medium text-navy">${e.title}</td>
                            <td class="px-6 py-4 text-gray-500">${e.expense_type}</td>
                            <td class="px-6 py-4 font-bold text-red-600">${e.amount.toLocaleString('tr-TR')} ₺</td>
                            <td class="px-6 py-4 text-gray-500">${e.created_at ? e.created_at.substring(0,10) : '-'}</td>
                            <td class="px-6 py-4"><span class="${statusColor} px-2 py-1 rounded text-xs font-bold uppercase">${e.status}</span></td>
                            <td class="px-6 py-4 text-right">
                                <button class="text-navy hover:text-gold transition-colors p-2"><i class="fa-solid fa-pen"></i></button>
                            </td>
                        `;
                        tbody.appendChild(tr);
                    });
                }
            } catch (err) { console.error(err); }
        }

        // ==========================================
        // PAYROLL (HAKEDİŞ) JS MANTIĞI
        // ==========================================
        async function fetchPayroll() {
            // Şimdilik sadece dummy data veya API entegrasyonu simülasyonu
            const tbody = document.getElementById('payroll-commissions-body');
            if (!tbody) return;
            tbody.innerHTML = '<tr><td colspan="5" class="p-8 text-center text-gray-400">Seçilen aya ait hakediş/komisyon verisi bulunamadı.</td></tr>';
        }

        // ==========================================
        // INTEGRATIONS JS MANTIĞI
        // ==========================================
        async function fetchIntegrations() {
            const tbody = document.getElementById('publications-table-body');
            if (!tbody) return;
            tbody.innerHTML = '<tr><td colspan="4" class="p-8 text-center text-gray-400">Henüz son platform paylaşımları veritabanına işlenmedi.</td></tr>';
        }
"""

# Replace showSection logic to include these new fetches
html = html.replace("""if (sectionId === 'appointments') fetchAppointments();
        }""", """if (sectionId === 'appointments') fetchAppointments();
            if (sectionId === 'leads') fetchLeads();
            if (sectionId === 'expenses') fetchExpenses();
            if (sectionId === 'payroll') fetchPayroll();
            if (sectionId === 'integrations') fetchIntegrations();
        }""")

# 2. Add MODAL HTMLs before closing body
modals_html = """
<!-- ================= MISSING MODALS ================= -->
<div id="contract-modal" class="fixed inset-0 z-50 hidden bg-navy/60 backdrop-blur-sm flex items-center justify-center p-4">
    <div class="bg-white rounded-3xl w-full max-w-lg shadow-2xl overflow-hidden p-6 relative">
        <h3 class="text-2xl font-serif font-bold text-navy mb-4">Sözleşme Ekle (Hızlı)</h3>
        <p class="text-sm text-gray-500 mb-6">Detaylı sözleşme oluşturmak için sol menüden 'Sözleşme Sihirbazı'nı kullanınız. Bu alan basit kayıtlar içindir.</p>
        <button onclick="document.getElementById('contract-modal').classList.add('hidden')" class="w-full py-3 bg-gray-100 rounded-lg text-navy font-bold hover:bg-gray-200">Kapat</button>
    </div>
</div>

<div id="tax-modal" class="fixed inset-0 z-50 hidden bg-navy/60 backdrop-blur-sm flex items-center justify-center p-4">
    <div class="bg-white rounded-3xl w-full max-w-lg shadow-2xl overflow-hidden p-6 relative">
        <h3 class="text-2xl font-serif font-bold text-navy mb-4">Finans / Vergi Ekle</h3>
        <p class="text-sm text-gray-500 mb-6">Sistem yapım aşamasında. Çok yakında otomatik TCMB entegrasyonuyla canlıya alınacaktır.</p>
        <button onclick="document.getElementById('tax-modal').classList.add('hidden')" class="w-full py-3 bg-gray-100 rounded-lg text-navy font-bold hover:bg-gray-200">Kapat</button>
    </div>
</div>

<div id="maintenance-req-modal" class="fixed inset-0 z-50 hidden bg-navy/60 backdrop-blur-sm flex items-center justify-center p-4">
    <div class="bg-white rounded-3xl w-full max-w-lg shadow-2xl overflow-hidden p-6 relative">
        <h3 class="text-2xl font-serif font-bold text-navy mb-4">Bakım Talebi Oluştur</h3>
        <p class="text-sm text-gray-500 mb-6">Mülkünüzle ilgili onarım talebi göndermek yapım aşamasındadır.</p>
        <button onclick="document.getElementById('maintenance-req-modal').classList.add('hidden')" class="w-full py-3 bg-gray-100 rounded-lg text-navy font-bold hover:bg-gray-200">Kapat</button>
    </div>
</div>

<div id="appointment-modal" class="fixed inset-0 z-50 hidden bg-navy/60 backdrop-blur-sm flex items-center justify-center p-4">
    <div class="bg-white rounded-3xl w-full max-w-lg shadow-2xl overflow-hidden p-6 relative">
        <h3 class="text-2xl font-serif font-bold text-navy mb-4">Manuel Randevu Ekle</h3>
        <p class="text-sm text-gray-500 mb-6">Müşterileriniz için takvime manuel randevu ekleme modülü yapım aşamasındadır.</p>
        <button onclick="document.getElementById('appointment-modal').classList.add('hidden')" class="w-full py-3 bg-gray-100 rounded-lg text-navy font-bold hover:bg-gray-200">Kapat</button>
    </div>
</div>

<div id="lead-modal" class="fixed inset-0 z-50 hidden bg-navy/60 backdrop-blur-sm flex items-center justify-center p-4">
    <div class="bg-white rounded-3xl w-full max-w-lg shadow-2xl overflow-hidden p-6 relative">
        <h3 class="text-2xl font-serif font-bold text-navy mb-4">Yeni Müşteri Adayı Ekle</h3>
        <p class="text-sm text-gray-500 mb-6">Manuel CRM girişi modülü yapım aşamasındadır. Adaylar şu an otomatik olarak web formundan düşmektedir.</p>
        <button onclick="document.getElementById('lead-modal').classList.add('hidden')" class="w-full py-3 bg-gray-100 rounded-lg text-navy font-bold hover:bg-gray-200">Kapat</button>
    </div>
</div>

<div id="expense-modal" class="fixed inset-0 z-50 hidden bg-navy/60 backdrop-blur-sm flex items-center justify-center p-4">
    <div class="bg-white rounded-3xl w-full max-w-lg shadow-2xl overflow-hidden p-6 relative">
        <h3 class="text-2xl font-serif font-bold text-navy mb-4">Harcama Fişi Ekle</h3>
        <p class="text-sm text-gray-500 mb-6">Fiş girişi ve onay mekanizması yapım aşamasındadır.</p>
        <button onclick="document.getElementById('expense-modal').classList.add('hidden')" class="w-full py-3 bg-gray-100 rounded-lg text-navy font-bold hover:bg-gray-200">Kapat</button>
    </div>
</div>

<div id="publish-wizard-modal" class="fixed inset-0 z-50 hidden bg-navy/60 backdrop-blur-sm flex items-center justify-center p-4">
    <div class="bg-white rounded-3xl w-full max-w-lg shadow-2xl overflow-hidden p-6 relative">
        <h3 class="text-2xl font-serif font-bold text-navy mb-4">Yeni Paylaşım Oluştur</h3>
        <p class="text-sm text-gray-500 mb-6">Çoklu platform paylaşım asistanı yapım aşamasındadır.</p>
        <button onclick="document.getElementById('publish-wizard-modal').classList.add('hidden')" class="w-full py-3 bg-gray-100 rounded-lg text-navy font-bold hover:bg-gray-200">Kapat</button>
    </div>
</div>
"""

html = re.sub(r'</body>', modals_html + '\n</body>', html, flags=re.IGNORECASE)

# 3. APPEND THE MISSING JS BEFORE </script>
html = re.sub(r'(</script>)', missing_js + r'\n\1', html, flags=re.IGNORECASE)

# 4. REPLACE alert() with modal opens
html = re.sub(r"alert\('Sözleşme Ekleme Modalı Yapım Aşamasında.'\);?", "document.getElementById('contract-modal').classList.remove('hidden');", html)
html = re.sub(r"alert\('Finans Ekleme Modalı Yapım Aşamasında.'\);?", "document.getElementById('tax-modal').classList.remove('hidden');", html)
html = re.sub(r"alert\('Bakım Talebi Modalı Yapım Aşamasında.'\);?", "document.getElementById('maintenance-req-modal').classList.remove('hidden');", html)
html = re.sub(r"alert\('Randevu Modalı Yapım Aşamasında.'\);?", "document.getElementById('appointment-modal').classList.remove('hidden');", html)

# For un-implemented functions that didn't even have alert() yet, let's inject them:
html = re.sub(r'(</script>)', """
        function openLeadModal() { document.getElementById('lead-modal').classList.remove('hidden'); }
        function openExpenseModal() { document.getElementById('expense-modal').classList.remove('hidden'); }
        function openPublishWizard() { document.getElementById('publish-wizard-modal').classList.remove('hidden'); }
\n""" + r'\1', html, flags=re.IGNORECASE)


with open('portal.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Patch successful.")
