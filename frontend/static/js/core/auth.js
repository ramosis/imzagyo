import { apiFetch, API_BASE } from './api.js';
import { showToast } from './ui.js';

export function checkAuth() {
    const token = localStorage.getItem('imza_admin_token');
    const role = localStorage.getItem('imza_admin_role') || 'admin';
    const loginSection = document.getElementById('login-section');
    const portalApp = document.getElementById('portal-app');
    
    if (token) {
        if (loginSection) loginSection.classList.add('hidden');
        if (portalApp) {
            portalApp.classList.remove('hidden');
            portalApp.classList.add('show-app');
        }
        
        // Sync UI with user info
        const userSpan = document.getElementById('sidebar-user-name');
        if (userSpan) userSpan.textContent = localStorage.getItem('imza_admin_username') || 'Yönetici';
        
        updateRoleUI(role);
        return true;
    } else {
        if (loginSection) loginSection.classList.remove('hidden');
        if (portalApp) portalApp.classList.add('hidden');
        return false;
    }
}

export async function login(username, password) {
    const loginBtn = document.getElementById('login-btn');
    const loginBtnText = document.getElementById('login-btn-text');
    const errorDiv = document.getElementById('login-error');

    try {
        if (loginBtn) {
            loginBtn.disabled = true;
            if (loginBtnText) loginBtnText.textContent = 'Giriş Yapılıyor...';
        }

        const response = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();

        if (response.ok) {
            localStorage.setItem('imza_admin_token', data.token);
            localStorage.setItem('imza_admin_role', data.role);
            localStorage.setItem('imza_admin_username', data.username || username);
            window.location.reload();
        } else {
            showLoginError(data.error || 'Giriş başarısız.');
        }
    } catch (error) {
        console.error('Login error:', error);
        showLoginError('Sunucu bağlantı hatası.');
    } finally {
        if (loginBtn) {
            loginBtn.disabled = false;
            if (loginBtnText) loginBtnText.textContent = 'Güvenli Giriş';
        }
    }
}

export function logout() {
    // Show confirmation modal (uses global ensureModal from modals.js)
    if (window.ensureModal) {
        window.ensureModal('logout-confirm', 'logout-confirm-modal');
    } else {
        if (confirm('Oturumu kapatmak istediğinize emin misiniz?')) {
            executeLogout();
        }
    }
}

export function executeLogout() {
    localStorage.removeItem('imza_admin_token');
    localStorage.removeItem('imza_admin_role');
    localStorage.removeItem('imza_admin_username');
    window.location.reload();
}

export function switchRole(role) {
    const roleMap = {
        'admin': 'Yönetici (Admin)',
        'broker': 'Broker',
        'standart': 'Danışman (Agent)'
    };
    
    localStorage.setItem('imza_admin_role', role);
    updateRoleUI(role);
    
    showToast(`Oturum ${roleMap[role] || role} olarak güncellendi`, 'info');
    // Reload dashboard to reflect role permissions
    if (window.showSection) window.showSection('dashboard');
}

function updateRoleUI(role) {
    const roleSpan = document.getElementById('sidebar-user-role');
    const roleMap = { 'admin': 'Admin', 'broker': 'Broker', 'standart': 'Standart' };
    if (roleSpan) roleSpan.textContent = roleMap[role] || 'Admin';
}

function showLoginError(msg) {
    const errorDiv = document.getElementById('login-error');
    if (errorDiv) {
        errorDiv.classList.remove('hidden');
        const span = errorDiv.querySelector('span');
        if (span) span.textContent = msg;
    }
}
