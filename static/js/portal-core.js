// --- IMZA PORTAL CORE JS ---
// Extracted from portal.html for audit compliance and maintainability.

const API_BASE = '/api/v1';

// --- CONSTANTS & CONFIG ---
const PROPERTY_CATEGORIES = {
    konut: ["Daire", "Villa", "Müstakil Ev", "Rezidans", "Yazlık", "Prefabrik"],
    ticari: ["Ofis", "Dükkan", "Depo", "Plaza Katı", "Aura", "Otis"],
    arsa: ["İmarlı Arsa", "Tarla", "Zeytinlik", "Hobi Bahçesi"],
    proje: ["İmza Mahalle", "Göl Evleri", "Forest Village"]
};

const PLATFORM_URLS = {
    sahibinden: 'https://www.sahibinden.com',
    hepsiemlak: 'https://www.hepsiemlak.com',
    emlakjet: 'https://www.emlakjet.com',
    n11emlak: 'https://www.n11.com/emlak',
    instagram: 'https://www.instagram.com',
    facebook: 'https://www.facebook.com',
    youtube: 'https://studio.youtube.com',
    tiktok: 'https://www.tiktok.com',
    linkedin: 'https://www.linkedin.com',
    x_twitter: 'https://x.com',
    canva: 'https://www.canva.com/design/create',
    reddit: 'https://www.reddit.com'
};

// --- CORE FETCH WRAPPER ---
async function apiFetch(url, options = {}) {
    const token = localStorage.getItem('imza_admin_token');
    const defaultHeaders = {
        'Authorization': token ? `Bearer ${token}` : '',
        'Content-Type': 'application/json'
    };
    const fetchOptions = { ...options, headers: { ...defaultHeaders, ...options.headers } };
    const response = await fetch(url, fetchOptions);
    if (response.status === 401) {
        alert('Oturum süreniz doldu. Lütfen tekrar giriş yapın.');
        window.location.reload();
    }
    return response;
}

// --- NAVIGATION & UI MANTIĞI ---
function showSection(sectionId, btnElement) {
    console.log("[İmza Portal] showSection çağrıldı:", sectionId);

    // Normalize ID: Ensure the section ID ends with '-section' for DOM lookup
    let targetId = sectionId;
    if (!sectionId.endsWith('-section')) {
        const potentialTargetId = sectionId + '-section';
        if (document.getElementById(potentialTargetId)) {
            targetId = potentialTargetId;
        }
    }

    // Role Check
    const currentRole = localStorage.getItem('imza_portal_role') || 'admin';
    const targetBtn = btnElement || document.querySelector(`button[onclick*="'${sectionId}'"]`);
    if (targetBtn && targetBtn.hasAttribute('data-access')) {
        const requiredAccess = targetBtn.getAttribute('data-access');
        if (requiredAccess === 'admin' && currentRole !== 'admin') {
            showToast('Bu bölüme erişim yetkiniz yok.', 'error');
            return;
        }
        if (requiredAccess === 'broker' && currentRole === 'standart') {
            showToast('Bu bölüm Broker ve üzeri yetki gerektirir.', 'error');
            return;
        }
    }

    // Section visibility
    const allSections = document.querySelectorAll('.content-section');
    allSections.forEach(s => s.classList.add('hidden'));

    const target = document.getElementById(targetId);
    if (target) {
        target.classList.remove('hidden');
        console.log("[İmza Portal] Bölüm gösteriliyor:", targetId);
    } else {
        console.error("[İmza Portal] HATA: Hedef bölüm bulunamadı ->", targetId);
    }

    // Sidebar highlight
    document.querySelectorAll('#sidebar nav .nav-item').forEach(a => {
        a.classList.remove('bg-gold/10', 'text-gold', 'border-r-4', 'border-gold');
    });
    if (btnElement) {
        btnElement.classList.add('bg-gold/10', 'text-gold', 'border-r-4', 'border-gold');
    }

    // Data loading switch (Standardized Keys)
    const loaders = {
        'dashboard': typeof fetchDashboardStats !== 'undefined' ? fetchDashboardStats : null,
        'leads': typeof fetchLeads !== 'undefined' ? fetchLeads : null,
        'expenses': typeof fetchExpenses !== 'undefined' ? fetchExpenses : null,
        'portfolios': typeof fetchAllPortfolios !== 'undefined' ? fetchAllPortfolios : null,
        'global-sync': typeof fetchGlobalVisibility !== 'undefined' ? fetchGlobalVisibility : null,
        'campaigns': () => {
           const autoTab = document.getElementById('campaign-tab-content-automation');
           const isAutoActive = autoTab && !autoTab.classList.contains('hidden');
           const tempTab = document.getElementById('campaign-tab-content-templates');
           const isTempActive = tempTab && !tempTab.classList.contains('hidden');
           
           if (isAutoActive) fetchAutomationRules();
           else if (isTempActive) fetchTemplates();
           else fetchCampaigns();
        },
        'barter-wizard-section': () => renderComingSoon('barter-wizard-section', 'Alım Gücü Sihirbazı', 'fa-wand-magic-sparkles'),
        'hero': typeof fetchHeroSlides !== 'undefined' ? fetchHeroSlides : null,
        'appointments': typeof fetchAppointments !== 'undefined' ? fetchAppointments : null,
        'taxes': typeof fetchTaxes !== 'undefined' ? fetchTaxes : null,
        'maintenance': typeof fetchMaintenance !== 'undefined' ? fetchMaintenance : null,
        'contracts': typeof fetchContracts !== 'undefined' ? fetchContracts : null,
        'contract-builder': typeof initContractBuilder !== 'undefined' ? initContractBuilder : null,
        'site-settings': typeof fetchSettings !== 'undefined' ? fetchSettings : null,
        'system-settings': typeof fetchSettings !== 'undefined' ? fetchSettings : null,
        'contacts': typeof fetchContacts !== 'undefined' ? fetchContacts : null,
        'integrations': typeof fetchIntegrations !== 'undefined' ? fetchIntegrations : null,
        'users': () => fetchUsers(),
        'payroll': typeof fetchPayroll !== 'undefined' ? fetchPayroll : null,
        'projects': typeof fetchProjects !== 'undefined' ? fetchProjects : null,
        'taxes-calculator': () => renderComingSoon('taxes-calculator-section', 'Finansal Hesaplayıcılar', 'fa-calculator'),
        'imza-lens': () => {
           const trafficTab = document.getElementById('lens-tab-content-traffic');
           const isTrafficActive = trafficTab && !trafficTab.classList.contains('hidden');
           if (isTrafficActive) fetchTrafficData();
           else fetchShadowListings();
        },
        'market-analytics': typeof updateAnalytics !== 'undefined' ? updateAnalytics : null,
        'neighborhood': () => renderComingSoon('neighborhood-section', 'Mahalle Hub', 'fa-map-location-dot'),
        'apartments': () => renderComingSoon('apartments-section', 'Apartman Yönetimi', 'fa-city'),
        'ai-reports': typeof fetchAiReports !== 'undefined' ? fetchAiReports : null,
        'project-hub': typeof fetchProjectHub !== 'undefined' ? fetchProjectHub : null,
        'media-center': typeof fetchMediaVault !== 'undefined' ? fetchMediaVault : null,
        'cms': typeof fetchCmsPosts !== 'undefined' ? fetchCmsPosts : null,
        'notices': typeof fetchNotices !== 'undefined' ? fetchNotices : null
    };
    
    // Normalize ID: ensure the loader key is clean
    let loaderKey = targetId.endsWith('-section') ? targetId.replace('-section', '') : targetId;
    
    const loader = loaders[loaderKey];
    if (loader && typeof loader === 'function') {
        loader();
    }
}
function switchRole(role) {
    console.log("[İMZA] Rol değiştiriliyor:", role);
    localStorage.setItem('imza_portal_role', role);
    
    // UI Update
    const badge = document.getElementById('sidebar-user-role');
    if (badge) {
        badge.innerText = role.charAt(0).toUpperCase() + role.slice(1);
    }
    
    // Sidebar Filter
    document.querySelectorAll('#sidebar .nav-item').forEach(btn => {
        if (btn.hasAttribute('data-access')) {
            const access = btn.getAttribute('data-access');
            if (access === 'admin' && role !== 'admin') {
                btn.classList.add('hidden');
            } else if (access === 'broker' && role === 'standart') {
                btn.classList.add('hidden');
            } else {
                btn.classList.remove('hidden');
            }
        loaders[loaderKey]();
    } else {
        console.warn("[İmza Portal] Loader bulunamadı veya tanım yok:", loaderKey);
    }
}

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebar-overlay');
    
    if (sidebar) {
        sidebar.classList.toggle('-translate-x-full');
        // Toggle overlay visibility
        if (overlay) {
            overlay.classList.toggle('hidden');
        }
        // Lock body scroll on mobile when sidebar is open
        if (!sidebar.classList.contains('-translate-x-full') && window.innerWidth < 1024) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = '';
        }
    }
}

const toggleBtn = document.getElementById('sidebar-toggle');
if (toggleBtn) {
    // Note: Inline onclick also exists, this adds a second listener or we can rely on one.
    // Standardizing to ensure it works consistently.
}

function logout() {
    document.getElementById('logout-confirm-modal').classList.remove('hidden');
}

function executeLogout() {
    localStorage.removeItem('imza_admin_token');
    localStorage.removeItem('imza_admin_role');
    localStorage.removeItem('imza_admin_username');
    window.location.reload();
}

// --- PREMIUM UI HELPERS (V3) ---
function toggleDropdown(id) {
    const dropdown = document.getElementById(id);
    if (!dropdown) return;
    
    // Close other dropdowns
    document.querySelectorAll('.dropdown-menu').forEach(d => {
        if (d.id !== id) d.classList.remove('active');
    });
    
    dropdown.classList.toggle('active');
}

// Close dropdowns on outside click
document.addEventListener('click', (e) => {
    if (!e.target.closest('.premium-dropdown')) {
        document.querySelectorAll('.dropdown-menu.active').forEach(d => d.classList.remove('active'));
    }
});

function switchRole(role) {
    const roleMap = {
        'admin': 'Yönetici (Admin)',
        'broker': 'Broker',
        'standart': 'Danışman (Agent)'
    };
    
    localStorage.setItem('imza_admin_role', role);
    const roleDisplay = document.getElementById('sidebar-user-role');
    if (roleDisplay) roleDisplay.textContent = roleMap[role] || 'Admin';
    
    console.log("[İmza Portal] Rol Değiştirildi:", role);
    document.querySelectorAll('.dropdown-menu.active').forEach(d => d.classList.remove('active'));
    
    // Optional: Refresh data based on new role context
    fetchDashboardStats();
    showToast(`Oturum ${roleMap[role]} olarak güncellendi`, 'info');
}

function changeLang(lang) {
    localStorage.setItem('imza_admin_lang', lang);
    const langText = document.getElementById('active-lang-text');
    if (langText) langText.textContent = lang.toUpperCase();
    
    document.querySelectorAll('.dropdown-menu.active').forEach(d => d.classList.remove('active'));
    console.log("[İmza Portal] Dil Değiştirildi:", lang);
    showToast(`Dil ${lang.toUpperCase()} olarak güncellendi`, 'info');
}

function changeCurrency(cur) {
    localStorage.setItem('imza_admin_cur', cur);
    const curNames = { 'try': 'TRY (₺)', 'usd': 'USD ($)', 'eur': 'EUR (€)' };
    const curText = document.getElementById('active-cur-text');
    if (curText) curText.textContent = curNames[cur] || cur.toUpperCase();
    
    document.querySelectorAll('.dropdown-menu.active').forEach(d => d.classList.remove('active'));
    console.log("[İmza Portal] Para Birimi Değiştirildi:", cur);
    showToast(`Para Birimi ${cur.toUpperCase()} olarak güncellendi`, 'info');
}

// --- BARTER WIZARD LOGIC ---
window.barterNext = function(stepIndex) {
    document.getElementById('step-' + (stepIndex - 1)).classList.add('hidden');
    document.getElementById('step-' + stepIndex).classList.remove('hidden');
};
window.barterPrev = function(stepIndex) {
    document.getElementById('step-' + (stepIndex + 1)).classList.add('hidden');
    document.getElementById('step-' + stepIndex).classList.remove('hidden');
};

