/**
 * İmza Gayrimenkul - Anasayfa Logic
 * Extracted from inline script block for better maintainability (Audit Ref 3.0)
 * Enhanced: 3-Mode System (Demo/Placeholder/Live) + Lead Form
 */

// Lux Image Optimizer (Unsplash API Bridge)
function optimizeLuxuryImage(url, width = null) {
    if (!url || !url.includes('unsplash.com')) return url;
    const targetWidth = width || (window.innerWidth < 768 ? 800 : 1920);
    
    // Clean existing w param and add new one
    let baseUrl = url.split('?')[0];
    let params = new URLSearchParams(url.split('?')[1] || '');
    params.set('w', targetWidth);
    params.set('q', window.innerWidth < 768 ? 70 : 85); 
    params.set('auto', 'format');
    params.set('fit', 'crop');
    
    return `${baseUrl}?${params.toString()}`;
}

// Lux Curtain Bridge Logic (Fluid Outro, Luxury Intro)
function luxNavigate(url) {
    const curtain = document.querySelector('.lux-curtain');
    if (curtain) {
        curtain.style.transition = 'opacity 1.1s cubic-bezier(0.16, 1, 0.3, 1)'; 
        curtain.classList.remove('hidden');
        setTimeout(() => {
            window.location.href = url;
        }, 1100);
    } else {
        window.location.href = url;
    }
}

// Header Glass Effect
window.addEventListener('scroll', function () {
    const header = document.querySelector('header');
    if (header) {
        if (window.scrollY > 50) {
            header.classList.add('glass-header');
        } else {
            header.classList.remove('glass-header');
        }
    }
});

// ═══════════════════════════════════════════════════
// 3-MODE SYSTEM: Site Mode Aware Portfolio Rendering
// ═══════════════════════════════════════════════════

/**
 * Checks site_mode and renders appropriate content:
 * - demo: Shows all portfolios (including samples)  
 * - placeholder: Shows Geo-SEO empty state + lead form
 * - live: Shows only real (non-sample) portfolios
 */
async function checkSiteModeAndRender() {
    try {
        const res = await fetch('/api/v1/settings/site_mode');
        const data = await res.json();
        const mode = data.site_mode || 'placeholder';
        
        const container = document.getElementById('portfoy-list-container');
        if (!container) return;
        
        if (mode === 'placeholder') {
            renderGeoPlaceholder(container);
        }
        // demo and live modes: API already filters, frontend just renders normally
    } catch (err) {
        console.warn('Site mode check failed, using existing content:', err);
    }
}

/**
 * Renders the Geo-SEO placeholder with lead form when no listings are available
 */
function renderGeoPlaceholder(container) {
    container.innerHTML = `
        <div class="empty-state-geo col-span-full" itemscope itemtype="https://schema.org/RealEstateAgent">
            <meta itemprop="name" content="İmza Emlak - Kütahya"/>
            <meta itemprop="areaServed" content="Kütahya, Türkiye"/>
            
            <div class="empty-state-geo__icon">
                <i class="fa-solid fa-building-columns"></i>
            </div>
            
            <h3 class="empty-state-geo__title">
                Kütahya'da Yeni Dönem Başlıyor
            </h3>
            
            <p class="empty-state-geo__subtitle">
                İmza Gayrimenkul, Kütahya'nın en prestijli lokasyonlarında 
                benzersiz yatırım fırsatlarını sizinle buluşturmaya hazırlanıyor. 
                Lansman öncesi bildirim alın.
            </p>
            
            <div class="empty-state-geo__stats">
                <div class="empty-state-geo__stat">
                    <span class="empty-state-geo__stat-value">43</span>
                    <span class="empty-state-geo__stat-label">İlçe Kapsama</span>
                </div>
                <div class="empty-state-geo__stat">
                    <span class="empty-state-geo__stat-value">7/24</span>
                    <span class="empty-state-geo__stat-label">Danışmanlık</span>
                </div>
                <div class="empty-state-geo__stat">
                    <span class="empty-state-geo__stat-value">%100</span>
                    <span class="empty-state-geo__stat-label">Şeffaf</span>
                </div>
            </div>
            
            <!-- Lead Form -->
            <div class="lead-form-wrapper">
                <form class="lead-form" id="geoLeadForm" onsubmit="return submitGeoLeadForm(event)">
                    <h4 class="lead-form__title">
                        <i class="fa-solid fa-bell" style="margin-right: 0.5rem; font-size: 0.9em;"></i>
                        Bize Ulaşın
                    </h4>
                    <p class="lead-form__subtitle">
                        İhtiyacınıza uygun portföyleri sizin için bulalım.
                    </p>
                    
                    <div class="lead-form__options" id="leadActionOptions">
                        <div class="lead-form__option">
                            <input type="radio" name="action_type" id="lead_buy" value="buy" checked>
                            <label for="lead_buy">
                                <i class="fa-solid fa-house-chimney"></i> Satılık Arıyorum
                            </label>
                        </div>
                        <div class="lead-form__option">
                            <input type="radio" name="action_type" id="lead_rent" value="rent">
                            <label for="lead_rent">
                                <i class="fa-solid fa-key"></i> Kiralık Arıyorum
                            </label>
                        </div>
                        <div class="lead-form__option">
                            <input type="radio" name="action_type" id="lead_sell" value="sell">
                            <label for="lead_sell">
                                <i class="fa-solid fa-tag"></i> Mülkümü Satmak İstiyorum
                            </label>
                        </div>
                        <div class="lead-form__option">
                            <input type="radio" name="action_type" id="lead_lease" value="lease">
                            <label for="lead_lease">
                                <i class="fa-solid fa-file-signature"></i> Mülkümü Kiraya Vermek İstiyorum
                            </label>
                        </div>
                    </div>
                    
                    <div class="lead-form__group">
                        <input type="text" class="lead-form__input" id="leadName" name="name" 
                               placeholder="Adınız Soyadınız" required autocomplete="name">
                    </div>
                    <div class="lead-form__group">
                        <input type="tel" class="lead-form__input" id="leadPhone" name="phone" 
                               placeholder="Telefon (0 5XX XXX XX XX)" autocomplete="tel">
                    </div>
                    <div class="lead-form__group">
                        <input type="email" class="lead-form__input" id="leadEmail" name="email" 
                               placeholder="E-posta (opsiyonel)" autocomplete="email">
                    </div>
                    
                    <button type="submit" class="lead-form__submit" id="leadSubmitBtn">
                        <i class="fa-solid fa-paper-plane" style="margin-right: 0.5rem;"></i>
                        Haber Ver
                    </button>
                </form>
                
                <div class="lead-form__success" id="leadFormSuccess">
                    <div class="lead-form__success-icon">
                        <i class="fa-solid fa-check-circle"></i>
                    </div>
                    <h4 class="lead-form__success-title">Teşekkürler!</h4>
                    <p class="lead-form__success-text">
                        Bilgileriniz alındı. En kısa sürede sizinle iletişime geçeceğiz.
                    </p>
                </div>
            </div>
        </div>
    `;
}

