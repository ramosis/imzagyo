// --- PORTAL PAGES JS ---
document.addEventListener('DOMContentLoaded', () => {
    console.log('[İmza Portal] DOM Yüklendi, init ediliyor...');

    // Sidebar Navigation Listener
    const sidebar = document.getElementById('sidebar');
    if (sidebar) {
        sidebar.addEventListener('click', (e) => {
            const btn = e.target.closest('.nav-item');
            if (btn && btn.dataset.section) {
                if (typeof showSection === 'function') {
                    showSection(btn.dataset.section, btn);
                }
            }
        });
    }
    
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
    document.addEventListener('sectionShown', async (e) => {
        const sectionId = e.detail.sectionId;
        console.log(`[Portal] Event Captured: sectionShown -> ${sectionId}`);
        
        // Dinamik modül yükleme (Phase 9 ve sonrası için)
        if (sectionId === 'customer-portal') {
            try {
                const { customer_portal } = await import('/static/js/modules/customer_portal.js');
                if (customer_portal && customer_portal.init) {
                    await customer_portal.init();
                }
            } catch (err) {
                console.error("Modül yükleme hatası:", err);
            }
        }
        
        // Mevcut global fonksiyonlu modülleri de buradan çağırabiliriz
        if (sectionId === 'leads' && typeof fetchLeads === 'function') fetchLeads();
    });
    
    // Close dropdowns on outside click (premium UI helper)
    document.addEventListener('click', (e) => {
        if (!e.target.closest('.premium-dropdown')) {
            document.querySelectorAll('.dropdown-menu.active').forEach(d => d.classList.remove('active'));
        }
    });
});