window.calculateBarterPower = function() {
    const cash = parseFloat(document.getElementById('bw-cash').value) || 0;
    const creditStr = document.querySelector('input[name="kredi"]:checked').value;
    const credit = creditStr === 'yes' ? (parseFloat(document.getElementById('bw-credit').value) || 0) : 0;
    
    const carVal = parseFloat(document.getElementById('bw-car-val').value) || 0;
    const propVal = parseFloat(document.getElementById('bw-prop-val').value) || 0;
    
    const total = cash + credit + carVal + propVal;
    const barterTotal = carVal + propVal;

    // Update UI
    document.getElementById('bw-total-power').textContent = new Intl.NumberFormat('tr-TR', { style: 'currency', currency: 'TRY' }).format(total);
    document.getElementById('bw-res-cash').textContent = new Intl.NumberFormat('tr-TR', { style: 'currency', currency: 'TRY' }).format(cash);
    document.getElementById('bw-res-barter').textContent = new Intl.NumberFormat('tr-TR', { style: 'currency', currency: 'TRY' }).format(barterTotal);
    document.getElementById('bw-res-credit').textContent = new Intl.NumberFormat('tr-TR', { style: 'currency', currency: 'TRY' }).format(credit);

    // Move to Step 3
    barterNext(3);
};

// --- AUTH & LOGIN ---
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
        
        // URL'de reset token var mı kontrol et (Şifre sıfırlama akışı için)
        const params = new URLSearchParams(window.location.search);
        if (params.has('reset_token')) {
            document.getElementById('reset-token').value = params.get('reset_token');
            document.getElementById('new-password-modal').classList.remove('hidden');
            // URL'den token'ı temizle (güvenlik için)
            window.history.replaceState({}, document.title, window.location.pathname);
        }

        fetchDashboardStats();
    } else {
        if (loginSection) loginSection.classList.remove('hidden');
        if (portalApp) portalApp.classList.add('hidden');
    }
}

async function login() {
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const errorDiv = document.getElementById('login-error');
    const loginBtn = document.getElementById('login-btn');
    const loginBtnText = document.getElementById('login-btn-text');

    if (!username || !password) {
        errorDiv.classList.remove('hidden');
        errorDiv.querySelector('span').textContent = 'Lütfen tüm alanları doldurun.';
        return;
    }

    // Loading state
    loginBtn.disabled = true;
    loginBtn.classList.add('opacity-70', 'cursor-not-allowed');
    if (loginBtnText) loginBtnText.textContent = 'Giriş Yapılıyor...';
    errorDiv.classList.add('hidden');

    try {
        const response = await fetch(`${API_BASE}/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        if (response.ok) {
            const data = await response.json();
            // Ensure storage is written before reload
            localStorage.setItem('imza_admin_token', data.token);
            localStorage.setItem('imza_admin_role', data.role);
            localStorage.setItem('imza_admin_username', data.username || username);
            
            // Give a tiny moment for mobile storage sync
            setTimeout(() => {
                window.location.reload();
            }, 100);
        } else {
            const errorData = await response.json().catch(() => ({}));
            errorDiv.classList.remove('hidden');
            errorDiv.querySelector('span').textContent = errorData.error || 'Giriş bilgileri hatalı (Şifre veya Kullanıcı adı yanlış).';
        }
    } catch (error) {
        console.error('Login error:', error);
        errorDiv.classList.remove('hidden');
        errorDiv.querySelector('span').textContent = 'Bir hata oluştu. Sunucuya erişilemiyor.';
    } finally {
        loginBtn.disabled = false;
        loginBtn.classList.remove('opacity-70', 'cursor-not-allowed');
        if (loginBtnText) loginBtnText.textContent = 'Güvenli Giriş';
    }
}

function togglePasswordVisibility() {
    const passInput = document.getElementById('password');
    const toggleIcon = document.getElementById('toggle-icon');
    if (!passInput || !toggleIcon) return;
    
    if (passInput.type === 'password') {
        passInput.type = 'text';
        toggleIcon.classList.remove('fa-eye-slash');
        toggleIcon.classList.add('fa-eye');
    } else {
        passInput.type = 'password';
        toggleIcon.classList.remove('fa-eye');
        toggleIcon.classList.add('fa-eye-slash');
    }
}


// --- PASSWORD RESET LOGIC ---
function openResetModal() {
    document.getElementById('reset-modal').classList.remove('hidden');
    document.getElementById('reset-request-step').classList.remove('hidden');
    document.getElementById('reset-success-step').classList.add('hidden');
}

function closeResetModal() {
    document.getElementById('reset-modal').classList.add('hidden');
}

async function requestPasswordReset() {
    const email = document.getElementById('reset-email').value;
    if (!email || !email.includes('@')) return alert('Lütfen geçerli bir e-posta adresi girin.');
    
    const btn = document.getElementById('reset-req-btn');
    btn.disabled = true;
    btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Gönderiliyor...';

    try {
        const res = await fetch(`${API_BASE}/auth/request-reset`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email: email })
        });
        if (res.ok) {
            document.getElementById('reset-request-step').classList.add('hidden');
            document.getElementById('reset-success-step').classList.remove('hidden');
        } else {
            const data = await res.json();
            alert(data.error || 'Sıfırlama talebi başarısız oldu.');
        }
    } catch (e) {
        alert('Bağlantı hatası.');
    } finally {
        btn.disabled = false;
        btn.innerHTML = 'Bağlantı Gönder';
    }
}

async function submitNewPassword() {
    const token = document.getElementById('reset-token').value;
    const pass = document.getElementById('new-password').value;
    const confirm = document.getElementById('new-password-confirm').value;
    
    if (pass !== confirm) return alert('Şifreler eşleşmiyor.');
    if (pass.length < 6) return alert('Şifre en az 6 karakter olmalıdır.');

    try {
        const res = await apiFetch(`${API_BASE}/auth/reset-password`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ token: token, password: pass })
        });
        if (res.ok) {
            alert('Şifreniz başarıyla güncellendi! Giriş yapabilirsiniz.');
            window.location.reload();
        } else {
            const data = await res.json();
            alert(data.error || 'İşlem başarısız.');
        }
    } catch (e) {
        alert('Bir hata oluştu.');
    }
}

// --- DASHBOARD ---
async function fetchDashboardStats() {
    try {
        const res = await apiFetch(`${API_BASE}/dashboard/stats`);
        if (res.ok) {
            const stats = await res.json();
            document.getElementById('dash-stat-leads').textContent = stats.leads_count || 0;
            document.getElementById('dash-stat-expenses').textContent = stats.pending_expenses_count || 0;
            fetchPortfoliosForDashboard();
            fetchUpcomingBirthdays();
        }
    } catch (e) { console.error('Dashboard error:', e); }
}

async function fetchPortfoliosForDashboard() {
    try {
        const res = await apiFetch(`${API_BASE}/portfolios`);
        const data = await res.json();
        const tableBody = document.getElementById('dashboard-portfolio-list');
        if (!tableBody) return;
        tableBody.innerHTML = '';
        data.slice(0, 3).forEach(item => {
            tableBody.innerHTML += `
                <tr class="border-b border-gray-50 last:border-0 hover:bg-gray-50 transition-colors">
                    <td class="py-3 px-4"><span class="bg-gray-100 text-gray-500 px-2 py-1 rounded text-xs font-mono font-bold">${item.ref_no}</span></td>
                    <td class="py-3 px-4 font-medium text-navy">${item.title}</td>
                    <td class="py-3 px-4 text-gray-500">${item.location}</td>
                    <td class="py-3 px-4 font-bold text-slate-700">${item.price}</td>
                </tr>`;
        });
    } catch (err) { console.error(err); }
}

async function fetchUpcomingBirthdays() {
    try {
        const res = await apiFetch(`${API_BASE}/contacts/birthdays`);
        if (res.ok) {
            const birthdays = await res.json();
            const container = document.getElementById('dashboard-birthdays-list');
            if (!container) return;
            container.innerHTML = birthdays.length === 0 ? '<p class="text-gray-400 text-xs italic">Yaklaşan doğum günü yok.</p>' : '';
            birthdays.slice(0, 4).forEach(b => {
                const dayText = b.days_left === 0 ? '<span class="text-red-600 font-bold">BUGÜN!</span>' : `${b.days_left} gün`;
                container.innerHTML += `<div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg border border-gray-100 hover:border-gold/30 transition-colors">
                    <div class="flex items-center gap-3">
                        <div class="w-10 h-10 rounded-full bg-gold/10 text-gold flex items-center justify-center text-lg"><i class="fa-solid fa-cake-candles"></i></div>
                        <div><p class="text-sm font-bold text-navy">${b.name}</p><p class="text-[10px] text-gray-500">${b.occupation || 'Müşteri'}</p></div>
                    </div>
                    <div class="text-right"><p class="text-xs font-bold text-gold">${dayText}</p></div>
                </div>`;
            });
        }
    } catch (e) { console.error(e); }
}

// --- PORTFOLIO (CRUD & AI SUMMARY) ---
async function fetchAllPortfolios() {
    try {
        const res = await apiFetch(`${API_BASE}/portfolios`);
        const data = await res.json();
        const container = document.getElementById('portfolio-grid');
        const tableBody = document.getElementById('portfolios-table-body');
        if (container) {
            container.innerHTML = '';
            data.forEach(p => {
                container.innerHTML += `<div class="bg-white rounded-2xl border border-gray-100 overflow-hidden hover:shadow-xl transition-all">
                    <div class="h-40 bg-cover bg-center" style="background-image: url('${p.resim_hero || 'https://via.placeholder.com/400x200'}')"></div>
                    <div class="p-4">
                        <h4 class="font-bold text-navy text-sm mb-1 truncate" title="${p.baslik1}">${p.baslik1}</h4>
                        <p class="text-[10px] text-gray-400 mb-4 tracking-tighter uppercase truncate"><i class="fa-solid fa-location-dot"></i> ${p.lokasyon}</p>
                        <div class="flex justify-between items-center"><span class="text-gold font-bold text-sm">${p.fiyat}</span>
                        <div class="flex gap-2"><button onclick="editPortfolio(${p.id})" class="text-xs text-navy font-bold">Düzenle</button></div></div>
                    </div>
                </div>`;
            });
        }
        if (tableBody) {
            tableBody.innerHTML = '';
            data.forEach(item => {
                tableBody.innerHTML += `<tr class="border-b border-gray-100 hover:bg-gray-50 transition-colors group">
                    <td class="py-3 px-6"><div class="w-12 h-12 rounded bg-cover bg-center border border-gray-200" style="background-image: url('${item.image_hero}')"></div></td>
                    <td class="py-3 px-6"><span class="bg-gray-100 text-gray-600 px-2 py-1 rounded text-xs font-mono font-bold">${item.ref_no}</span></td>
                    <td class="py-3 px-6"><span class="text-xs font-bold uppercase tracking-wider ${item.ozellik_renk}">${item.koleksiyon}</span></td>
                    <td class="py-3 px-6 font-bold text-navy truncate max-w-[200px]" title="${item.title}">${item.title}</td>
                    <td class="py-3 px-6 font-bold text-slate-700">${item.price}</td>
                    <td class="py-3 px-6 text-right flex gap-2 justify-end opacity-0 group-hover:opacity-100 transition-opacity">
                        <button onclick="openMediaManager('${item.id}')" class="text-emerald-500 p-2 bg-emerald-50 rounded shadow hover:bg-emerald-100 transition-colors" title="Medya Yönetimi"><i class="fa-solid fa-camera"></i> Medya</button>
                        <button onclick="editPortfolio('${item.id}')" class="text-blue-500 p-2"><i class="fa-solid fa-pen"></i></button>
                        <button onclick="deletePortfolio('${item.id}')" class="text-red-500 p-2"><i class="fa-solid fa-trash"></i></button>
                    </td>
                </tr>`;
            });
        }
    } catch (err) { console.error(err); }
}

async function generateStoryFromAI() {
    const btn = document.getElementById('btn-ai-generate');
    if (btn) btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i> Yazılıyor...';
    const payload = {
        fiyat: document.getElementById('p-fiyat').value,
        il_ilce: document.getElementById('p-lokasyon').value,
        oda: document.getElementById('p-oda').value,
        alt_tip: document.getElementById('p-alt_tip').value,
        ozellikler: document.getElementById('p-ozellikler_arr').value
    };
    try {
        const res = await apiFetch(`${API_BASE}/generate-summary`, { method: 'POST', body: JSON.stringify(payload) });
        const data = await res.json();
        if (res.ok && data.story) document.getElementById('p-hikaye').value = data.story;
        else alert('Yapay zeka hatası.');
    } catch (err) { console.error(err); }
    finally { if (btn) btn.innerHTML = '<i class="fa-solid fa-wand-magic-sparkles"></i> AI ile Üret'; }
}

// --- LEAFLET MAP ---
let portfolioMap = null, portfolioMarker = null;
function initPortfolioMap(lat, lng) {
    if (portfolioMap !== null) portfolioMap.remove();
    portfolioMap = L.map('portfolio-map').setView([lat, lng], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(portfolioMap);
    portfolioMarker = L.marker([lat, lng], { draggable: true }).addTo(portfolioMap);
    portfolioMarker.on('dragend', () => {
        const pos = portfolioMarker.getLatLng();
        document.getElementById('p-enlem').value = pos.lat;
        document.getElementById('p-boylam').value = pos.lng;
    });
    setTimeout(() => { if (portfolioMap) portfolioMap.invalidateSize(); }, 100);
}

// --- LEADS ---
// --- LEADS ---
async function fetchLeads(filterType = 'all') {
    try {
        console.log("[İMZA] Leads fetch ediliyor, filtre:", filterType);
        
        let url = `${API_BASE}/leads`;
        if (filterType === 'pipeline') url += '?pipeline=true';
        else if (filterType === 'standby') url += '?pipeline=false';

        const res = await apiFetch(url);
        const data = await res.json();
        
        // Update Filter UI status
        document.querySelectorAll('.lead-filter-btn').forEach(btn => {
            btn.classList.remove('active', 'bg-white', 'text-navy', 'shadow-sm');
            btn.classList.add('text-gray-500');
        });
        const currentBtn = Array.from(document.querySelectorAll('.lead-filter-btn')).find(b => b.getAttribute('onclick')?.includes(`'${filterType}'`));
        if (currentBtn) {
            currentBtn.classList.add('active', 'bg-white', 'text-navy', 'shadow-sm');
            currentBtn.classList.remove('text-gray-500');
        }

        // Render List View
        const tbody = document.getElementById('leads-table-body');
        if (tbody) {
            tbody.innerHTML = data.length === 0 ? '<tr><td colspan="6" class="p-8 text-center text-gray-400 font-serif italic">Seçilen filtrede aday bulunmuyor.</td></tr>' : '';
            data.forEach(l => {
                const dateStr = l.created_at ? new Date(l.created_at).toLocaleString('tr-TR') : '-';
                const tr = document.createElement('tr');
                tr.className = 'border-b border-gray-50 hover:bg-gray-50 group transition-colors';
                tr.innerHTML = `
                    <td class="px-6 py-4">
                        <div class="font-bold text-navy">${l.name || 'İsimsiz'}</div>
                        <div class="text-[10px] text-gray-500 font-medium tracking-tighter">#${l.id}</div>
                    </td>
                    <td class="px-6 py-4 text-xs font-medium">
                        <div class="text-navy">${l.phone || '-'}</div>
                        <div class="text-gray-500">${l.email || '-'}</div>
                    </td>
                    <td class="px-6 py-4">
                        <span class="px-2 py-1 rounded-[4px] text-[10px] font-black uppercase tracking-widest ${l.source === 'ai_rotasi' ? 'bg-gold/10 text-gold shadow-sm' : 'bg-gray-100 text-gray-600'}">
                            ${l.source || 'Genel'}
                        </span>
                    </td>
                    <td class="px-6 py-4">
                        <div class="text-[11px] text-gray-600 max-w-[200px] truncate italic" title="${l.notes || ''}">${l.notes || '-'}</div>
                    </td>
                    <td class="px-6 py-4 text-xs font-bold text-gray-500">
                        ${dateStr}
                    </td>
                    <td class="px-6 py-4 text-right flex gap-1 justify-end opacity-0 group-hover:opacity-100 transition-opacity">
                        <button onclick="editLead('${l.id}')" class="w-8 h-8 rounded-lg bg-navy/5 text-navy hover:bg-navy hover:text-white transition-all flex items-center justify-center shadow-sm"><i class="fa-solid fa-pen text-[10px]"></i></button>
                        <button onclick="deleteLead('${l.id}')" class="w-8 h-8 rounded-lg bg-red-50 text-red-500 hover:bg-red-500 hover:text-white transition-all flex items-center justify-center shadow-sm"><i class="fa-solid fa-trash-can text-[10px]"></i></button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }

        // Render Pipeline View
        renderLeadPipeline(data);

        // Highlight pending lead if any
        if (window._pendingLeadId) {
            setTimeout(() => highlightLeadInPipeline(window._pendingLeadId), 500);
            window._pendingLeadId = null;
        }

    } catch (err) { console.error(err); }
}

