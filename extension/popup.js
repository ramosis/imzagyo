/**
 * Evrensel ROI Asistanı - Popup Mantığı
 */

let currentData = {
    category: 'Konut',
    listing_type: 'Satılık'
};

const API_BASE = "https://imzagayrimenkul.com";

document.addEventListener('DOMContentLoaded', async () => {
    // Dil ayarını yükle ve uygula
    const { user_lang = 'tr' } = await chrome.storage.local.get('user_lang');
    const langSelect = document.getElementById('langSelect');
    if (langSelect) langSelect.value = user_lang;
    applyLanguage(user_lang);

    const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    
    // Content script'ten veri iste
    chrome.tabs.sendMessage(tab.id, { action: "GET_LISTING_DATA" }, (response) => {
        if (chrome.runtime.lastError) {
            console.error("Mesaj gönderme hatası:", chrome.runtime.lastError.message);
            document.getElementById('listingTitle').value = "İletişim hatası. Sayfa script'i aktif mi?";
            updateUI(currentData); 
            return;
        }
        
        if (response) {
            Object.assign(currentData, response);
            updateUI(currentData);
        } else {
            document.getElementById('listingTitle').value = "Veri okunamadı. Sayfayı yenileyin.";
            updateUI(currentData);
        }
    });

    // Olay Dinleyicileri
    document.getElementById('rentInput').addEventListener('input', (e) => calculateROI(e.target.value));
    document.getElementById('addToListBtn').addEventListener('click', saveToLocal);
    document.getElementById('syncToPortalBtn').addEventListener('click', syncToPortal);
    document.getElementById('openDashboardBtn').addEventListener('click', () => chrome.tabs.create({ url: 'dashboard.html' }));
    
    // Auth Olayları
    document.getElementById('loginBtn').addEventListener('click', handleLogin);
    document.getElementById('logoutBtn').addEventListener('click', handleLogout);

    // İlk Auth Kontrolü
    checkAuth();

    // Buton Grubu Dinleyicileri
    document.getElementById('ilan-tipi-group').addEventListener('click', (e) => {
        if (e.target.matches('.option-button')) {
            const value = e.target.dataset.value;
            handleCategoryChange(value);
        }
    });

    document.getElementById('islem-tipi-group').addEventListener('click', (e) => {
        if (e.target.matches('.option-button')) {
            const value = e.target.dataset.value;
            handleListingTypeChange(value);
        }
    });

    // Tab Mantığı
    document.getElementById('tab-portal').addEventListener('click', () => switchTab('portal'));
    document.getElementById('tab-research').addEventListener('click', () => {
        switchTab('research');
        loadSavedParcels();
    });

    document.getElementById('langSelect').addEventListener('change', async (e) => {
        const lang = e.target.value;
        await chrome.storage.local.set({ user_lang: lang });
        location.reload();
    });
});

function applyLanguage(lang) {
    document.querySelectorAll('[id^="msg-"]').forEach(el => {
        const key = el.id.replace('msg-', '');
        const message = chrome.i18n.getMessage(key);
        if (message) el.innerText = message;
    });

    document.getElementById('addToListBtn').innerText = chrome.i18n.getMessage('addToList') || "Listeye Ekle";
    document.getElementById('openDashboardBtn').innerText = chrome.i18n.getMessage('openDashboard') || "Paneli Aç";
    
    if (document.getElementById('rentInput')) {
        document.getElementById('rentInput').placeholder = (chrome.i18n.getMessage('monthlyRent') || "Aylık Kira").replace(' (₺)', '');
    }
    
    document.body.style.direction = (lang === 'ar') ? 'rtl' : 'ltr';
}

function handleCategoryChange(value) {
    currentData.category = value;
    updateButtonGroup('ilan-tipi-group', value);

    const m2Fields = document.getElementById('m2-fields');
    const arsaFields = document.getElementById('arsa-fields');
    const tarlaFields = document.getElementById('tarla-fields');

    if (m2Fields) m2Fields.classList.add('hidden');
    if (arsaFields) arsaFields.classList.add('hidden');
    if (tarlaFields) tarlaFields.classList.add('hidden');

    switch(value) {
        case 'Konut':
        case 'Dükkan':
            if (m2Fields) m2Fields.classList.remove('hidden');
            break;
        case 'Arsa':
            if (arsaFields) arsaFields.classList.remove('hidden');
            break;
        case 'Tarla':
            if (tarlaFields) tarlaFields.classList.remove('hidden');
            break;
    }
}

function handleListingTypeChange(value) {
    currentData.listing_type = value;
    updateButtonGroup('islem-tipi-group', value);
    calculateROI(document.getElementById('rentInput').value);
}

function updateButtonGroup(groupId, activeValue) {
    const group = document.getElementById(groupId);
    if (!group) return;
    group.querySelectorAll('.option-button').forEach(btn => {
        btn.classList.remove('active');
        if (btn.dataset.value === activeValue) {
            btn.classList.add('active');
        }
    });
}

