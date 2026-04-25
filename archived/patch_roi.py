import sys

with open('detay.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Inject ROI Calculator section between Section 3 (Features) and Section 4 (Similar)
roi_section = '''
        <!-- Section 3.5: ROI / Yatırım Getirisi Hesaplayıcı -->
        <section class="snap-section bg-white border-t border-gray-100">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full">
                <div class="text-center md:text-left mb-10">
                    <h2 class="text-3xl md:text-4xl font-bold text-navy font-serif mb-2 uppercase tracking-tighter">
                        Yatırım Getirisi Analizi</h2>
                    <div class="w-16 h-1 bg-gold mx-auto md:mx-0 mb-4"></div>
                    <p class="text-gray-400 text-sm font-light">Bu mülkün yatırım potansiyelini anında analiz edin.
                    </p>
                </div>

                <div class="grid grid-cols-1 lg:grid-cols-2 gap-12 items-start">
                    <!-- Sol: Girdiler -->
                    <div class="bg-soft rounded-[2rem] p-8 md:p-10 border border-gray-100 shadow-sm space-y-6">
                        <h3 class="font-bold text-navy uppercase tracking-widest text-xs mb-2"><i
                                class="fa-solid fa-sliders text-gold mr-2"></i> Parametrelerinizi Girin</h3>

                        <div>
                            <label class="block text-xs font-bold text-gray-600 mb-2">Mülk Değeri (₺)</label>
                            <input type="number" id="roi-mulk-degeri" value="35000000"
                                class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-gold/50 focus:border-gold outline-none text-lg font-bold text-navy"
                                oninput="hesaplaROI()">
                        </div>
                        <div>
                            <label class="block text-xs font-bold text-gray-600 mb-2">Peşinat Oranı (%)</label>
                            <input type="range" id="roi-pesinat" min="10" max="100" value="30"
                                class="w-full accent-gold" oninput="hesaplaROI(); document.getElementById('roi-pesinat-label').textContent=this.value+'%'">
                            <span id="roi-pesinat-label" class="text-sm font-bold text-navy">30%</span>
                        </div>
                        <div>
                            <label class="block text-xs font-bold text-gray-600 mb-2">Aylık Beklenen Kira Geliri
                                (₺)</label>
                            <input type="number" id="roi-kira" value="75000"
                                class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-gold/50 focus:border-gold outline-none text-lg font-bold text-navy"
                                oninput="hesaplaROI()">
                        </div>
                        <div>
                            <label class="block text-xs font-bold text-gray-600 mb-2">Yıllık Giderler (Aidat,
                                Bakım, Vergi) (₺)</label>
                            <input type="number" id="roi-gider" value="60000"
                                class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-gold/50 focus:border-gold outline-none text-lg font-bold text-navy"
                                oninput="hesaplaROI()">
                        </div>
                    </div>

                    <!-- Sağ: Sonuçlar -->
                    <div class="space-y-6">
                        <div
                            class="bg-gradient-to-br from-navy to-slate-800 rounded-[2rem] p-8 md:p-10 text-white relative overflow-hidden shadow-2xl">
                            <div class="absolute -right-10 -top-10 text-gold/10 text-[120px]">
                                <i class="fa-solid fa-chart-pie"></i>
                            </div>
                            <div class="absolute inset-0 brand-pattern opacity-10"></div>
                            <div class="relative z-10 space-y-8">
                                <div>
                                    <p class="text-gray-400 text-xs font-bold uppercase tracking-widest mb-1">Yıllık Net
                                        İşletme Geliri (NOI)</p>
                                    <h3 id="roi-noi" class="text-3xl md:text-4xl font-serif font-bold text-gold">
                                        ₺840.000</h3>
                                </div>
                                <div class="grid grid-cols-2 gap-6">
                                    <div class="bg-white/10 rounded-2xl p-5">
                                        <p class="text-gray-400 text-[10px] font-bold uppercase tracking-wider mb-1">
                                            Cap Rate</p>
                                        <h4 id="roi-caprate" class="text-2xl font-bold text-white">2.4%</h4>
                                        <p class="text-gray-500 text-[9px] mt-1">Amortisman Oranı</p>
                                    </div>
                                    <div class="bg-white/10 rounded-2xl p-5">
                                        <p class="text-gray-400 text-[10px] font-bold uppercase tracking-wider mb-1">
                                            Cash-on-Cash</p>
                                        <h4 id="roi-coc" class="text-2xl font-bold text-white">8.0%</h4>
                                        <p class="text-gray-500 text-[9px] mt-1">Nakit Getiri</p>
                                    </div>
                                </div>
                                <div class="bg-white/5 rounded-2xl p-5 flex items-center justify-between">
                                    <div>
                                        <p class="text-gray-400 text-[10px] font-bold uppercase tracking-wider">
                                            Tahmini Kendini Ödeme Süresi</p>
                                        <h4 id="roi-amortisman" class="text-xl font-bold text-gold mt-1">~42 Yıl</h4>
                                    </div>
                                    <i class="fa-solid fa-hourglass-half text-gold/30 text-4xl"></i>
                                </div>
                            </div>
                        </div>
                        <p class="text-[10px] text-gray-400 text-center">
                            <i class="fa-solid fa-circle-info mr-1"></i> Bu hesaplama tahminidir ve değer artışı, vergi
                            avantajları gibi ek faktörleri içermemektedir.
                        </p>
                    </div>
                </div>
            </div>
        </section>
'''

# Find the marker: <!-- Section 4: Buna Bakanlar Buna da Baktı -->
marker = '<!-- Section 4: Buna Bakanlar'
idx = content.find(marker)
if idx == -1:
    print("Could not find Section 4 marker")
    sys.exit(1)

# Also find the </section> just before it
prev_section_end = content.rfind('</section>', 0, idx)
if prev_section_end == -1:
    print("Could not find previous </section>")
    sys.exit(1)

insert_pos = prev_section_end + len('</section>')
content = content[:insert_pos] + '\n' + roi_section + '\n' + content[insert_pos:]

# Add the ROI calculation JS
roi_js = '''
        function hesaplaROI() {
            const mulkDegeri = parseFloat(document.getElementById('roi-mulk-degeri').value) || 0;
            const pesinatOrani = parseFloat(document.getElementById('roi-pesinat').value) / 100;
            const aylikKira = parseFloat(document.getElementById('roi-kira').value) || 0;
            const yillikGider = parseFloat(document.getElementById('roi-gider').value) || 0;

            const yillikKira = aylikKira * 12;
            const noi = yillikKira - yillikGider;
            const capRate = mulkDegeri > 0 ? (noi / mulkDegeri) * 100 : 0;
            const pesinat = mulkDegeri * pesinatOrani;
            const coc = pesinat > 0 ? (noi / pesinat) * 100 : 0;
            const amortisman = noi > 0 ? Math.round(mulkDegeri / noi) : 0;

            document.getElementById('roi-noi').textContent = '₺' + noi.toLocaleString('tr-TR');
            document.getElementById('roi-caprate').textContent = capRate.toFixed(1) + '%';
            document.getElementById('roi-coc').textContent = coc.toFixed(1) + '%';
            document.getElementById('roi-amortisman').textContent = '~' + amortisman + ' Yıl';
        }
        // İlk yüklemede hesapla
        document.addEventListener('DOMContentLoaded', () => { if(document.getElementById('roi-mulk-degeri')) hesaplaROI(); });
'''

# Inject JS before </script> at the bottom
last_script_close = content.rfind('</script>')
if last_script_close != -1:
    content = content[:last_script_close] + roi_js + '\n' + content[last_script_close:]

with open('detay.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("ROI Calculator injected into detay.html!")