function renderLeadPipeline(leads) {
    const container = document.getElementById('pipeline-container');
    if (!container) return;

    // Define standard stages (will eventually come from backend)
    const stages = [
        { id: 1, name: 'Yeni Aday', color: 'blue', status: 'new' },
        { id: 2, name: 'İletişim Kuruldu', color: 'yellow', status: 'contacted' },
        { id: 3, name: 'Gösterim/Sunum', color: 'orange', status: 'showing' },
        { id: 4, name: 'Teklif/Pazarlık', color: 'emerald', status: 'negotiating' },
        { id: 5, name: 'Sözleşme/Kapanış', color: 'navy', status: 'closed' }
    ];

    container.innerHTML = '';
    stages.forEach(stage => {
        const stageLeads = leads.filter(l => (l.pipeline_stage_id == stage.id || (!l.pipeline_stage_id && stage.status === 'new')));
        
        const stageEl = document.createElement('div');
        stageEl.className = "kanban-column shrink-0 w-72 flex flex-col h-full bg-gray-50/50 rounded-2xl border border-gray-100 p-4";
        stageEl.innerHTML = `
            <div class="flex justify-between items-center mb-4 px-2">
                <div class="flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full bg-${stage.color}-500"></span>
                    <h4 class="text-xs font-bold text-navy uppercase tracking-wider">${stage.name}</h4>
                </div>
                <span class="text-[10px] font-bold text-gray-400 bg-white px-2 py-0.5 rounded-full border border-gray-100">${stageLeads.length}</span>
            </div>
            <div class="flex-1 overflow-y-auto space-y-3 custom-scrollbar kanban-list" data-stage-id="${stage.id}">
                ${stageLeads.map(l => `
                    <div class="kanban-card bg-white p-4 rounded-xl border border-gray-100 shadow-sm hover:shadow-md hover:border-gold/30 transition-all cursor-pointer group relative" 
                         id="lead-card-${l.id}" onclick="editLead('${l.id}')">
                        <div class="flex justify-between items-start mb-2">
                            <span class="font-bold text-navy text-sm leading-tight">${l.name}</span>
                            <span class="text-[10px] font-black ${l.ai_score >= 80 ? 'text-emerald-500' : 'text-gold'}">%${l.ai_score || 0}</span>
                        </div>
                        <p class="text-[10px] text-gray-500 line-clamp-2 mb-3 font-medium">${l.notes || 'Not bulunmuyor.'}</p>
                        <div class="flex items-center justify-between">
                            <div class="flex -space-x-2">
                                <div class="w-6 h-6 rounded-full bg-navy/10 border-2 border-white flex items-center justify-center text-[8px] font-bold text-navy uppercase">${l.name[0]}</div>
                            </div>
                            <span class="text-[10px] text-gray-400">${l.phone || ''}</span>
                        </div>
                    </div>
                `).join('')}
            </div>
        `;
        container.appendChild(stageEl);
    });
}

function switchLeadsView(view) {
    const listView = document.getElementById('leads-list-view');
    const pipeView = document.getElementById('leads-pipeline-view');
    const listBtn = document.getElementById('leads-list-btn');
    const pipeBtn = document.getElementById('leads-pipeline-btn');

    if (view === 'pipeline') {
        listView.classList.add('hidden');
        pipeView.classList.remove('hidden');
        pipeBtn.classList.add('bg-white', 'text-navy', 'shadow-sm');
        pipeBtn.classList.remove('text-gray-500');
        listBtn.classList.remove('bg-white', 'text-navy', 'shadow-sm');
        listBtn.classList.add('text-gray-500');
    } else {
        listView.classList.remove('hidden');
        pipeView.classList.add('hidden');
        listBtn.classList.add('bg-white', 'text-navy', 'shadow-sm');
        listBtn.classList.remove('text-gray-500');
        pipeBtn.classList.remove('bg-white', 'text-navy', 'shadow-sm');
        pipeBtn.classList.add('text-gray-500');
    }
}

function viewInPipeline(leadId) {
    window._pendingLeadId = leadId;
    showSection('leads');
}

function highlightLeadInPipeline(leadId) {
    const card = document.getElementById(`lead-card-${leadId}`);
    if (card) {
        card.scrollIntoView({ behavior: 'smooth', block: 'center', inline: 'center' });
        card.classList.add('ring-2', 'ring-gold', 'scale-105', 'z-20');
        setTimeout(() => {
            card.classList.remove('ring-2', 'ring-gold', 'scale-105', 'z-20');
        }, 3000);
    }
}

async function openQuickWhatsApp(id) {
    try {
        const res = await apiFetch(`${API_BASE}/leads/${id}/whatsapp-template`);
        if (res.ok) {
            const data = await res.json();
            window.open(data.whatsapp_link, '_blank');
        }
    } catch (e) { console.error(e); }
}

// --- EXPENSES ---
async function fetchExpenses() {
    try {
        const res = await apiFetch(`${API_BASE}/expenses`);
        const data = await res.json();
        const tbody = document.getElementById('expenses-table-body');
        if (!tbody) return;
        tbody.innerHTML = data.length === 0 ? '<tr><td colspan="6" class="p-8 text-center text-gray-400">Kayıt yok.</td></tr>' : '';
        data.forEach(e => {
            const tr = document.createElement('tr');
            tr.className = 'border-b border-gray-50 hover:bg-gray-50';
            const badge = e.status === 'approved' ? '<span class="bg-green-50 text-green-600 px-2 py-1 rounded text-[10px] font-bold">ONAYLI</span>' : '<span class="bg-yellow-50 text-yellow-600 px-2 py-1 rounded text-[10px] font-bold">BEKLİYOR</span>';
            tr.innerHTML = `
                <td class="px-6 py-4 text-gray-500">${e.date}</td>
                <td class="px-6 py-4 font-bold text-navy">${e.username}</td>
                <td class="px-6 py-4 text-xs tracking-wider">${e.category}</td>
                <td class="px-6 py-4 font-bold text-red-600">${e.amount.toLocaleString()} ₺</td>
                <td class="px-6 py-4">${badge}</td>
                <td class="px-6 py-4 text-right">${e.status === 'pending' ? `<button onclick="approveExpense(${e.id})" class="text-green-500"><i class="fa-solid fa-check"></i></button>` : ''}</td>`;
            tbody.appendChild(tr);
        });
    } catch (e) { console.error(e); }
}

async function approveExpense(id) {
    if (!confirm('Harcamayı onaylamak istiyor musunuz?')) return;
    try {
        const res = await apiFetch(`${API_BASE}/expenses/${id}/approve`, { method: 'PUT' });
        if (res.ok) fetchExpenses();
    } catch (e) { console.error(e); }
}

// --- APPOINTMENTS (V2) ---
async function fetchAppointments() {
    try {
        const res = await apiFetch(`${API_BASE}/appointments`);
        const data = await res.json();
        const tbody = document.getElementById('appointments-table-body');
        if (!tbody) return;
        tbody.innerHTML = '';
        data.forEach(a => {
            const tr = document.createElement('tr');
            tr.className = 'border-b border-gray-100/50 hover:bg-gray-50';
            const statusColor = (a.status || '').toLowerCase().includes('tamam') ? 'bg-green-100 text-green-700' : 'bg-blue-100 text-blue-700';
            const clientName = a.client_name || a.baslik1 || '-';
            tr.innerHTML = `
                <td class="px-6 py-4 font-medium text-navy">#${a.id}</td>
                <td class="px-6 py-4 font-bold text-navy truncate max-w-[150px]" title="${clientName}">${clientName}</td>
                <td class="px-6 py-4">${a.phone || '-'}</td>
                <td class="px-6 py-4 text-gray-600 font-medium">${a.datetime || a.date}</td>
                <td class="px-6 py-4"><span class="${statusColor} px-2 py-1 rounded text-[10px] font-bold uppercase">${a.status}</span></td>
                <td class="px-6 py-4 text-right"><button onclick="deleteAppointment(${a.id})" class="text-red-400 p-2"><i class="fa-regular fa-trash-can"></i></button></td>`;
            tbody.appendChild(tr);
        });
    } catch (e) { console.error(e); }
}

async function saveAppointmentV2() {
    const payload = {
        client_name: document.getElementById('appt2-client').value,
        client_phone: document.getElementById('appt2-phone').value,
        purpose: document.getElementById('appt2-purpose').value,
        datetime: document.getElementById('appt2-datetime').value.replace('T', ' '),
        notes: document.getElementById('appt2-notes').value,
        status: 'pending'
    };
    if (!payload.client_name || !payload.datetime) return alert('İsim ve tarih zorunludur.');
    try {
        const res = await apiFetch(`${API_BASE}/appointments`, { method: 'POST', body: JSON.stringify(payload) });
        if (res.ok) { alert('Randevu oluşturuldu!'); document.getElementById('appointment-modal-v2').classList.add('hidden'); fetchAppointments(); }
    } catch (e) { console.error(e); }
}