function updateUI(data) {
    handleCategoryChange(data.category || 'Konut');
    handleListingTypeChange(data.listing_type || 'Satılık');
    
    document.getElementById('listingTitle').value = data.title || '';
    document.getElementById('listingPrice').value = data.price || '0';
    document.getElementById('listingM2Brut').value = data.m2_brut || 0;
    document.getElementById('listingM2Net').value = data.m2_net || 0;
    document.getElementById('listingRooms').value = data.rooms || '0+0';
}

function calculateROI(monthlyRent) {
    if (currentData.listing_type !== 'Satılık') {
        document.getElementById('roiValue').innerText = "N/A";
        document.getElementById('amortizationYears').innerText = "-";
        document.getElementById('resultArea').style.display = "block";
        return;
    }

    const priceRaw = document.getElementById('listingPrice').value;
    const priceNumeric = parseFloat(priceRaw.toString().replace(/\./g, '').replace(/[^\d]/g, ''));
    const rentNumeric = parseFloat(monthlyRent);

    if (priceNumeric > 0 && rentNumeric > 0) {
        const annualRent = rentNumeric * 12;
        const roi = (annualRent / priceNumeric) * 100;
        const amortization = priceNumeric / annualRent;

        document.getElementById('roiValue').innerText = `%${roi.toFixed(2)}`;
        document.getElementById('amortizationYears').innerText = amortization.toFixed(1);
        document.getElementById('resultArea').style.display = "block";
    }
}

async function checkAuth() {
    const { token, username } = await chrome.storage.local.get(['token', 'username']);
    const loginSection = document.getElementById('loginSection');
    const mainSection = document.getElementById('mainSection');
    const userBadge = document.getElementById('userBadge');

    if (token) {
        if (loginSection) loginSection.classList.add('hidden');
        if (mainSection) mainSection.classList.remove('hidden');
        if (userBadge) userBadge.innerText = `👤 ${username}`;
    } else {
        // AUTO-LOGIN ATTEMPT for the User (admin/admin123)
        const { autoLoginTried = false } = await chrome.storage.local.get('autoLoginTried');
        if (!autoLoginTried) {
            console.log("İlk açılış: Otomatik giriş deneniyor...");
            await chrome.storage.local.set({ autoLoginTried: true });
            await handleLogin("admin", "admin123");
            return;
        }
        if (loginSection) loginSection.classList.remove('hidden');
        if (mainSection) mainSection.classList.add('hidden');
    }
}

