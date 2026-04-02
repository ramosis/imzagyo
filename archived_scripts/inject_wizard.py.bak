import re

with open('portal.html', 'r', encoding='utf-8') as f:
    html = f.read()

# --- NEW JS LOGIC ---
new_js = """
        // ==========================================
        // YENİ WIZARD: PORTFOLIO CMS JS MANTIĞI
        // ==========================================
        let currentWizStep = 1;
        const totalWizSteps = 4;

        function renderInspectionChecklists(mulk_tipi) {
            const container = document.getElementById('dynamic-inspection-container');
            container.innerHTML = '';
            
            let groupKey = "Grup_1"; // Default Konut
            if (mulk_tipi === "Ticari" || mulk_tipi === "Endüstriyel") groupKey = "Grup_2";
            if (mulk_tipi === "Arsa" || mulk_tipi === "Arazi") groupKey = "Grup_3";

            if (!typeof inspectionData !== 'undefined' && inspectionData[groupKey]) {
                const group = inspectionData[groupKey];
                let html = `<p class="text-[10px] text-gray-500 mb-4 bg-gray-100 p-2 rounded">Denetim Grubu: <b>${group.title}</b></p>`;
                
                group.categories.forEach((cat, cIdx) => {
                    html += `<div class="mb-6 border-l-2 border-gold pl-3">`;
                    html += `<h4 class="text-xs font-bold text-navy mb-3">${cat.name}</h4>`;
                    
                    cat.questions.forEach((q, qIdx) => {
                        const qId = `q_${groupKey}_${cIdx}_${qIdx}`;
                        html += `
                        <div class="mb-3 p-3 bg-gray-50 rounded-lg border border-gray-100 hover:border-gold/30 transition-colors">
                            <p class="text-[10px] font-medium text-gray-700 mb-2">${q}</p>
                            <div class="flex gap-2">
                                <label class="cursor-pointer group flex items-center justify-center bg-green-50 hover:bg-green-100 border border-green-200 rounded px-2 py-1 flex-1">
                                    <input type="radio" name="${qId}" value="1" class="hidden peer">
                                    <span class="text-[9px] font-bold text-green-700 peer-checked:bg-green-600 peer-checked:text-white px-2 py-1 rounded w-full text-center transition-all">İyi (1)</span>
                                </label>
                                <label class="cursor-pointer group flex items-center justify-center bg-yellow-50 hover:bg-yellow-100 border border-yellow-200 rounded px-2 py-1 flex-1">
                                    <input type="radio" name="${qId}" value="2" class="hidden peer">
                                    <span class="text-[9px] font-bold text-yellow-700 peer-checked:bg-yellow-500 peer-checked:text-white px-2 py-1 rounded w-full text-center transition-all">Bakım (2)</span>
                                </label>
                                <label class="cursor-pointer group flex items-center justify-center bg-red-50 hover:bg-red-100 border border-red-200 rounded px-2 py-1 flex-1">
                                    <input type="radio" name="${qId}" value="3" class="hidden peer">
                                    <span class="text-[9px] font-bold text-red-700 peer-checked:bg-red-600 peer-checked:text-white px-2 py-1 rounded w-full text-center transition-all">Risk (3)</span>
                                </label>
                                <label class="cursor-pointer group flex items-center justify-center bg-gray-100 hover:bg-gray-200 border border-gray-200 rounded px-2 py-1 flex-1">
                                    <input type="radio" name="${qId}" value="0" class="hidden peer" checked>
                                    <span class="text-[9px] font-bold text-gray-500 peer-checked:bg-gray-500 peer-checked:text-white px-2 py-1 rounded w-full text-center transition-all">Bilinmiyor (0)</span>
                                </label>
                            </div>
                        </div>
                        `;
                    });
                    html += `</div>`;
                });
                container.innerHTML = html;
            } else {
                container.innerHTML = '<p class="text-xs text-red-500">Denetim verisi bulunamadı.</p>';
            }
        }

        // Collect answers from generated radio buttons
        function collectInspectionData() {
            const container = document.getElementById('dynamic-inspection-container');
            const inputs = container.querySelectorAll('input[type="radio"]:checked');
            const result = {};
            inputs.forEach(input => {
                const questionText = input.closest('.mb-3').querySelector('p').innerText;
                result[questionText] = input.value;
            });
            return result;
        }

        function restoreInspectionData(mulk_tipi, jsonStr) {
            renderInspectionChecklists(mulk_tipi);
            if (!jsonStr) return;
            try {
                const answers = JSON.parse(jsonStr);
                const container = document.getElementById('dynamic-inspection-container');
                const pElements = container.querySelectorAll('p.text-\\\\[10px\\\\]');
                pElements.forEach(p => {
                    const qText = p.innerText;
                    if (answers[qText] !== undefined) {
                        const val = answers[qText];
                        const inputs = p.parentElement.querySelectorAll(`input[value="${val}"]`);
                        if (inputs.length > 0) inputs[0].checked = true;
                    }
                });
            } catch (e) { console.warn("Restore error", e); }
        }

        // --- UPLOAD MANTIĞI ---
        async function handleImageUpload(inputId, hiddenUrlId, previewId) {
            const fileInput = document.getElementById(inputId);
            const file = fileInput.files[0];
            if (!file) return;

            const token = localStorage.getItem('imza_admin_token');
            const formData = new FormData();
            formData.append('image', file);

            const label = document.getElementById(inputId + '-label');
            label.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Yükleniyor...`;

            try {
                const res = await fetch(`${API_BASE}/upload-image`, {
                    method: 'POST',
                    headers: { 'Authorization': `Bearer ${token}` },
                    body: formData
                });
                if (res.ok) {
                    const data = await res.json();
                    document.getElementById(hiddenUrlId).value = data.url;
                    document.getElementById(previewId).src = data.url;
                    document.getElementById(previewId).classList.remove('hidden');
                    label.innerHTML = `<i class="fa-solid fa-check text-green-500"></i> Yüklendi!`;
                } else {
                    alert("Yükleme başarısız oldu.");
                    label.innerHTML = `Tekrar Dene`;
                }
            } catch(e) {
                console.error("Upload error", e);
                label.innerHTML = `Hata Oluştu`;
            }
        }


        function updateWizUI() {
            for(let i=1; i<=totalWizSteps; i++) {
                const stepDiv = document.getElementById(`wiz-step-${i}`);
                if (!stepDiv) continue;
                
                // Indicators
                const ind = document.getElementById(`step-ind-${i}`);
                if (ind) {
                    if (i <= currentWizStep) {
                        ind.classList.remove('bg-gray-200');
                        ind.classList.add('bg-gold');
                    } else {
                        ind.classList.add('bg-gray-200');
                        ind.classList.remove('bg-gold');
                    }
                }

                if (i === currentWizStep) {
                    stepDiv.classList.remove('hidden');
                    // Gecikmeli opacity
                    setTimeout(() => {
                        stepDiv.classList.remove('opacity-0', 'translate-x-[10px]', 'pointer-events-none');
                        stepDiv.classList.add('opacity-100', 'translate-x-0');
                    }, 50);
                } else {
                    stepDiv.classList.add('opacity-0', 'translate-x-[10px]', 'pointer-events-none');
                    // Animasyon bitince display none yapıp akışı rahatlat
                    setTimeout(() => {
                        if (i !== currentWizStep) stepDiv.classList.add('hidden');
                    }, 300);
                }
            }

            const prevBtn = document.getElementById('wiz-prev-btn');
            const nextBtn = document.getElementById('wiz-next-btn');
            const saveBtn = document.getElementById('wiz-save-btn');

            if (currentWizStep === 1) {
                prevBtn.classList.add('hidden');
            } else {
                prevBtn.classList.remove('hidden');
            }

            if (currentWizStep === totalWizSteps) {
                nextBtn.classList.add('hidden');
                saveBtn.classList.remove('hidden');
            } else {
                nextBtn.classList.remove('hidden');
                saveBtn.classList.add('hidden');
            }
        }

        function wizNext() {
            if (currentWizStep === 2) {
                const tip = document.getElementById('pf-mulktipi').value;
                renderInspectionChecklists(tip);
            }
            if (currentWizStep < totalWizSteps) {
                currentWizStep++;
                updateWizUI();
            }
        }

        function wizPrev() {
            if (currentWizStep > 1) {
                currentWizStep--;
                updateWizUI();
            }
        }

        function openPortfolioModal(editData = null) {
            const backdrop = document.getElementById('portfolio-modal-backdrop');
            const modal = document.getElementById('portfolio-slide-over');
            const title = document.getElementById('portfolio-modal-title');

            currentWizStep = 1;

            if (editData) {
                title.innerText = "Portföy Düzenle";
                document.getElementById('pf-id').value = editData.id;
                document.getElementById('pf-id').disabled = true;

                document.getElementById('pf-mulktipi').value = editData.mulk_tipi || 'Konut';
                document.getElementById('pf-koleksiyon').value = editData.koleksiyon;
                document.getElementById('pf-baslik1').value = editData.baslik1;
                document.getElementById('pf-baslik2').value = editData.baslik2;
                document.getElementById('pf-lokasyon').value = editData.lokasyon;
                document.getElementById('pf-refno').value = editData.refNo;
                document.getElementById('pf-fiyat').value = editData.fiyat;

                document.getElementById('pf-oda').value = editData.oda;
                document.getElementById('pf-alan').value = editData.alan;
                document.getElementById('pf-kat').value = editData.kat;

                document.getElementById('pf-icon-renk').value = editData.icon_renk;
                document.getElementById('pf-resim-hero').value = editData.resim_hero;
                document.getElementById('pf-resim-hikaye').value = editData.resim_hikaye;
                document.getElementById('pf-hikaye').value = editData.hikaye;

                document.getElementById('pf-ozellikler').value = editData.ozellikler ? editData.ozellikler.join(', ') : '';

                document.getElementById('pf-danisman-isim').value = editData.danisman_isim;
                document.getElementById('pf-danisman-unvan').value = editData.danisman_unvan;
                document.getElementById('pf-danisman-resim').value = editData.danisman_resim;

                restoreInspectionData(editData.mulk_tipi || 'Konut', editData.denetim_notlari);
            } else {
                title.innerText = "Yeni İlan Ekle (Sihirbaz)";
                document.getElementById('portfolio-form').reset();
                document.getElementById('pf-id').disabled = false;
                document.getElementById('pf-id').value = `IMZ-${Math.floor(Math.random() * 1000)}`;
                renderInspectionChecklists('Konut'); // Default render
                
                // Reset Preview Images
                document.getElementById('preview-hero').src = '';
                document.getElementById('preview-hero').classList.add('hidden');
                document.getElementById('pf-upload-hero-label').innerHTML = 'Yerel Dosya Seç';
            }

            updateWizUI();

            backdrop.classList.remove('hidden');
            setTimeout(() => {
                backdrop.classList.remove('opacity-0');
                modal.classList.remove('translate-x-full');
            }, 10);
        }

        function closePortfolioModal() {
            const backdrop = document.getElementById('portfolio-modal-backdrop');
            const modal = document.getElementById('portfolio-slide-over');

            backdrop.classList.add('opacity-0');
            modal.classList.add('translate-x-full');

            setTimeout(() => {
                backdrop.classList.add('hidden');
            }, 500);
        }

        function editPortfolio(data) {
            openPortfolioModal(data);
        }

        async function savePortfolio() {
            const token = localStorage.getItem('imza_admin_token');
            if (!token) return alert("Oturum süreniz dolmuş, lütfen tekrar giriş yapın.");

            const isEdit = document.getElementById('pf-id').disabled;
            const id = document.getElementById('pf-id').value;
            const ozelliklerStr = document.getElementById('pf-ozellikler').value;
            const ozellikler = ozelliklerStr.split(',').map(s => s.trim()).filter(s => s.length > 0);
            const denetimNotlari = collectInspectionData();

            const data = {
                id: id,
                mulk_tipi: document.getElementById('pf-mulktipi').value,
                koleksiyon: document.getElementById('pf-koleksiyon').value,
                baslik1: document.getElementById('pf-baslik1').value,
                baslik2: document.getElementById('pf-baslik2').value,
                lokasyon: document.getElementById('pf-lokasyon').value,
                refNo: document.getElementById('pf-refno').value,
                fiyat: document.getElementById('pf-fiyat').value,

                oda: document.getElementById('pf-oda').value,
                alan: document.getElementById('pf-alan').value,
                kat: document.getElementById('pf-kat').value,

                ozellik_renk: "text-gold", 
                bg_renk: "bg-navy",
                btn_renk: "bg-gold hover:bg-yellow-600 shadow-gold/20",
                icon_renk: document.getElementById('pf-icon-renk').value || "border-gold",

                resim_hero: document.getElementById('pf-resim-hero').value,
                resim_hikaye: document.getElementById('pf-resim-hikaye').value,
                hikaye: document.getElementById('pf-hikaye').value,
                ozellikler: ozellikler,
                denetim_notlari: JSON.stringify(denetimNotlari),

                danisman_isim: document.getElementById('pf-danisman-isim').value,
                danisman_unvan: document.getElementById('pf-danisman-unvan').value,
                danisman_resim: document.getElementById('pf-danisman-resim').value
            };

            const method = isEdit ? 'PUT' : 'POST';
            const url = isEdit ? `${API_BASE}/portfoyler/${id}` : `${API_BASE}/portfoyler`;

            try {
                const res = await fetch(url, {
                    method: method,
                    headers: { 'Content-Type': 'application/json', 'Authorization': `Bearer ${token}` },
                    body: JSON.stringify(data)
                });
                if (res.ok) {
                    closePortfolioModal();
                    fetchAllPortfolios();
                    fetchPortfoliosForDashboard();
                } else if (res.status === 403) {
                    alert("Yetkiniz yok.");
                } else alert("Hata oluştu.");
            } catch (err) { console.error(err); }
        }

        async function deletePortfolio(id) {
            const token = localStorage.getItem('imza_admin_token');
            if (confirm(`Referens No: ${id} tamamen silinecek?`)) {
                try {
                    const res = await fetch(`${API_BASE}/portfoyler/${id}`, {
                        method: 'DELETE', headers: { 'Authorization': `Bearer ${token}` }
                    });
                    if (res.ok) {
                        fetchAllPortfolios();
                        fetchPortfoliosForDashboard();
                    } else alert("Silme başarısız.");
                } catch (err) { console.error(err); }
            }
        }
"""