// --- CONTRACT BUILDER ---
let conWizStep = 1;
let selectedParties = { seller: null, buyer: null, extra: [] };
let selectedProperty = null;
let allParties = [];
let allProperties = [];

async function initContractBuilder() {
    conWizStep = 1;
    selectedParties = { seller: null, buyer: null, extra: [] };
    selectedProperty = null;
    updateConWizUI();
    try {
        const resP = await apiFetch(`${API_BASE}/portfolios`);
        allProperties = await resP.json();
        const resT = await apiFetch(`${API_BASE}/parties`);
        allParties = await resT.json();
    } catch (e) { console.error(e); }
}

function searchParty(type) {
    const val = document.getElementById(`${type}-search`).value.trim().toLowerCase();
    const results = allParties.filter(p => p.name.toLowerCase().includes(val) || p.tc_vkn.includes(val));
    const container = document.getElementById(`${type}-results`);
    container.innerHTML = '';
    results.slice(0, 5).forEach(p => {
        const div = document.createElement('div');
        div.className = 'p-2 hover:bg-gray-50 cursor-pointer border-b text-xs';
        div.innerHTML = `<b>${p.name}</b> <br> ${p.tc_vkn}`;
        div.onclick = () => selectParty(type, p);
        container.appendChild(div);
    });
    container.classList.toggle('hidden', results.length === 0);
}

function selectParty(type, party) {
    selectedParties[type] = party;
    document.getElementById(`${type}-selected`).innerHTML = `<div class="p-2 bg-gold/5 border border-gold/20 rounded-lg text-xs font-bold text-navy">${party.name}<br>${party.tc_vkn}</div>`;
    document.getElementById(`${type}-results`).classList.add('hidden');
}

function searchProperties(val) {
    const term = val.toLowerCase();
    const results = allProperties.filter(p => p.baslik1.toLowerCase().includes(term) || p.refNo.toLowerCase().includes(term));
    const container = document.getElementById('property-results');
    container.innerHTML = '';
    results.slice(0, 5).forEach(p => {
        const div = document.createElement('div');
        div.className = 'p-2 hover:bg-gray-50 cursor-pointer border-b text-xs';
        div.innerHTML = `<b>${p.baslik1}</b> (${p.refNo})`;
        div.onclick = () => selectProperty(p);
        container.appendChild(div);
    });
    container.classList.toggle('hidden', results.length === 0);
}

function selectProperty(p) {
    selectedProperty = p;
    document.getElementById('property-selected').innerHTML = `<div class="p-2 bg-gold/5 border border-gold/20 rounded-lg text-xs font-bold text-navy">${p.baslik1}<br>${p.refNo}</div>`;
    document.getElementById('property-results').classList.add('hidden');
}

function updateConWizUI() {
    document.querySelectorAll('.con-wiz-step').forEach((s, i) => s.classList.toggle('hidden', (i + 1) !== conWizStep));
    document.getElementById('con-wiz-prev').classList.toggle('hidden', conWizStep === 1);
    document.getElementById('con-wiz-next').textContent = conWizStep === 4 ? 'Oluştur' : 'Devam Et';
}

async function conWizNext() {
    if (conWizStep === 4) { await finalizeContract(); return; }
    conWizStep++;
    if (conWizStep === 4) {
        document.getElementById('preview-property').textContent = selectedProperty ? selectedProperty.baslik1 : '-';
        document.getElementById('preview-seller').textContent = selectedParties.seller ? selectedParties.seller.name : '-';
        document.getElementById('preview-buyer').textContent = selectedParties.buyer ? selectedParties.buyer.name : '-';
    }
    updateConWizUI();
}

function conWizPrev() { if (conWizStep > 1) { conWizStep--; updateConWizUI(); } }

async function finalizeContract() {
    if (!selectedProperty || !selectedParties.seller || !selectedParties.buyer) return alert('Eksik bilgi.');
    try {
        const res = await apiFetch(`${API_BASE}/contracts`, {
            method: 'POST',
            body: JSON.stringify({ 
                property_id: selectedProperty.id, 
                seller_id: selectedParties.seller.id, 
                buyer_id: selectedParties.buyer.id, 
                contract_type: document.getElementById('contract-type').value, 
                status: 'draft' 
            })
        });
        if (res.ok) { 
            showToast('Sözleşme taslağı oluşturuldu!', 'success'); 
            showSection('contracts'); 
        } else {
            showToast('Sözleşme oluşturulamadı', 'error');
        }
    } catch (e) { showToast('Bağlantı hatası', 'error'); }
}

async function saveNewParty() {
    const payload = {
        name: document.getElementById('party-name').value,
        tc_vkn: document.getElementById('party-tc').value,
        phone: document.getElementById('party-phone').value,
        type: document.getElementById('party-type').value
    };
    try {
        const res = await apiFetch(`${API_BASE}/parties`, { method: 'POST', body: JSON.stringify(payload) });
        if (res.ok) {
            showToast('Taraf eklendi', 'success');
            closePartyModal();
            // Refresh party list if in wizard
            const resT = await apiFetch(`${API_BASE}/parties`);
            allParties = await resT.json();
        }
    } catch (e) { showToast('Hata oluştu', 'error'); }
}

// --- CONTACTS ---
async function fetchContacts() {
    try {
        const res = await apiFetch(`${API_BASE}/contacts`);
        const data = await res.json();
        const tbody = document.getElementById('contacts-table-body');
        if (!tbody) return;
        tbody.innerHTML = '';
        data.forEach(c => {
            tbody.innerHTML += `<tr class="border-b border-gray-50"><td class="px-6 py-4 font-bold text-navy">${c.name}</td>
                <td class="px-6 py-4 text-gray-500">${c.role}</td>
                <td class="px-6 py-4 text-xs font-medium">${c.phone || '-'}</td>
                <td class="px-6 py-4 text-right"><button onclick="deleteContact(${c.id})" class="text-red-400 hover:text-red-500"><i class="fa-solid fa-trash"></i></button></td></tr>`;
        });
    } catch (e) { console.error(e); }
}

async function saveContact() {
    const payload = {
        name: document.getElementById('contact-name').value.trim(),
        role: document.getElementById('contact-role').value,
        phone: document.getElementById('contact-phone').value.trim(),
        email: document.getElementById('contact-email').value.trim(),
        bdate: document.getElementById('contact-bdate').value
    };
    if (!payload.name) return alert('İsim zorunludur.');
    try {
        const res = await apiFetch(`${API_BASE}/contacts`, { method: 'POST', body: JSON.stringify(payload) });
        if (res.ok) { document.getElementById('contact-modal').classList.add('hidden'); fetchContacts(); }
    } catch (e) { console.error(e); }
}

// --- INTEGRATIONS ---
async function fetchIntegrations() {
    const tbody = document.getElementById('publications-table-body');
    if (tbody) tbody.innerHTML = '<tr><td colspan="4" class="p-8 text-center text-gray-400 font-serif italic text-sm">Entegrasyonlar yakında aktif edilecek.</td></tr>';
}

// --- CAMPAIGN & AUTOMATION ---
function switchCampaignTab(tabName) {
    document.querySelectorAll('.campaign-tab-btn').forEach(btn => {
        btn.classList.remove('active');
        btn.classList.add('text-gray-500', 'hover:text-navy');
    });
    const activeBtn = document.getElementById(`campaign-tab-btn-${tabName}`);
    if (activeBtn) {
        activeBtn.classList.add('active');
        activeBtn.classList.remove('text-gray-500', 'hover:text-navy');
    }
    document.querySelectorAll('.campaign-tab-content').forEach(content => {
        content.classList.add('hidden');
    });
    const targetContent = document.getElementById(`campaign-tab-content-${tabName}`);
    if (targetContent) {
        targetContent.classList.remove('hidden', 'animate-fade-in');
        void targetContent.offsetWidth; // Trigger reflow
        targetContent.classList.add('animate-fade-in');
    }
    if (tabName === 'manual') fetchCampaigns();
    if (tabName === 'automation') fetchAutomationRules();
    if (tabName === 'templates') fetchTemplates();
}

async function fetchCampaigns() {
    try {
        const res = await apiFetch(`${API_BASE}/campaigns`);
        const data = await res.json();
        const tbody = document.getElementById('campaigns-table-body');
        if (!tbody) return;
        tbody.innerHTML = data.length === 0 ? '<tr><td colspan="6" class="p-8 text-center text-gray-400 font-serif italic">Henüz kampanya gönderimi yapılmadı.</td></tr>' : '';
        data.forEach(c => {
            const dateStr = new Date(c.created_at).toLocaleString('tr-TR');
            tbody.innerHTML += `
                <tr class="border-b border-gray-50 hover:bg-gray-50/80 transition-colors">
                    <td class="p-6">
                        <div class="font-bold text-navy">${c.title}</div>
                        <div class="text-[10px] text-gray-400 italic">${c.subject}</div>
                    </td>
                    <td class="p-6"><span class="px-2 py-0.5 bg-modern/10 text-modern rounded text-[10px] font-bold uppercase">${c.type}</span></td>
                    <td class="p-6 text-xs text-gray-500 font-medium">${c.target_audience || 'Tüm Liste'}</td>
                    <td class="p-6">
                        <div class="flex items-center gap-2">
                            <div class="w-16 h-1.5 bg-gray-100 rounded-full overflow-hidden">
                                <div class="h-full bg-gold" style="width: ${c.sent_count ? (c.sent_count/c.total_recipients)*100 : 0}%"></div>
                            </div>
                            <span class="text-[10px] font-bold text-navy">${c.sent_count || 0}/${c.total_recipients || 0}</span>
                        </div>
                    </td>
                    <td class="p-6 text-xs text-gray-400">${dateStr}</td>
                    <td class="p-6 text-right">
                        <span class="px-3 py-1 bg-green-50 text-green-600 rounded-full text-[10px] font-black uppercase tracking-widest border border-green-100 shadow-sm">${c.status}</span>
                    </td>
                </tr>`;
        });
    } catch (e) { console.error(e); }
}

async function fetchAutomationRules() {
    try {
        const res = await apiFetch(`${API_BASE}/automation/rules`);
        const data = await res.json();
        const tbody = document.getElementById('automation-rules-table-body');
        if (!tbody) return;
        tbody.innerHTML = data.length === 0 ? '<tr><td colspan="5" class="p-8 text-center text-gray-400 font-serif italic">Aktif otomasyon kuralı bulunmuyor.</td></tr>' : '';
        data.forEach(r => {
            const tr = document.createElement('tr');
            tr.className = 'border-b border-gray-50 hover:bg-gray-50/80 transition-colors';
            const statusToggle = r.is_active ?
                '<span class="flex items-center gap-1 text-green-600 font-bold"><i class="fa-solid fa-circle text-[6px]"></i> Aktif</span>' :
                '<span class="flex items-center gap-1 text-gray-400 font-bold"><i class="fa-solid fa-circle text-[6px]"></i> Pasif</span>';
            
            tr.innerHTML = `
                <td class="p-6 font-bold text-navy">${r.name}</td>
                <td class="p-6"><span class="px-2 py-1 bg-gray-100 rounded text-[10px] font-bold text-gray-600 uppercase tracking-widest">${r.trigger_event}</span></td>
                <td class="p-6 text-xs text-gray-500 font-medium">${r.action_type}: ${r.template_id || 'Otomatik Mesaj'}</td>
                <td class="p-6">${statusToggle}</td>
                <td class="p-6 text-right">
                    <button onclick="toggleRule(${r.id})" class="text-navy hover:text-gold transition-colors p-2"><i class="fa-solid fa-power-off"></i></button>
                    <button onclick="deleteRule(${r.id})" class="text-red-400 hover:text-red-500 transition-colors p-2"><i class="fa-solid fa-trash"></i></button>
                </td>`;
            tbody.appendChild(tr);
        });
    } catch (e) { console.error(e); }
}

