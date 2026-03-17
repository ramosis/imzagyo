/**
 * Mobil Uygulama Deneyimi Cilas - Faz 3
 * Splash Screen, Bottom Sheet ve Native-like Navigasyon
 */

const mobileAppPolish = {
    init() {
        this.createSplashScreen();
        this.initBottomMenu();
        this.preventSystemScroll();
    },

    createSplashScreen() {
        // Eğer daha önce splash gösterildiyse (session) gösterme
        if (sessionStorage.getItem('splash_shown')) return;

        const splash = document.createElement('div');
        splash.id = 'app-splash';
        splash.className = 'fixed inset-0 z-[10000] bg-navy flex flex-col items-center justify-center transition-opacity duration-1000';
        splash.innerHTML = `
            <div class="relative">
                <!-- Logo Animasyonu -->
                <div class="w-24 h-24 border-2 border-gold rounded-full flex items-center justify-center animate-pulse">
                    <span class="text-gold text-4xl font-serif">İ</span>
                </div>
                <div class="absolute -inset-4 border border-gold/20 rounded-full animate-ping"></div>
            </div>
            <div class="mt-8 text-center">
                <h2 class="text-gold text-2xl font-serif tracking-[0.2em] uppercase mb-2">İmza</h2>
                <p class="text-gold/60 text-[10px] uppercase tracking-[0.4em]">Real Estate & Investment</p>
            </div>
            <!-- Yükleme Barı -->
            <div class="absolute bottom-20 w-48 h-[1px] bg-white/10 overflow-hidden">
                <div id="splash-progress" class="h-full bg-gold w-0 transition-all duration-[2000ms] ease-out"></div>
            </div>
        `;
        document.body.appendChild(splash);

        // İlerlemeyi başlat
        setTimeout(() => {
            const bar = document.getElementById('splash-progress');
            if (bar) bar.style.width = '100%';
        }, 100);

        // 2.5 saniye sonra kaldır
        setTimeout(() => {
            splash.style.opacity = '0';
            setTimeout(() => {
                splash.remove();
                sessionStorage.setItem('splash_shown', 'true');
            }, 1000);
        }, 2500);
    },

    initBottomMenu() {
        // Mobil cihazlarda alt menü (Native App Look)
        if (window.innerWidth < 768) {
            // İçeriğin menü altında kalmaması için body'ye padding ekle
            document.body.style.paddingBottom = '6rem';

            const bottomMenu = document.createElement('div');
            bottomMenu.className = 'fixed bottom-4 left-4 right-4 h-16 bg-white/90 backdrop-blur-xl rounded-2xl shadow-2xl border border-white/20 z-[9000] flex items-center justify-between px-8 text-navy/40';
            bottomMenu.innerHTML = `
                <button onclick="window.location.href='anasayfa.html'" class="flex flex-col items-center hover:text-gold transition-colors">
                    <i class="fa-solid fa-house text-lg"></i>
                    <span class="text-[8px] font-bold mt-1 uppercase">Ana</span>
                </button>
                <button onclick="window.location.href='portfoyler.html'" class="flex flex-col items-center hover:text-gold transition-colors">
                    <i class="fa-solid fa-building text-lg"></i>
                    <span class="text-[8px] font-bold mt-1 uppercase">İlan</span>
                </button>
                <div onclick="window.scrollTo({top: 0, behavior: 'smooth'})" class="w-12 h-12 bg-gold rounded-full -mt-10 flex items-center justify-center text-white shadow-lg border-4 border-white cursor-pointer active:scale-95 transition-transform">
                    <i class="fa-solid fa-arrow-up"></i>
                </div>
                <button onclick="window.location.href='favorites.html'" class="flex flex-col items-center hover:text-gold transition-colors">
                    <i class="fa-solid fa-heart text-lg"></i>
                    <span class="text-[8px] font-bold mt-1 uppercase">Favori</span>
                </button>
                <button onclick="window.location.href='portal.html'" class="flex flex-col items-center hover:text-gold transition-colors">
                    <i class="fa-solid fa-user text-lg"></i>
                    <span class="text-[8px] font-bold mt-1 uppercase">Profil</span>
                </button>
            `;
            document.body.appendChild(bottomMenu);
        }
    },

    preventSystemScroll() {
        // Mobil PWA deneyiminde elastik scroll bazen can sıkıcı olabilir
        // Gelişmiş kontrol gerekirse eklenebilir.
    }
};

document.addEventListener('DOMContentLoaded', () => mobileAppPolish.init());
