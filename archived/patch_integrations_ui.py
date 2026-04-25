import sys

with open('portal.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Sidebar'a Entegrasyon Merkezi butonu ekle
sidebar_marker = '''<i class="fa-solid fa-money-bill-trend-up w-5 text-center"></i> Hakediş & Komisyon
                </button>'''

sidebar_insert = '''<i class="fa-solid fa-money-bill-trend-up w-5 text-center"></i> Hakediş & Komisyon
                </button>

                <div class="mt-4 mb-2 px-4">
                    <p class="text-[10px] font-bold text-gray-500 uppercase tracking-widest">Entegrasyonlar</p>
                </div>

                <button onclick="showSection('integrations', this)"
                    class="nav-item w-full flex items-center gap-3 px-4 py-3 rounded-lg text-gray-400 hover:text-white hover:bg-white/5 transition-all text-sm font-medium">
                    <i class="fa-solid fa-share-nodes w-5 text-center"></i> Entegrasyon Merkezi
                    <span class="bg-gold/20 text-gold text-[10px] py-0.5 px-2 rounded-full">Yeni</span>
                </button>'''

content = content.replace(sidebar_marker, sidebar_insert)

# 2. Entegrasyon Merkezi section HTML'i
integration_section = '''
            <!-- ========================================== -->
            <!-- ENTEGRASYON MERKEZİ SECTION -->
            <section id="integrations-section" class="content-section flex flex-col h-full bg-white hidden">
                <div class="px-8 py-6 border-b border-gray-100 shrink-0">
                    <div class="flex justify-between items-end">
                        <div class="space-y-1">
                            <h2 class="text-2xl font-serif font-bold text-navy">Entegrasyon Merkezi</h2>
                            <p class="text-sm text-gray-500">İlan siteleri, sosyal medya ve tasarım araçlarına tek noktadan paylaşım.</p>
                        </div>
                        <button onclick="openPublishWizard()"
                            class="bg-navy hover:bg-slate-800 text-gold font-bold py-3 px-6 rounded-lg transition-all text-xs uppercase tracking-widest">
                            <i class="fa-solid fa-paper-plane mr-2"></i> Yeni Paylaşım
                        </button>
                    </div>
                </div>
                <div class="flex-1 overflow-auto p-8">
                    <!-- Platform Kartları -->
                    <div class="mb-8">
                        <h3 class="text-sm font-bold text-navy uppercase tracking-wider mb-4"><i class="fa-solid fa-house-laptop mr-2 text-gold"></i> İlan Siteleri</h3>
                        <div class="grid grid-cols-2 md:grid-cols-4 gap-4" id="listing-platforms-grid"></div>
                    </div>
                    <div class="mb-8">
                        <h3 class="text-sm font-bold text-navy uppercase tracking-wider mb-4"><i class="fa-brands fa-instagram mr-2 text-gold"></i> Sosyal Medya</h3>
                        <div class="grid grid-cols-2 md:grid-cols-6 gap-4" id="social-platforms-grid"></div>
                    </div>
                    <div class="mb-8">
                        <h3 class="text-sm font-bold text-navy uppercase tracking-wider mb-4"><i class="fa-solid fa-palette mr-2 text-gold"></i> Tasarım Araçları</h3>
                        <div class="grid grid-cols-2 md:grid-cols-4 gap-4" id="design-platforms-grid"></div>
                    </div>

                    <!-- Son Paylaşımlar -->
                    <div class="mt-8">
                        <h3 class="text-sm font-bold text-navy uppercase tracking-wider mb-4"><i class="fa-solid fa-clock-rotate-left mr-2 text-gold"></i> Son Paylaşımlar</h3>
                        <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
                            <table class="w-full text-left">
                                <thead>
                                    <tr class="border-b border-gray-100 text-[10px] uppercase font-bold text-gray-500 tracking-wider">
                                        <th class="px-6 py-3">Portföy</th>
                                        <th class="px-6 py-3">Platform</th>
                                        <th class="px-6 py-3">Tarih</th>
                                        <th class="px-6 py-3">Durum</th>
                                    </tr>
                                </thead>
                                <tbody id="publications-table-body" class="text-sm"></tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </section>
'''

# payroll-section'dan önce ekle
payroll_marker = '<!-- PAYROLL'
content = content.replace(payroll_marker, integration_section + '\n            ' + payroll_marker)

# 3. Paylaşım sihirbazı modal HTML'i
publish_modal = '''
    <!-- PAYLAŞIM SİHİRBAZI MODALI -->
    <div id="publish-wizard-modal" class="fixed inset-0 bg-black/60 backdrop-blur-sm z-[100] hidden flex items-center justify-center">
        <div class="bg-white rounded-[2rem] w-full max-w-2xl max-h-[90vh] overflow-auto p-8 shadow-2xl relative">
            <button onclick="closePublishWizard()" class="absolute top-6 right-6 text-gray-400 hover:text-navy transition-colors">
                <i class="fa-solid fa-xmark text-xl"></i>
            </button>
            <h3 class="text-2xl font-serif font-bold text-navy mb-6"><i class="fa-solid fa-paper-plane text-gold mr-2"></i> Paylaşım Oluştur</h3>

            <!-- Adım 1: Portföy Seç -->
            <div id="pub-step-1">
                <label class="block text-xs font-bold text-gray-600 mb-2 uppercase tracking-wider">1. Portföy Seçin</label>
                <select id="pub-property-select" class="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-gold/50 focus:border-gold outline-none text-navy font-medium mb-4">
                    <option value="">Yükleniyor...</option>
                </select>

                <label class="block text-xs font-bold text-gray-600 mb-2 uppercase tracking-wider">2. Platform Seçin</label>
                <div class="grid grid-cols-3 gap-3 mb-6" id="pub-platform-selector"></div>

                <button onclick="generatePreview()" class="w-full bg-navy hover:bg-slate-800 text-gold py-3 rounded-xl font-bold text-sm uppercase tracking-widest transition-all">
                    <i class="fa-solid fa-wand-magic-sparkles mr-2"></i> Şablon Oluştur
                </button>
            </div>

            <!-- Adım 2: Önizleme ve Düzenleme -->
            <div id="pub-step-2" class="hidden">
                <div class="flex items-center gap-2 mb-4">
                    <button onclick="showPubStep(1)" class="text-gray-400 hover:text-navy"><i class="fa-solid fa-arrow-left"></i></button>
                    <span class="text-xs font-bold text-gray-600 uppercase tracking-wider">Önizleme & Düzenleme</span>
                </div>
                <div id="pub-platform-badge" class="inline-flex items-center gap-2 bg-gray-100 rounded-full px-4 py-2 mb-4 text-sm font-bold"></div>
                
                <label class="block text-xs font-bold text-gray-600 mb-1 uppercase tracking-wider">Başlık</label>
                <input type="text" id="pub-title" class="w-full px-4 py-3 border border-gray-200 rounded-xl mb-4 outline-none focus:ring-2 focus:ring-gold/50 font-medium text-navy">

                <label class="block text-xs font-bold text-gray-600 mb-1 uppercase tracking-wider">İçerik</label>
                <textarea id="pub-content" rows="10" class="w-full px-4 py-3 border border-gray-200 rounded-xl mb-4 outline-none focus:ring-2 focus:ring-gold/50 font-mono text-sm resize-none"></textarea>

                <div class="flex gap-3">
                    <button onclick="copyToClipboard()" class="flex-1 bg-gray-100 hover:bg-gray-200 text-navy py-3 rounded-xl font-bold text-sm uppercase tracking-widest transition-all">
                        <i class="fa-regular fa-copy mr-2"></i> Kopyala
                    </button>
                    <button onclick="publishAndSave()" class="flex-1 bg-navy hover:bg-slate-800 text-gold py-3 rounded-xl font-bold text-sm uppercase tracking-widest transition-all">
                        <i class="fa-solid fa-paper-plane mr-2"></i> Yayınla & Kaydet
                    </button>
                </div>
            </div>
        </div>
    </div>
'''

content = content.replace('</body>', publish_modal + '\n</body>')

# 4. JS fonksiyonları ekle
integration_js = '''
        // --- ENTEGRASYON MERKEZİ LOGİĞİ ---
        const PLATFORM_URLS = {
            sahibinden: 'https://www.sahibinden.com',
            hepsiemlak: 'https://www.hepsiemlak.com',
            emlakjet: 'https://www.emlakjet.com',
            n11emlak: 'https://www.n11.com/emlak',
            instagram: 'https://www.instagram.com',
            facebook: 'https://www.facebook.com',
            youtube: 'https://studio.youtube.com',
            tiktok: 'https://www.tiktok.com',
            linkedin: 'https://www.linkedin.com',
            x_twitter: 'https://x.com',
            canva: 'https://www.canva.com/design/create'
        };

        async function fetchIntegrations() {
            try {
                // Platform kartlarını doldur
                const platRes = await fetch(`${API_BASE}/platforms`);
                const platforms = await platRes.json();

                // İlan siteleri
                const listingGrid = document.getElementById('listing-platforms-grid');
                listingGrid.innerHTML = '';
                (platforms.listing || []).forEach(p => {
                    listingGrid.innerHTML += buildPlatformCard(p, false);
                });

                // Sosyal medya
                const socialGrid = document.getElementById('social-platforms-grid');
                socialGrid.innerHTML = '';
                (platforms.social || []).forEach(p => {
                    socialGrid.innerHTML += buildPlatformCard(p, true);
                });

                // Tasarım araçları
                const designGrid = document.getElementById('design-platforms-grid');
                designGrid.innerHTML = '';
                (platforms.design || []).forEach(p => {
                    designGrid.innerHTML += buildPlatformCard(p, false);
                });

                // Son paylaşımlar
                const pubRes = await fetch(`${API_BASE}/publications`);
                const pubs = await pubRes.json();
                const pubBody = document.getElementById('publications-table-body');
                pubBody.innerHTML = '';
                if (pubs.length === 0) {
                    pubBody.innerHTML = '<tr><td colspan="4" class="px-6 py-8 text-center text-gray-400">Henüz paylaşım yapılmadı.</td></tr>';
                } else {
                    pubs.forEach(pub => {
                        pubBody.innerHTML += `
                            <tr class="border-b border-gray-50 hover:bg-gray-50">
                                <td class="px-6 py-3 font-bold text-navy">${pub.baslik1 || '-'}</td>
                                <td class="px-6 py-3"><span class="bg-navy/5 text-navy px-2 py-1 rounded text-[10px] font-bold uppercase">${pub.platform_name}</span></td>
                                <td class="px-6 py-3 text-gray-500 text-xs">${pub.published_at || pub.created_at}</td>
                                <td class="px-6 py-3"><span class="bg-green-100 text-green-700 px-2 py-1 rounded text-[10px] font-bold">Yayınlandı</span></td>
                            </tr>
                        `;
                    });
                }
            } catch(e) { console.error('Entegrasyon hatası:', e); }
        }

        function buildPlatformCard(p, isBrand) {
            const iconPrefix = isBrand ? 'fa-brands' : 'fa-solid';
            return `
                <div class="border border-gray-100 rounded-2xl p-5 hover:shadow-lg hover:border-gray-200 transition-all cursor-pointer group text-center"
                     onclick="window.open('${PLATFORM_URLS[p.key] || '#'}', '_blank')">
                    <div class="w-12 h-12 rounded-xl flex items-center justify-center mx-auto mb-3 group-hover:scale-110 transition-transform"
                         style="background:${p.color}15; color:${p.color}">
                        <i class="${iconPrefix} ${p.icon} text-xl"></i>
                    </div>
                    <p class="font-bold text-navy text-sm">${p.name}</p>
                    <p class="text-[10px] text-gray-400 mt-1 uppercase tracking-wider">Manuel</p>
                </div>
            `;
        }

        // Paylaşım sihirbazı
        let selectedPubPlatform = '';
        let selectedPubPropertyId = '';

        async function openPublishWizard() {
            document.getElementById('publish-wizard-modal').classList.remove('hidden');
            showPubStep(1);

            // Portföyleri yükle
            const token = localStorage.getItem('imza_admin_token');
            try {
                const res = await fetch(`${API_BASE}/contract-builder/properties`, { headers: {'Authorization': `Bearer ${token}`} });
                const props = await res.json();
                const select = document.getElementById('pub-property-select');
                select.innerHTML = '<option value="">Portföy seçin...</option>';
                props.forEach(p => {
                    select.innerHTML += `<option value="${p.id}">${p.baslik1} (${p.refNo})</option>`;
                });
            } catch(e) { console.error(e); }

            // Platform seçici
            const platRes = await fetch(`${API_BASE}/platforms`);
            const platforms = await platRes.json();
            const container = document.getElementById('pub-platform-selector');
            container.innerHTML = '';
            const allPlats = [...(platforms.listing||[]), ...(platforms.social||[]), ...(platforms.design||[])];
            allPlats.forEach(p => {
                const iconPfx = p.brand ? 'fa-brands' : 'fa-solid';
                container.innerHTML += `
                    <button onclick="selectPubPlatform('${p.key}', this)" 
                        class="pub-plat-btn border-2 border-gray-100 rounded-xl p-3 text-center hover:border-navy/30 transition-all"
                        data-platform="${p.key}">
                        <i class="${iconPfx} ${p.icon} text-lg" style="color:${p.color}"></i>
                        <p class="text-[10px] font-bold text-navy mt-1">${p.name}</p>
                    </button>
                `;
            });
        }

        function closePublishWizard() {
            document.getElementById('publish-wizard-modal').classList.add('hidden');
        }

        function showPubStep(step) {
            document.getElementById('pub-step-1').classList.toggle('hidden', step !== 1);
            document.getElementById('pub-step-2').classList.toggle('hidden', step !== 2);
        }

        function selectPubPlatform(key, btn) {
            selectedPubPlatform = key;
            document.querySelectorAll('.pub-plat-btn').forEach(b => b.classList.remove('border-navy', 'bg-navy/5'));
            btn.classList.add('border-navy', 'bg-navy/5');
        }

        async function generatePreview() {
            selectedPubPropertyId = document.getElementById('pub-property-select').value;
            if (!selectedPubPropertyId) { alert('Lütfen bir portföy seçin.'); return; }
            if (!selectedPubPlatform) { alert('Lütfen bir platform seçin.'); return; }

            try {
                const res = await fetch(`${API_BASE}/publish/generate`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({ property_id: selectedPubPropertyId, platform: selectedPubPlatform })
                });
                const data = await res.json();

                document.getElementById('pub-title').value = data.title || '';
                document.getElementById('pub-content').value = data.description || '';
                document.getElementById('pub-platform-badge').innerHTML = `<span style="font-size:14px">${selectedPubPlatform.toUpperCase()}</span>`;
                showPubStep(2);
            } catch(e) { console.error(e); alert('Şablon oluşturma hatası.'); }
        }

        function copyToClipboard() {
            const title = document.getElementById('pub-title').value;
            const content = document.getElementById('pub-content').value;
            navigator.clipboard.writeText(title + '\\n\\n' + content).then(() => {
                alert('İçerik panoya kopyalandı! Şimdi ilgili platforma yapıştırabilirsiniz.');
            });
        }

        async function publishAndSave() {
            const content = document.getElementById('pub-content').value;
            try {
                const res = await fetch(`${API_BASE}/publish`, {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        property_id: selectedPubPropertyId,
                        platform_name: selectedPubPlatform,
                        content_type: 'listing',
                        generated_text: content,
                        status: 'published'
                    })
                });
                if (res.ok) {
                    alert('Paylaşım kaydedildi!');
                    closePublishWizard();
                    fetchIntegrations();
                    // Platforma yönlendir
                    const url = PLATFORM_URLS[selectedPubPlatform];
                    if (url) window.open(url, '_blank');
                }
            } catch(e) { console.error(e); }
        }
'''

# showSection genişletmesi
old_show = "if (sectionId === 'payroll') fetchPayroll();"
new_show = "if (sectionId === 'payroll') fetchPayroll();\n            if (sectionId === 'integrations') fetchIntegrations();"
content = content.replace(old_show, new_show)

# JS'yi </script> öncesine ekle (son script bloğundaki)
# Find the last occurrence of the inspection-data script
marker = "// --- HAKEDİŞ & KOMİSYON LOGİĞİ ---"
content = content.replace(marker, integration_js + '\n\n        ' + marker)

with open('portal.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Entegrasyon Merkezi UI tamamlandı!")
