// --- PORTAL PAGES JS ---
document.addEventListener('DOMContentLoaded', () => {
    console.log('[İmza Portal] DOM Yüklendi, init ediliyor...');
    
    // Check Auth when portal loads
    if (typeof checkAuth === 'function') {
        checkAuth();
    }
    
    // Setup Sidebar Toggle if exists
    const toggleBtn = document.getElementById('sidebar-toggle');
    if (toggleBtn) {
        // Prevent multiple bindings if it has inline onclick, but adding it for safety
        if (!toggleBtn.onclick) {
            toggleBtn.addEventListener('click', () => {
                if (typeof toggleSidebar === 'function') toggleSidebar();
            });
        }
    }
    
    // Listen for custom 'sectionShown' events dispatched by router.js
    document.addEventListener('sectionShown', (e) => {
        const sectionId = e.detail.sectionId;
        console.log(`[Portal] Event Captured: sectionShown -> ${sectionId}`);
        // Optionally bind specific page-level logic here if needed
    });
    
    // Close dropdowns on outside click (premium UI helper)
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.premium-dropdown')) {
            document.querySelectorAll('.dropdown-menu.active').forEach(d => d.classList.remove('active'));
        }
    });
});