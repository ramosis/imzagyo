/**
 * İmza Gayrimenkul - Anasayfa Logic
 * Extracted from inline script block for better maintainability (Audit Ref 3.0)
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
});
