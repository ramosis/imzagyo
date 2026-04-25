import sys

with open('anasayfa.html', 'r', encoding='utf-8') as f:
    content = f.read()

if 'lifestyle-matcher' in content:
    print("Already patched!")
    sys.exit(0)

# Inject a Lifestyle Matching section between Section 3 (Portfolios) and Section 4 (Yatırımcı Araçları)
lifestyle_section = '''
        <!-- Section 3.5: Akıllı Ev Eşleştirme (Lifestyle Matching) -->
        <section id="lifestyle-matcher" class="snap-section bg-navy text-white relative overflow-hidden">
            <div class="absolute inset-0 brand-pattern opacity-10"></div>
            <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 w-full relative z-10 text-center">
                <div class="mb-10">
                    <h2 class="text-3xl md:text-5xl font-bold font-serif mb-4 uppercase tracking-tighter">Bana Uygun
                        Evi Bul</h2>
                    <div class="w-16 h-1 bg-gold mx-auto mb-4"></div>
                    <p class="text-gray-400 text-sm font-light max-w-lg mx-auto">Yaşam tarzınıza en uygun mülkü
                        bulmak için birkaç soruya cevap verin.</p>
                </div>

                <!-- Soru Kartları -->
                <div id="lm-questions" class="space-y-0">
                    <!-- Soru 1 -->
                    <div id="lm-q1" class="lm-question">
                        <div class="bg-white/5 backdrop-blur-xl rounded-[2rem] p-8 md:p-12 border border-white/10 max-w-2xl mx-auto">
                            <p class="text-gold text-[10px] font-bold uppercase tracking-widest mb-4">Soru 1 / 4</p>
                            <h3 class="text-xl md:text-2xl font-serif font-bold mb-8">Günlük çalışma düzeniniz nasıl?
                            </h3>
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <button onclick="lmAnswer(1, 'remote')"
                                    class="bg-white/10 hover:bg-gold/20 border border-white/10 hover:border-gold/50 rounded-2xl p-6 transition-all text-left group">
                                    <i class="fa-solid fa-laptop-house text-gold text-2xl mb-3 group-hover:scale-110 transition-transform"></i>
                                    <h4 class="font-bold text-white text-sm">Uzaktan Çalışıyorum</h4>
                                    <p class="text-gray-400 text-xs mt-1">Evde geniş çalışma alanı lazım</p>
                                </button>
                                <button onclick="lmAnswer(1, 'office')"
                                    class="bg-white/10 hover:bg-gold/20 border border-white/10 hover:border-gold/50 rounded-2xl p-6 transition-all text-left group">
                                    <i class="fa-solid fa-building text-gold text-2xl mb-3 group-hover:scale-110 transition-transform"></i>
                                    <h4 class="font-bold text-white text-sm">Ofise Gidiyorum</h4>
                                    <p class="text-gray-400 text-xs mt-1">Ulaşım ve merkeze yakınlık önemli</p>
                                </button>
                            </div>
                        </div>
                    </div>

                    <!-- Soru 2 -->
                    <div id="lm-q2" class="lm-question hidden">
                        <div class="bg-white/5 backdrop-blur-xl rounded-[2rem] p-8 md:p-12 border border-white/10 max-w-2xl mx-auto">
                            <p class="text-gold text-[10px] font-bold uppercase tracking-widest mb-4">Soru 2 / 4</p>
                            <h3 class="text-xl md:text-2xl font-serif font-bold mb-8">Evcil hayvanınız var mı?</h3>
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <button onclick="lmAnswer(2, 'pet_yes')"
                                    class="bg-white/10 hover:bg-gold/20 border border-white/10 hover:border-gold/50 rounded-2xl p-6 transition-all text-left group">
                                    <i class="fa-solid fa-dog text-gold text-2xl mb-3 group-hover:scale-110 transition-transform"></i>
                                    <h4 class="font-bold text-white text-sm">Evet, Var</h4>
                                    <p class="text-gray-400 text-xs mt-1">Bahçeli veya park yakını tercih</p>
                                </button>
                                <button onclick="lmAnswer(2, 'pet_no')"
                                    class="bg-white/10 hover:bg-gold/20 border border-white/10 hover:border-gold/50 rounded-2xl p-6 transition-all text-left group">
                                    <i class="fa-solid fa-city text-gold text-2xl mb-3 group-hover:scale-110 transition-transform"></i>
                                    <h4 class="font-bold text-white text-sm">Hayır, Yok</h4>
                                    <p class="text-gray-400 text-xs mt-1">Bahçe şartı önemli değil</p>
                                </button>
                            </div>
                        </div>
                    </div>

                    <!-- Soru 3 -->
                    <div id="lm-q3" class="lm-question hidden">
                        <div class="bg-white/5 backdrop-blur-xl rounded-[2rem] p-8 md:p-12 border border-white/10 max-w-2xl mx-auto">
                            <p class="text-gold text-[10px] font-bold uppercase tracking-widest mb-4">Soru 3 / 4</p>
                            <h3 class="text-xl md:text-2xl font-serif font-bold mb-8">Sosyal hayat sizin için ne kadar
                                önemli?</h3>
                            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <button onclick="lmAnswer(3, 'social')"
                                    class="bg-white/10 hover:bg-gold/20 border border-white/10 hover:border-gold/50 rounded-2xl p-6 transition-all text-left group">
                                    <i class="fa-solid fa-champagne-glasses text-gold text-2xl mb-3 group-hover:scale-110 transition-transform"></i>
                                    <h4 class="font-bold text-white text-sm">Çok Önemli</h4>
                                    <p class="text-gray-400 text-xs mt-1">Restoran, kafe ve gece hayatı</p>
                                </button>
                                <button onclick="lmAnswer(3, 'quiet')"
                                    class="bg-white/10 hover:bg-gold/20 border border-white/10 hover:border-gold/50 rounded-2xl p-6 transition-all text-left group">
                                    <i class="fa-solid fa-tree text-gold text-2xl mb-3 group-hover:scale-110 transition-transform"></i>
                                    <h4 class="font-bold text-white text-sm">Sakin Tercih Ederim</h4>
                                    <p class="text-gray-400 text-xs mt-1">Doğa, huzur ve sessizlik</p>
                                </button>
                            </div>
                        </div>
                    </div>

                    <!-- Soru 4 -->
                    <div id="lm-q4" class="lm-question hidden">
                        <div class="bg-white/5 backdrop-blur-xl rounded-[2rem] p-8 md:p-12 border border-white/10 max-w-2xl mx-auto">
                            <p class="text-gold text-[10px] font-bold uppercase tracking-widest mb-4">Soru 4 / 4</p>
                            <h3 class="text-xl md:text-2xl font-serif font-bold mb-8">Ailenizin büyüklüğü nasıl?</h3>
                            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                                <button onclick="lmAnswer(4, 'single')"
                                    class="bg-white/10 hover:bg-gold/20 border border-white/10 hover:border-gold/50 rounded-2xl p-6 transition-all text-left group">
                                    <i class="fa-solid fa-user text-gold text-2xl mb-3"></i>
                                    <h4 class="font-bold text-white text-sm">Tekil</h4>
                                </button>
                                <button onclick="lmAnswer(4, 'couple')"
                                    class="bg-white/10 hover:bg-gold/20 border border-white/10 hover:border-gold/50 rounded-2xl p-6 transition-all text-left group">
                                    <i class="fa-solid fa-user-group text-gold text-2xl mb-3"></i>
                                    <h4 class="font-bold text-white text-sm">Çift</h4>
                                </button>
                                <button onclick="lmAnswer(4, 'family')"
                                    class="bg-white/10 hover:bg-gold/20 border border-white/10 hover:border-gold/50 rounded-2xl p-6 transition-all text-left group">
                                    <i class="fa-solid fa-people-roof text-gold text-2xl mb-3"></i>
                                    <h4 class="font-bold text-white text-sm">Aile (3+)</h4>
                                </button>
                            </div>
                        </div>
                    </div>

                    <!-- Sonuç -->
                    <div id="lm-result" class="lm-question hidden">
                        <div class="bg-gradient-to-br from-gold/20 via-navy to-navy rounded-[2rem] p-8 md:p-12 border border-gold/30 max-w-2xl mx-auto shadow-2xl">
                            <i class="fa-solid fa-sparkles text-gold text-4xl mb-6"></i>
                            <h3 class="text-2xl md:text-3xl font-serif font-bold text-gold mb-4">Size En Uygun Portföy</h3>
                            <div id="lm-match-card" class="bg-white/10 rounded-2xl p-6 mt-6 text-left">
                                <!-- JS ile doldurulacak -->
                            </div>
                            <button onclick="resetLifestyle()"
                                class="mt-8 border border-white/20 hover:bg-white/10 text-white px-8 py-3 rounded-full font-bold text-xs uppercase tracking-widest transition-all">
                                <i class="fa-solid fa-rotate-left mr-2"></i> Tekrar Dene
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </section>
'''

