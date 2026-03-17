/**
 * İmza Lens - UI Components (imza-lens.ui.js)
 * Akıllı SSS Ticker ve Kişiselleştirilmiş Banner Enjeksiyon Motoru
 */

const ImzaLensUI = {
    // 1. SSS TICKER ENJEKSİYONU
    // Verilen soru havuzunu 'İmza Lens' zekasıyla filtreleyip render eder.
    initFaqTicker(containerId, allQuestions) {
        const container = document.getElementById(containerId);
        if (!container) return;

        // İmza Lens zekasından niyeti al
        const intent = window.ImzaLens ? window.ImzaLens.getIntent() : 'konut';
        
        // Akıllı Sıralama Algoritması (Prioritized First)
        const prioritized = allQuestions.filter(q => q.cat === intent);
        const others = allQuestions.filter(q => q.cat !== intent);
        const activeList = [...prioritized, ...others].slice(0, 10);

        container.innerHTML = ''; // Mevcut içeriği temizle
        
        activeList.forEach((q, idx) => {
            const div = document.createElement('div');
            div.className = `faq-ticker-item text-[10px] md:text-xs font-bold tracking-[0.2em] text-gray-400 hover:text-gold transition-colors ${idx === 0 ? 'active' : ''}`;
            div.innerHTML = `
                <span class="bg-gold/10 text-gold px-3 py-1 rounded-full mr-4 text-[9px]">Soru</span> 
                ${q.text.toUpperCase()} 
                <i class="fa-solid fa-arrow-up-right-from-square ml-3 text-[8px] opacity-0 group-hover:opacity-100 transition-opacity"></i>
            `;
            
            // Tıklama analizi
            div.onclick = () => {
                if (window.ImzaLens) window.ImzaLens.track(q.cat);
                this.handleFaqClick(q);
            };
            
            container.appendChild(div);
        });

        this.startTickerRotation(containerId, activeList.length);
        return activeList;
    },

    // 2. KİŞİSELLEŞTİRİLMİŞ BANNER ENJEKSİYONU (Geo-Lens Destekli)
    renderPersonalizedBanner(containerId) {
        if (!window.ImzaLens) return;
        const topInterest = window.ImzaLens.getTopInterest();
        if (!topInterest) return;

        const container = document.getElementById(containerId);
        if (!container) return;

        const geo = JSON.parse(localStorage.getItem('imza_lens_geo') || '{}');
        const cityPrefix = geo.city ? `<span class="text-gold/80 block mb-1 text-[9px] font-bold tracking-[0.2em] uppercase">${geo.city}'dan Hoş Geldiniz</span>` : '';

        const collections = { 
            prestij: 'Prestij', 
            modern: 'Modern', 
            doga: 'Doğa', 
            yatirim: 'Yatırım',
            sanayi: 'Sanayi',
            ticari: 'Ticari',
            rezidans: 'Rezidans'
        };
        const name = collections[topInterest] || topInterest;

        container.innerHTML = `
            <div class="bg-gradient-to-r from-navy via-slate-800 to-navy rounded-[2.5rem] p-8 md:p-10 text-white relative overflow-hidden shadow-xl mb-10 border border-gold/20">
                <div class="absolute inset-0 brand-pattern opacity-10"></div>
                <div class="relative z-10 flex flex-col md:flex-row items-center justify-between gap-6 text-left">
                    <div class="flex items-center gap-4">
                        <div class="w-14 h-14 bg-gold/20 rounded-2xl flex items-center justify-center">
                            <i class="fa-solid fa-sparkles text-gold text-2xl"></i>
                        </div>
                        <div>
                            ${cityPrefix}
                            <p class="text-gold text-[10px] font-bold uppercase tracking-widest text-left">Sizin İçin Seçtik</p>
                            <h3 class="text-xl font-serif font-bold text-left">${name} koleksiyonundan özel önerilerimiz var</h3>
                        </div>
                    </div>
                    <button onclick="luxNavigate('koleksiyon.html?tip=${topInterest}')"
                        class="bg-gold hover:bg-yellow-600 text-navy px-8 py-3 rounded-full font-bold text-xs uppercase tracking-widest transition-all shadow-lg shadow-gold/20 whitespace-nowrap">
                        Keşfet <i class="fa-solid fa-arrow-right ml-2"></i>
                    </button>
                </div>
            </div>
        `;
        container.classList.remove('hidden');

        // SEO Lens: Meta verilerini kullanıcıya özel güncelle
        this.updateMetaLens(topInterest);
    },

    // 3. DİNAMİK SEO LENS (Meta Tag Güncelleme)
    updateMetaLens(topInterest) {
        if (!topInterest) return;
        const metaDesc = document.querySelector('meta[name="description"]');
        if (metaDesc) {
            const currentText = metaDesc.getAttribute('content');
            if (!currentText.includes(topInterest.toUpperCase())) {
                metaDesc.setAttribute('content', `${topInterest.toUpperCase()} Odaklı Yatırım Fırsatları: ${currentText}`);
                console.log(`[İmza Lens] SEO Lens: Meta açıklaması optimize edildi.`);
            }
        }
        
        // Title güncelleme (Opsiyonel but effective)
        if (!document.title.includes('|')) {
             document.title = `${topInterest.toUpperCase()} Koleksiyonu | ${document.title}`;
        }
    },

    // YARDIMCI METODLAR
    startTickerRotation(containerId, length) {
        let currentIndex = 0;
        const container = document.getElementById(containerId);
        
        setInterval(() => {
            const items = container.querySelectorAll('.faq-ticker-item');
            if (items.length < 2) return;

            items[currentIndex].classList.remove('active');
            items[currentIndex].classList.add('exit');
            
            currentIndex = (currentIndex + 1) % length;
            
            items[currentIndex].classList.remove('exit');
            items[currentIndex].classList.add('active');
            
            setTimeout(() => {
                items.forEach((item, idx) => {
                    if (idx !== currentIndex) item.classList.remove('exit');
                });
            }, 1100);
        }, 6000);
    },

    handleFaqClick(faq) {
        // Bu metod ana uygulama tarafından override edilebilir veya alert verebilir
        const report = `[İmza Lens Raporu]\nSegment: ${faq.cat.toUpperCase()}\nİçerik: ${faq.link}`;
        console.log(report);
        if (window.onImzaLensFaqClick) {
            window.onImzaLensFaqClick(faq);
        } else {
             alert(`İmza Lens Raporu:\nSizi ${faq.cat.toUpperCase()} kategorisiyle ilgilenen bir kullanıcı olarak analiz ettik.\nYakında: ${faq.link} makalesine yönlendirileceksiniz.`);
        }
    },

    // 4. DİNAMİK KAMPANYA & LANSMAN ENJEKSİYONU
    async injectHeroCampaign(wrapperId, dotsId) {
        try {
            // Aktif kampanyaları çek (Gelecekte API'den gelecek)
            // Simülasyon: Sağlık Yatırım Ortaklığı (SYO)
            const campaigns = [{
                id: 'syo-arsa',
                type: 'arsa',
                title: 'Sağlık Yatırım Ortaklığı Arsa Projesi',
                subtitle: 'Geleceğinize Güvenle İmza Atın',
                image: 'https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&q=80&w=1920',
                cta: 'Hemen Bilgi Al',
                partner: 'YATIRIM FIRSATI'
            }];

            if (campaigns.length === 0) return;

            const wrapper = document.getElementById(wrapperId);
            const dotsContainer = document.getElementById(dotsId);
            if (!wrapper || !dotsContainer) return;

            campaigns.forEach(camp => {
                const slide = document.createElement('div');
                slide.className = `slide campaign-slide absolute inset-0 transition-opacity duration-1000 opacity-0 z-0`;
                slide.innerHTML = `
                    <div class="absolute inset-0 bg-cover bg-center" style="background-image: url('${camp.image}');"></div>
                    <div class="absolute inset-0 bg-navy/70 backdrop-blur-[2px]"></div>
                    <div class="absolute inset-0 brand-pattern opacity-20"></div>
                    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative h-full flex items-center w-full">
                        <div class="max-w-4xl text-left">
                            <div class="flex items-center gap-4 mb-6">
                                <span class="bg-gold text-navy px-4 py-1 rounded-full text-[10px] font-bold uppercase tracking-widest">${camp.partner}</span>
                                <span class="text-white/50 text-[10px] font-bold uppercase tracking-[0.3em]">Süreli Lansman</span>
                            </div>
                            <p class="text-gold uppercase tracking-[0.4em] text-xs font-bold mb-4 drop-shadow-md border-l-2 border-gold pl-4 italic slide-up">
                                ${camp.subtitle}
                            </p>
                            <h1 class="text-5xl md:text-7xl font-serif text-white mb-6 leading-tight slide-up">
                                ${camp.title}
                            </h1>
                            <div class="flex flex-col md:flex-row gap-6 mt-8 slide-up">
                                <button onclick="ImzaLensUI.openDemandForm('${camp.id}')" 
                                    class="px-12 py-5 bg-gold text-navy font-bold uppercase tracking-widest hover:bg-white transition-all duration-500 rounded-full shadow-2xl shadow-gold/20">
                                    ${camp.cta}
                                </button>
                                <button onclick="luxNavigate('kampanya-detay.html?id=${camp.id}')"
                                    class="px-12 py-5 border border-white/30 text-white font-bold uppercase tracking-widest hover:bg-white hover:text-navy transition-all duration-500 rounded-full backdrop-blur-md">
                                    Projeyi İncele
                                </button>
                            </div>
                        </div>
                    </div>
                `;
                // Slaytı en başa ekle
                wrapper.prepend(slide);

                // Dot ekle
                const dot = document.createElement('button');
                dot.className = "w-10 h-1 bg-white/30 rounded-full transition-colors campaign-dot";
                dot.onclick = () => window.goToSlide(0); // Kampanya her zaman 0. slayt olacak
                dotsContainer.prepend(dot);
            });

            console.log(`[İmza Lens] Kampanya Modülü: ${campaigns.length} kampanya enjekte edildi.`);
            
            // Slider değişkenlerini yenilemek için anasayfadaki initSlide referansını tetiklemek gerekebilir.
            // Bu kısım anasayfa.html tarafında halledilecek.
        } catch (e) {
            console.error("[İmza Lens] Kampanya enjeksiyon hatası:", e);
        }
    },

    // 5. MERKEZİ TALEP FORMU (MODAL)
    openDemandForm(campaignId) {
        // Modal HTML'ini dinamik oluştur (Z-Index 1000+)
        let modal = document.getElementById('imza-campaign-modal');
        if (!modal) {
            modal = document.createElement('div');
            modal.id = 'imza-campaign-modal';
            modal.className = 'fixed inset-0 z-[1000] invisible opacity-0 transition-all duration-500 flex items-center justify-center p-4 md:p-8';
            document.body.appendChild(modal);
        }

        modal.innerHTML = `
            <div class="absolute inset-0 bg-navy/95 backdrop-blur-xl" onclick="ImzaLensUI.closeDemandForm()"></div>
            <div class="relative w-full max-w-2xl bg-white rounded-[3rem] overflow-hidden shadow-2xl transform translate-y-10 transition-transform duration-500" id="modal-content">
                <div class="absolute inset-0 brand-pattern opacity-5"></div>
                
                <div class="p-8 md:p-12 relative z-10">
                    <button onclick="ImzaLensUI.closeDemandForm()" class="absolute top-8 right-8 text-navy/20 hover:text-gold transition-colors text-2xl">
                        <i class="fa-solid fa-xmark"></i>
                    </button>

                    <div class="text-center mb-10">
                        <span class="text-gold text-[10px] font-bold uppercase tracking-[0.4em] mb-4 block">Yatırım Talebi</span>
                        <h2 class="text-3xl md:text-4xl font-serif font-bold text-navy uppercase tracking-tighter">Geleceğinize İmza Atın</h2>
                        <p class="text-gray-400 text-sm mt-4 font-light">Ekiplerimiz size en avantajlı ödeme planını sunmak için ulaşacaktır.</p>
                    </div>

                    <form onsubmit="ImzaLensUI.submitCampaignLead(event, '${campaignId}')" class="space-y-6">
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div class="space-y-2">
                                <label class="text-[10px] font-bold uppercase tracking-widest text-navy/40 ml-4">Ad</label>
                                <input type="text" name="firstName" required class="w-full bg-soft border-none rounded-2xl px-6 py-4 focus:ring-2 focus:ring-gold/50 transition-all text-navy font-medium" placeholder="Örn: Selim">
                            </div>
                            <div class="space-y-2">
                                <label class="text-[10px] font-bold uppercase tracking-widest text-navy/40 ml-4">Soyad</label>
                                <input type="text" name="lastName" required class="w-full bg-soft border-none rounded-2xl px-6 py-4 focus:ring-2 focus:ring-gold/50 transition-all text-navy font-medium" placeholder="Örn: Bey">
                            </div>
                        </div>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                            <div class="space-y-2">
                                <label class="text-[10px] font-bold uppercase tracking-widest text-navy/40 ml-4">Telefon</label>
                                <input type="tel" name="phone" required class="w-full bg-soft border-none rounded-2xl px-6 py-4 focus:ring-2 focus:ring-gold/50 transition-all text-navy font-medium" placeholder="05xx xxx xx xx">
                            </div>
                            <div class="space-y-2 flex items-end">
                                <p class="text-[9px] text-gray-400 font-light leading-tight mb-2 italic">Telefon numaranız sadece bilgilendirme için kullanılacaktır.</p>
                            </div>
                        </div>
                        <div class="space-y-2">
                            <label class="text-[10px] font-bold uppercase tracking-widest text-navy/40 ml-4">Mesajınız (Opsiyonel)</label>
                            <textarea name="note" rows="3" class="w-full bg-soft border-none rounded-2xl px-6 py-4 focus:ring-2 focus:ring-gold/50 transition-all text-navy font-medium" placeholder="Eklemek istediğiniz bir not var mı?"></textarea>
                        </div>
                        
                        <button type="submit" class="w-full bg-navy text-gold py-5 rounded-2xl font-bold uppercase tracking-[0.3em] hover:bg-gold hover:text-navy transition-all duration-500 shadow-xl shadow-navy/20 mt-4 group">
                            Talebi Gönder 
                            <i class="fa-solid fa-paper-plane ml-3 group-hover:translate-x-2 transition-transform"></i>
                        </button>
                    </form>
                </div>
            </div>
        `;

        modal.classList.remove('invisible', 'opacity-0');
        setTimeout(() => {
            document.getElementById('modal-content').classList.remove('translate-y-10');
            document.getElementById('modal-content').classList.add('translate-y-0');
        }, 10);
    },

    closeDemandForm() {
        const modal = document.getElementById('imza-campaign-modal');
        const content = document.getElementById('modal-content');
        if (!modal) return;

        content.classList.replace('translate-y-0', 'translate-y-10');
        modal.classList.add('opacity-0');
        setTimeout(() => {
            modal.classList.add('invisible');
        }, 500);
    },

    async submitCampaignLead(event, campaignId) {
        event.preventDefault();
        const form = event.target;
        const btn = form.querySelector('button');
        const originalText = btn.innerHTML;

        btn.disabled = true;
        btn.innerHTML = '<i class="fa-solid fa-circle-notch animate-spin mr-3"></i> İŞLENİYOR...';

        const formData = {
            campaign_id: campaignId,
            name: `${form.firstName.value} ${form.lastName.value}`.trim(),
            phone: form.phone.value,
            notes: form.note.value,
            source: 'hero_campaign',
            metrics: window.ImzaLensMetrics ? window.ImzaLensMetrics.getMetrics() : {}
        };

        try {
            // Shadow Bridge üzerinden niyet skoru gönder
            if (window.ImzaLens && window.ImzaLens.syncShadowBridge) {
                window.ImzaLens.syncShadowBridge();
            }

            // Gerçek API'ye gönder
            const response = await fetch('/api/leads', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });

            if (!response.ok) throw new Error('API hatası');
            const result = await response.json();
            console.log("[İmza Lens] Kurşun Başarıyla Gönderildi:", result);

            form.innerHTML = `
                <div class="text-center py-12 animate-bounce">
                    <div class="w-24 h-24 bg-green-500 text-white rounded-full flex items-center justify-center mx-auto mb-8 shadow-2xl">
                        <i class="fa-solid fa-check text-4xl"></i>
                    </div>
                    <h3 class="text-2xl font-serif font-bold text-navy mb-4">TALEBİNİZ ALINDI</h3>
                    <p class="text-gray-400">Yatırım danışmanlarımız en kısa sürede sizinle iletişime geçecektir. 🥂</p>
                </div>
            `;

            setTimeout(() => this.closeDemandForm(), 4000);

        } catch (e) {
            btn.disabled = false;
            btn.innerHTML = originalText;
            alert("Bir hata oluştu. Lütfen tekrar deneyin.");
        }
    }
};

// Global Erişilebilirlik
window.ImzaLensUI = ImzaLensUI;
