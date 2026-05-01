import { checkAuth, login, logout, switchRole } from '../core/auth.js';
import { loadSection, showSection } from '../core/router.js';
import { initPortfolioEvents } from '../modules/portfolio.js';
import { initCrmEvents } from '../modules/crm.js';
import { initMarketing } from '../modules/marketing.js';
import { showToast } from '../core/ui.js';

/**
 * Main Portal Initialization
 */
document.addEventListener('DOMContentLoaded', async () => {
    console.log("[İmza Portal] Başlatılıyor...");

    // 1. Auth Check
    const isAuthenticated = checkAuth();
    if (!isAuthenticated) {
        initLoginEvents();
        return;
    }

    // 2. Initialize Core Modules
    initGlobalEvents();
    initPortfolioEvents();
    initCrmEvents();

    // 3. Section Lifecycle Hooks
    window.addEventListener('sectionShown', (e) => {
        if (e.detail.sectionId === 'campaigns') {
            initMarketing();
        }
    });

    // 4. Load Initial Section (Dashboard or from URL hash)
    const initialSection = getInitialSection();
    showSection(initialSection);

    console.log("[İmza Portal] Modüler yapı hazır.");
});

function getInitialSection() {
    const hash = window.location.hash.replace('#', '');
    return hash || 'dashboard';
}

function initLoginEvents() {
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const username = loginForm.username.value;
            const password = loginForm.password.value;
            await login(username, password);
        });
    }
}

function initGlobalEvents() {
    // Sidebar Toggles
    document.addEventListener('click', (e) => {
        if (e.target.closest('#sidebar-toggle')) {
            toggleSidebar();
        }
        
        if (e.target.closest('#sidebar-overlay')) {
            toggleSidebar();
        }

        // Nav Items (using delegation)
        const navItem = e.target.closest('.nav-item');
        if (navItem && navItem.dataset.section) {
            showSection(navItem.dataset.section, navItem);
            if (window.innerWidth < 1024) toggleSidebar(); // Auto-close on mobile
        }

        // Logout
        if (e.target.closest('#logout-btn')) {
            logout();
        }

        // Role Switch
        const roleBtn = e.target.closest('[data-role]');
        if (roleBtn) {
            switchRole(roleBtn.dataset.role);
        }
    });

    // Hash Change support
    window.addEventListener('hashchange', () => {
        const sectionId = window.location.hash.replace('#', '');
        if (sectionId) showSection(sectionId);
    });
}

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebar-overlay');
    if (sidebar) {
        sidebar.classList.toggle('-translate-x-full');
        if (overlay) overlay.classList.toggle('hidden');
    }
}

// Global exposure for legacy scripts if needed during transition
window.showSection = showSection;
window.showToast = showToast;
