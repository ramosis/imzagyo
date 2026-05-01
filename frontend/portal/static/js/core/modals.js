const MODALS = {
    'campaign': '/portal/sections/modals/campaign',
    'appointment': '/portal/sections/modals/appointment',
    'reschedule': '/portal/sections/modals/reschedule',
    'publish-wizard': '/portal/sections/modals/publish-wizard',
    'logout-confirm': '/portal/sections/modals/logout-confirm',
    'hero-slide-over': '/portal/sections/modals/hero-slide-over',
    'user': '/portal/sections/modals/user',
    'portfolio-slide-over': '/portal/sections/modals/portfolio-slide-over',
    'lead': '/portal/sections/modals/lead',
    'contact': '/portal/sections/modals/contact',
    'expense': '/portal/sections/modals/expense',
    'tax': '/portal/sections/modals/tax',
    'maintenance': '/portal/sections/modals/maintenance',
    'portfolio': '/portal/sections/modals/portfolio',
    'password-reset': '/portal/sections/modals/password-reset',
    'new-password': '/portal/sections/modals/new-password',
    'rule': '/portal/sections/modals/rule',
    'template': '/portal/sections/modals/template',
    'media': '/portal/sections/modals/media',
    'route-playback': '/portal/sections/modals/route-playback'
};

const loadedModals = new Set();

export async function loadModal(modalName) {
    if (loadedModals.has(modalName)) return true;

    const url = MODALS[modalName];
    if (!url) {
        console.error(`[İmza Modals] Modal bulunamadı: ${modalName}`);
        return false;
    }

    const container = document.getElementById('modal-container');
    if (!container) {
        console.error("[İmza Modals] #modal-container bulunamadı.");
        return false;
    }

    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const html = await response.text();
        
        // Append to container instead of replacing
        const tempDiv = document.createElement('div');
        tempDiv.innerHTML = html;
        container.appendChild(tempDiv.firstElementChild);
        
        loadedModals.add(modalName);
        console.log(`[İmza Modals] Modal yüklendi: ${modalName}`);
        return true;
    } catch (err) {
        console.error(`[İmza Modals] Modal yükleme hatası (${modalName}):`, err);
        return false;
    }
}

// Global helper to load and then show a modal
window.ensureModal = async function(modalName, modalId) {
    const success = await loadModal(modalName);
    if (success) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.remove('hidden');
            if (modal.classList.contains('flex')) {
                // Already has flex, keep it
            } else if (modalId.includes('modal')) {
                 modal.classList.add('flex');
            }
            return modal;
        }
    }
    return null;
};