# Find Section 4 marker: <!-- Section 4: Yatırımcı Araçları -->
marker = '<!-- Section 4: Yatırımcı Araçları -->'
idx = content.find(marker)
if idx == -1:
    # Try alt
    marker = 'id="araclar"'
    idx = content.find(marker)
    if idx != -1:
        idx = content.rfind('<section', 0, idx)

if idx == -1:
    print("Could not find Section 4")
    sys.exit(1)

content = content[:idx] + lifestyle_section + '\n\n        ' + content[idx:]

# Add Lifestyle Matching JS
lifestyle_js = '''
        // --- LIFESTYLE MATCHING ENGINE ---
        let lmAnswers = {};

        function lmAnswer(qNum, answer) {
            lmAnswers[qNum] = answer;
            // Hide current, show next
            document.getElementById('lm-q' + qNum).classList.add('hidden');
            if (qNum < 4) {
                document.getElementById('lm-q' + (qNum + 1)).classList.remove('hidden');
            } else {
                // Show result
                showLifestyleResult();
            }
        }

        function showLifestyleResult() {
            const resultDiv = document.getElementById('lm-result');
            const cardDiv = document.getElementById('lm-match-card');
            resultDiv.classList.remove('hidden');

            // Simple scoring algorithm
            let scores = {
                'Boğaz Manzaralı Villa': { score: 50, img: 'https://images.unsplash.com/photo-1613977257363-707ba9348227?w=400&fit=crop', loc: 'Sarıyer, İstanbul', price: '₺35M', rooms: '6+2' },
                'Modern Loft Daire': { score: 50, img: 'https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=400&fit=crop', loc: 'Kadıköy, İstanbul', price: '₺12M', rooms: '3+1' },
                'Ekolojik Orman Evi': { score: 50, img: 'https://images.unsplash.com/photo-1518780664697-55e3ad937233?w=400&fit=crop', loc: 'Sapanca, Sakarya', price: '₺24M', rooms: '4+1' }
            };

            // Q1: Work style
            if (lmAnswers[1] === 'remote') {
                scores['Ekolojik Orman Evi'].score += 30;
                scores['Boğaz Manzaralı Villa'].score += 20;
            } else {
                scores['Modern Loft Daire'].score += 30;
            }

            // Q2: Pets
            if (lmAnswers[2] === 'pet_yes') {
                scores['Ekolojik Orman Evi'].score += 25;
                scores['Boğaz Manzaralı Villa'].score += 15;
            } else {
                scores['Modern Loft Daire'].score += 15;
            }

            // Q3: Social life
            if (lmAnswers[3] === 'social') {
                scores['Modern Loft Daire'].score += 30;
                scores['Boğaz Manzaralı Villa'].score += 10;
            } else {
                scores['Ekolojik Orman Evi'].score += 30;
            }

            // Q4: Family size
            if (lmAnswers[4] === 'family') {
                scores['Boğaz Manzaralı Villa'].score += 30;
                scores['Ekolojik Orman Evi'].score += 15;
            } else if (lmAnswers[4] === 'single') {
                scores['Modern Loft Daire'].score += 25;
            } else {
                scores['Boğaz Manzaralı Villa'].score += 10;
                scores['Modern Loft Daire'].score += 10;
            }

            // Normalize scores to percentage
            const maxPossible = 135; // max possible score
            const sorted = Object.entries(scores).sort((a, b) => b[1].score - a[1].score);
            const best = sorted[0];
            const matchPercent = Math.min(99, Math.round((best[1].score / maxPossible) * 100));

            cardDiv.innerHTML = `
                <div class="flex gap-5 items-center">
                    <img src="${best[1].img}" class="w-24 h-24 rounded-xl object-cover shadow-lg">
                    <div>
                        <div class="flex items-center gap-3 mb-2">
                            <h4 class="font-serif font-bold text-gold text-lg">${best[0]}</h4>
                            <span class="bg-green-500/20 text-green-400 text-[10px] font-bold px-2 py-0.5 rounded-full">%${matchPercent} Uyumlu</span>
                        </div>
                        <p class="text-gray-400 text-xs"><i class="fa-solid fa-location-dot mr-1"></i> ${best[1].loc}</p>
                        <p class="text-white font-bold mt-1">${best[1].price} <span class="text-gray-500 text-xs font-normal ml-2">${best[1].rooms}</span></p>
                    </div>
                </div>
            `;
        }

        function resetLifestyle() {
            lmAnswers = {};
            document.getElementById('lm-result').classList.add('hidden');
            document.querySelectorAll('.lm-question').forEach(q => q.classList.add('hidden'));
            document.getElementById('lm-q1').classList.remove('hidden');
        }
'''

last_script = content.rfind('</script>')
if last_script != -1:
    content = content[:last_script] + lifestyle_js + '\n' + content[last_script:]

with open('anasayfa.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Lifestyle Matching wizard injected into anasayfa.html!")
