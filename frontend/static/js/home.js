/**
 * İmza Gayrimenkul - Anasayfa Logic
 * Extracted from inline script block for better maintainability (Audit Ref 3.0)
 * Enhanced: 3-Mode System (Demo/Placeholder/Live) + Lead Form + Shared Navigation + Maybach Scroll
 */

// ═══════════════════════════════════════════════════
// SHARED NAVIGATION & UI HELPERS
// ═══════════════════════════════════════════════════

function toggleSearch() {
    const modal = document.getElementById('searchModal');
    if (!modal) return;
    
    if (modal.classList.contains('invisible') || modal.classList.contains('opacity-0')) {
        modal.classList.remove('invisible', 'opacity-0');
        modal.classList.add('opacity-100', 'open');
        document.body.style.overflow = 'hidden';
    } else {
        modal.classList.remove('opacity-100', 'open');
        modal.classList.add('opacity-0');
        setTimeout(() => { 
            modal.classList.add('invisible'); 
            document.body.style.overflow = '';
        }, 400);
    }
}

function toggleMobileMenu() {
    const menu = document.getElementById('mobileMenu');
    const overlay = document.getElementById('menuOverlay');
    if (!menu || !overlay) return;
    
    if (menu.classList.contains('translate-x-full')) {
        menu.classList.remove('translate-x-full');
        overlay.classList.remove('hidden');
        setTimeout(() => overlay.classList.add('opacity-100'), 10);
        document.body.style.overflow = 'hidden';
    } else {
        menu.classList.add('translate-x-full');
        overlay.classList.remove('opacity-100');
        setTimeout(() => {
            overlay.classList.add('hidden');
            document.body.style.overflow = '';
        }, 300);
    }
}

// Lux Image Optimizer (Unsplash API Bridge)
function optimizeLuxuryImage(url, width = null) {
    if (!url || !url.includes('unsplash.com')) return url;
    const targetWidth = width || (window.innerWidth < 768 ? 800 : 1920);
    let baseUrl = url.split('?')[0];
    let params = new URLSearchParams(url.split('?')[1] || '');
    params.set('w', targetWidth);
    params.set('q', window.innerWidth < 768 ? 70 : 85); 
    params.set('auto', 'format');
    params.set('fit', 'crop');
    return `${baseUrl}?${params.toString()}`;
}

// Lux Curtain Bridge Logic
function luxNavigate(url) {
    const curtain = document.querySelector('.lux-curtain');
    if (curtain) {
        curtain.style.transition = 'opacity 1.1s cubic-bezier(0.16, 1, 0.3, 1)'; 
        curtain.classList.remove('hidden');
        setTimeout(() => { window.location.href = url; }, 1100);
    } else {
        window.location.href = url;
    }
}

// ═══════════════════════════════════════════════════
// MAYBACH SCROLL LOGIC (Full Page Snap)
// ═══════════════════════════════════════════════════

let currentSectionIndex = 0;
let isScrolling = false;
let maybachEnabled = localStorage.getItem('maybach_scroll') !== 'disabled';
const mainWrapper = document.getElementById('mainWrapper');
const sections = document.querySelectorAll('.intro-screen, section.snap-section, footer.snap-section');

function toggleMaybachScroll() {
    maybachEnabled = !maybachEnabled;
    localStorage.setItem('maybach_scroll', maybachEnabled ? 'enabled' : 'disabled');
    applyMaybachSettings();
}

function applyMaybachSettings() {
    const toggleDot = document.getElementById('toggleDot');
    const toggleBtn = document.getElementById('maybachToggle');
    const wrapper = document.getElementById('mainWrapper');
    
    if (maybachEnabled) {
        if (toggleDot) {
            toggleDot.style.transform = 'translateX(20px)';
            toggleDot.style.backgroundColor = '#c5a059'; 
        }
        if (toggleBtn) toggleBtn.style.backgroundColor = 'rgba(197, 160, 89, 0.2)';
        
        if (window.innerWidth >= 768) {
            document.documentElement.style.overflow = 'hidden';
            document.body.style.overflow = 'hidden';
            document.documentElement.style.height = '100%';
            document.body.style.height = '100%';
        }
    } else {
        if (toggleDot) {
            toggleDot.style.transform = 'translateX(0)';
            toggleDot.style.backgroundColor = '#9ca3af';
        }
        if (toggleBtn) toggleBtn.style.backgroundColor = 'rgba(255, 255, 255, 0.1)';
        
        document.documentElement.style.overflow = 'auto';
        document.body.style.overflow = 'auto';
        document.documentElement.style.height = 'auto';
        document.body.style.height = 'auto';
        if (wrapper) wrapper.style.transform = 'none';
        currentSectionIndex = 0;
    }
}

