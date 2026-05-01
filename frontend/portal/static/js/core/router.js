const SECTIONS = {
    'dashboard': '/portal/sections/dashboard',
    'imza-lens': '/portal/sections/imza-lens',
    'portfolios': '/portal/sections/portfolios',
    'leads': '/portal/sections/leads',
    'finance': '/portal/sections/finance',
    'ai-reports': '/portal/sections/ai-reports',
    'analytics': '/portal/sections/analytics',
    'settings': '/portal/sections/settings',
    'campaigns': '/portal/sections/campaigns',
    'market-analytics': '/portal/sections/market-analytics',
    'contract-builder': '/portal/sections/contract-builder',
    'global-sync': '/portal/sections/global-sync',
    'barter-wizard': '/portal/sections/barter-wizard',
    'projects': '/portal/sections/projects',
    'users': '/portal/sections/users',
    'contracts': '/portal/sections/contracts',
    'taxes': '/portal/sections/taxes',
    'maintenance': '/portal/sections/maintenance',
    'appointments': '/portal/sections/appointments',
    'integrations': '/portal/sections/integrations',
    'contacts': '/portal/sections/contacts',
    'expenses': '/portal/sections/expenses',
    'system-settings': '/portal/sections/system-settings',
    'project-hub': '/portal/sections/project-hub',
    'media-center': '/portal/sections/media-center',
    'cms': '/portal/sections/cms',
    'notices': '/portal/sections/notices',
    'neighborhood': '/portal/sections/neighborhood',
    'apartments': '/portal/sections/apartments',
    'customer-portal': '/portal/sections/customer-portal'
};

async function showSection(sectionId, btnElement) {
    console.log("[İmza Portal] showSection (Lazy Load) çağrıldı:", sectionId);
    const container = document.getElementById('section-container');
    if (!container) {
        console.error("Shell hatası: #section-container bulunamadı.");
        return;
    }

    // Role Check
    const currentRole = localStorage.getItem('imza_admin_role') || 'admin';
    const targetBtn = btnElement || document.querySelector(`button[onclick*="'${sectionId}'"]`);
    if (targetBtn && targetBtn.hasAttribute('data-access')) {
        const requiredAccess = targetBtn.getAttribute('data-access');
        if (requiredAccess === 'admin' && currentRole !== 'admin') {
            if (typeof showToast === 'function') showToast('Bu bölüme erişim yetkiniz yok.', 'error');
            return;
        }
    }

    // Lazy Load HTML
    const url = SECTIONS[sectionId];
    if (url) {
        try {
            const response = await fetch(url);
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const html = await response.text();
            container.innerHTML = html;
        } catch (err) {
            console.error('Section load error:', err);
            if (typeof showToast === 'function') showToast('Sayfa parçası yüklenemedi.', 'error');
            return;
        }
    }

    // Sidebar highlight
    document.querySelectorAll('#sidebar nav .nav-item').forEach(a => {
        a.classList.remove('bg-gold/10', 'text-gold', 'border-r-4', 'border-gold');
    });
    if (btnElement) {
        btnElement.classList.add('bg-gold/10', 'text-gold', 'border-r-4', 'border-gold');
    }

    // Dispatch a custom event so specific modules can load data when their section is shown
    const event = new CustomEvent('sectionShown', { detail: { sectionId: sectionId } });
    document.dispatchEvent(event);
}

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebar-overlay');
    
    if (sidebar) {
        sidebar.classList.toggle('-translate-x-full');
        if (overlay) overlay.classList.toggle('hidden');
        
        if (!sidebar.classList.contains('-translate-x-full') && window.innerWidth < 1024) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = '';
        }
    }
}
