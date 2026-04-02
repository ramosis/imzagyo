import re

with open('portal.html', 'r', encoding='utf-8') as f:
    html = f.read()

new_sections = """
            <!-- ========================================== -->
            <!-- CONTRACTS SECTİON -->
            <section id="contracts-section" class="flex flex-col h-full bg-white hidden">
                <div class="px-8 py-6 border-b border-gray-100 shrink-0">
                    <div class="flex justify-between items-end">
                        <div class="space-y-1">
                            <h2 class="text-2xl font-serif font-bold text-navy">Sözleşmeler</h2>
                            <p class="text-sm text-gray-500">Mülklerin kira ve satış durumlarını, sözleşme sürelerini yönetin.</p>
                        </div>
                        <button onclick="openContractModal()" class="bg-navy hover:bg-slate-800 text-gold font-bold py-3 px-6 rounded-lg transition-all gold-glow uppercase tracking-[0.15em] text-xs flex items-center gap-2">
                            <i class="fa-solid fa-plus"></i> Yeni Sözleşme
                        </button>
                    </div>
                </div>

                <!-- Tablo Alanı -->
                <div class="flex-1 overflow-auto p-8 relative">
                    <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden relative z-10">
                        <table class="w-full text-left premium-table">
                            <thead>
                                <tr>
                                    <th class="px-6 py-4 font-bold text-xs">Sözleşme ID</th>
                                    <th class="px-6 py-4 font-bold text-xs">Portföy (Mülk)</th>
                                    <th class="px-6 py-4 font-bold text-xs">İlgili Taraf</th>
                                    <th class="px-6 py-4 font-bold text-xs">Tip</th>
                                    <th class="px-6 py-4 font-bold text-xs">Başlangıç</th>
                                    <th class="px-6 py-4 font-bold text-xs">Bitiş</th>
                                    <th class="px-6 py-4 text-right">Aksiyonlar</th>
                                </tr>
                            </thead>
                            <tbody id="contracts-table-body" class="text-sm">
                                <!-- JS Dinamik Dolduracak -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </section>

            <!-- ========================================== -->
            <!-- TAXES SECTİON -->
            <section id="taxes-section" class="flex flex-col h-full bg-white hidden">
                <div class="px-8 py-6 border-b border-gray-100 shrink-0">
                    <div class="flex justify-between items-end">
                        <div class="space-y-1">
                            <h2 class="text-2xl font-serif font-bold text-navy">Finans ve Vergi</h2>
                            <p class="text-sm text-gray-500">Mülk vergisi, beyanname, aidat ve diğer mali yükümlülükleri izleyin.</p>
                        </div>
                        <button onclick="openTaxModal()" class="bg-navy hover:bg-slate-800 text-white font-bold py-3 px-6 rounded-lg transition-all uppercase tracking-[0.15em] text-xs flex items-center gap-2">
                            <i class="fa-solid fa-plus text-gold"></i> Kayıt Ekle
                        </button>
                    </div>
                </div>

                <div class="flex-1 overflow-auto p-8 relative">
                    <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden relative z-10">
                        <table class="w-full text-left premium-table">
                            <thead>
                                <tr>
                                    <th class="px-6 py-4 font-bold text-xs">ID</th>
                                    <th class="px-6 py-4 font-bold text-xs">Portföy</th>
                                    <th class="px-6 py-4 font-bold text-xs">Ödeme Tipi</th>
                                    <th class="px-6 py-4 font-bold text-xs">Tutar (₺)</th>
                                    <th class="px-6 py-4 font-bold text-xs">Son Ödeme</th>
                                    <th class="px-6 py-4 font-bold text-xs">Durum</th>
                                    <th class="px-6 py-4 text-right">Aksiyonlar</th>
                                </tr>
                            </thead>
                            <tbody id="taxes-table-body" class="text-sm">
                            </tbody>
                        </table>
                    </div>
                </div>
            </section>

            <!-- ========================================== -->
            <!-- MAINTENANCE SECTİON -->
            <section id="maintenance-section" class="flex flex-col h-full bg-white hidden">
                <div class="px-8 py-6 border-b border-gray-100 shrink-0">
                    <div class="flex justify-between items-end">
                        <div class="space-y-1">
                            <h2 class="text-2xl font-serif font-bold text-navy">Bakım & Onarım Talepleri</h2>
                            <p class="text-sm text-gray-500">Kiracı veya mülk sahibi tarafından açılan teknik destek ve tadilat talepleri.</p>
                        </div>
                        <button onclick="openMaintenanceModal()" class="bg-navy hover:bg-slate-800 text-white font-bold py-3 px-6 rounded-lg transition-all shadow-xl uppercase tracking-[0.15em] text-xs flex items-center gap-2">
                            <i class="fa-solid fa-screwdriver-wrench text-gold"></i> Talep Oluştur
                        </button>
                    </div>
                </div>

                <div class="flex-1 overflow-auto p-8 relative">
                    <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden relative z-10">
                        <table class="w-full text-left premium-table">
                            <thead>
                                <tr>
                                    <th class="px-6 py-4 font-bold text-xs">Talep No</th>
                                    <th class="px-6 py-4 font-bold text-xs">Portföy</th>
                                    <th class="px-6 py-4 font-bold text-xs">Talep Veren</th>
                                    <th class="px-6 py-4 font-bold text-xs">Tarih</th>
                                    <th class="px-6 py-4 font-bold text-xs">Açıklama Özeti</th>
                                    <th class="px-6 py-4 font-bold text-xs">Durum</th>
                                    <th class="px-6 py-4 text-right">Cevapla</th>
                                </tr>
                            </thead>
                            <tbody id="maintenance-table-body" class="text-sm">
                            </tbody>
                        </table>
                    </div>
                </div>
            </section>
            
            <!-- ========================================== -->
            <!-- APPOINTMENTS SECTİON -->
            <section id="appointments-section" class="flex flex-col h-full bg-white hidden">
                <div class="px-8 py-6 border-b border-gray-100 shrink-0">
                    <div class="flex justify-between items-end">
                        <div class="space-y-1">
                            <h2 class="text-2xl font-serif font-bold text-navy">Randevular ve Keşifler</h2>
                            <p class="text-sm text-gray-500">Oluşturulan gösterim randevularını onaylayın ve takip edin.</p>
                        </div>
                        <button onclick="openAppointmentModal()" class="bg-navy border border-gold hover:bg-slate-800 text-gold font-bold py-3 px-6 rounded-lg transition-all uppercase tracking-[0.15em] text-xs flex items-center gap-2">
                            <i class="fa-regular fa-calendar-plus"></i> Manuel Randevu
                        </button>
                    </div>
                </div>

                <div class="flex-1 overflow-auto p-8 relative">
                    <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden relative z-10">
                        <table class="w-full text-left premium-table">
                            <thead>
                                <tr>
                                    <th class="px-6 py-4 font-bold text-xs">ID</th>
                                    <th class="px-6 py-4 font-bold text-xs">Mülk (Portföy)</th>
                                    <th class="px-6 py-4 font-bold text-xs">Talep Sahibi</th>
                                    <th class="px-6 py-4 font-bold text-xs">Tarih / Saat</th>
                                    <th class="px-6 py-4 font-bold text-xs">Durum</th>
                                    <th class="px-6 py-4 text-right">Aksiyonlar</th>
                                </tr>
                            </thead>
                            <tbody id="appointments-table-body" class="text-sm">
                            </tbody>
                        </table>
                    </div>
                </div>
            </section>
"""

# Insert just before the closing </main> tag
pattern = re.compile(r'(</main>)', re.IGNORECASE)
html = pattern.sub(new_sections + r'\1', html)

with open('portal.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Sections injected.")
