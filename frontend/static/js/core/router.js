export const SECTIONS = {
    // 1. AI & Strateji
    'dashboard': '/portal/sections/dashboard',
    'imza-lens': '/portal/sections/imza-lens',
    'ai-reports': '/portal/sections/ai-reports',
    'market-analytics': '/portal/sections/market-analytics',
    'global-sync': '/portal/sections/global-sync',
    
    // 2. Portföy & Saha
    'portfolios': '/portal/sections/portfolios',
    'media-center': '/portal/sections/media-center',
    'projects': '/portal/sections/projects',
    
    // 3. Müşteri & CRM
    'leads': '/portal/sections/leads',
    'pipeline': '/portal/sections/pipeline',
    'project-hub': '/portal/sections/project-hub',
    'appointments': '/portal/sections/appointments',
    'contacts': '/portal/sections/contacts',
    
    // 4. Sözleşme & Hukuk
    'contracts': '/portal/sections/contracts',
    'contract-builder': '/portal/sections/contract-builder',
    'payroll': '/portal/sections/payroll',
    
    // 5. Finans & Muhasebe
    'finance': '/portal/sections/finance',
    'taxes': '/portal/sections/taxes',
    'taxes-calculator': '/portal/sections/taxes-calculator',
    'expenses': '/portal/sections/expenses',
    
    // 6. Pazarlama & Otomasyon
    'campaigns': '/portal/sections/campaigns',
    'integrations': '/portal/sections/integrations',
    
    // 7. Teknik & Operasyon
    'maintenance': '/portal/sections/maintenance',
    
    // 8. Sistem & Ayarlar
    'users': '/portal/sections/users',
    'system-settings': '/portal/sections/system-settings',
    'cms': '/portal/sections/cms',
    'notices': '/portal/sections/notices',
    'neighborhood': '/portal/sections/neighborhood',
    'apartments': '/portal/sections/apartments'
};

export async function loadSection(sectionId) {
    const url = SECTIONS[sectionId];
    if (!url) {
        console.error(`[İmza Router] Section bulunamadı: ${sectionId}`);
        return false;
    }

    const container = document.getElementById('section-container');
    if (!container) {
        console.error("[İmza Router] #section-container bulunamadı.");
        return false;
    }

    try {
        const response = await fetch(url);
        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
        const html = await response.text();
        
        container.innerHTML = html;
        
        // Dispatch event for other modules to re-bind events
        window.dispatchEvent(new CustomEvent('sectionShown', { detail: { sectionId } }));
        
        console.log(`[İmza Router] Section yüklendi: ${sectionId}`);
        return true;
    } catch (err) {
        console.error(`[İmza Router] Yükleme hatası (${sectionId}):`, err);
        return false;
    }
}

window.showSection = function(sectionId, element) {
    loadSection(sectionId).then(success => {
        if (success) {
            // Update sidebar active state
            document.querySelectorAll('.nav-item').forEach(link => {
                link.classList.remove('active', 'bg-gold/10', 'text-gold');
            });
            if (element) {
                element.classList.add('active', 'bg-gold/10', 'text-gold');
            } else {
                // Find by data-section or something if needed
                const target = document.querySelector(`[onclick*="'${sectionId}'"]`);
                if (target) target.classList.add('active', 'bg-gold/10', 'text-gold');
            }
        }
    });
};