async function handleLogin(manualUser, manualPass) {
    const userInput = manualUser || document.getElementById('username').value;
    const passInput = manualPass || document.getElementById('password').value;
    const errorDiv = document.getElementById('loginError');

    if (!userInput || !passInput) {
        if (errorDiv) errorDiv.innerText = "Lütfen alanları doldurun.";
        return;
    }

    if (errorDiv) errorDiv.innerText = "Giriş yapılıyor...";

    try {
        const response = await fetch(`${API_BASE}/api/v1/auth/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: userInput, password: passInput })
        });

        const data = await response.json();

        if (response.ok && data.access_token) {
            await chrome.storage.local.set({ 
                token: data.access_token, 
                username: data.user.username,
                is_admin: data.user.is_admin
            });
            if (errorDiv) errorDiv.innerText = "";
            checkAuth();
        } else {
            if (errorDiv) errorDiv.innerText = data.error || "Giriş başarısız.";
        }
    } catch (e) {
        if (errorDiv) errorDiv.innerText = "Sunucuya bağlanılamadı.";
        console.error(e);
    }
}

async function handleLogout() {
    await chrome.storage.local.remove(['token', 'username', 'is_admin']);
    checkAuth();
}

async function syncToPortal() {
    const { token } = await chrome.storage.local.get('token');
    if (!token) {
        alert("Lütfen önce giriş yapın.");
        return;
    }

    const btn = document.getElementById('syncToPortalBtn');
    const originalText = btn.innerText;
    btn.innerText = "⏳ Gönderiliyor...";
    btn.disabled = true;

    const portfolioData = {
        title: document.getElementById('listingTitle').value,
        price: parseFloat(document.getElementById('listingPrice').value.toString().replace(/\./g, '').replace(/[^\d]/g, '')) || 0,
        m2_brut: parseInt(document.getElementById('listingM2Brut').value) || 0,
        m2_net: parseInt(document.getElementById('listingM2Net').value) || 0,
        rooms: document.getElementById('listingRooms').value,
        category: currentData.category,
        listing_type: currentData.listing_type,
        city: currentData.city,
        district: currentData.district,
        neighborhood: currentData.neighborhood,
        external_url: currentData.url,
        estimated_rent: parseFloat(document.getElementById('rentInput').value) || 0
    };

    try {
        const response = await fetch(`${API_BASE}/api/v1/portfolios`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify(portfolioData)
        });

        if (response.ok) {
            btn.innerText = "✅ Portala Eklendi!";
            btn.style.background = "#059669";
            setTimeout(() => {
                btn.innerText = originalText;
                btn.style.background = "#10b981";
                btn.disabled = false;
            }, 3000);
        } else {
            const err = await response.json();
            alert(`Hata: ${err.error || 'Gönderilemedi'}`);
            btn.innerText = originalText;
            btn.disabled = false;
        }
    } catch (e) {
        alert("Sunucu hatası: " + e.message);
        btn.innerText = originalText;
        btn.disabled = false;
    }
}

async function saveToLocal() {
    if (!currentData) return;

    const itemToSave = {
        title: document.getElementById('listingTitle').value,
        price: document.getElementById('listingPrice').value,
        rooms: document.getElementById('listingRooms').value,
        m2_brut: document.getElementById('listingM2Brut').value,
        m2_net: document.getElementById('listingM2Net').value,
        listing_type: currentData.listing_type,
        category: currentData.category,
        estimated_rent: document.getElementById('rentInput').value,
        url: currentData.url,
        city: currentData.city,
        district: currentData.district,
        neighborhood: currentData.neighborhood,
        saved_at: new Date().toLocaleString()
    };
    
    if(currentData.category === 'Arsa'){
        itemToSave.emsal = document.getElementById('listingEmsal').value;
        itemToSave.kat_sayisi = document.getElementById('listingKatSayisi').value;
    }
    if(currentData.category === 'Tarla'){
        itemToSave.imara_yakin = document.getElementById('checkImaraYakin').checked;
        itemToSave.gese_uygun = document.getElementById('checkGeseUygun').checked;
    }

    const { my_listings = [] } = await chrome.storage.local.get('my_listings');
    my_listings.push(itemToSave);
    await chrome.storage.local.set({ my_listings });
    
    const btn = document.getElementById('addToListBtn');
    btn.innerText = "✅ Eklendi";
    btn.style.background = "#10b981";
    setTimeout(() => {
        btn.innerText = "🌟 Karşılaştırma Listeme Ekle";
        btn.style.background = "#f59e0b";
    }, 2000);
}

function switchTab(tab) {
    const portalBtn = document.getElementById('tab-portal');
    const researchBtn = document.getElementById('tab-research');
    const portalView = document.getElementById('view-portal');
    const researchView = document.getElementById('view-research');

    if (tab === 'portal') {
        portalBtn.classList.add('active');
        researchBtn.classList.remove('active');
        portalView.classList.remove('hidden');
        researchView.classList.add('hidden');
    } else {
        portalBtn.classList.remove('active');
        researchBtn.classList.add('active');
        portalView.classList.add('hidden');
        researchView.classList.remove('hidden');
    }
}

async function loadSavedParcels() {
    const { savedParcels = [] } = await chrome.storage.local.get('savedParcels');
    const list = document.getElementById('parcel-list');
    list.innerHTML = '';

    if (savedParcels.length === 0) {
        list.innerHTML = '<div style="text-align:center; padding:20px; color:#64748b; font-size:12px;">Henüz kaydedilmiş parsel yok.</div>';
        return;
    }

    savedParcels.reverse().forEach((p, index) => {
        const item = document.createElement('div');
        item.className = 'card';
        item.style.marginBottom = '8px';
        item.style.padding = '10px';
        item.innerHTML = `
            <div style="font-weight:bold; font-size:13px; color:var(--gold);">${p.province} / ${p.district}</div>
            <div style="font-size:11px; color:#94a3b8; margin:4px 0;">Ada: ${p.island} | Parsel: ${p.parcel}</div>
            <div style="font-size:10px; color:#64748b;">${p.neighborhood}</div>
            <div style="display:flex; gap:5px; margin-top:8px;">
                <button class="imza-hud-btn" style="padding:4px; font-size:10px;" onclick="window.openEimar('${p.province}','${p.district}')">E-İmar Sorgula</button>
                <button class="imza-hud-btn" style="padding:4px; font-size:10px; background:#334155; color:white;" onclick="window.deleteParcel(${savedParcels.length - 1 - index})">Sil</button>
            </div>
        `;
        list.appendChild(item);
    });
}

window.openEimar = (prov, dist) => {
    if (dist.toLowerCase().includes("kütahya") || prov.toLowerCase().includes("kütahya")) {
        chrome.runtime.sendMessage({ action: "OPEN_KUTAHYA_EIMAR" });
    } else {
        alert("Bu ilçe için otomatik E-İmar entegrasyonu henüz aktif değil. Lütfen belediye sitesini kontrol edin.");
    }
};

window.deleteParcel = async (index) => {
    const { savedParcels = [] } = await chrome.storage.local.get('savedParcels');
    savedParcels.splice(index, 1);
    await chrome.storage.local.set({ savedParcels });
    loadSavedParcels();
};
