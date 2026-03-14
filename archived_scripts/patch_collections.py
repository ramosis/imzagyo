import sys

with open('anasayfa.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Tailwind config'e yeni koleksiyon renklerini ekle
old_colors = """colors: {
                        navy: '#0a192f',
                        gold: '#c5a059',
                        modern: '#e17055',
                        nature: '#1b4d3e',
                        natureLight: '#f3e5ab',
                        soft: '#f8fafc',
                    },"""

new_colors = """colors: {
                        navy: '#0a192f',
                        gold: '#c5a059',
                        modern: '#e17055',
                        nature: '#1b4d3e',
                        natureLight: '#f3e5ab',
                        soft: '#f8fafc',
                        arsaColor: '#8B6914',
                        tarlaColor: '#6B8E23',
                        ciftlikColor: '#8B4513',
                        ticariColor: '#DC143C',
                        sanayiColor: '#4A5568',
                        turizmColor: '#0891B2',
                        donusumColor: '#B45309',
                        binaColor: '#6366F1',
                        devremulkColor: '#9333EA',
                    },"""
content = content.replace(old_colors, new_colors)

# 2. Koleksiyonlar section'ını dinamik yapıya çevir
old_collections = """        <!-- Section 2: Koleksiyonlar -->
        <section id="seriler" class="snap-section bg-white border-b border-gray-100 text-navy">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full text-center">
                <div class="mb-10 md:mb-12 text-center">
                    <h2 class="text-3xl md:text-5xl font-bold font-serif mb-4 uppercase tracking-tighter">Yaşam
                        Koleksiyonları</h2>
                    <div class="w-16 h-1 bg-gold mx-auto mb-4"></div>
                    <p class="text-gray-400 text-sm max-w-lg mx-auto font-light">Gayrimenkul dünyasında üç farklı
                        vizyon, binlerce farklı hikaye.</p>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-3 gap-6 md:gap-8 lg:gap-10">
                    <div onclick="trackUserInterest('prestij', 35000000); luxNavigate('koleksiyon.html?tip=prestij')"
                        class="relative h-56 md:h-[450px] lg:h-[500px] rounded-[2.5rem] overflow-hidden group cursor-pointer shadow-2xl">
                        <img src="https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80"
                            class="absolute inset-0 w-full h-full object-cover group-hover:scale-110 transition-transform duration-1000">
                        <div
                            class="absolute inset-0 bg-gradient-to-t from-navy/90 via-navy/20 to-transparent text-left">
                        </div>
                        <div
                            class="absolute bottom-6 md:bottom-10 left-6 md:left-10 right-6 md:right-10 text-white text-left">
                            <div
                                class="w-10 h-10 md:w-12 md:h-12 bg-gold rounded-2xl flex items-center justify-center text-navy mb-4 shadow-xl transform group-hover:-translate-y-2 transition-transform">
                                <i class="fas fa-crown text-xl"></i>
                            </div>
                            <h3
                                class="text-2xl md:text-3xl font-serif font-bold text-gold mb-2 uppercase tracking-tight text-left">
                                Prestij</h3>
                            <p
                                class="text-[10px] md:text-sm text-gray-300 leading-relaxed font-light opacity-0 group-hover:opacity-100 transition-opacity duration-500 text-left">
                                Lüks konut ve seçkin yalı portföyü.</p>
                        </div>
                    </div>
                    <div onclick="trackUserInterest('modern', 12000000); luxNavigate('koleksiyon.html?tip=modern')"
                        class="relative h-56 md:h-[450px] lg:h-[500px] rounded-[2.5rem] overflow-hidden group cursor-pointer shadow-2xl">
                        <img src="https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?auto=format&fit=crop&w=800&q=80"
                            class="absolute inset-0 w-full h-full object-cover group-hover:scale-110 transition-transform duration-1000">
                        <div
                            class="absolute inset-0 bg-gradient-to-t from-modern/90 via-navy/20 to-transparent opacity-80 text-left">
                        </div>
                        <div
                            class="absolute bottom-6 md:bottom-10 left-6 md:left-10 right-6 md:right-10 text-white text-left">
                            <div
                                class="w-10 h-10 md:w-12 md:h-12 bg-white/20 backdrop-blur-xl rounded-2xl flex items-center justify-center text-white mb-4 shadow-xl transform group-hover:-translate-y-2 transition-transform">
                                <i class="fas fa-city text-xl text-white"></i>
                            </div>
                            <h3
                                class="text-2xl md:text-3xl font-serif font-bold text-white mb-2 uppercase tracking-tight text-left">
                                Modern</h3>
                            <p
                                class="text-[10px] md:text-sm text-gray-200 leading-relaxed font-light opacity-0 group-hover:opacity-100 transition-opacity duration-500 text-left">
                                Şehrin dinamizmini yansıtan projeler.</p>
                        </div>
                    </div>
                    <div onclick="trackUserInterest('doga', 24000000); luxNavigate('koleksiyon.html?tip=doga')"
                        class="relative h-56 md:h-[450px] lg:h-[500px] rounded-[2.5rem] overflow-hidden group cursor-pointer shadow-2xl text-left">
                        <img src="https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80"
                            class="absolute inset-0 w-full h-full object-cover group-hover:scale-110 transition-transform duration-1000">
                        <div
                            class="absolute inset-0 bg-gradient-to-t from-nature/90 via-navy/20 to-transparent opacity-80 text-left">
                        </div>
                        <div
                            class="absolute bottom-6 md:bottom-10 left-6 md:left-10 right-6 md:right-10 text-white text-left">
                            <div
                                class="w-10 h-10 md:w-12 md:h-12 bg-natureLight/20 backdrop-blur-xl rounded-2xl flex items-center justify-center text-natureLight mb-4 shadow-xl transform group-hover:-translate-y-2 transition-transform">
                                <i class="fas fa-leaf text-xl text-natureLight"></i>
                            </div>
                            <h3
                                class="text-2xl md:text-3xl font-serif font-bold text-natureLight mb-2 uppercase tracking-tight text-left text-natureLight">
                                Doğa</h3>
                            <p
                                class="text-[10px] md:text-sm text-gray-200 leading-relaxed font-light opacity-0 group-hover:opacity-100 transition-opacity duration-500 text-left">
                                Doğayla iç içe lüks yaşam alanları.</p>
                        </div>
                    </div>
                </div>
            </div>
        </section>"""

new_collections = """        <!-- Section 2: Koleksiyonlar (Dinamik) -->
        <section id="seriler" class="snap-section bg-white border-b border-gray-100 text-navy">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full text-center">
                <div class="mb-10 md:mb-12 text-center">
                    <h2 class="text-3xl md:text-5xl font-bold font-serif mb-4 uppercase tracking-tighter">Emlak
                        Koleksiyonları</h2>
                    <div class="w-16 h-1 bg-gold mx-auto mb-4"></div>
                    <p class="text-gray-400 text-sm max-w-lg mx-auto font-light">Her segmentte profesyonel hizmet,
                        Kütahya'nın güvenilir adresi.</p>
                </div>
                <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 md:gap-6" id="collections-grid">
                    <!-- Dinamik olarak JS ile doldurulur -->
                </div>
            </div>
        </section>"""

content = content.replace(old_collections, new_collections)

# 3. Portföy sekmelerini dinamik yap
old_tabs = """                        <div class="flex flex-wrap justify-center md:justify-start gap-3" id="portfolio-tabs">
                            <button onclick="setPortfolioTab('tumu')" id="tab-tumu"
                                class="bg-navy text-gold px-6 py-1.5 rounded-full text-[9px] font-black uppercase tracking-widest shadow-xl">Tümü</button>
                            <button onclick="setPortfolioTab('prestij')" id="tab-prestij"
                                class="bg-white/80 text-gray-400 hover:text-navy px-6 py-1.5 rounded-full text-[9px] font-black uppercase tracking-widest border border-gray-100 transition-all">Prestij</button>
                            <button onclick="setPortfolioTab('modern')" id="tab-modern"
                                class="bg-white/80 text-gray-400 hover:text-navy px-6 py-1.5 rounded-full text-[9px] font-black uppercase tracking-widest border border-gray-100 transition-all">Modern</button>
                            <button onclick="setPortfolioTab('doga')" id="tab-doga"
                                class="bg-white/80 text-gray-400 hover:text-navy px-6 py-1.5 rounded-full text-[9px] font-black uppercase tracking-widest border border-gray-100 transition-all">Doğa</button>
                        </div>"""

new_tabs = """                        <div class="flex flex-wrap justify-center md:justify-start gap-3" id="portfolio-tabs">
                            <button onclick="setPortfolioTab('tumu')" id="tab-tumu"
                                class="bg-navy text-gold px-6 py-1.5 rounded-full text-[9px] font-black uppercase tracking-widest shadow-xl">Tümü</button>
                            <!-- Dinamik sekmeler JS ile eklenir -->
                        </div>"""

content = content.replace(old_tabs, new_tabs)

# 4. Eski filtre mantığını güncelle
old_tabs_list = "const tabs = ['tumu', 'prestij', 'modern', 'doga'];"
new_tabs_list = "const tabs = ['tumu', ...COLLECTIONS.map(c => c.key)];"
content = content.replace(old_tabs_list, new_tabs_list)

old_collection_names = "const collectionNames = { prestij: 'Prestij', modern: 'Modern', doga: 'Doğa' };"
new_collection_names = "const collectionNames = Object.fromEntries(COLLECTIONS.map(c => [c.key, c.name]));"
content = content.replace(old_collection_names, new_collection_names)

# 5. COLLECTIONS tanımı ve dinamik render JS'i ekle (</script> öncesine)
collections_js = """
        // === KOLEKSİYON TANIMLARI ===
        const COLLECTIONS = [
            { key: 'konut',    name: 'Konut',          icon: 'fa-house',        color: '#c5a059', gradient: 'from-navy/90',   img: 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?auto=format&fit=crop&w=800&q=80', desc: 'Villa, müstakil ev, daire, rezidans' },
            { key: 'arsa',     name: 'Arsa',           icon: 'fa-vector-square', color: '#8B6914', gradient: 'from-amber-900/90', img: 'https://images.unsplash.com/photo-1500382017468-9049fed747ef?auto=format&fit=crop&w=800&q=80', desc: 'İmarlı arsa, köy içi arsa' },
            { key: 'tarla',    name: 'Tarla & Bağ',    icon: 'fa-wheat-awn',    color: '#6B8E23', gradient: 'from-green-900/90', img: 'https://images.unsplash.com/photo-1625246333195-78d9c38ad449?auto=format&fit=crop&w=800&q=80', desc: 'Tarım arazisi, bağ, bahçe, zeytinlik' },
            { key: 'ciftlik',  name: 'Çiftlik',        icon: 'fa-cow',          color: '#8B4513', gradient: 'from-amber-800/90', img: 'https://images.unsplash.com/photo-1500595046743-cd271d694d30?auto=format&fit=crop&w=800&q=80', desc: 'Hobi çiftliği, besi, sera, mandıra' },
            { key: 'isyeri',   name: 'İş Yeri',        icon: 'fa-store',        color: '#DC143C', gradient: 'from-red-900/90',  img: 'https://images.unsplash.com/photo-1441986300917-64674bd600d8?auto=format&fit=crop&w=800&q=80', desc: 'Dükkan, mağaza, ofis, akaryakıt' },
            { key: 'sanayi',   name: 'Sanayi',         icon: 'fa-industry',     color: '#4A5568', gradient: 'from-gray-900/90', img: 'https://images.unsplash.com/photo-1504307651254-35680f356dfd?auto=format&fit=crop&w=800&q=80', desc: 'Fabrika, depo, atölye, tesis' },
            { key: 'turizm',   name: 'Turizm & Termal',icon: 'fa-hot-tub-person',color: '#0891B2',gradient: 'from-cyan-900/90',img: 'https://images.unsplash.com/photo-1571896349842-33c89424de2d?auto=format&fit=crop&w=800&q=80', desc: 'Otel, pansiyon, termal tesis' },
            { key: 'donusum',  name: 'Kentsel Dönüşüm',icon: 'fa-helmet-safety',color: '#B45309', gradient: 'from-orange-900/90',img: 'https://images.unsplash.com/photo-1504307651254-35680f356dfd?auto=format&fit=crop&w=800&q=80',desc: 'Eski bina, dönüşüm projesi' },
            { key: 'bina',     name: 'Bina & Komple',  icon: 'fa-building',     color: '#6366F1', gradient: 'from-indigo-900/90',img: 'https://images.unsplash.com/photo-1486325212027-8081e485255e?auto=format&fit=crop&w=800&q=80',desc: 'Apartman, iş hanı, komple satılık' },
            { key: 'devremulk',name: 'Devremülk',      icon: 'fa-calendar-days', color: '#9333EA',gradient: 'from-purple-900/90',img: 'https://images.unsplash.com/photo-1582719508461-905c673771fd?auto=format&fit=crop&w=800&q=80',desc: 'Devremülk, tatil hakkı' },
        ];

        // Koleksiyonları API'den gelen ilan sayılarına göre dinamik render et
        async function renderCollections() {
            try {
                const res = await fetch('/api/portfoyler');
                const allProps = await res.json();

                // Her koleksiyondaki ilan sayısını hesapla
                const counts = {};
                COLLECTIONS.forEach(c => counts[c.key] = 0);
                allProps.forEach(p => {
                    const k = (p.koleksiyon || '').toLowerCase().trim();
                    COLLECTIONS.forEach(c => {
                        if (k === c.key || k === c.name.toLowerCase() || k.includes(c.key)) {
                            counts[c.key]++;
                        }
                    });
                });

                // Koleksiyon kartlarını render et (sadece ilanı olanlar)
                const grid = document.getElementById('collections-grid');
                grid.innerHTML = '';
                const activeCollections = COLLECTIONS.filter(c => counts[c.key] > 0);

                if (activeCollections.length === 0) {
                    // Hiç ilan yoksa tüm koleksiyonları göster (placeholder)
                    COLLECTIONS.forEach(c => renderCollectionCard(grid, c, 0));
                } else {
                    activeCollections.forEach(c => renderCollectionCard(grid, c, counts[c.key]));
                }

                // Portföy sekmelerini de güncelle (sadece ilanı olan koleksiyonlar)
                const tabsContainer = document.getElementById('portfolio-tabs');
                // Tümü butonu zaten var, geri kalanları ekle
                const existingDynamic = tabsContainer.querySelectorAll('.dynamic-tab');
                existingDynamic.forEach(el => el.remove());

                const tabCollections = activeCollections.length > 0 ? activeCollections : COLLECTIONS;
                tabCollections.forEach(c => {
                    const btn = document.createElement('button');
                    btn.onclick = () => setPortfolioTab(c.key);
                    btn.id = 'tab-' + c.key;
                    btn.className = 'dynamic-tab bg-white/80 text-gray-400 hover:text-navy px-6 py-1.5 rounded-full text-[9px] font-black uppercase tracking-widest border border-gray-100 transition-all';
                    btn.textContent = c.name;
                    tabsContainer.appendChild(btn);
                });

            } catch(e) {
                console.error('Koleksiyon render hatası:', e);
                // Hata durumunda tüm koleksiyonları göster
                const grid = document.getElementById('collections-grid');
                COLLECTIONS.forEach(c => renderCollectionCard(grid, c, 0));
            }
        }

        function renderCollectionCard(container, col, count) {
            const card = document.createElement('div');
            card.onclick = () => luxNavigate('arama.html?koleksiyon=' + col.key);
            card.className = 'relative h-48 md:h-64 rounded-2xl overflow-hidden group cursor-pointer shadow-lg hover:shadow-2xl transition-all duration-500';
            card.innerHTML = `
                <img src="${col.img}" class="absolute inset-0 w-full h-full object-cover group-hover:scale-110 transition-transform duration-1000" loading="lazy">
                <div class="absolute inset-0 bg-gradient-to-t ${col.gradient} via-navy/30 to-transparent"></div>
                <div class="absolute bottom-4 left-4 right-4 text-white text-left">
                    <div class="w-9 h-9 rounded-xl flex items-center justify-center mb-2 shadow-lg transform group-hover:-translate-y-1 transition-transform" style="background:${col.color}30">
                        <i class="fa-solid ${col.icon} text-sm" style="color:${col.color}"></i>
                    </div>
                    <h3 class="text-lg font-serif font-bold mb-0.5 uppercase tracking-tight" style="color:${col.color}">${col.name}</h3>
                    <p class="text-[9px] text-gray-300 font-light leading-tight">${col.desc}</p>
                    ${count > 0 ? '<span class="absolute top-4 right-4 bg-white/20 backdrop-blur-sm text-white text-[10px] font-bold px-2 py-1 rounded-full">' + count + ' ilan</span>' : ''}
                </div>
            `;
            container.appendChild(card);
        }

        // Sayfa yüklenince koleksiyonları render et
        document.addEventListener('DOMContentLoaded', renderCollections);
"""

# Son </script> öncesine ekle
last_script = content.rfind('</script>')
content = content[:last_script] + collections_js + '\n    ' + content[last_script:]

# 6. Eski filtreleme mantığını güncelle
old_filter = """                    const kolek = p.koleksiyon.toLowerCase();
                    // Koleksiyon "Doğa" veya "Prestij" veya "Modern" objelerine esitse ceker
                    return kolek.includes(filt) || (kolek.includes('doğa') && filt === 'doga');"""

new_filter = """                    const kolek = (p.koleksiyon || '').toLowerCase();
                    // Koleksiyon filtreleme: key veya isim eşleşmesi
                    const col = COLLECTIONS.find(c => c.key === filt);
                    return kolek.includes(filt) || (col && kolek.includes(col.name.toLowerCase()));"""

content = content.replace(old_filter, new_filter)

with open('anasayfa.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Koleksiyon sistemi dinamik hale getirildi! 10 kategori, ilan yoksa gizlenir.")