async function fetchTemplates() {
    try {
        const res = await apiFetch(`${API_BASE}/campaigns/templates`);
        const data = await res.json().catch(() => []);
        const grid = document.getElementById('templates-grid');
        if (!grid) return;
        grid.innerHTML = data.length === 0 ? '<div class="p-12 text-center text-gray-400 col-span-full border-2 border-dashed border-gray-100 rounded-[2rem]">Henüz mesaj şablonu oluşturulmadı.</div>' : '';
        data.forEach(t => {
            grid.innerHTML += `
                <div class="bg-white p-6 rounded-[2rem] border border-gray-100 shadow-sm hover:shadow-md transition-all group relative overflow-hidden">
                    <div class="absolute top-0 left-0 w-1 h-full bg-modern opacity-20 group-hover:opacity-100 transition-opacity"></div>
                    <div class="flex justify-between items-start mb-4">
                        <h4 class="font-bold text-navy font-serif text-lg">${t.name}</h4>
                        <span class="text-[10px] font-black text-gray-500 uppercase tracking-widest">${t.type}</span>
                    </div>
                    <p class="text-gray-600 text-xs line-clamp-3 mb-6 font-medium italic">"${t.content}"</p>
                    <div class="flex justify-between items-center">
                        <span class="text-[9px] text-gray-500 font-bold uppercase tracking-tighter"><i class="fa-solid fa-clock mr-1"></i> ${new Date(t.created_at).toLocaleDateString()}</span>
                        <div class="flex gap-2">
                            <button class="text-gray-600 hover:text-navy transition-colors text-sm"><i class="fa-solid fa-pen"></i></button>
                            <button class="text-gray-600 hover:text-red-500 transition-colors text-sm"><i class="fa-solid fa-trash"></i></button>
                        </div>
                    </div>
                </div>`;
        });
    } catch (e) { console.error(e); }
}

async function fetchUsers() {
    const tbody = document.getElementById('users-table-body');
    if (!tbody) return;
    tbody.innerHTML = '<tr><td colspan="4" class="py-8 text-center text-gray-400">Yükleniyor...</td></tr>';
    try {
        const res = await apiFetch(`${API_BASE}/users`);
        const data = await res.json();
        tbody.innerHTML = '';
        data.forEach(u => {
            const isStaff = ['broker', 'standart'].includes(u.role);
            const trackingBtn = isStaff ? `
                <button onclick="openRoutePlayback(${u.id}, '${u.username}')" 
                        class="w-8 h-8 rounded-lg bg-emerald-50 text-emerald-600 hover:bg-emerald-600 hover:text-white transition-all flex items-center justify-center shadow-sm" 
                        title="Rota Geçmişi">
                    <i class="fa-solid fa-route text-xs"></i>
                </button>` : '';
            tbody.innerHTML += `
                <tr class="border-b border-gray-100 hover:bg-gray-50 transition-colors group">
                    <td class="px-6 py-4 font-mono text-xs text-gray-500">#${u.id}</td>
                    <td class="px-6 py-4 font-bold text-navy">${u.username}</td>
                    <td class="px-6 py-4"><span class="px-2 py-1 bg-gray-100 rounded text-[10px] font-bold text-gray-600 uppercase">${u.role}</span></td>
                    <td class="px-6 py-4 text-right flex gap-3 justify-end opacity-0 group-hover:opacity-100 transition-opacity">
                        ${trackingBtn}
                        <button onclick="editUser(${u.id})" class="w-8 h-8 rounded-lg bg-blue-50 text-blue-600 hover:bg-blue-600 hover:text-white transition-all flex items-center justify-center shadow-sm"><i class="fa-solid fa-pen text-xs"></i></button>
                        <button onclick="deleteUser(${u.id})" class="w-8 h-8 rounded-lg bg-red-50 text-red-600 hover:bg-red-600 hover:text-white transition-all flex items-center justify-center shadow-sm"><i class="fa-solid fa-trash text-xs"></i></button>
                    </td>
                </tr>`;
        });
    } catch (err) { console.error(err); }
}

// --- İMZA LENS (SHADOW LISTINGS) ---
async function fetchShadowListings() {
    const tbody = document.getElementById('shadow-listings-table-body');
    if (!tbody) return;
    tbody.innerHTML = '<tr><td colspan="6" class="py-12 text-center text-gray-400"><i class="fa-solid fa-spinner fa-spin mr-2"></i> Veriler yükleniyor...</td></tr>';
    try {
        const res = await apiFetch(`${API_BASE}/extension/listings`);
        const data = await res.json();
        tbody.innerHTML = data.length === 0 ? '<tr><td colspan="6" class="py-12 text-center text-gray-400">Henüz senkronize edilmiş veri bulunamadı.</td></tr>' : '';
        data.forEach(item => {
            const dateStr = new Date(item.last_seen_at || item.last_sync).toLocaleString('tr-TR');
            const location = (item.city || item.district) ? `${item.city} / ${item.district}` : '<span class="text-gray-300">Belirtilmedi</span>';
            const roiUI = item.listing_type === 'Satılık' && item.roi_score > 0 ? `<div class="flex flex-col"><span class="px-2 py-0.5 rounded text-[10px] font-bold text-green-600 bg-green-50 w-fit">%${item.roi_score.toFixed(2)} ROI</span></div>` : '-';
            tbody.innerHTML += `
                <tr class="border-b border-gray-100 hover:bg-gray-50 transition-colors group">
                    <td class="py-4 px-6 text-center"><span class="px-3 py-1 bg-gold/10 text-gold rounded-full text-[10px] font-black uppercase tracking-widest border shadow-sm">${item.source}</span></td>
                    <td class="py-4 px-6"><span class="px-2 py-1 bg-navy/5 text-navy rounded text-[10px] font-bold">${item.listing_type || 'Satılık'}</span></td>
                    <td class="py-4 px-6"><div class="font-bold text-navy text-sm leading-tight">${item.title}</div></td>
                    <td class="py-4 px-6"><div class="text-sm font-medium text-navy/80">${location}</div></td>
                    <td class="py-4 px-6"><div class="font-bold text-green-700 text-sm">${item.price}</div></td>
                    <td class="py-4 px-6">${roiUI}</td>
                    <td class="py-4 px-6 text-right"><a href="${item.url}" target="_blank" class="text-navy"><i class="fa-solid fa-external-link"></i></a></td>
                </tr>`;
        });
    } catch (err) { console.error(err); }
}

// --- TRAFFIC & L-METRICS ---
async function fetchTrafficData() {
    const tbody = document.getElementById('traffic-table-body');
    if (!tbody) return;
    try {
        const res = await apiFetch(`${API_BASE}/tracking/interactions`);
        const data = await res.json();
        tbody.innerHTML = data.length === 0 ? '<tr><td colspan="5" class="py-12 text-center text-gray-400">Veri yok.</td></tr>' : '';
        data.forEach(item => {
            const dateStr = new Date(item.created_at).toLocaleString('tr-TR');
            tbody.innerHTML += `<tr class="border-b border-gray-50"><td class="py-4 px-6">${item.tool_name}</td><td class="py-4 px-6">${item.session_id}</td><td class="py-4 px-6 text-[10px]">${dateStr}</td></tr>`;
        });
    } catch (e) { console.error(e); }
}

function switchLensTab(tabName) {
    document.querySelectorAll('.lens-tab-btn').forEach(btn => {
        btn.classList.remove('active');
        btn.classList.add('text-gray-500', 'hover:text-navy');
    });
    const activeBtn = document.getElementById(`tab-btn-${tabName}`);
    if (activeBtn) {
        activeBtn.classList.add('active');
        activeBtn.classList.remove('text-gray-500', 'hover:text-navy');
    }
    document.querySelectorAll('.lens-tab-content').forEach(content => { content.classList.add('hidden'); });
    const targetContent = document.getElementById(`lens-tab-content-${tabName}`);
    if (targetContent) targetContent.classList.remove('hidden');
    if (tabName === 'shadow') fetchShadowListings();
    if (tabName === 'traffic') fetchTrafficData();
}

// --- TOAST SYSTEM ---
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    const colors = { 'success': 'from-emerald-500 to-teal-600', 'error': 'from-red-500 to-rose-600', 'info': 'from-blue-500 to-indigo-600' };
    toast.className = `fixed bottom-8 right-8 px-6 py-3 rounded-2xl bg-gradient-to-r ${colors[type]} text-white shadow-2xl z-[9999] animate-bounce-short`;
    toast.innerHTML = `<span>${message}</span>`;
    document.body.appendChild(toast);
    setTimeout(() => { toast.classList.add('opacity-0'); setTimeout(() => toast.remove(), 500); }, 3000);
}

// --- INIT ---
document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
    const catSelect = document.getElementById('p-kategori');
    if (catSelect) {
        catSelect.innerHTML = '<option value="">Seçiniz...</option>';
        Object.keys(PROPERTY_CATEGORIES).forEach(k => {
            const group = document.createElement('optgroup');
            group.label = k.toUpperCase();
            PROPERTY_CATEGORIES[k].forEach(v => {
                const opt = document.createElement('option'); opt.value = v; opt.textContent = v;
                group.appendChild(opt);
            });
            catSelect.appendChild(group);
        });
    }
});

// Helpers & Modal Managers
function openLeadModal() { document.getElementById('lead-modal').classList.remove('hidden'); }
function closeLeadModal() { document.getElementById('lead-modal').classList.add('hidden'); }
function openExpenseModal() { document.getElementById('expense-modal').classList.remove('hidden'); }
function closeExpenseModal() { document.getElementById('expense-modal').classList.add('hidden'); }
function openProjectModal() { document.getElementById('project-modal')?.classList.remove('hidden'); }
function closeProjectModal() { document.getElementById('project-modal')?.classList.add('hidden'); }
function openPortfolioModal() { document.getElementById('portfolio-modal')?.classList.remove('hidden'); }
function closePortfolioModal() { document.getElementById('portfolio-modal')?.classList.add('hidden'); }
function openCampaignModal() { document.getElementById('campaign-modal')?.classList.remove('hidden'); }
function closeCampaignModal() { document.getElementById('campaign-modal')?.classList.add('hidden'); }
function openRuleModal() { document.getElementById('rule-modal')?.classList.remove('hidden'); }
function closeRuleModal() { document.getElementById('rule-modal')?.classList.add('hidden'); }
function openTemplateModal() { document.getElementById('template-modal')?.classList.remove('hidden'); }
function closeTemplateModal() { document.getElementById('template-modal')?.classList.add('hidden'); }
function closePartyModal() { document.getElementById('party-modal')?.classList.add('hidden'); }

// --- CRUD HANDLERS ---
async function deletePortfolio(id) {
    if (!confirm('Bu portföyü silmek istediğinize emin misiniz?')) return;
    try {
        const res = await apiFetch(`${API_BASE}/portfolios/${id}`, { method: 'DELETE' });
        if (res.ok) { showToast('Portföy silindi', 'success'); fetchAllPortfolios(); }
        else showToast('Silme hatası', 'error');
    } catch (e) { showToast('Bağlantı hatası', 'error'); }
}

async function editPortfolio(id) {
    openPortfolioModal();
    // Fetch data and fill form...
    try {
        const res = await apiFetch(`${API_BASE}/portfolios/${id}`);
        const data = await res.json();
        // Populate form fields (Standardized Mapping)
        document.getElementById('p-id').value = data.id || '';
        document.getElementById('p-refNo').value = data.ref_no || '';
        document.getElementById('p-ozellik_kategori').value = data.listing_category || 'Satılık';
        document.getElementById('p-baslik1').value = data.title || '';
        document.getElementById('p-baslik2').value = data.subtitle || '';
        document.getElementById('p-koleksiyon').value = data.category || 'Konut';
        document.getElementById('p-fiyat').value = data.price || '';
        document.getElementById('p-lokasyon').value = data.location || '';
        document.getElementById('p-oda').value = data.rooms || '';
        document.getElementById('p-alan').value = data.area || '';
        document.getElementById('p-isitma').value = data.heating || '';
        document.getElementById('p-kat').value = data.floor || '';
        document.getElementById('p-resim_hero').value = data.image_hero || '';
        document.getElementById('p-resim_hikaye').value = data.image_story || '';
        document.getElementById('p-ozellikler_arr').value = data.features ? data.features.join(', ') : '';
        document.getElementById('p-hikaye').value = data.description || '';
    } catch (e) { console.error(e); }
}

async function runAutomationNow() {
    showToast('Otomasyon tetiklendi...', 'info');
    try {
        await apiFetch(`${API_BASE}/automation/run`, { method: 'POST' });
        showToast('Otomasyon tamamlandı', 'success');
    } catch (e) { showToast('Hata oluştu', 'error'); }
}

async function editLead(id) {
    try {
        const res = await apiFetch(`${API_BASE}/leads/${id}`);
        if (!res.ok) throw new Error('Yüklenemedi');
        const data = await res.json();
        
        // Formu temizle ve doldur
        openLeadModal(id);
        document.getElementById('lead-name').value = data.name || '';
        document.getElementById('lead-phone').value = data.phone || '';
        document.getElementById('lead-email').value = data.email || '';
        document.getElementById('lead-notes').value = data.notes || '';
        document.getElementById('lead-status').value = data.pipeline_stage_id || '1';
    } catch (e) { 
        console.error(e);
        showToast('Aday bilgileri alınamadı', 'error');
    }
}

