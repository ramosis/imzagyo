// --- IMZA PORTAL CORE JS ---
// Extracted from portal.html for audit compliance and maintainability.

const API_BASE = '/api';

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
        'leads': typeof initLeadsModule !== 'undefined' ? initLeadsModule : null,
        'expenses': typeof fetchExpenses !== 'undefined' ? fetchExpenses : null,
        'portfolios': typeof fetchAllPortfolios !== 'undefined' ? fetchAllPortfolios : null,
        'global-sync': typeof renderVisibilityMatrix !== 'undefined' ? renderVisibilityMatrix : null,
        'campaigns': () => {
           const autoTab = document.getElementById('campaign-tab-content-automation');
           const isAutoActive = autoTab && !autoTab.classList.contains('hidden');
           const tempTab = document.getElementById('campaign-tab-content-templates');
           const isTempActive = tempTab && !tempTab.classList.contains('hidden');
           
           if (isAutoActive) fetchAutomationRules();
           else if (isTempActive) fetchTemplates();
           else fetchCampaigns();
        },
        'barter-wizard': typeof fetchBarterWizard !== 'undefined' ? fetchBarterWizard : null,
        'hero': typeof fetchHeroSlides !== 'undefined' ? fetchHeroSlides : null,
        'appointments': typeof fetchAppointments !== 'undefined' ? fetchAppointments : null,
        'taxes': typeof fetchTaxes !== 'undefined' ? fetchTaxes : null,
        'maintenance': typeof fetchMaintenance !== 'undefined' ? fetchMaintenance : null,
        'contracts': typeof fetchContracts !== 'undefined' ? fetchContracts : null,
        'contract-builder': typeof initContractBuilder !== 'undefined' ? initContractBuilder : null,
        'site-settings': typeof fetchSettings !== 'undefined' ? fetchSettings : null,
        'contacts': typeof fetchContacts !== 'undefined' ? fetchContacts : null,
        'integrations': typeof fetchIntegrations !== 'undefined' ? fetchIntegrations : null,
        'users': () => fetchUsers(),
        'payroll': typeof fetchPayroll !== 'undefined' ? fetchPayroll : null,
        'projects': typeof fetchProjects !== 'undefined' ? fetchProjects : null,
        'imza-lens': () => {
           const trafficTab = document.getElementById('lens-tab-content-traffic');
           const isTrafficActive = trafficTab && !trafficTab.classList.contains('hidden');
           if (isTrafficActive) fetchTrafficData();
           else fetchShadowListings();
        },
        'market-analytics': typeof updateAnalytics !== 'undefined' ? updateAnalytics : null
    };
    
    // Normalize ID: ensure the loader key is clean
    let loaderKey = targetId.endsWith('-section') ? targetId.replace('-section', '') : targetId;
    
    // Special case for merged sections
    if (loaderKey === 'shadow-listings' || loaderKey === 'traffic') {
        loaderKey = 'imza-lens';
    }
    if (loaders[loaderKey]) {
        console.log("[İmza Portal] Veri yükleniyor:", loaderKey);
        loaders[loaderKey]();
    } else {
        console.warn("[İmza Portal] Loader bulunamadı veya tanım yok:", loaderKey);
    }
}

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    if (sidebar) sidebar.classList.toggle('-translate-x-full');
}

const toggleBtn = document.getElementById('sidebar-toggle');
if (toggleBtn) {
    toggleBtn.addEventListener('click', toggleSidebar);
}

function logout() {
    document.getElementById('logout-confirm-modal').classList.remove('hidden');
}