# --- NEW HTML LOGIC ---
new_html = """
<!-- ============================================== -->
<!-- PORTFOLIO WIZARD MODAL -->
<!-- ============================================== -->
<div id="portfolio-modal-backdrop" class="fixed inset-0 bg-navy/60 backdrop-blur-sm z-40 hidden transition-opacity duration-300 opacity-0" onclick="closePortfolioModal()"></div>

<div id="portfolio-slide-over" class="fixed top-0 right-0 min-h-screen w-full max-w-2xl bg-white/95 backdrop-blur-xl shadow-2xl z-50 transform translate-x-full transition-transform duration-500 cubic-bezier(0.16, 1, 0.3, 1) border-l border-white/20 flex flex-col">
    <!-- Dekoratif Üst Çizgi -->
    <div class="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-navy via-modern to-gold"></div>

    <div class="flex items-center justify-between p-6 border-b border-gray-100 shrink-0">
        <div>
            <h2 id="portfolio-modal-title" class="text-xl font-serif font-bold text-navy">Yeni İlan Ekle</h2>
            <!-- Step Indicators -->
            <div class="flex gap-1 mt-2">
                <div id="step-ind-1" class="w-8 h-1 bg-gold rounded transition-colors"></div>
                <div id="step-ind-2" class="w-8 h-1 bg-gray-200 rounded transition-colors"></div>
                <div id="step-ind-3" class="w-8 h-1 bg-gray-200 rounded transition-colors"></div>
                <div id="step-ind-4" class="w-8 h-1 bg-gray-200 rounded transition-colors"></div>
            </div>
        </div>
        <button onclick="closePortfolioModal()" class="w-8 h-8 flex items-center justify-center rounded-full bg-gray-50 text-gray-400 hover:text-navy hover:bg-gray-100 transition-colors">
            <i class="fa-solid fa-xmark"></i>
        </button>
    </div>

    <div class="flex-1 overflow-x-hidden overflow-y-auto p-0 relative">
        <form id="portfolio-form" class="h-full">
            
            <!-- STEP 1 -->
            <div id="wiz-step-1" class="p-6 transition-all duration-300 absolute inset-0 bg-transparent">
                <p class="text-xs font-bold text-gold uppercase tracking-widest mb-4"><i class="fa-solid fa-circle-info mr-2"></i> Adım 1: Temel Kimlik</p>
                
                <div class="grid grid-cols-2 gap-4 mb-4">
                    <div>
                        <label class="block text-[10px] font-bold text-navy uppercase tracking-wider mb-2">Sistem ID (URL Path)</label>
                        <input type="text" id="pf-id" class="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg focus:border-gold text-sm" placeholder="imz-doga-evleri" required>
                    </div>
                    <div>
                        <label class="block text-[10px] font-bold text-navy uppercase tracking-wider mb-2">Referans No</label>
                        <input type="text" id="pf-refno" class="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm" placeholder="IMZ-1234">
                    </div>
                </div>

                <div class="grid grid-cols-2 gap-4 mb-4">
                    <div>
                        <label class="block text-[10px] font-bold text-navy uppercase tracking-wider mb-2">Koleksiyon</label>
                        <select id="pf-koleksiyon" class="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm">
                            <option value="Prestij Koleksiyonu">Prestij Koleksiyonu</option>
                            <option value="Modern Koleksiyon">Modern Koleksiyon</option>
                            <option value="Doğa Koleksiyonu">Doğa Koleksiyonu</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-[10px] font-bold text-navy uppercase tracking-wider mb-2">Mülk Tipi (Ekspertiz İçin)</label>
                        <select id="pf-mulktipi" class="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm border-gold bg-gold/5">
                            <option value="Konut">Konut (Daire/Villa)</option>
                            <option value="Ticari">Ticari/Endüstriyel</option>
                            <option value="Arsa">Arsa/Arazi</option>
                        </select>
                    </div>
                </div>
                
                <div class="space-y-4">
                    <input type="text" id="pf-fiyat" class="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm" placeholder="Fiyat (Örn: 15.500.000 ₺)">
                    <input type="text" id="pf-baslik1" class="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm" placeholder="Ana Başlık (Örn: Boğaz Manzaralı)">
                    <input type="text" id="pf-baslik2" class="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm" placeholder="Alt Başlık (Örn: Modern Villa)">
                    <input type="text" id="pf-lokasyon" class="w-full px-4 py-2 bg-gray-50 border border-gray-200 rounded-lg text-sm" placeholder="Tam Lokasyon (Örn: İSTANBUL, SARIYER)">
                </div>
            </div>

            <!-- STEP 2 -->
            <div id="wiz-step-2" class="p-6 transition-all duration-300 absolute inset-0 bg-transparent opacity-0 translate-x-[10px] pointer-events-none hidden">
                <p class="text-xs font-bold text-gold uppercase tracking-widest mb-4"><i class="fa-solid fa-house mr-2"></i> Adım 2: Fiziksel Metrikler</p>
                
                <div class="grid grid-cols-3 gap-4 mb-4">
                    <div>
                        <label class="block text-[10px] font-bold text-gray-500 uppercase tracking-wider mb-2">Oda/Bölüm</label>
                        <input type="text" id="pf-oda" class="w-full px-4 py-2 bg-gray-50 border rounded-lg text-sm" placeholder="4+1">
                    </div>
                    <div>
                        <label class="block text-[10px] font-bold text-gray-500 uppercase tracking-wider mb-2">Alan (m²)</label>
                        <input type="text" id="pf-alan" class="w-full px-4 py-2 bg-gray-50 border rounded-lg text-sm" placeholder="250 m²">
                    </div>
                    <div>
                        <label class="block text-[10px] font-bold text-gray-500 uppercase tracking-wider mb-2">Kat</label>
                        <input type="text" id="pf-kat" class="w-full px-4 py-2 bg-gray-50 border rounded-lg text-sm" placeholder="2">
                    </div>
                </div>

                <div class="space-y-4">
                    <div>
                        <label class="block text-[10px] font-bold text-gray-500 uppercase mb-2">Ekstra Özellikler (Virgülle)</label>
                        <textarea id="pf-ozellikler" rows="2" class="w-full px-4 py-2 bg-gray-50 border rounded-lg text-sm" placeholder="Güvenlik, Havuz..."></textarea>
                    </div>
                    <div>
                        <label class="block text-[10px] font-bold text-gray-500 uppercase mb-2">Detaylı Hikaye Metni</label>
                        <textarea id="pf-hikaye" rows="4" class="w-full px-4 py-2 bg-gray-50 border rounded-lg text-sm"></textarea>
                    </div>
                    <div>
                        <label class="block text-[10px] font-bold text-gray-500 uppercase mb-2">Vurgu İkon CSS</label>
                        <input type="text" id="pf-icon-renk" class="w-full px-4 py-2 bg-gray-50 border rounded-lg text-sm" placeholder="border-gold">
                    </div>
                </div>
            </div>

            <!-- STEP 3 -->
            <div id="wiz-step-3" class="p-6 transition-all duration-300 absolute inset-0 bg-transparent opacity-0 translate-x-[10px] pointer-events-none hidden overflow-y-auto pb-20">
                <p class="text-xs font-bold text-gold uppercase tracking-widest mb-4"><i class="fa-solid fa-clipboard-check mr-2"></i> Adım 3: Denetim ve Ekspertiz</p>
                <div id="dynamic-inspection-container">
                    <!-- JS Dinamik Gömme Yeri -->
                </div>
            </div>

            <!-- STEP 4 -->
            <div id="wiz-step-4" class="p-6 transition-all duration-300 absolute inset-0 bg-transparent opacity-0 translate-x-[10px] pointer-events-none hidden">
                <p class="text-xs font-bold text-gold uppercase tracking-widest mb-4"><i class="fa-regular fa-images mr-2"></i> Adım 4: Medya & Arşiv</p>
                
                <div class="mb-6">
                    <label class="block text-[10px] font-bold text-navy uppercase tracking-wider mb-2">Hero / Vitrin Görseli</label>
                    <div class="flex gap-2">
                        <input type="text" id="pf-resim-hero" class="w-full px-4 py-2 bg-gray-50 border rounded-lg text-sm flex-1" placeholder="Dış URL (veya Yükle)">
                        
                        <!-- LOCAL UPLOAD BUTTON -->
                        <div class="relative overflow-hidden inline-block shrink-0">
                          <button type="button" class="bg-navy hover:bg-slate-800 text-white px-4 py-2 rounded-lg text-xs font-bold w-32 h-full" id="pf-upload-hero-label">Yerel Dosya Seç</button>
                          <input type="file" id="pf-upload-hero" class="absolute left-0 top-0 opacity-0 cursor-pointer h-full" accept="image/*" onchange="handleImageUpload('pf-upload-hero', 'pf-resim-hero', 'preview-hero')">
                        </div>
                    </div>
                    <img id="preview-hero" class="mt-2 h-24 rounded-lg object-cover hidden" src="" />
                </div>

                <div class="mb-6">
                    <label class="block text-[10px] font-bold text-gray-500 uppercase tracking-wider mb-2">Hikaye / İç Görsel (Dış URL)</label>
                    <input type="text" id="pf-resim-hikaye" class="w-full px-4 py-2 bg-gray-50 border rounded-lg text-sm" placeholder="https://...">
                </div>

                <div class="border-t border-gray-100 pt-5">
                    <p class="text-xs font-bold text-gold uppercase tracking-widest mb-4"><i class="fa-solid fa-user-tie mr-2"></i> Sorumlu Danışman</p>
                    <div class="grid grid-cols-2 gap-4 mb-4">
                        <input type="text" id="pf-danisman-isim" class="w-full px-4 py-2 bg-gray-50 border rounded-lg text-sm" placeholder="İsim (Örn: Selim Çınar)">
                        <input type="text" id="pf-danisman-unvan" class="w-full px-4 py-2 bg-gray-50 border rounded-lg text-sm" placeholder="Ünvan">
                    </div>
                    <input type="text" id="pf-danisman-resim" class="w-full px-4 py-2 bg-gray-50 border rounded-lg text-sm" placeholder="Danışman Fotoğrafı URL">
                </div>
            </div>

        </form>
    </div>

    <!-- WIZARD NAV BUTTONS -->
    <div class="p-6 border-t border-gray-100 bg-gray-50/50 shrink-0 flex gap-4">
        <button type="button" id="wiz-prev-btn" onclick="wizPrev()" class="hidden w-1/3 bg-white border border-gray-300 hover:bg-gray-50 text-navy font-bold py-3 rounded-lg transition-all uppercase tracking-widest text-xs shadow-sm">
            <i class="fa-solid fa-arrow-left mr-1"></i> Geri
        </button>
        <button type="button" id="wiz-next-btn" onclick="wizNext()" class="flex-1 bg-navy hover:bg-slate-800 text-gold font-bold py-3 rounded-lg transition-all uppercase tracking-widest text-xs shadow-xl shadow-navy/20">
            Devam Et <i class="fa-solid fa-arrow-right ml-1"></i>
        </button>
        <button type="button" id="wiz-save-btn" onclick="savePortfolio()" class="hidden flex-1 bg-gold hover:bg-yellow-600 text-white font-bold py-3 rounded-lg transition-all uppercase tracking-widest text-xs shadow-xl shadow-gold/20 gold-glow">
            <i class="fa-solid fa-cloud-arrow-up mr-1"></i> Yayına Al
        </button>
    </div>
</div>
</html>
"""

# 1. Add script import `inspection-data.js` to head or before closing tag
if '<script src="js/inspection-data.js"></script>' not in html:
    html = html.replace('</body>', '<script src="js/inspection-data.js"></script>\n</body>')

# 2. Replace OLD JS part
pattern_js = re.compile(r'// ==========================================\n\s*// PORTFOLIO CMS \(MÜLK YÖNETİMİ\) JS MANTIĞI.*?</script>', re.DOTALL)
html = pattern_js.sub(new_js + "\n    </script>", html)

# 3. Replace OLD HTML Modal part
pattern_html = re.compile(r'<!-- ============================================== -->\n<!-- PORTFOLIO SLIDE-OVER MODAL -->.*?</html>', re.DOTALL)
html = pattern_html.sub(new_html, html)

# Save
with open('portal.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Inject success!")
