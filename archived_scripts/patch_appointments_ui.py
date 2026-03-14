import sys

with open('portal.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Randevu tablosu başlıklarını güncelle - "Konu" kolonu ekle
old_thead = '''<th class="px-6 py-4 font-bold text-xs">ID</th>
                                    <th class="px-6 py-4 font-bold text-xs">Mülk (Portföy)</th>
                                    <th class="px-6 py-4 font-bold text-xs">Talep Sahibi</th>
                                    <th class="px-6 py-4 font-bold text-xs">Tarih / Saat</th>
                                    <th class="px-6 py-4 font-bold text-xs">Durum</th>
                                    <th class="px-6 py-4 text-right">Aksiyonlar</th>'''

new_thead = '''<th class="px-6 py-4 font-bold text-xs">ID</th>
                                    <th class="px-6 py-4 font-bold text-xs">Mülk (Portföy)</th>
                                    <th class="px-6 py-4 font-bold text-xs">Müşteri</th>
                                    <th class="px-6 py-4 font-bold text-xs">Konu</th>
                                    <th class="px-6 py-4 font-bold text-xs">Tarih / Saat</th>
                                    <th class="px-6 py-4 font-bold text-xs">Durum</th>
                                    <th class="px-6 py-4 text-right">Aksiyonlar</th>'''

content = content.replace(old_thead, new_thead)

# 2. fetchAppointments fonksiyonunu yeniden yaz
old_fetch = '''async function fetchAppointments() {
            const token = localStorage.getItem('imza_admin_token');
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
                        if (a.status === 'Tamamlandı') statusColor = 'bg-green-100 text-green-700';
                        if (a.status === 'İptal') statusColor = 'bg-red-100 text-red-700';

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
        }'''

new_fetch = '''async function fetchAppointments() {
            const token = localStorage.getItem('imza_admin_token');
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
                        let statusLabel = a.status;
                        if (a.status === 'confirmed') { statusColor = 'bg-green-100 text-green-700'; statusLabel = 'Onaylandı'; }
                        if (a.status === 'cancelled') { statusColor = 'bg-red-100 text-red-700'; statusLabel = 'İptal'; }
                        if (a.status === 'rescheduled') { statusColor = 'bg-amber-100 text-amber-700'; statusLabel = 'Ertelendi (' + (a.reschedule_count||1) + ')'; }
                        if (a.status === 'pending') { statusLabel = 'Bekliyor'; }

                        const clientName = a.client_name || a.username || 'Bilinmiyor';
                        const clientPhone = a.client_phone || a.user_phone || '-';
                        const purposeLabel = a.purpose_label || a.purpose || '-';

                        const tr = document.createElement('tr');
                        tr.className = 'border-b border-gray-100/50 hover:bg-gray-50 transition-colors';
                        tr.innerHTML = `
                            <td class="px-6 py-4 font-medium text-navy">#${a.id}</td>
                            <td class="px-6 py-4 font-bold text-navy">${a.baslik1 || '-'}</td>
                            <td class="px-6 py-4">
                                <span class="text-navy font-bold block">${clientName}</span>
                                <span class="text-[10px] text-gray-500">${clientPhone}</span>
                            </td>
                            <td class="px-6 py-4">
                                <span class="bg-navy/5 text-navy px-2 py-1 rounded text-[10px] font-bold uppercase">${purposeLabel}</span>
                            </td>
                            <td class="px-6 py-4 text-gray-600 font-medium">
                                ${a.datetime || '-'}
                                ${a.original_datetime ? '<br><span class=\\'text-[9px] text-gray-400 line-through\\'>Orijinal: ' + a.original_datetime + '</span>' : ''}
                            </td>
                            <td class="px-6 py-4"><span class="${statusColor} px-2 py-1 rounded text-xs font-bold">${statusLabel}</span></td>
                            <td class="px-6 py-4 text-right space-x-1">
                                ${a.status !== 'confirmed' ? '<button onclick="confirmAppt(' + a.id + ')" class="text-green-500 hover:text-green-700 p-1" title="Onayla"><i class="fa-solid fa-check"></i></button>' : ''}
                                ${a.status !== 'cancelled' ? '<button onclick="openRescheduleModal(' + a.id + ', \\'' + (a.datetime||'') + '\\')" class="text-amber-500 hover:text-amber-700 p-1" title="Ertele"><i class="fa-solid fa-clock-rotate-left"></i></button>' : ''}
                                <button onclick="deleteAppointment(${a.id})" class="text-red-400 hover:text-red-500 p-1" title="İptal"><i class="fa-regular fa-trash-can"></i></button>
                            </td>
                        `;
                        tbody.appendChild(tr);
                    });
                }
            } catch (err) { console.error(err); }
        }'''

content = content.replace(old_fetch, new_fetch)

# 3. openAppointmentModal'ı çalışan bir versiyona çevir
old_modal_fn = "function openAppointmentModal() { alert('Randevu Modalı Yapım Aşamasında.'); }"
new_modal_fn = '''function openAppointmentModal() {
            document.getElementById('appointment-modal-v2').classList.remove('hidden');
        }
        function closeAppointmentModalV2() {
            document.getElementById('appointment-modal-v2').classList.add('hidden');
        }

        async function saveAppointmentV2() {
            const clientName = document.getElementById('appt2-client').value.trim();
            const clientPhone = document.getElementById('appt2-phone').value.trim();
            const purpose = document.getElementById('appt2-purpose').value;
            const datetime = document.getElementById('appt2-datetime').value;
            const notes = document.getElementById('appt2-notes').value.trim();
            const token = localStorage.getItem('imza_admin_token');

            if (!clientName || !datetime) {
                alert('Müşteri adı ve tarih/saat zorunludur.');
                return;
            }

            try {
                const res = await fetch(`${API_BASE}/appointments`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                    body: JSON.stringify({
                        user_id: 1,
                        client_name: clientName,
                        client_phone: clientPhone,
                        purpose: purpose,
                        datetime: datetime.replace('T', ' '),
                        notes: notes,
                        assigned_user_id: 1,
                        status: 'pending'
                    })
                });
                if (res.ok) {
                    alert('Randevu başarıyla oluşturuldu!');
                    closeAppointmentModalV2();
                    fetchAppointments();
                } else {
                    const err = await res.json();
                    alert('Hata: ' + (err.error || 'Bilinmeyen hata'));
                }
            } catch (e) {
                console.error(e);
                alert('Bağlantı hatası.');
            }
        }

        async function confirmAppt(id) {
            const token = localStorage.getItem('imza_admin_token');
            try {
                const res = await fetch(`${API_BASE}/appointments/${id}/confirm`, {
                    method: 'PUT', headers: { 'Authorization': `Bearer ${token}` }
                });
                if (res.ok) fetchAppointments();
            } catch(e) { console.error(e); }
        }

        // --- ERTELEME (RESCHEDULE) ---
        let rescheduleApptId = null;
        function openRescheduleModal(id, currentDatetime) {
            rescheduleApptId = id;
            document.getElementById('reschedule-current-date').textContent = currentDatetime || '-';
            document.getElementById('reschedule-new-datetime').value = '';
            document.getElementById('reschedule-modal').classList.remove('hidden');
        }
        function closeRescheduleModal() {
            document.getElementById('reschedule-modal').classList.add('hidden');
            rescheduleApptId = null;
        }
        async function submitReschedule() {
            const newDatetime = document.getElementById('reschedule-new-datetime').value;
            if (!newDatetime) { alert('Lütfen yeni tarih ve saat seçin.'); return; }
            const token = localStorage.getItem('imza_admin_token');
            try {
                const res = await fetch(`${API_BASE}/appointments/${rescheduleApptId}/reschedule`, {
                    method: 'PUT',
                    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                    body: JSON.stringify({ new_datetime: newDatetime.replace('T', ' ') })
                });
                if (res.ok) {
                    const data = await res.json();
                    alert('Randevu ertelendi! Yeni tarih: ' + newDatetime.replace('T', ' ') + ' (Erteleme: ' + data.reschedule_count + ')');
                    closeRescheduleModal();
                    fetchAppointments();
                } else {
                    const err = await res.json();
                    alert('Hata: ' + (err.error || 'Bilinmeyen hata'));
                }
            } catch(e) {
                console.error(e);
                alert('Bağlantı hatası.');
            }
        }'''

content = content.replace(old_modal_fn, new_modal_fn)

# 4. Randevu ve Erteleme modalları HTML ekle (</body> öncesine)
modals_html = '''
    <!-- RANDEVU OLUŞTURMA MODALI V2 -->
    <div id="appointment-modal-v2" class="fixed inset-0 bg-black/50 backdrop-blur-sm z-[100] hidden flex items-center justify-center">
        <div class="bg-white rounded-[2rem] w-full max-w-lg p-8 shadow-2xl relative">
            <button onclick="closeAppointmentModalV2()" class="absolute top-6 right-6 text-gray-400 hover:text-navy transition-colors">
                <i class="fa-solid fa-xmark text-xl"></i>
            </button>
            <h3 class="text-2xl font-serif font-bold text-navy mb-6"><i class="fa-regular fa-calendar-plus text-gold mr-2"></i> Yeni Randevu</h3>
            <div class="space-y-4">
                <div>
                    <label class="block text-xs font-bold text-gray-600 mb-2 uppercase tracking-wider">Müşteri Adı *</label>
                    <input type="text" id="appt2-client" class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-gold/50 focus:border-gold outline-none" placeholder="Ad Soyad">
                </div>
                <div>
                    <label class="block text-xs font-bold text-gray-600 mb-2 uppercase tracking-wider">Telefon</label>
                    <input type="tel" id="appt2-phone" class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-gold/50 focus:border-gold outline-none" placeholder="05XX XXX XX XX">
                </div>
                <div>
                    <label class="block text-xs font-bold text-gray-600 mb-2 uppercase tracking-wider">Randevu Konusu *</label>
                    <select id="appt2-purpose" class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-gold/50 focus:border-gold outline-none text-navy font-medium">
                        <option value="gosterim">Portföy Gösterimi</option>
                        <option value="sozlesme">Sözleşme İmzası</option>
                        <option value="kapora">Kapora Görüşmesi</option>
                        <option value="expertiz">Expertiz / Değerleme</option>
                        <option value="sanal_tur">Sanal Tur</option>
                        <option value="diger">Diğer</option>
                    </select>
                </div>
                <div>
                    <label class="block text-xs font-bold text-gray-600 mb-2 uppercase tracking-wider">Tarih ve Saat *</label>
                    <input type="datetime-local" id="appt2-datetime" class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-gold/50 focus:border-gold outline-none">
                </div>
                <div>
                    <label class="block text-xs font-bold text-gray-600 mb-2 uppercase tracking-wider">Notlar</label>
                    <textarea id="appt2-notes" rows="2" class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-gold/50 focus:border-gold outline-none resize-none" placeholder="Ek bilgiler..."></textarea>
                </div>
                <button onclick="saveAppointmentV2()" class="w-full bg-navy hover:bg-slate-800 text-gold py-4 rounded-xl font-bold text-sm uppercase tracking-widest transition-all mt-2">
                    <i class="fa-solid fa-calendar-check mr-2"></i> Randevuyu Kaydet
                </button>
            </div>
        </div>
    </div>

    <!-- ERTELEME (RESCHEDULE) MODALI -->
    <div id="reschedule-modal" class="fixed inset-0 bg-black/50 backdrop-blur-sm z-[100] hidden flex items-center justify-center">
        <div class="bg-white rounded-[2rem] w-full max-w-md p-8 shadow-2xl relative">
            <button onclick="closeRescheduleModal()" class="absolute top-6 right-6 text-gray-400 hover:text-navy transition-colors">
                <i class="fa-solid fa-xmark text-xl"></i>
            </button>
            <h3 class="text-2xl font-serif font-bold text-navy mb-6"><i class="fa-solid fa-clock-rotate-left text-amber-500 mr-2"></i> Randevuyu Ertele</h3>
            <div class="space-y-4">
                <div class="bg-amber-50 border border-amber-200 rounded-xl p-4">
                    <p class="text-xs text-amber-700 font-bold uppercase tracking-wider mb-1">Mevcut Tarih</p>
                    <p id="reschedule-current-date" class="text-navy font-bold">-</p>
                </div>
                <div>
                    <label class="block text-xs font-bold text-gray-600 mb-2 uppercase tracking-wider">Yeni Tarih ve Saat *</label>
                    <input type="datetime-local" id="reschedule-new-datetime" class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-gold/50 focus:border-gold outline-none">
                </div>
                <button onclick="submitReschedule()" class="w-full bg-amber-500 hover:bg-amber-600 text-white py-4 rounded-xl font-bold text-sm uppercase tracking-widest transition-all">
                    <i class="fa-solid fa-calendar-days mr-2"></i> Randevuyu Ertele
                </button>
            </div>
        </div>
    </div>
'''

# </body> öncesine ekle
content = content.replace('</body>', modals_html + '\n</body>')

# alert'li eski butonları temizle (kullanıcı eklediği duplicate satırları)
content = content.replace(
    '''<button onclick="alert('Yeni Aday Ekleme Modalı Yapım Aşamasında')"
                        <button onclick="openLeadModal()"''',
    '<button onclick="openLeadModal()"'
)
content = content.replace(
    '''<button onclick="alert('Harcama Ekleme Modalı Yapım Aşamasında')"
                        <button onclick="openExpenseModal()"''',
    '<button onclick="openExpenseModal()"'
)

# Duplicate approve butonunu temizle
content = content.replace(
    '''${e.status === 'pending' ? `<button onclick="alert('Onay API çağrılacak')" class="text-green-500 hover:text-green-700"><i class="fa-solid fa-check"></i></button>` : ''}
                                ${e.status === 'pending' ? `<button onclick="approveExpense(${e.id})" class="text-green-500 hover:text-green-700"><i class="fa-solid fa-check"></i></button>` : ''}''',
    '''${e.status === 'pending' ? `<button onclick="approveExpense(${e.id})" class="text-green-500 hover:text-green-700"><i class="fa-solid fa-check"></i></button>` : ''}'''
)

with open('portal.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("portal.html UI güncellemeleri tamamlandı!")