/**
 * Handles lead form submission
 */
async function submitGeoLeadForm(e) {
    e.preventDefault();
    
    const form = document.getElementById('geoLeadForm');
    const submitBtn = document.getElementById('leadSubmitBtn');
    const successDiv = document.getElementById('leadFormSuccess');
    
    if (!form || !submitBtn || !successDiv) return false;
    
    const nameEl = document.getElementById('leadName');
    const phoneEl = document.getElementById('leadPhone');
    const emailEl = document.getElementById('leadEmail');
    
    if (!nameEl || !phoneEl || !emailEl) return false;

    const name = nameEl.value.trim();
    const phone = phoneEl.value.trim();
    const email = emailEl.value.trim();
    const actionType = document.querySelector('input[name="action_type"]:checked')?.value || 'buy';
    
    if (!name || (!phone && !email)) {
        // Shake animation for validation
        form.style.animation = 'shake 0.5s ease';
        setTimeout(() => form.style.removeProperty('animation'), 500);
        return false;
    }
    
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<i class="fa-solid fa-spinner fa-spin" style="margin-right: 0.5rem;"></i> Gönderiliyor...';
    
    try {
        const res = await fetch('/api/v1/leads/public', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, phone, email, action_type: actionType })
        });
        
        if (res.ok) {
            form.style.display = 'none';
            successDiv.classList.add('active');
        } else {
            const err = await res.json();
            alert(err.error || 'Bir hata oluştu. Lütfen tekrar deneyin.');
            submitBtn.disabled = false;
            submitBtn.innerHTML = '<i class="fa-solid fa-paper-plane" style="margin-right: 0.5rem;"></i> Haber Ver';
        }
    } catch (err) {
        alert('Bağlantı hatası. Lütfen internet bağlantınızı kontrol edin.');
        submitBtn.disabled = false;
        submitBtn.innerHTML = '<i class="fa-solid fa-paper-plane" style="margin-right: 0.5rem;"></i> Haber Ver';
    }
    
    return false;
}

// ═══════════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', () => {
    // Intro Transition
    const curtain = document.querySelector('.lux-curtain');
    if (curtain) {
        curtain.style.transition = 'opacity 1.1s cubic-bezier(0.16, 1, 0.3, 1)';
        setTimeout(() => {
            curtain.classList.add('hidden');
        }, 100);
    }

    // Bfcache fix for back button
    window.addEventListener('pageshow', (event) => {
        if (event.persisted) {
            const curtain = document.querySelector('.lux-curtain');
            if (curtain) curtain.classList.add('hidden');
        }
    });

    // Link Interceptor for Smooth Transitions
    document.addEventListener('click', (e) => {
        const link = e.target.closest('a');
        if (link && link.href && link.href.includes('.html') && !link.target && !e.ctrlKey && !e.shiftKey) {
            const targetUrl = link.href;
            const isInternal = targetUrl.includes(window.location.origin) || !targetUrl.startsWith('http');

            if (isInternal && !targetUrl.includes('#')) {
                e.preventDefault();
                luxNavigate(targetUrl);
            }
        }
    });

    // Initialize Dynamic Collections
    if (typeof renderCollections === 'function') {
        renderCollections();
    }
    
    // 3-Mode System: Check site mode and render appropriate content
    checkSiteModeAndRender();
});