function goToSection(index) {
    const wrapper = document.getElementById('mainWrapper');
    const sectionsCount = document.querySelectorAll('.intro-screen, section.snap-section, footer.snap-section').length;
    
    if (!maybachEnabled || window.innerWidth < 768 || !wrapper) return; 
    if (index < 0 || index >= sectionsCount || isScrolling) return;

    isScrolling = true;
    currentSectionIndex = index;
    const yOffset = index * 100;
    wrapper.style.transform = `translateY(-${yOffset}vh)`;

    setTimeout(() => { isScrolling = false; }, 1100);
}

// ═══════════════════════════════════════════════════
// HERO SLIDER LOGIC
// ═══════════════════════════════════════════════════

let slides = [];
let dots = [];
let currentSlide = 0;
let slideInterval;

async function initHeroSlider() {
    try {
        let heroData = [];
        try {
            const response = await fetch('/api/v1/hero');
            if (response.ok) {
                heroData = await response.json();
            } else {
                throw new Error("Fallback mode");
            }
        } catch (e) {
            console.warn("[İmza] Hero API unavailable, using fallback data.");
            heroData = [
                { id: 1, image_url: 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=1920', alt_title: 'Koleksiyon 01 // Executive' },
                { id: 2, image_url: 'https://images.unsplash.com/photo-1600607687920-4e2a09cf159d?w=1920', alt_title: 'Koleksiyon 02 // Panorama' }
            ];
        }

        const wrapper = document.getElementById('hero-slides-wrapper');
        const dotsContainer = document.getElementById('slider-dots');
        if (!wrapper || !dotsContainer) return;

        wrapper.innerHTML = '';
        dotsContainer.innerHTML = '';

        if (window.ImzaLensUI && window.ImzaLensUI.injectHeroCampaign) {
            await ImzaLensUI.injectHeroCampaign('hero-slides-wrapper', 'slider-dots');
        }

        heroData.forEach((item, index) => {
            const optimizedImg = optimizeLuxuryImage(item.image_url);
            const isFirst = index === 0 && wrapper.children.length === 0;
            
            const slide = document.createElement('div');
            slide.className = `absolute inset-0 transition-opacity duration-1000 hero-slide ${isFirst ? 'opacity-100 z-10 active' : 'opacity-0 z-0'}`;
            slide.innerHTML = `<img src="${optimizedImg}" class="w-full h-full object-cover"><div class="absolute inset-0 bg-gradient-to-b from-navy/40 to-navy/80"></div>`;
            wrapper.appendChild(slide);

            const dot = document.createElement('button');
            dot.className = `w-12 h-1 rounded-full transition-all ${isFirst ? 'bg-gold' : 'bg-white/30'}`;
            dot.onclick = () => goToSlide(index);
            dotsContainer.appendChild(dot);
        });

        slides = document.querySelectorAll('.hero-slide');
        dots = dotsContainer.querySelectorAll('button');
        resetInterval();
    } catch (e) { console.error("Slider init failed", e); }
}

function goToSlide(index) {
    if (!slides.length) return;
    slides[currentSlide].classList.remove('opacity-100', 'z-10', 'active');
    slides[currentSlide].classList.add('opacity-0', 'z-0');
    dots[currentSlide].classList.replace('bg-gold', 'bg-white/30');
    currentSlide = index;
    slides[currentSlide].classList.remove('opacity-0', 'z-0');
    slides[currentSlide].classList.add('opacity-100', 'z-10', 'active');
    dots[currentSlide].classList.replace('bg-white/30', 'bg-gold');
    resetInterval();
}

function nextSlide() { if (slides.length > 1) goToSlide((currentSlide + 1) % slides.length); }
function prevSlide() { if (slides.length > 1) goToSlide((currentSlide - 1 + slides.length) % slides.length); }
function resetInterval() { clearInterval(slideInterval); slideInterval = setInterval(nextSlide, 7000); }

// ═══════════════════════════════════════════════════
// PORTFOLIO & COLLECTIONS
// ═══════════════════════════════════════════════════

let allPortfolios = [];
let activePortfolioTab = 'tumu';

async function renderPortfolios(filterCategory = 'tumu') {
    activePortfolioTab = filterCategory;
    const container = document.getElementById('portfoy-list-container');
    if (!container) return;

    if (allPortfolios.length === 0) {
        try {
            const res = await fetch(`/api/v1/portfolios?lang=${i18n.getLang()}`);
            allPortfolios = await res.json();
        } catch (e) { console.warn("Portfolio fetch failed"); }
    }

    const filtered = filterCategory === 'tumu' ? allPortfolios : allPortfolios.filter(p => (p.category || '').toLowerCase().includes(filterCategory.toLowerCase()));
    container.innerHTML = '';
    filtered.slice(0, 3).forEach(item => {
        const cat = (item.category || '').toLowerCase();
        let theme = { text: 'text-gold', tag: 'bg-navy text-gold', label: 'Prestij' };
        if (cat.includes('modern')) theme = { text: 'text-modern', tag: 'bg-modern text-white', label: 'Modern' };
        else if (cat.includes('doğa') || cat.includes('doga')) theme = { text: 'text-natureLight', tag: 'bg-natureLight text-white', label: 'Doğa' };

        const fiyatKisa = String(item.price || '0').replace('0.000', 'M').replace('.000', 'K').replace('₺', '').trim();
        container.innerHTML += `
            <div onclick="luxNavigate('detay.html?id=${item.id}')" class="group bg-white rounded-[2.5rem] overflow-hidden shadow-sm hover:shadow-2xl transition-all duration-700 flex flex-col border border-gray-50 cursor-pointer h-full">
                <div class="relative h-56 md:h-64 overflow-hidden">
                    <img src="${optimizeLuxuryImage(item.image_hero, 600)}" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-700">
                    <div class="absolute bottom-0 left-0 right-0 p-6 bg-gradient-to-t from-navy/80 to-transparent text-white"><span class="font-serif font-bold text-2xl">₺${fiyatKisa}</span></div>
                </div>
                <div class="p-6 md:p-8 flex-1 flex flex-col justify-between">
                    <h3 class="font-bold text-navy text-base md:text-xl group-hover:${theme.text} transition-colors mb-1 uppercase tracking-tight line-clamp-2">${item.title}</h3>
                    <p class="text-gray-500 text-[10px] uppercase font-bold tracking-widest truncate">${item.location}</p>
                    <div class="grid grid-cols-3 border-t border-gray-100 pt-6 mt-4 gap-2 text-center text-xs font-bold text-navy">
                        <div><p class="text-[8px] text-gray-400 uppercase">Oda</p>${item.rooms}</div>
                        <div><p class="text-[8px] text-gray-400 uppercase">Alan</p>${item.area}</div>
                        <div class="${theme.text}"><p class="text-[8px] text-gray-400 uppercase">Tip</p>${theme.label}</div>
                    </div>
                </div>
            </div>`;
    });
    updateTabClasses(filterCategory);
}

function updateTabClasses(activeTabId) {
    document.querySelectorAll('#portfolio-tabs button').forEach(btn => {
        btn.id === 'tab-' + activeTabId 
            ? btn.className = 'bg-navy text-gold px-6 py-1.5 rounded-full text-[9px] font-black uppercase shadow-xl transition-all'
            : btn.className = 'bg-white/80 text-gray-400 hover:text-navy px-6 py-1.5 rounded-full text-[9px] font-black uppercase border border-gray-100 transition-all';
    });
}

function discoverAllPortfolios() { luxNavigate(activePortfolioTab === 'tumu' ? 'arama.html' : `arama.html?koleksiyon=${activePortfolioTab}`); }

function renderCollections() {
    const grid = document.getElementById('collections-grid');
    if (!grid) return;
    const collections = {
        'prestij': { title: 'Prestij', img: 'https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800', icon: 'fas fa-crown', color: 'gold', featured: true },
        'modern': { title: 'Modern', img: 'https://images.unsplash.com/photo-1600607687939-ce8a6c25118c?w=800', icon: 'fas fa-city', color: 'white' },
        'doga': { title: 'Doğa', img: 'https://images.unsplash.com/photo-1500382017468-9049fed747ef?w=800', icon: 'fas fa-leaf', color: 'natureLight' }
    };
    grid.innerHTML = Object.entries(collections).map(([key, data]) => `
        <div onclick="luxNavigate('koleksiyon.html?tip=${key}')" class="relative ${data.featured ? 'h-full md:row-span-2 md:col-span-2' : 'h-[220px]'} rounded-[2.5rem] overflow-hidden group cursor-pointer shadow-2xl bento-card">
            <img src="${data.img}" class="absolute inset-0 w-full h-full object-cover group-hover:scale-110 transition-transform duration-1000">
            <div class="absolute inset-0 bg-gradient-to-t from-navy/90 to-transparent"></div>
            <div class="absolute bottom-10 left-10 text-white">
                <div class="w-12 h-12 bg-${data.color === 'white' ? 'white/20' : 'gold'} rounded-2xl flex items-center justify-center text-navy mb-4"><i class="${data.icon} text-xl"></i></div>
                <h3 class="text-3xl font-serif font-bold text-${data.color === 'white' ? 'white' : 'gold'} uppercase">${data.title}</h3>
            </div>
        </div>`).join('');
}

// ═══════════════════════════════════════════════════
// INITIALIZATION
// ═══════════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', () => {
    // Basic Page Setup
    applyMaybachSettings();
    const curtain = document.querySelector('.lux-curtain');
    if (curtain) setTimeout(() => curtain.classList.add('hidden'), 100);

    // Scroll Events
    window.addEventListener('scroll', () => {
        const header = document.querySelector('header');
        if (header) window.scrollY > 50 ? header.classList.add('glass-header') : header.classList.remove('glass-header');
    });

    // Maybach Scroll Wheel/Keys
    window.addEventListener('wheel', (e) => {
        if (!isScrolling && Math.abs(e.deltaY) > 50) goToSection(currentSectionIndex + (e.deltaY > 0 ? 1 : -1));
    }, { passive: false });

    window.addEventListener('keydown', (e) => {
        if (!isScrolling) {
            if (e.key === 'ArrowDown') goToSection(currentSectionIndex + 1);
            if (e.key === 'ArrowUp') goToSection(currentSectionIndex - 1);
        }
    });

    // Mobile Swipe (Maybach)
    let touchStartY = 0;
    window.addEventListener('touchstart', (e) => { touchStartY = e.touches[0].clientY; }, { passive: true });
    window.addEventListener('touchmove', (e) => {
        if (isScrolling) return;
        const touchEndY = e.touches[0].clientY;
        if (touchStartY - touchEndY > 50) goToSection(currentSectionIndex + 1);
        else if (touchEndY - touchStartY > 50) goToSection(currentSectionIndex - 1);
    }, { passive: true });

    // Page Specific Inits
    if (document.getElementById('hero-slides-wrapper')) initHeroSlider();
    if (document.getElementById('portfoy-list-container')) renderPortfolios();
    if (document.getElementById('collections-grid')) renderCollections();
});

// Export functions to window
window.toggleSearch = toggleSearch;
window.toggleMobileMenu = toggleMobileMenu;
window.goToSection = goToSection;
window.toggleMaybachScroll = toggleMaybachScroll;
window.luxNavigate = luxNavigate;
window.renderPortfolios = renderPortfolios;
window.discoverAllPortfolios = discoverAllPortfolios;
window.nextSlide = nextSlide;
window.prevSlide = prevSlide;
window.startLifestyle = () => { document.getElementById('lm-intro')?.classList.add('hidden'); document.getElementById('lm-q1')?.classList.remove('hidden'); };
window.lmAnswer = (q, a) => { 
    lmAnswers[q] = a; 
    document.getElementById('lm-q'+q)?.classList.add('hidden'); 
    if(q<4) document.getElementById('lm-q'+(q+1))?.classList.remove('hidden'); 
    else showLifestyleResult(); 
};
window.resetLifestyle = () => { lmAnswers={}; document.querySelectorAll('.lm-question').forEach(q=>q.classList.add('hidden')); document.getElementById('lm-intro')?.classList.remove('hidden'); };
