function checkAuth() {
    const token = localStorage.getItem('imza_admin_token');
    const role = localStorage.getItem('imza_admin_role') || 'admin';
    const lang = localStorage.getItem('imza_admin_lang') || 'tr';
    const cur = localStorage.getItem('imza_admin_cur') || 'try';
    
    const loginSection = document.getElementById('login-section');
    const portalApp = document.getElementById('portal-app');
    
    if (token) {
        if (loginSection) loginSection.classList.add('hidden');
        if (portalApp) {
            portalApp.classList.remove('hidden');
            portalApp.classList.add('show-app');
        }
        
        // Sidebar info
        const userSpan = document.getElementById('sidebar-user-name');
        if (userSpan) userSpan.textContent = localStorage.getItem('imza_admin_username') || 'Yönetici';
        
        const roleSpan = document.getElementById('sidebar-user-role');
        const roleMap = { 'admin': 'Admin', 'broker': 'Broker', 'standart': 'Standart' };
        if (roleSpan) roleSpan.textContent = roleMap[role] || 'Admin';

        // Lang & Cur UI update
        const langText = document.getElementById('active-lang-text');
        if (langText) langText.textContent = lang.toUpperCase();
        
        const curNames = { 'try': 'TRY (₺)', 'usd': 'USD ($)', 'eur': 'EUR (€)' };
        const curText = document.getElementById('active-cur-text');
        if (curText) curText.textContent = curNames[cur] || 'TRY (₺)';
        
        // If fetchDashboardStats exists globally, it might be called here, but it's better handled in pages/portal.js
        if (typeof fetchDashboardStats === 'function') {
            fetchDashboardStats();
        }
    } else {
        if (loginSection) loginSection.classList.remove('hidden');
        if (portalApp) portalApp.classList.add('hidden');
    }
}

async function login() {
    const userField = document.getElementById('username');
    const passField = document.getElementById('password');
    const errorDiv = document.getElementById('login-error');
    const loginBtn = document.getElementById('login-btn');
    const loginBtnText = document.getElementById('login-btn-text');

    if (!userField || !passField) return;
    
    const username = userField.value.trim();
    const password = passField.value;

    if (!username || !password) {
        if (typeof showLoginError === 'function') showLoginError('Lütfen tüm alanları doldurun.');
        return;
    }

    if (loginBtn) {
        loginBtn.disabled = true;
        loginBtn.classList.add('opacity-70', 'cursor-wait');
        if (loginBtnText) loginBtnText.textContent = 'Giriş Yapılıyor...';
    }
    if (errorDiv) errorDiv.classList.add('hidden');

    try {
        // Assume API_BASE is globally available
        const base = typeof API_BASE !== 'undefined' ? API_BASE : '/api/v1';
        const response = await fetch(`${base}/auth/login`, {
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
            if (typeof showLoginError === 'function') {
                showLoginError(data.error || 'Giriş bilgileri hatalı.');
            }
        }
    } catch (error) {
        console.error('Login error:', error);
        if (typeof showLoginError === 'function') {
            showLoginError('Sunucu bağlantı hatası. Lütfen internetinizi kontrol edin.');
        }
    } finally {
        if (loginBtn) {
            loginBtn.disabled = false;
            loginBtn.classList.remove('opacity-70', 'cursor-wait');
            if (loginBtnText) loginBtnText.textContent = 'Güvenli Giriş';
        }
    }
}

function logout() {
    const modal = document.getElementById('logout-confirm-modal');
    if (modal) modal.classList.remove('hidden');
}

function executeLogout() {
    localStorage.removeItem('imza_admin_token');
    localStorage.removeItem('imza_admin_role');
    localStorage.removeItem('imza_admin_username');
    window.location.reload();
}

function switchRole(newRole) {
    const token = localStorage.getItem('imza_admin_token');
    if (!token) return;
    
    const roleMap = {
        'admin': 'Yönetici (Admin)',
        'broker': 'Broker',
        'standart': 'Danışman (Agent)'
    };
    
    // Switch token role internally (if payload decoded) or just update UI preference
    localStorage.setItem('imza_admin_role', newRole);
    
    if (typeof showToast === 'function') {
        showToast(`Rol değiştirildi: ${roleMap[newRole] || newRole}`, 'info');
    }
    
    window.location.reload();
}