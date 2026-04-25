import re

with open('portal.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_js = """
        // ==========================================
        // SÖZLEŞMELER (CONTRACTS) JS MANTIĞI
        // ==========================================
        async function fetchContracts() {
            const token = localStorage.getItem('imza_admin_token');
            if(!token) return;
            try {
                const res = await fetch(`${API_BASE}/contracts`, {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                if (res.ok) {
                    const data = await res.json();
                    const tbody = document.getElementById('contracts-table-body');
                    tbody.innerHTML = '';
                    data.forEach(c => {
                        const tr = document.createElement('tr');
                        tr.className = 'border-b border-gray-100/50';
                        tr.innerHTML = `
                            <td class="px-6 py-4 font-medium text-navy">#${c.id}</td>
                            <td class="px-6 py-4">
                                <span class="font-bold text-navy block">${c.baslik1 || 'Bilinmiyor'}</span>
                                <span class="text-[10px] text-gray-400">${c.refNo || '-'}</span>
                            </td>
                            <td class="px-6 py-4">
                                <span class="font-medium text-navy">${c.username || 'Sistem'}</span>
                                <span class="text-[10px] text-gray-500 block uppercase">${c.role || '-'}</span>
                            </td>
                            <td class="px-6 py-4"><span class="bg-gray-100 text-gray-700 px-2 py-1 rounded text-xs">${c.type}</span></td>
                            <td class="px-6 py-4 text-gray-600">${c.start_date.substring(0,10)}</td>
                            <td class="px-6 py-4 font-medium text-modern">${c.end_date.substring(0,10)}</td>
                            <td class="px-6 py-4 text-right">
                                <button onclick="deleteContract(${c.id})" class="text-red-400 hover:text-red-500 transition-colors p-2"><i class="fa-regular fa-trash-can"></i></button>
                            </td>
                        `;
                        tbody.appendChild(tr);
                    });
                }
            } catch (err) { console.error(err); }
        }

        async function deleteContract(id) {
            const token = localStorage.getItem('imza_admin_token');
            if(confirm('Sözleşmeyi iptal etmek/silmek istediğinize emin misiniz?')) {
                const res = await fetch(`${API_BASE}/contracts/${id}`, {
                    method: 'DELETE', headers: { 'Authorization': `Bearer ${token}` }
                });
                if(res.ok) fetchContracts();
            }
        }

        function openContractModal() {
            alert('Sözleşme Ekleme Modalı Yapım Aşamasında.');
        }

        // ==========================================
        // VERGİ VE FİNANS (TAXES) JS MANTIĞI
        // ==========================================
        async function fetchTaxes() {
            const token = localStorage.getItem('imza_admin_token');
            if(!token) return;
            try {
                const res = await fetch(`${API_BASE}/taxes`, {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                if (res.ok) {
                    const data = await res.json();
                    const tbody = document.getElementById('taxes-table-body');
                    tbody.innerHTML = '';
                    data.forEach(t => {
                        const isPaid = t.status === 'Ödendi';
                        const statusColor = isPaid ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700';
                        const tr = document.createElement('tr');
                        tr.className = 'border-b border-gray-100/50';
                        tr.innerHTML = `
                            <td class="px-6 py-4 font-medium text-navy">#${t.id}</td>
                            <td class="px-6 py-4 font-bold text-navy">${t.baslik1 || '-'}</td>
                            <td class="px-6 py-4 text-gray-600">${t.tax_type}</td>
                            <td class="px-6 py-4 font-bold ${isPaid ? 'text-gray-800' : 'text-red-600'}">${t.amount.toLocaleString()} ₺</td>
                            <td class="px-6 py-4 text-gray-600">${t.due_date.substring(0,10)}</td>
                            <td class="px-6 py-4"><span class="${statusColor} px-2 py-1 rounded text-xs font-bold">${t.status}</span></td>
                            <td class="px-6 py-4 text-right">
                                <button onclick="deleteTax(${t.id})" class="text-red-400 hover:text-red-500 transition-colors p-2"><i class="fa-regular fa-trash-can"></i></button>
                            </td>
                        `;
                        tbody.appendChild(tr);
                    });
                }
            } catch (err) { console.error(err); }
        }

        async function deleteTax(id) {
            const token = localStorage.getItem('imza_admin_token');
            if(confirm('Vergi kaydını silmek istediğinize emin misiniz?')) {
                const res = await fetch(`${API_BASE}/taxes/${id}`, {
                    method: 'DELETE', headers: { 'Authorization': `Bearer ${token}` }
                });
                if(res.ok) fetchTaxes();
            }
        }
        function openTaxModal() { alert('Finans Ekleme Modalı Yapım Aşamasında.'); }

        // ==========================================
        // BAKIM TALEPLERİ (MAINTENANCE) JS MANTIĞI
        // ==========================================
        async function fetchMaintenance() {
            const token = localStorage.getItem('imza_admin_token');
            if(!token) return;
            try {
                const res = await fetch(`${API_BASE}/maintenance`, {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                if (res.ok) {
                    const data = await res.json();
                    const tbody = document.getElementById('maintenance-table-body');
                    tbody.innerHTML = '';
                    data.forEach(m => {
                        let statusColor = 'bg-yellow-100 text-yellow-700';
                        if(m.status === 'Çözüldü') statusColor = 'bg-green-100 text-green-700';
                        if(m.status === 'İptal') statusColor = 'bg-gray-100 text-gray-500';

                        const tr = document.createElement('tr');
                        tr.className = 'border-b border-gray-100/50';
                        tr.innerHTML = `
                            <td class="px-6 py-4 font-medium text-navy">#${m.id}</td>
                            <td class="px-6 py-4 font-bold text-navy">${m.baslik1 || '-'}</td>
                            <td class="px-6 py-4 text-gray-600">${m.username || 'Bilinmiyor'}</td>
                            <td class="px-6 py-4 text-gray-500">${m.request_date.substring(0,10)}</td>
                            <td class="px-6 py-4 text-gray-800 text-xs max-w-xs truncate" title="${m.description}">${m.description}</td>
                            <td class="px-6 py-4"><span class="${statusColor} px-2 py-1 rounded text-xs font-bold">${m.status}</span></td>
                            <td class="px-6 py-4 text-right">
                                <button onclick="deleteMaintenance(${m.id})" class="text-red-400 hover:text-red-500 transition-colors p-2"><i class="fa-regular fa-trash-can"></i></button>
                            </td>
                        `;
                        tbody.appendChild(tr);
                    });
                }
            } catch (err) { console.error(err); }
        }

        async function deleteMaintenance(id) {
            const token = localStorage.getItem('imza_admin_token');
            if(confirm('Talebi silmek istediğinize emin misiniz?')) {
                const res = await fetch(`${API_BASE}/maintenance/${id}`, {
                    method: 'DELETE', headers: { 'Authorization': `Bearer ${token}` }
                });
                if(res.ok) fetchMaintenance();
            }
        }
        function openMaintenanceModal() { alert('Bakım Talebi Modalı Yapım Aşamasında.'); }
        
        // ==========================================
        // RANDEVULAR (APPOINTMENTS) JS MANTIĞI
        // ==========================================
        async function fetchAppointments() {
            const token = localStorage.getItem('imza_admin_token');
            if(!token) return;
            try {
                const res = await fetch(`${API_BASE}/appointments`, {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                if (res.ok) {
                    const data = await res.json();
                    const tbody = document.getElementById('appointments-table-body');
                    tbody.innerHTML = '';
                    data.forEach(a => {
                        let statusColor = 'bg-blue-100 text-blue-700';
                        if(a.status === 'Tamamlandı') statusColor = 'bg-green-100 text-green-700';
                        if(a.status === 'İptal') statusColor = 'bg-red-100 text-red-700';

                        const tr = document.createElement('tr');
                        tr.className = 'border-b border-gray-100/50';
                        tr.innerHTML = `
                            <td class="px-6 py-4 font-medium text-navy">#${a.id}</td>
                            <td class="px-6 py-4 font-bold text-navy">${a.baslik1 || '-'}</td>
                            <td class="px-6 py-4">
                                <span class="text-navy font-bold block">${a.username || 'Bilinmiyor'}</span>
                                <span class="text-[10px] text-gray-500">${a.phone || '-'}</span>
                            </td>
                            <td class="px-6 py-4 text-gray-600 font-medium">${a.date}</td>
                            <td class="px-6 py-4"><span class="${statusColor} px-2 py-1 rounded text-xs font-bold">${a.status}</span></td>
                            <td class="px-6 py-4 text-right">
                                <button onclick="deleteAppointment(${a.id})" class="text-red-400 hover:text-red-500 transition-colors p-2"><i class="fa-regular fa-trash-can"></i></button>
                            </td>
                        `;
                        tbody.appendChild(tr);
                    });
                }
            } catch (err) { console.error(err); }
        }

        async function deleteAppointment(id) {
            const token = localStorage.getItem('imza_admin_token');
            if(confirm('Randevuyu iptal etmek istediğinize emin misiniz?')) {
                const res = await fetch(`${API_BASE}/appointments/${id}`, {
                    method: 'DELETE', headers: { 'Authorization': `Bearer ${token}` }
                });
                if(res.ok) fetchAppointments();
            }
        }
        function openAppointmentModal() { alert('Randevu Modalı Yapım Aşamasında.'); }
"""

# Fetch these automatically when their section is shown
new_show_logic = """
        const originalShowSectionForModules = showSection;
        showSection = function(sectionId, btnElement) {
            originalShowSectionForModules(sectionId, btnElement);
            if (sectionId === 'contracts') fetchContracts();
            if (sectionId === 'taxes') fetchTaxes();
            if (sectionId === 'maintenance') fetchMaintenance();
            if (sectionId === 'appointments') fetchAppointments();
        }
"""

pattern_script = re.compile(r'(</script>)', re.IGNORECASE)
html = pattern_script.sub(new_js + new_show_logic + r'\n\1', html)

with open('portal.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("JS injected.")