// --- REFACTORED SPECIFIC DELETE HANDLERS ---
function deleteUser(id) { deleteRecord(id, 'users', fetchUsers); }
function deleteContact(id) { deleteRecord(id, 'contacts', fetchContacts); }
function deletePortfolio(id) { deleteRecord(id, 'portfolios', fetchAllPortfolios); }
function deleteAppointment(id) { deleteRecord(id, 'appointments', fetchAppointments); }
function deleteNotice(id) { deleteRecord(id, 'notices', fetchNotices); }

async function toggleRule(id) {
    try {
        const res = await apiFetch(`${API_BASE}/automation/rules/${id}/toggle`, { method: 'POST' });
        if (res.ok) fetchAutomationRules();
    } catch (e) { console.error(e); }
}

function deleteRule(id) { deleteRecord(id, 'automation/rules', fetchAutomationRules); }

async function savePortfolio() {
    // Shared implementation with submitPortfolioForm for consistency
    await submitPortfolioForm();
}

async function submitPortfolioForm() {
    const id = document.getElementById('p-id')?.value;
    const featuresRaw = document.getElementById('p-ozellikler_arr')?.value || '';
    
    // Payload mapped to current standardized English Schema (Phase 14)
    const payload = {
        ref_no: document.getElementById('p-refNo')?.value,
        listing_category: document.getElementById('p-ozellik_kategori')?.value,
        title: document.getElementById('p-baslik1')?.value,
        subtitle: document.getElementById('p-baslik2')?.value,
        category: document.getElementById('p-koleksiyon')?.value,
        price: parseFloat(document.getElementById('p-fiyat')?.value) || 0,
        location: document.getElementById('p-lokasyon')?.value,
        rooms: document.getElementById('p-oda')?.value,
        area: document.getElementById('p-alan')?.value,
        heating: document.getElementById('p-isitma')?.value,
        floor: document.getElementById('p-kat')?.value,
        image_hero: document.getElementById('p-resim_hero')?.value,
        image_story: document.getElementById('p-resim_hikaye')?.value,
        features: featuresRaw.split(',').map(s => s.trim()).filter(s => s !== ''),
        description: document.getElementById('p-hikaye')?.value
    };
    
    const method = id ? 'PUT' : 'POST';
    const url = id ? `${API_BASE}/portfolios/${id}` : `${API_BASE}/portfolios`;
    
    try {
        const res = await apiFetch(url, { method, body: JSON.stringify(payload) });
        if (res.ok) {
            showToast('Portföy başarıyla kaydedildi', 'success');
            closePortfolioModal();
            fetchAllPortfolios();
            // Also update dashboard if visible
            if (typeof fetchDashboardStats === 'function') fetchDashboardStats();
        } else {
            const err = await res.json();
            showToast(`Hata: ${err.message || 'Kaydedilemedi'}`, 'error');
        }
    } catch (e) { 
        console.error(e);
        showToast('Bağlantı hatası oluştu', 'error'); 
    }
}

async function saveLead() {
    const id = document.getElementById('lead-id')?.value;
    const payload = {
        name: document.getElementById('lead-name')?.value,
        phone: document.getElementById('lead-phone')?.value,
        email: document.getElementById('lead-email')?.value,
        notes: document.getElementById('lead-notes')?.value,
        status: document.getElementById('lead-status')?.value || 'new'
    };
    
    const method = id ? 'PUT' : 'POST';
    const url = id ? `${API_BASE}/leads/${id}` : `${API_BASE}/leads`;

    try {
        const res = await apiFetch(url, { method, body: JSON.stringify(payload) });
        if (res.ok) {
            showToast(id ? 'Müşteri adayı güncellendi' : 'Müşteri adayı başarıyla kaydedildi', 'success');
            toggleModal('lead-modal', false);
            fetchLeads();
        } else {
            const err = await res.json();
            showToast(err.error || 'Kaydedilemedi', 'error');
        }
    } catch (e) { showToast('Hata oluştu', 'error'); }
}

function openLeadModal(id = null) {
    // Reset form
    const form = document.getElementById('lead-form');
    if (form) form.reset();
    document.getElementById('lead-id').value = id || '';
    document.getElementById('lead-modal-title').textContent = id ? 'Aday Müşteri Düzenle' : 'Yeni Müşteri Adayı';
    
    if (id) {
        // Fetch and fill logic would go here
        console.log("Edit Lead ID:", id);
    }
    
    toggleModal('lead-modal', true);
}

function openContractModal(id = null) {
    toggleModal('contract-modal', true);
}

function openTaxModal(id = null) {
    toggleModal('tax-modal', true);
}

function openMaintenanceModal(id = null) {
    toggleModal('maintenance-modal', true);
}

function openExpenseModal(id = null) {
    toggleModal('expense-modal', true);
}

async function deleteRecord(id, type, refreshFunc) {
    if (!confirm('Bu kaydı silmek istediğinize emin misiniz?')) return;
    
    try {
        const res = await apiFetch(`${API_BASE}/${type}/${id}`, { method: 'DELETE' });
        if (res.ok) {
            showToast('Kayıt başarıyla silindi', 'success');
            if (typeof refreshFunc === 'function') refreshFunc();
        } else {
            showToast('Silme işlemi başarısız oldu', 'error');
        }
    } catch (e) { showToast('Bağlantı hatası', 'error'); }
}

function deleteLead(id, section = 'leads') {
    deleteRecord(id, 'leads', section === 'ai-reports' ? fetchAiReports : fetchLeads);
}

async function saveExpense() {
    const payload = {
        date: document.getElementById('exp-date')?.value,
        category: document.getElementById('exp-category')?.value,
        amount: parseFloat(document.getElementById('exp-amount')?.value) || 0,
        description: document.getElementById('exp-desc')?.value
    };
    try {
        const res = await apiFetch(`${API_BASE}/expenses`, { method: 'POST', body: JSON.stringify(payload) });
        if (res.ok) {
            showToast('Harcama kaydedildi', 'success');
            closeExpenseModal();
            if (typeof fetchExpenses === 'function') fetchExpenses();
        }
    } catch (e) { showToast('Hata oluştu', 'error'); }
}

async function triggerAiTranslation() {
    const id = document.getElementById('p-id')?.value;
    if (!id) {
        showToast('Lütfen önce portföyü kaydedin.', 'error');
        return;
    }
    showToast('AI Çeviri başlatıldı...', 'info');
    try {
        await apiFetch(`${API_BASE}/portfolios/${id}/translate`, { method: 'POST' });
        showToast('Çeviriler tamamlandı', 'success');
} catch (e) { showToast('Çeviri hatası', 'error'); }
}

// --- MODAL & SETTINGS HELPERS ---
function toggleModal(modalId, show = true) {
    const modal = document.getElementById(modalId);
    if (!modal) return;
    if (show) modal.classList.remove('hidden');
    else modal.classList.add('hidden');
}

async function fetchSettings() {
    try {
        const res = await apiFetch(`${API_BASE}/settings/site_mode`);
        if (res.ok) {
            const data = await res.json();
            const mode = data.site_mode || 'placeholder';
            const radio = document.querySelector(`input[name="site_mode"][value="${mode}"]`);
            if (radio) radio.checked = true;
        }
    } catch (e) {
        console.error('Settings fetch error:', e);
    }
}

async function saveSiteSettings() {
    const selectedMode = document.querySelector('input[name="site_mode"]:checked')?.value;
    if (!selectedMode) {
        if(typeof showToast === 'function') showToast('Lütfen bir mod seçin', 'error');
        else alert('Lütfen bir mod seçin');
        return;
    }
    
    try {
        const res = await apiFetch(`${API_BASE}/settings/site_mode`, {
            method: 'PUT',
            body: JSON.stringify({ site_mode: selectedMode })
        });
        
        if (res.ok) {
            if(typeof showToast === 'function') showToast('Site modu başarıyla güncellendi.', 'success');
            else alert('Site modu başarıyla güncellendi.');
        } else {
            const err = await res.json();
            if(typeof showToast === 'function') showToast(err.error || 'Ayarlar kaydedilemedi', 'error');
            else alert(err.error || 'Ayarlar kaydedilemedi');
        }
    } catch (e) {
        console.error('Settings save error:', e);
        if(typeof showToast === 'function') showToast('Bağlantı hatası', 'error');
        else alert('Bağlantı hatası');
    }
}
// --- AI ANALİZ RAPORLARI LOGIC ---
async function fetchAiReports() {
    const tableBody = document.getElementById('ai-reports-table-body');
    if (!tableBody) return;
    
    tableBody.innerHTML = '<tr><td colspan="5" class="py-20 text-center text-gray-400 font-medium animate-pulse">Analitik veriler işleniyor...</td></tr>';

    try {
        // Fetch leads from AI Rotasi source
        const res = await apiFetch(`${API_BASE}/leads?source=ai_rotasi`);
        if (!res.ok) throw new Error('Yüklenemedi');
        
        const leads = await res.json();
        if (leads.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="5" class="py-20 text-center text-gray-400">Henüz AI analiz verisi bulunmuyor.</td></tr>';
            return;
        }

        tableBody.innerHTML = '';
        leads.forEach(lead => {
            // Parse AI diagnosis from notes
            const diagnosis = parseAiDiagnosis(lead.notes);
            const scoreClass = lead.ai_score >= 80 ? 'text-emerald-500' : (lead.ai_score >= 50 ? 'text-gold' : 'text-gray-400');
            
            const tr = document.createElement('tr');
            tr.className = "hover:bg-gray-50/50 transition-colors group";
            tr.innerHTML = `
                <td class="py-6 px-8">
                    <div class="flex flex-col">
                        <span class="font-bold text-navy">${lead.name}</span>
                        <span class="text-[10px] text-gray-400 font-medium">${lead.phone || lead.email || '-'}</span>
                    </div>
                </td>
                <td class="py-6 px-8">
                    <div class="inline-flex items-center gap-2 px-3 py-1 bg-navy/5 rounded-full border border-navy/10">
                        <span class="w-1.5 h-1.5 rounded-full ${diagnosis.dotColor}"></span>
                        <span class="text-[10px] font-bold text-navy uppercase tracking-wider">${diagnosis.label}</span>
                    </div>
                </td>
                <td class="py-6 px-8">
                    <span class="text-xs font-bold text-gray-600">${diagnosis.budget}</span>
                </td>
                <td class="py-6 px-8">
                    <span class="text-sm font-black ${scoreClass}">%${lead.ai_score || 0}</span>
                </td>
                <td class="py-6 px-8 text-right">
                    <button onclick="viewInPipeline('${lead.id}')" class="text-navy hover:text-gold transition-colors p-2" title="Pipeline'da Gör">
                        <i class="fa-solid fa-diagram-project"></i>
                    </button>
                    <button onclick="deleteLead('${lead.id}', 'ai-reports')" class="text-gray-300 hover:text-red-500 transition-colors p-2">
                        <i class="fa-solid fa-trash-can"></i>
                    </button>
                </td>
            `;
            tableBody.appendChild(tr);
        });
    } catch (e) {
        console.error(e);
        tableBody.innerHTML = '<tr><td colspan="5" class="py-20 text-center text-red-400">Veriler yüklenirken bir hata oluştu.</td></tr>';
    }
}

function parseAiDiagnosis(notes) {
    if (!notes) return { label: 'Analiz Edilmedi', dotColor: 'bg-gray-400', budget: 'Belirsiz' };
    
    const n = notes.toLowerCase();
    
    // Premium Labels Mapping
    if (n.includes('yatırımcı') || n.includes('vizyon')) {
        return { label: 'Vizyoner Yatırımcı', dotColor: 'bg-gold', budget: 'Yüksek (Premium)' };
    }
    if (n.includes('fırsat') || n.includes('strateji')) {
        return { label: 'Stratejik Planlamacı', dotColor: 'bg-emerald-500', budget: 'Orta-Yüksek' };
    }
    if (n.includes('istikrar') || n.includes('garanti')) {
        return { label: 'İstikrar Odaklı', dotColor: 'bg-blue-500', budget: 'Düzenli Nakit' };
    }
    if (n.includes('analist') || n.includes('rasyonel')) {
        return { label: 'Rasyonel Analist', dotColor: 'bg-purple-500', budget: 'Optimum ROI' };
    }
    
    return { label: 'Standart Profil', dotColor: 'bg-gray-400', budget: 'İnceleniyor' };
}

