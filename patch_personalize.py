import sys

with open('anasayfa.html', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add localStorage tracking + "Sizin İçin Seçilenler" section
# We'll inject tracking in the existing script and add a personalized section

# Find the portfolio rendering area near line 1181 where JS renders cards
# Looking for the renderPortfolios or DOMContentLoaded

personalization_js = '''
        // --- PROGRESSIVE PROFILING: localStorage Kişiselleştirme ---
        function trackUserInterest(collection, price) {
            let interests = JSON.parse(localStorage.getItem('imza_interests') || '[]');
            interests.push({ collection: collection, price: price, time: Date.now() });
            // Son 20 etkileşimi tut
            if (interests.length > 20) interests = interests.slice(-20);
            localStorage.setItem('imza_interests', JSON.stringify(interests));
        }

        function getTopInterest() {
            const interests = JSON.parse(localStorage.getItem('imza_interests') || '[]');
            if (interests.length === 0) return null;
            const counts = {};
            interests.forEach(i => { counts[i.collection] = (counts[i.collection] || 0) + 1; });
            return Object.entries(counts).sort((a, b) => b[1] - a[1])[0][0];
        }

        function showPersonalizedBanner() {
            const topInterest = getTopInterest();
            if (!topInterest) return;

            const bannerContainer = document.getElementById('personalized-banner');
            if (!bannerContainer) return;

            const collectionNames = { prestij: 'Prestij', modern: 'Modern', doga: 'Doğa' };
            const name = collectionNames[topInterest] || topInterest;

            bannerContainer.innerHTML = `
                <div class="bg-gradient-to-r from-navy via-slate-800 to-navy rounded-[2rem] p-8 md:p-10 text-white relative overflow-hidden shadow-xl mb-10 border border-gold/20">
                    <div class="absolute inset-0 brand-pattern opacity-10"></div>
                    <div class="relative z-10 flex flex-col md:flex-row items-center justify-between gap-6">
                        <div class="flex items-center gap-4">
                            <div class="w-14 h-14 bg-gold/20 rounded-2xl flex items-center justify-center">
                                <i class="fa-solid fa-sparkles text-gold text-2xl"></i>
                            </div>
                            <div>
                                <p class="text-gold text-[10px] font-bold uppercase tracking-widest">Sizin İçin Seçtik</p>
                                <h3 class="text-xl font-serif font-bold">${name} koleksiyonundan özel önerilerimiz var</h3>
                            </div>
                        </div>
                        <button onclick="setPortfolioTab('${topInterest}')"
                            class="bg-gold hover:bg-yellow-600 text-navy px-8 py-3 rounded-full font-bold text-xs uppercase tracking-widest transition-all shadow-lg shadow-gold/20 whitespace-nowrap">
                            Keşfet <i class="fa-solid fa-arrow-right ml-2"></i>
                        </button>
                    </div>
                </div>
            `;
            bannerContainer.classList.remove('hidden');
        }

        // Sayfa yüklendiğinde kişiselleştirilmiş banner'ı göster
        document.addEventListener('DOMContentLoaded', () => { showPersonalizedBanner(); });
'''

# Inject the personalization JS before the last </script>
last_script = content.rfind('</script>')
if last_script != -1:
    content = content[:last_script] + personalization_js + '\n' + content[last_script:]

# Add personalized banner div right before the portfolio grid
portfolio_grid_marker = '<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 md:gap-8 lg:gap-12 text-left">'
grid_idx = content.find(portfolio_grid_marker)
if grid_idx != -1:
    banner_html = '\n                <div id="personalized-banner" class="hidden col-span-full"></div>\n'
    content = content[:grid_idx] + banner_html + content[grid_idx:]

# Add tracking calls to the collection cards (onclick)
# Replace onclick="luxNavigate('koleksiyon.html?tip=prestij')" with tracking + navigate
content = content.replace(
    "onclick=\"luxNavigate('koleksiyon.html?tip=prestij')\"",
    "onclick=\"trackUserInterest('prestij', 35000000); luxNavigate('koleksiyon.html?tip=prestij')\""
)
content = content.replace(
    "onclick=\"luxNavigate('koleksiyon.html?tip=modern')\"",
    "onclick=\"trackUserInterest('modern', 12000000); luxNavigate('koleksiyon.html?tip=modern')\""
)
content = content.replace(
    "onclick=\"luxNavigate('koleksiyon.html?tip=doga')\"",
    "onclick=\"trackUserInterest('doga', 24000000); luxNavigate('koleksiyon.html?tip=doga')\""
)

with open('anasayfa.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Progressive Profiling injected into anasayfa.html!")