function executeLogout() {
    localStorage.removeItem('imza_admin_token');
    localStorage.removeItem('imza_admin_role');
    window.location.reload();
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
    const role = localStorage.getItem('imza_admin_role');
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
        const response = await fetch(`${API_BASE}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('imza_admin_token', data.token);
            localStorage.setItem('imza_admin_role', data.role);
            localStorage.setItem('imza_admin_username', data.username || username);
            window.location.reload();
        } else {
            const errorData = await response.json().catch(() => ({}));
            errorDiv.classList.remove('hidden');
            errorDiv.querySelector('span').textContent = errorData.error || 'Giriş bilgileri hatalı.';
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
        const res = await apiFetch(`${API_BASE}/portfoyler`);
        const data = await res.json();
        const tableBody = document.getElementById('dashboard-portfolio-list');
        if (!tableBody) return;
        tableBody.innerHTML = '';
        data.slice(0, 3).forEach(item => {
            tableBody.innerHTML += `
                <tr class="border-b border-gray-50 last:border-0 hover:bg-gray-50 transition-colors">
                    <td class="py-3 px-4"><span class="bg-gray-100 text-gray-500 px-2 py-1 rounded text-xs font-mono font-bold">${item.refNo}</span></td>
                    <td class="py-3 px-4 font-medium text-navy">${item.baslik1}</td>
                    <td class="py-3 px-4 text-gray-500">${item.lokasyon}</td>
                    <td class="py-3 px-4 font-bold text-slate-700">${item.fiyat}</td>
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
        const res = await apiFetch(`${API_BASE}/portfoyler`);
        const data = await res.json();
        const container = document.getElementById('portfolio-grid');
        const tableBody = document.getElementById('portfolios-table-body');
        if (container) {
            container.innerHTML = '';
            data.forEach(p => {
                container.innerHTML += `<div class="bg-white rounded-2xl border border-gray-100 overflow-hidden hover:shadow-xl transition-all">
                    <div class="h-40 bg-cover bg-center" style="background-image: url('${p.resim_hero || 'https://via.placeholder.com/400x200'}')"></div>
                    <div class="p-4">
                        <h4 class="font-bold text-navy text-sm mb-1">${p.baslik1}</h4>
                        <p class="text-[10px] text-gray-400 mb-4 tracking-tighter uppercase"><i class="fa-solid fa-location-dot"></i> ${p.lokasyon}</p>
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
                    <td class="py-3 px-6"><div class="w-12 h-12 rounded bg-cover bg-center border border-gray-200" style="background-image: url('${item.resim_hero}')"></div></td>
                    <td class="py-3 px-6"><span class="bg-gray-100 text-gray-600 px-2 py-1 rounded text-xs font-mono font-bold">${item.refNo}</span></td>
                    <td class="py-3 px-6"><span class="text-xs font-bold uppercase tracking-wider ${item.ozellik_renk}">${item.koleksiyon}</span></td>
                    <td class="py-3 px-6 font-bold text-navy">${item.baslik1}</td>
                    <td class="py-3 px-6 font-bold text-slate-700">${item.fiyat}</td>
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
async function fetchLeads() {
    try {
        const res = await apiFetch(`${API_BASE}/leads`);
        const data = await res.json();
        const tbody = document.getElementById('leads-table-body');
        if (!tbody) return;
        tbody.innerHTML = data.length === 0 ? '<tr><td colspan="6" class="p-8 text-center text-gray-400">Yeni aday bulunmuyor.</td></tr>' : '';
        data.forEach(l => {
            const dateStr = l.created_at ? new Date(l.created_at).toLocaleString('tr-TR') : '-';
            const tr = document.createElement('tr');
            tr.className = 'border-b border-gray-50 hover:bg-gray-50';
            tr.innerHTML = `
                <td class="px-6 py-4">
                    <div class="font-bold text-navy">${l.name || 'İsimsiz'}</div>
                </td>
                <td class="px-6 py-4 text-xs">
                    <div>${l.phone || '-'}</div>
                    <div class="text-gray-400">${l.email || '-'}</div>
                </td>
                <td class="px-6 py-4">
                    <span class="px-2 py-1 rounded text-[10px] font-bold uppercase ${l.source === 'campaign' ? 'bg-gold/10 text-gold' : 'bg-gray-100 text-gray-500'}">
                        ${l.source || 'Genel'}
                    </span>
                </td>
                <td class="px-6 py-4 text-xs font-medium text-gray-500">
                    ${l.message || l.project_slug || '-'}
                </td>
                <td class="px-6 py-4 text-xs text-gray-400">${dateStr}</td>
                <td class="px-6 py-4 text-right">
                    <button onclick="openQuickWhatsApp(${l.id})" class="text-green-600 p-2"><i class="fa-brands fa-whatsapp"></i></button>
                    <button class="text-gray-400 p-2"><i class="fa-solid fa-ellipsis"></i></button>
                </td>`;
            tbody.appendChild(tr);
        });
    } catch (e) { console.error(e); }
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
            tr.innerHTML = `
                <td class="px-6 py-4 font-medium text-navy">#${a.id}</td>
                <td class="px-6 py-4 font-bold text-navy">${a.client_name || a.baslik1 || '-'}</td>
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
        const resP = await apiFetch(`${API_BASE}/portfoyler`);
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
                        <span class="text-[10px] font-black text-gray-300 uppercase tracking-widest">${t.type}</span>
                    </div>
                    <p class="text-gray-500 text-xs line-clamp-3 mb-6 font-medium italic">"${t.content}"</p>
                    <div class="flex justify-between items-center">
                        <span class="text-[9px] text-gray-400 font-bold uppercase tracking-tighter"><i class="fa-solid fa-clock mr-1"></i> ${new Date(t.created_at).toLocaleDateString()}</span>
                        <div class="flex gap-2">
                            <button class="text-gray-400 hover:text-navy transition-colors text-sm"><i class="fa-solid fa-pen"></i></button>
                            <button class="text-gray-400 hover:text-red-500 transition-colors text-sm"><i class="fa-solid fa-trash"></i></button>
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
                    <td class="px-6 py-4 font-mono text-xs text-gray-400">#${u.id}</td>
                    <td class="px-6 py-4 font-bold text-navy">${u.username}</td>
                    <td class="px-6 py-4"><span class="px-2 py-1 bg-gray-100 rounded text-[10px] font-bold text-gray-500 uppercase">${u.role}</span></td>
                    <td class="px-6 py-4 text-right flex gap-2 justify-end opacity-0 group-hover:opacity-100 transition-opacity">
                        ${trackingBtn}
                        <button onclick="editUser(${u.id})" class="w-8 h-8 rounded-lg bg-blue-50 text-blue-500 hover:bg-blue-600 hover:text-white transition-all flex items-center justify-center shadow-sm"><i class="fa-solid fa-pen text-xs"></i></button>
                        <button onclick="deleteUser(${u.id})" class="w-8 h-8 rounded-lg bg-red-50 text-red-500 hover:bg-red-600 hover:text-white transition-all flex items-center justify-center shadow-sm"><i class="fa-solid fa-trash text-xs"></i></button>
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

// --- LEADS VIEW & PIPELINE ---
let currentLeadsView = 'list';
function switchLeadsView(view) {
    currentLeadsView = view;
    const listBtn = document.getElementById('leads-list-btn');
    const pipeBtn = document.getElementById('leads-pipeline-btn');
    const listView = document.getElementById('leads-list-view');
    const pipeView = document.getElementById('leads-pipeline-view');
    if (view === 'list') {
        listBtn.classList.add('bg-white', 'text-navy', 'shadow-sm');
        pipeBtn.classList.remove('bg-white', 'text-navy', 'shadow-sm');
        listView.classList.remove('hidden');
        pipeView.classList.add('hidden');
        fetchLeads();
    } else {
        pipeBtn.classList.add('bg-white', 'text-navy', 'shadow-sm');
        listBtn.classList.remove('bg-white', 'text-navy', 'shadow-sm');
        listView.classList.add('hidden');
        pipeView.classList.remove('hidden');
        fetchPipeline();
    }
}

async function fetchPipeline() {
    const container = document.getElementById('pipeline-container');
    if (!container) return;
    try {
        const res = await apiFetch(`${API_BASE}/pipeline`);
        const stages = await res.json();
        container.innerHTML = '';
        stages.forEach(stage => {
            const column = document.createElement('div');
            column.className = 'kanban-column';
            column.dataset.id = stage.id;
            column.innerHTML = `<div class="kanban-header" style="border-bottom-color: ${stage.color}">
                <h3 class="kanban-title">${stage.name}</h3>
                <span class="kanban-count">${stage.leads.length}</span>
            </div>`;
            const list = document.createElement('div');
            list.className = 'kanban-list custom-scrollbar';
            list.dataset.stageId = stage.id;
            stage.leads.forEach(lead => {
                const item = document.createElement('div');
                item.className = 'kanban-item';
                item.dataset.id = lead.id;
                item.innerHTML = `<div class="kanban-item-title">${lead.name}</div>`;
                list.appendChild(item);
            });
            column.appendChild(list);
            container.appendChild(column);
            new Sortable(list, {
                group: 'leads-pipeline',
                onEnd: async (evt) => {
                    await apiFetch(`${API_BASE}/leads/${evt.item.dataset.id}/move`, {
                        method: 'PUT',
                        body: JSON.stringify({ stage_id: evt.to.dataset.stageId })
                    });
                }
            });
        });
    } catch (e) { console.error(e); }
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
        const res = await apiFetch(`${API_BASE}/portfoyler/${id}`, { method: 'DELETE' });
        if (res.ok) { showToast('Portföy silindi', 'success'); fetchAllPortfolios(); }
        else showToast('Silme hatası', 'error');
    } catch (e) { showToast('Bağlantı hatası', 'error'); }
}

async function editPortfolio(id) {
    openPortfolioModal();
    // Fetch data and fill form...
    try {
        const res = await apiFetch(`${API_BASE}/portfoyler/${id}`);
        const data = await res.json();
        // Populate form fields (This is a simplified version for restoration)
        document.getElementById('p-id').value = data.id;
        document.getElementById('p-baslik1').value = data.baslik1;
        document.getElementById('p-fiyat').value = data.fiyat;
        // ... populate more fields as needed
    } catch (e) { console.error(e); }
}

async function deleteUser(id) {
    if (!confirm('Kullanıcıyı silmek istediğinize emin misiniz?')) return;
    try {
        const res = await apiFetch(`${API_BASE}/users/${id}`, { method: 'DELETE' });
        if (res.ok) { showToast('Kullanıcı silindi', 'success'); fetchUsers(); }
    } catch (e) { console.error(e); }
}

async function deleteContact(id) {
    if (!confirm('Kişiyi silmek istediğinize emin misiniz?')) return;
    try {
        const res = await apiFetch(`${API_BASE}/contacts/${id}`, { method: 'DELETE' });
        if (res.ok) { showToast('Kişi silindi', 'success'); fetchContacts(); }
    } catch (e) { console.error(e); }
}

async function deleteAppointment(id) {
    if (!confirm('Randevuyu silmek istediğinize emin misiniz?')) return;
    try {
        const res = await apiFetch(`${API_BASE}/appointments/${id}`, { method: 'DELETE' });
        if (res.ok) { showToast('Randevu silindi', 'success'); fetchAppointments(); }
    } catch (e) { console.error(e); }
}

async function toggleRule(id) {
    try {
        const res = await apiFetch(`${API_BASE}/automation/rules/${id}/toggle`, { method: 'POST' });
        if (res.ok) fetchAutomationRules();
    } catch (e) { console.error(e); }
}

async function deleteRule(id) {
    if (!confirm('Kuralı silmek istediğinize emin misiniz?')) return;
    try {
        const res = await apiFetch(`${API_BASE}/automation/rules/${id}`, { method: 'DELETE' });
        if (res.ok) fetchAutomationRules();
    } catch (e) { console.error(e); }
}

async function runAutomationNow() {
    showToast('Otomasyon tetiklendi...', 'info');
    try {
        await apiFetch(`${API_BASE}/automation/run`, { method: 'POST' });
        showToast('Otomasyon tamamlandı', 'success');
    } catch (e) { showToast('Hata oluştu', 'error'); }
}

async function savePortfolio() {
    const id = document.getElementById('p-id')?.value;
    const payload = {
        baslik1: document.getElementById('p-baslik1')?.value,
        fiyat: document.getElementById('p-fiyat')?.value,
    };
    
    const method = id ? 'PUT' : 'POST';
    const url = id ? `${API_BASE}/portfoyler/${id}` : `${API_BASE}/portfoyler`;
    
    try {
        const res = await apiFetch(url, { method, body: JSON.stringify(payload) });
        if (res.ok) {
            showToast('Portföy kaydedildi', 'success');
            closePortfolioModal();
            fetchAllPortfolios();
        }
    } catch (e) { showToast('Kaydetme hatası', 'error'); }
}

async function triggerAiTranslation() {
    const id = document.getElementById('p-id')?.value;
    if (!id) {
        showToast('Lütfen önce portföyü kaydedin.', 'error');
        return;
    }
    showToast('AI Çeviri başlatıldı...', 'info');
    try {
        await apiFetch(`${API_BASE}/portfoyler/${id}/translate`, { method: 'POST' });
        showToast('Çeviriler tamamlandı', 'success');
    } catch (e) { showToast('Çeviri hatası', 'error'); }
}