// --- PROJE MASASI LOGIC ---
async function fetchProjects() {
    const tbody = document.getElementById('projects-table-body');
    if (!tbody) return;
    tbody.innerHTML = '<tr><td colspan="5" class="py-20 text-center animate-pulse">Projeler yükleniyor...</td></tr>';
    try {
        const res = await apiFetch(`${API_BASE}/projects`);
        const projects = await res.json();
        tbody.innerHTML = projects.length ? '' : '<tr><td colspan="5" class="py-20 text-center text-gray-400 font-serif italic">Henüz aktif proje bulunmuyor.</td></tr>';
        projects.forEach(p => {
            const statusClass = p.status === 'active' ? 'bg-emerald-50 text-emerald-600' : 'bg-gray-100 text-gray-500';
            tbody.innerHTML += `
                <tr class="border-b border-gray-50 hover:bg-gray-50 transition-colors group">
                    <td class="px-6 py-4 font-bold text-navy">${p.title}</td>
                    <td class="px-6 py-4"><span class="px-2 py-1 ${statusClass} rounded text-[10px] font-black uppercase tracking-widest">${p.status}</span></td>
                    <td class="px-6 py-4 text-xs text-gray-500">${p.total_units || 0} Ünite</td>
                    <td class="px-6 py-4 text-right">
                        <button class="text-navy hover:text-gold transition-colors"><i class="fa-solid fa-pen-to-square"></i></button>
                    </td>
                </tr>`;
        });
    } catch (e) { tbody.innerHTML = '<tr><td colspan="5" class="py-20 text-center text-red-400">Veriler yüklenirken hata oluştu.</td></tr>'; }
}

async function fetchContracts() {
    const tbody = document.getElementById('contracts-table-body');
    if (!tbody) return;
    tbody.innerHTML = '<tr><td colspan="6" class="py-20 text-center animate-pulse text-gray-400 font-serif italic">Sözleşmeler taranıyor...</td></tr>';
    try {
        const res = await apiFetch(`${API_BASE}/contracts/`);
        const result = await res.json();
        const contracts = result.data || [];
        tbody.innerHTML = contracts.length ? '' : '<tr><td colspan="6" class="py-20 text-center text-gray-400 font-serif italic">Arşivde kayıtlı sözleşme bulunamadı.</td></tr>';
        contracts.forEach(c => {
            const dateStr = c.created_at ? c.created_at.split('T')[0] : '-';
            tbody.innerHTML += `
                <tr class="border-b border-gray-50 hover:bg-gray-50 transition-colors group">
                    <td class="px-6 py-4 font-mono text-[10px] text-gray-400">#${c.contract_number}</td>
                    <td class="px-6 py-4 font-bold text-navy">${c.contract_type}</td>
                    <td class="px-6 py-4 text-xs font-semibold text-gray-600">${c.price} ${c.currency}</td>
                    <td class="px-6 py-4"><span class="px-2 py-0.5 bg-modern/10 text-modern rounded text-[10px] font-bold uppercase">${c.status}</span></td>
                    <td class="px-6 py-4 text-[10px] text-gray-400">${dateStr}</td>
                    <td class="px-6 py-4 text-right">
                        <button onclick="downloadContractPdf(${c.id})" class="text-navy hover:text-gold transition-colors p-2"><i class="fa-solid fa-file-pdf"></i></button>
                    </td>
                </tr>`;
        });
    } catch (e) { tbody.innerHTML = '<tr><td colspan="6" class="py-20 text-center text-red-400">Yükleme hatası.</td></tr>'; }
}

async function fetchPayroll() {
    try {
        const res = await apiFetch(`${API_BASE}/finance/summary`);
        const data = await res.json();
        // Update the summary cards in the payroll section (Matching portal.html IDs)
        const commTotal = document.getElementById('payroll-commission-total');
        const expTotal = document.getElementById('payroll-expense-total');
        const contractCount = document.getElementById('payroll-contract-count');
        const netTotal = document.getElementById('payroll-net');
        
        if (commTotal) commTotal.textContent = new Intl.NumberFormat('tr-TR').format(data.total_commissions || 0) + ' ' + (data.currency || '₺');
        if (expTotal) expTotal.textContent = new Intl.NumberFormat('tr-TR').format(data.total_expenses || 0) + ' ' + (data.currency || '₺');
        if (contractCount) contractCount.textContent = data.active_contracts_count || 0;
        if (netTotal) netTotal.textContent = new Intl.NumberFormat('tr-TR').format(data.net_profit || 0) + ' ' + (data.currency || '₺');
    } catch (e) { console.warn("Payroll summary update failed"); }
}

async function fetchGlobalVisibility() {
    const tbody = document.getElementById('visibility-matrix');
    if (!tbody) return;
    tbody.innerHTML = '<tr><td colspan="6" class="py-20 text-center animate-pulse text-gray-400">Görünürlük verileri taranıyor...</td></tr>';
    try {
        const res = await apiFetch(`${API_BASE}/portfolios`);
        const result = await res.json();
        const portfolios = result.data || [];
        tbody.innerHTML = portfolios.length ? '' : '<tr><td colspan="6" class="py-20 text-center text-gray-400">Aktif ilan bulunamadı.</td></tr>';
        portfolios.forEach(p => {
            tbody.innerHTML += `
                <tr class="border-b border-gray-50 hover:bg-gray-50/50 transition-colors">
                    <td class="px-8 py-6">
                        <div class="flex items-center gap-4">
                            <img src="${p.media_url || 'https://placehold.co/100x100/0a192f/c5a059?text=IMG'}" class="w-12 h-12 rounded-xl object-cover shadow-sm">
                            <div>
                                <p class="font-bold text-navy text-sm">${p.title}</p>
                                <p class="text-[10px] text-gray-400">${p.location}</p>
                            </div>
                        </div>
                    </td>
                    <td class="px-6 py-6 text-center"><input type="checkbox" checked class="w-5 h-5 accent-navy rounded-lg"></td>
                    <td class="px-6 py-6 text-center"><input type="checkbox" ${p.is_global ? 'checked' : ''} class="w-5 h-5 accent-navy rounded-lg"></td>
                    <td class="px-6 py-6 text-center"><input type="checkbox" class="w-5 h-5 accent-navy rounded-lg"></td>
                    <td class="px-6 py-6 text-center"><input type="checkbox" class="w-5 h-5 accent-navy rounded-lg"></td>
                    <td class="px-8 py-6">
                        <button onclick="triggerAiTranslation(${p.id})" class="text-indigo-600 font-bold text-[10px] uppercase tracking-widest hover:underline">AI Optimize Et</button>
                    </td>
                </tr>`;
        });
    } catch (e) { tbody.innerHTML = '<tr><td colspan="6" class="py-20 text-center text-red-400">Veriler yüklenemedi.</td></tr>'; }
}

async function fetchTaxes() {
    const tbody = document.getElementById('taxes-table-body');
    if (!tbody) return;
    tbody.innerHTML = '<tr><td colspan="5" class="py-20 text-center animate-pulse">Vergi kayıtları listeleniyor...</td></tr>';
    try {
        const res = await apiFetch(`${API_BASE}/finance/taxes`);
        const taxes = await res.json();
        tbody.innerHTML = taxes.length ? '' : '<tr><td colspan="5" class="py-20 text-center text-gray-400 font-serif italic">Yakın zamanda ödenmiş vergi kaydı bulunmuyor.</td></tr>';
        taxes.forEach(t => {
            tbody.innerHTML += `
                <tr class="border-b border-gray-50 hover:bg-gray-50 transition-colors group">
                    <td class="px-6 py-4 font-bold text-navy">${t.type}</td>
                    <td class="px-6 py-4 text-xs text-gray-500">${t.period}</td>
                    <td class="px-6 py-4 font-bold text-red-600">${t.amount} ${t.currency || 'TRY'}</td>
                    <td class="px-6 py-4"><span class="px-2 py-0.5 bg-green-50 text-green-600 rounded text-[10px] font-bold uppercase">${t.status}</span></td>
                </tr>`;
        });
    } catch (e) { tbody.innerHTML = '<tr><td colspan="5" class="py-20 text-center text-red-400">Veriler alınamadı.</td></tr>'; }
}

async function fetchMaintenance() {
    const tbody = document.getElementById('maintenance-table-body');
    if (!tbody) return;
    tbody.innerHTML = '<tr><td colspan="5" class="py-20 text-center animate-pulse">Teknik talepler taranıyor...</td></tr>';
    try {
        const res = await apiFetch(`${API_BASE}/maintenance/tickets`);
        const tickets = await res.json();
        tbody.innerHTML = tickets.length ? '' : '<tr><td colspan="5" class="py-20 text-center text-gray-400 font-serif italic">Aktif teknik servis talebi bulunmuyor.</td></tr>';
        tickets.forEach(t => {
            const priorityColors = { 'high': 'text-red-600 bg-red-50', 'medium': 'text-gold bg-gold/10', 'low': 'text-gray-500 bg-gray-100' };
            const pClass = priorityColors[t.priority] || priorityColors.medium;
            tbody.innerHTML += `
                <tr class="border-b border-gray-50 hover:bg-gray-50 transition-colors group">
                    <td class="px-6 py-4">
                        <div class="font-bold text-navy">${t.title}</div>
                        <div class="text-[10px] text-gray-400">${t.description}</div>
                    </td>
                    <td class="px-6 py-4"><span class="px-2 py-1 ${pClass} rounded text-[10px] font-black uppercase tracking-widest">${t.priority}</span></td>
                    <td class="px-6 py-4 text-xs font-semibold text-navy/80">${t.status.toUpperCase()}</td>
                    <td class="px-6 py-4 text-right">
                        <button class="text-navy hover:text-gold transition-colors"><i class="fa-solid fa-check-double"></i></button>
                    </td>
                </tr>`;
        });
    } catch (e) { tbody.innerHTML = '<tr><td colspan="5" class="py-20 text-center text-red-400">Hata oluştu.</td></tr>'; }
}

async function fetchNotices() {
    const container = document.getElementById('notices-container');
    if (!container) return;
    container.innerHTML = '<div class="col-span-full py-20 text-center animate-pulse text-gray-400 font-serif italic">Duyuru merkezi güncelleniyor...</div>';
    try {
        const res = await apiFetch(`${API_BASE}/notices/`);
        const notices = await res.json();
        container.innerHTML = notices.length ? '' : '<div class="col-span-full py-20 text-center text-gray-400 font-serif italic">Henüz bir duyuru yayınlanmadı.</div>';
        notices.forEach(n => {
            const bgClass = n.type === 'urgent' ? 'bg-red-50 border-red-100' : 'bg-white border-gray-100';
            const iconClass = n.type === 'urgent' ? 'fa-triangle-exclamation text-red-500' : 'fa-bullhorn text-gold';
            container.innerHTML += `
                <div class="${bgClass} p-6 rounded-[2rem] border shadow-sm hover:shadow-md transition-all group">
                    <div class="flex justify-between items-start mb-4">
                        <div class="w-10 h-10 rounded-full bg-white shadow-sm flex items-center justify-center">
                            <i class="fa-solid ${iconClass}"></i>
                        </div>
                        <span class="text-[10px] font-black text-gray-400 uppercase tracking-widest">${new Date(n.created_at).toLocaleDateString()}</span>
                    </div>
                    <h4 class="font-bold text-navy font-serif text-lg mb-2">${n.title}</h4>
                    <p class="text-gray-500 text-xs leading-relaxed line-clamp-3 mb-4">${n.message}</p>
                    <div class="flex justify-end gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
                        <button class="text-[10px] font-black text-navy uppercase tracking-widest hover:text-gold">Detay <i class="fa-solid fa-arrow-right ml-1"></i></button>
                    </div>
                </div>`;
        });
    } catch (e) { container.innerHTML = '<div class="col-span-full py-20 text-center text-red-400 font-serif italic">Bağlantı hatası: Duyurular yüklenemedi.</div>'; }
}

async function fetchHeroSlides() {
    const tbody = document.getElementById('hero-slides-table-body');
    if (!tbody) return;
    tbody.innerHTML = '<tr><td colspan="5" class="py-20 text-center animate-pulse">Vitrin verileri taranıyor...</td></tr>';
    try {
        const res = await apiFetch(`${API_BASE}/hero`);
        const slides = await res.json();
        tbody.innerHTML = slides.length ? '' : '<tr><td colspan="5" class="py-20 text-center text-gray-400 font-serif italic">Vitrinde aktif slide bulunmuyor.</td></tr>';
        slides.forEach(s => {
            tbody.innerHTML += `
                <tr class="border-b border-gray-50 hover:bg-gray-50 transition-colors group">
                    <td class="px-6 py-4">
                        <div class="w-16 h-10 rounded shadow-sm overflow-hidden bg-gray-100">
                            <img src="${s.image_url}" class="w-full h-full object-cover" onerror="this.src='https://placehold.co/100x60/0a192f/c5a059?text=IMG'">
                        </div>
                    </td>
                    <td class="px-6 py-4 font-bold text-navy">${s.title}</td>
                    <td class="px-6 py-4 text-xs text-gray-500">${s.order_index}</td>
                    <td class="px-6 py-4 text-right">
                        <button onclick="deleteHeroSlide(${s.id})" class="text-red-400 hover:text-red-600 transition-all p-2 group-hover:scale-110">
                            <i class="fa-solid fa-trash-can"></i>
                        </button>
                    </td>
                </tr>`;
        });
    } catch (e) { tbody.innerHTML = '<tr><td colspan="5" class="py-20 text-center text-red-400">Veriler alınamadı.</td></tr>'; }
}

