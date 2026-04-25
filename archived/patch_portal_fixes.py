import sys
import re

with open('portal.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix Contract Builder
# Ensure con-next-btn calls a function that handles the final step, or change con-save-btn to call finalizeContract
# Let's check the HTML for con-save-btn
save_btn_match = re.search(r'<button\s+id="con-save-btn"[^>]*onclick="([^"]*)"', content)
if save_btn_match:
    print(f"con-save-btn onclick: {save_btn_match.group(1)}")
    # It might be empty or missing. Let's force it to call finalizeContract()
    
# Actually let's just use string replace to inject the proper onclick if it doesn't have it
content = content.replace(
    'id="con-save-btn" class="hidden', 
    'id="con-save-btn" onclick="finalizeContract()" class="hidden'
)

# And fix conWizNext to ensure it doesn't throw errors
# The code for conWizNext looks okay, it stops at step < 4.

# 2. Fix Appointments
# We need to add an Appointment Modal HTML and change openAppointmentModal()
appt_modal_html = '''
    <!-- RANDEVU MODALI -->
    <div id="appointment-modal" class="fixed inset-0 bg-navy/80 backdrop-blur-sm z-50 hidden flex items-center justify-center">
        <div class="bg-white rounded-[2rem] w-full max-w-md p-8 shadow-2xl relative">
            <button onclick="closeAppointmentModal()" class="absolute top-6 right-6 text-gray-400 hover:text-navy transition-colors">
                <i class="fa-solid fa-xmark text-xl"></i>
            </button>
            <h3 class="text-2xl font-serif font-bold text-navy mb-6">Yeni Randevu Oluştur</h3>
            
            <div class="space-y-4">
                <div>
                    <label class="block text-xs font-bold text-gray-600 mb-2 uppercase tracking-wider">İlgili Portföy / Başlık</label>
                    <input type="text" id="appt-title" class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-gold/50 focus:border-gold outline-none" placeholder="Örn: Boğaz Manzaralı Villa Gösterimi">
                </div>
                <div>
                    <label class="block text-xs font-bold text-gray-600 mb-2 uppercase tracking-wider">Müşteri Adı</label>
                    <input type="text" id="appt-client" class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-gold/50 focus:border-gold outline-none" placeholder="Müşteri Adı Soyadı">
                </div>
                <div>
                    <label class="block text-xs font-bold text-gray-600 mb-2 uppercase tracking-wider">Telefon Numarası</label>
                    <input type="tel" id="appt-phone" class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-gold/50 focus:border-gold outline-none" placeholder="05XX XXX XX XX">
                </div>
                <div>
                    <label class="block text-xs font-bold text-gray-600 mb-2 uppercase tracking-wider">Tarih ve Saat</label>
                    <input type="datetime-local" id="appt-date" class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-gold/50 focus:border-gold outline-none">
                </div>
                <button onclick="saveAppointment()" class="w-full bg-navy hover:bg-slate-800 text-gold py-4 rounded-xl font-bold text-sm uppercase tracking-widest transition-all mt-4">
                    Randevuyu Kaydet
                </button>
            </div>
        </div>
    </div>
'''

# Inject modal before the closing body tag
content = content.replace('</body>', appt_modal_html + '\n</body>')

# Update JS for appointments
appt_js = '''
        function openAppointmentModal() {
            document.getElementById('appointment-modal').classList.remove('hidden');
        }

        function closeAppointmentModal() {
            document.getElementById('appointment-modal').classList.add('hidden');
            document.getElementById('appt-title').value = '';
            document.getElementById('appt-client').value = '';
            document.getElementById('appt-phone').value = '';
            document.getElementById('appt-date').value = '';
        }

        async function saveAppointment() {
            const title = document.getElementById('appt-title').value.trim();
            const client = document.getElementById('appt-client').value.trim();
            const phone = document.getElementById('appt-phone').value.trim();
            let date = document.getElementById('appt-date').value;

            if (!title || !client || !date) {
                alert('Lütfen başlık, müşteri adı ve tarih alanlarını doldurun.');
                return;
            }

            // Tarihi formatla (YYYY-MM-DDTHH:mm -> YYYY-MM-DD HH:mm)
            date = date.replace('T', ' ');

            try {
                const response = await fetch(`${API_BASE}/appointments`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${localStorage.getItem('imza_admin_token')}`
                    },
                    body: JSON.stringify({
                        property_id: null,
                        baslik1: title,
                        username: client,
                        phone: phone,
                        date: date,
                        status: 'Bekliyor'
                    })
                });

                if (response.ok) {
                    alert('Randevu başarıyla oluşturuldu!');
                    closeAppointmentModal();
                    fetchAppointments();
                } else {
                    alert('Randevu oluşturulurken bir hata oluştu.');
                }
            } catch (error) {
                console.error('Randevu hatası:', error);
                alert('Randevu oluşturulurken bağlantı hatası oluştu.');
            }
        }
'''

# Replace the dummy openAppointmentModal with the real functions
content = content.replace("function openAppointmentModal() { alert('Randevu Modalı Yapım Aşamasında.'); }", appt_js)

# Fix contract save button if needed
# We need to make sure `con-save-btn` actually calls `finalizeContract()`

with open('portal.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("portal.html patched successfully for contracts and appointments.")
