/**
 * Evrensel ROI Asistanı - Dashboard Mantığı
 */

document.addEventListener('DOMContentLoaded', async () => {
    const { user_lang = 'tr' } = await chrome.storage.local.get('user_lang');
    applyLanguage(user_lang);
    loadListings();

    // Export Butonları
    document.getElementById('exportExcelBtn').addEventListener('click', exportToExcel);
    document.getElementById('exportGoogleBtn').addEventListener('click', exportToExcel); // Google için de Excel en iyi format

    // Filtreleme
    document.getElementById('filterType').addEventListener('change', loadListings);
    document.getElementById('filterCategory').addEventListener('change', loadListings);
    document.getElementById('filterSearch').addEventListener('input', loadListings);
    document.getElementById('clearFilters').addEventListener('click', () => {
        document.getElementById('filterType').value = '';
        document.getElementById('filterCategory').value = '';
        document.getElementById('filterSearch').value = '';
        loadListings();
    });
});

function applyLanguage(lang) {
    document.querySelectorAll('[id^="msg-"]').forEach(el => {
        const key = el.id.replace('msg-', '').replace(/[0-9]/g, ''); // all2 gibi durumlar için
        const message = chrome.i18n.getMessage(key);
        if (message) el.innerText = message;
    });

    document.getElementById('exportExcelBtn').innerText = chrome.i18n.getMessage('exportExcel');
    document.getElementById('exportGoogleBtn').innerText = chrome.i18n.getMessage('exportGoogle');
    document.getElementById('clearFilters').innerText = chrome.i18n.getMessage('clearFilters');
    document.getElementById('filterSearch').placeholder = chrome.i18n.getMessage('search') + '...';

    if (lang === 'ar') document.body.style.direction = 'rtl';
}

async function loadListings() {
    const { my_listings = [] } = await chrome.storage.local.get('my_listings');
    const tbody = document.getElementById('tableBody');
    tbody.innerHTML = '';

    const typeFilter = document.getElementById('filterType').value;
    const catFilter = document.getElementById('filterCategory').value;
    const searchFilter = document.getElementById('filterSearch').value.toLowerCase();

    const filtered = my_listings.filter(item => {
        const matchesType = !typeFilter || item.listing_type === typeFilter;
        const matchesCat = !catFilter || item.category === catFilter;
        const matchesSearch = !searchFilter || 
            item.title.toLowerCase().includes(searchFilter) || 
            (item.city && item.city.toLowerCase().includes(searchFilter)) ||
            (item.district && item.district.toLowerCase().includes(searchFilter));
        return matchesType && matchesCat && matchesSearch;
    });

    filtered.forEach((item, index) => {
        const tr = document.createElement('tr');
        
        const priceNum = parseFloat(item.price.toString().replace(/\./g, '').replace(/[^\d]/g, '')) || 0;
        const rentNum = parseFloat(item.estimated_rent) || 0;
        const roi = priceNum > 0 && rentNum > 0 ? (rentNum * 12 / priceNum * 100).toFixed(2) : 0;
        
        const location = `${item.city || ''} / ${item.district || ''} / ${item.neighborhood || ''}`;

        tr.innerHTML = `
            <td><div style="font-size: 11px; color: #94a3b8;">${item.saved_at}</div></td>
            <td>
                <div style="font-weight: bold;">${item.listing_type}</div>
                <div style="font-size: 12px; color: #94a3b8;">${item.category}</div>
            </td>
            <td>
                <div style="font-weight: bold;">${item.title}</div>
                <div style="font-size: 12px; color: #94a3b8;">${location}</div>
            </td>
            <td><div style="font-weight: bold; color: #f59e0b;">${item.price} ₺</div></td>
            <td>
                <div>${item.m2_brut || 0} / ${item.m2_net || 0} m²</div>
                <div style="font-size: 11px; color: #94a3b8;">${item.rooms || '-'}</div>
            </td>
            <td><div style="font-weight: bold; color: #10b981;">${rentNum.toLocaleString('tr-TR')} ₺</div></td>
            <td><span class="roi-tag">%${roi}</span></td>
            <td>
                <a href="${item.url}" target="_blank" class="link-btn">${chrome.i18n.getMessage('goToListing')}</a>
                <button class="delete-btn" data-index="${index}">${chrome.i18n.getMessage('delete')}</button>
            </td>
        `;
        tbody.appendChild(tr);
    });

    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', deleteListing);
    });
}

async function deleteListing(e) {
    const index = e.target.getAttribute('data-index');
    const { my_listings = [] } = await chrome.storage.local.get('my_listings');
    my_listings.splice(index, 1);
    await chrome.storage.local.set({ my_listings });
    loadListings();
}

async function exportToExcel() {
    const { my_listings = [] } = await chrome.storage.local.get('my_listings');
    if (my_listings.length === 0) return alert('Aktarılacak veri bulunamadı.');

    const wb = XLSX.utils.book_new();

    // Kategorilere göre grupla
    const categories = [...new Set(my_listings.map(i => i.category))];

    categories.forEach(cat => {
        const catData = my_listings.filter(i => i.category === cat).map(item => {
            const priceNum = parseFloat(item.price.toString().replace(/\./g, '').replace(/[^\d]/g, '')) || 0;
            const rentNum = parseFloat(item.estimated_rent) || 0;
            const roi = priceNum > 0 && rentNum > 0 ? (rentNum * 12 / priceNum * 100) : 0;

            const row = {
                "Tarih": item.saved_at,
                "İşlem Tipi": item.listing_type,
                "İlan Başlığı": item.title,
                "Şehir": item.city,
                "İlçe": item.district,
                "Mahalle": item.neighborhood,
                "Fiyat (₺)": priceNum,
                "Brüt m2": item.m2_brut,
                "Net m2": item.m2_net,
                "Oda": item.rooms,
                "Tahmini Kira (₺)": rentNum,
                "ROI (%)": roi.toFixed(2),
                "İlan Linki": item.url
            };

            // Kategori bazlı ek sütunlar
            if (cat === 'Arsa') {
                row["Emsal"] = item.emsal;
                row["Kat Sayısı"] = item.kat_sayisi;
            } else if (cat === 'Tarla') {
                row["İmara Yakın"] = item.imara_yakin ? "Evet" : "Hayır";
                row["GES'e Uygun"] = item.gese_uygun ? "Evet" : "Hayır";
            }

            return row;
        });

        const ws = XLSX.utils.json_to_sheet(catData);
        XLSX.utils.book_append_sheet(wb, ws, cat || "Diğer");
    });

    XLSX.writeFile(wb, "Imza_Gayrimenkul_ROI_Analiz.xlsx");
}