// --- FİNANS & MUHASEBE (Gider Yönetimi) ---
async function fetchExpenses() {
    const tbody = document.getElementById('expenses-table-body');
    if (!tbody) return;
    tbody.innerHTML = '<tr><td colspan="6" class="py-12 text-center animate-pulse">Harcamalar taranıyor...</td></tr>';
    try {
        const res = await apiFetch(`${API_BASE}/finance/expenses`);
        const data = await res.json();
        tbody.innerHTML = data.length === 0 ? '<tr><td colspan="6" class="py-12 text-center text-gray-500 font-serif italic">Henüz harcama kaydı bulunmuyor.</td></tr>' : '';
        data.forEach(ex => {
            const statusClass = ex.status === 'approved' ? 'bg-green-50 text-green-600' : 'bg-orange-50 text-orange-600';
            const statusLabel = ex.status === 'approved' ? 'Onaylandı' : 'Beklemede';
            tbody.innerHTML += `
                <tr class="border-b border-gray-100 hover:bg-gray-50 transition-colors group">
                    <td class="px-6 py-4 text-xs font-semibold text-gray-600">${new Date(ex.created_at).toLocaleDateString()}</td>
                    <td class="px-6 py-4 font-bold text-navy">${ex.personnel_name || 'Sistem'}</td>
                    <td class="px-6 py-4"><span class="px-2 py-0.5 bg-navy/5 text-navy rounded text-[10px] font-bold uppercase">${ex.category}</span></td>
                    <td class="px-6 py-4 font-black text-navy">${ex.amount} ₺</td>
                    <td class="px-6 py-4"><span class="px-2 py-1 rounded-full text-[10px] font-black uppercase tracking-widest ${statusClass}">${statusLabel}</span></td>
                    <td class="px-6 py-4 text-right">
                        ${ex.status !== 'approved' ? `<button onclick="approveExpense(${ex.id})" class="text-green-500 hover:text-green-700 p-2 transition-transform hover:scale-110"><i class="fa-solid fa-check-double"></i></button>` : '<i class="fa-solid fa-circle-check text-green-200"></i>'}
                        <button onclick="deleteRecord('finance/expenses', ${ex.id}, fetchExpenses)" class="text-red-400 hover:text-red-600 p-2 ml-2"><i class="fa-solid fa-trash-can"></i></button>
                    </td>
                </tr>`;
        });
    } catch (e) { tbody.innerHTML = '<tr><td colspan="6" class="py-12 text-center text-red-500">Gider verileri alınamadı.</td></tr>'; }
}

async function approveExpense(id) {
    if (!confirm('Bu harcamayı onaylamak istediğinize emin misiniz?')) return;
    try {
        const res = await apiFetch(`${API_BASE}/finance/expenses/${id}/approve`, { method: 'PUT' });
        if (res.ok) {
            showToast('Harcama onaylandı', 'success');
            fetchExpenses();
        }
    } catch (e) { showToast('Onaylama işlemi başarısız', 'error'); }
}

async function updateAnalytics() {
    const container = document.getElementById('market-analytics-container');
    if (!container) return;
    console.log("[İMZA] Pazar Analitiği Güncelleniyor...");
    try {
        const res = await apiFetch(`${API_BASE}/compass/heatmaps`);
        const data = await res.json();
        // Here we would typically update Chart.js instances if they exist
        // For now, logging success
        console.log("[İMZA] Analitik veri senkronize edildi:", data.length, "kayıt.");
    } catch (e) { console.warn("Analytics update failed"); }
}

async function fetchProjectHub() {
    console.log("[İMZA] Proje Masası Yükleniyor...");
    updateProjectHubCounts();
    const tableBody = document.getElementById('project-hub-table-body');
    if (!tableBody) return;
    tableBody.innerHTML = '<tr><td colspan="5" class="py-20 text-center animate-pulse">Operasyonel veriler yükleniyor...</td></tr>';
    try {
        const res = await apiFetch(`${API_BASE}/projects`);
        const projects = await res.json();
        tableBody.innerHTML = projects.length ? '' : '<tr><td colspan="5" class="py-20 text-center text-gray-400 font-serif italic">Henüz bir proje kaydı yok.</td></tr>';
        projects.forEach(p => {
            const tr = document.createElement('tr');
            tr.className = "hover:bg-gray-50 transition-colors group";
            tr.innerHTML = `
                <td class="px-6 py-4 font-mono text-[10px] text-gray-400">#${p.id}</td>
                <td class="px-6 py-4 font-bold text-navy">${p.title}</td>
                <td class="px-6 py-4"><span class="px-2 py-0.5 bg-gold/10 text-gold rounded text-[10px] font-bold uppercase">${p.status}</span></td>
                <td class="px-6 py-4 text-xs font-semibold text-gray-600">${p.total_units || 0} Ünite</td>
                <td class="px-6 py-4 text-right">
                    <button class="text-navy hover:text-gold transition-colors p-2"><i class="fa-solid fa-circle-info"></i></button>
                </td>`;
            tableBody.appendChild(tr);
        });
    } catch (e) { tableBody.innerHTML = '<tr><td colspan="5" class="py-20 text-center text-red-400">Veriler yüklenirken bir hata oluştu.</td></tr>'; }
}

async function fetchCmsPosts() {
    const tableBody = document.getElementById('cms-table-body');
    if (!tableBody) return;
    tableBody.innerHTML = '<tr><td colspan="5" class="py-20 text-center animate-pulse">Haberler taranıyor...</td></tr>';
    try {
        const res = await apiFetch(`${API_BASE}/cms/posts`);
        const posts = await res.json();
        tableBody.innerHTML = posts.length ? '' : '<tr><td colspan="5" class="py-20 text-center text-gray-400 font-serif italic">Henüz yayınlanmış bir haber bulunmuyor.</td></tr>';
        posts.forEach(p => {
            const tr = document.createElement('tr');
            tr.className = "hover:bg-gray-50 transition-colors group";
            tr.innerHTML = `
                <td class="px-6 py-4 font-mono text-[10px] text-gray-400">#${p.id}</td>
                <td class="px-6 py-4 font-bold text-navy">${p.title}</td>
                <td class="px-6 py-4 text-xs text-gray-500">${p.author || 'Editör'}</td>
                <td class="px-6 py-4"><span class="px-2 py-0.5 bg-modern/10 text-modern rounded text-[10px] font-bold uppercase">${p.category}</span></td>
                <td class="px-6 py-4 text-right">
                    <button onclick="deleteCmsPost(${p.id})" class="text-red-400 hover:text-red-600 transition-all p-2 group-hover:scale-110">
                        <i class="fa-solid fa-trash-can"></i>
                    </button>
                </td>`;
            tableBody.appendChild(tr);
        });
    } catch (e) { tableBody.innerHTML = '<tr><td colspan="5" class="py-20 text-center text-red-400">Haberler alınamadı.</td></tr>'; }
}

async function fetchMediaVault() {
    const tableBody = document.getElementById('media-vault-table-body');
    if (!tableBody) return;
    tableBody.innerHTML = '<tr><td colspan="4" class="py-20 text-center animate-pulse">Dosyalar listeleniyor...</td></tr>';
    try {
        const res = await apiFetch(`${API_BASE}/media/vault`);
        const files = await res.json();
        tableBody.innerHTML = files.length ? '' : '<tr><td colspan="4" class="py-20 text-center text-gray-400 font-serif italic">Medya merkezi henüz boş.</td></tr>';
        files.forEach(f => {
            const icon = f.type === 'xlsx' || f.type === 'xls' ? 'fa-file-excel text-green-600' : (f.type === 'pdf' ? 'fa-file-pdf text-red-500' : 'fa-file-word text-blue-600');
            const tr = document.createElement('tr');
            tr.className = "hover:bg-gray-50 transition-colors group";
            tr.innerHTML = `
                <td class="px-6 py-4 text-center"><i class="fa-solid ${icon} text-lg"></i></td>
                <td class="px-6 py-4 font-bold text-navy">${f.name}</td>
                <td class="px-6 py-4 text-[10px] font-black text-gray-400 uppercase tracking-widest">${f.type.toUpperCase()}</td>
                <td class="px-6 py-4 text-right">
                    <a href="${f.url}" target="_blank" class="text-navy hover:text-gold transition-colors p-2"><i class="fa-solid fa-download"></i></a>
                    <button onclick="deleteMediaArchiveItem('${f.name}')" class="text-red-400 hover:text-red-600 transition-all p-2 ml-2 group-hover:scale-110">
                        <i class="fa-solid fa-trash-can"></i>
                    </button>
                </td>`;
            tableBody.appendChild(tr);
        });
    } catch (e) { tableBody.innerHTML = '<tr><td colspan="4" class="py-20 text-center text-red-400">Dosyalar listelenirken hata oluştu.</td></tr>'; }
}

async function fetchNotices() {
    const container = document.getElementById('notices-container');
    if (!container) return;
    container.innerHTML = '<div class="p-10 text-center animate-pulse">Duyurular alınıyor...</div>';
    try {
        const res = await apiFetch(`${API_BASE}/notices`);
        const notices = await res.json();
        container.innerHTML = notices.length ? '' : '<div class="p-20 text-center text-gray-400">Yeni duyuru bulunmuyor.</div>';
        notices.forEach(n => {
            const div = document.createElement('div');
            div.className = "p-4 border-b border-gray-100 flex gap-4 hover:bg-gray-50 transition-colors";
            div.innerHTML = `<div class="w-10 h-10 rounded-full bg-navy/10 flex items-center justify-center text-navy shrink-0"><i class="fa-solid fa-bullhorn"></i></div>
                             <div><h4 class="font-bold text-navy">${n.title}</h4><p class="text-sm text-gray-500">${n.message}</p>
                             <span class="text-xs text-gray-300">${n.created_at.split('T')[0]}</span></div>`;
            container.appendChild(div);
        });
    } catch (e) { container.innerHTML = '<div class="p-10 text-center text-red-400">Hata oluştu.</div>'; }
}

// --- DELETION HARDENING HANDLERS ---

async function deleteCmsPost(postId) {
    if (!confirm('Bu haberi silmek istediğinize emin misiniz? Bu işlem geri alınamaz.')) return;
    
    try {
        const response = await apiFetch(`${API_BASE}/cms/posts/${postId}`, { method: 'DELETE' });
        if (response.ok) {
            showToast('Haber başarıyla silindi.', 'success');
            fetchCmsPosts(); // Refresh list
        } else {
            const data = await response.json().catch(() => ({}));
            showToast('Hata: ' + (data.error || 'Silme işlemi başarısız.'), 'error');
        }
    } catch (err) {
        console.error('Delete CMS error:', err);
        showToast('Sunucu hatası oluştu.', 'error');
    }
}

async function deleteHeroSlide(slideId) {
    if (!confirm('Bu vitrin slaytını silmek istediğinize emin misiniz?')) return;
    
    try {
        const response = await apiFetch(`${API_BASE}/hero/${slideId}`, { method: 'DELETE' });
        if (response.ok) {
            showToast('Slayt başarıyla silindi.', 'success');
            fetchHeroSlides(); // Refresh list
        } else {
            const data = await response.json().catch(() => ({}));
            showToast('Hata: ' + (data.error || 'Silme işlemi başarısız.'), 'error');
        }
    } catch (err) {
        console.error('Delete Hero error:', err);
        showToast('Sunucu hatası oluştu.', 'error');
    }
}

async function deleteMediaArchiveItem(mediaName) {
    if (!confirm('Bu medyayı arşivden silmek istediğinize emin misiniz?')) return;
    
    // Media vault deletion (placeholder backend support usually needed)
    // Here we use the name as identifier for the vault delete
    try {
        const response = await apiFetch(`${API_BASE}/media/vault/${mediaName}`, { method: 'DELETE' });
        if (response.ok) {
            showToast('Medya başarıyla silindi.', 'success');
            fetchMediaVault();
        } else {
            const data = await response.json().catch(() => ({}));
            showToast('Hata: ' + (data.error || 'Silme işlemi başarısız.'), 'error');
        }
    } catch (err) {
        console.error('Delete Media error:', err);
        showToast('Sunucu hatası oluştu.', 'error');
    }
}

// Export to window for global access
window.deleteCmsPost = deleteCmsPost;
window.deleteHeroSlide = deleteHeroSlide;
window.deleteMediaArchiveItem = deleteMediaArchiveItem;
