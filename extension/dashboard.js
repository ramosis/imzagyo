/**
 * Evrensel ROI Asistanı - Dashboard Mantığı
 */

document.addEventListener('DOMContentLoaded', loadListings);

async function loadListings() {
    const { my_listings = [] } = await chrome.storage.local.get('my_listings');
    const tbody = document.getElementById('tableBody');
    tbody.innerHTML = '';

    my_listings.forEach((item, index) => {
        const tr = document.createElement('tr');
        
        // Fiyat temizleme ve ROI hesaplama (Görsel amaçlı tekrar)
        const priceNum = parseFloat(item.price.toString().replace(/\./g, '').replace(/[^\d]/g, '')) || 0;
        const rentNum = parseFloat(item.estimated_rent) || 0;
        const roi = priceNum > 0 && rentNum > 0 ? (rentNum * 12 / priceNum * 100).toFixed(2) : 0;
        const m2Price = item.m2 > 0 ? (priceNum / item.m2).toLocaleString('tr-TR') : '0';

        tr.innerHTML = `
            <td><div style="font-size: 11px; color: #94a3b8;">${item.saved_at}</div></td>
            <td>
                <div style="font-weight: bold;">${item.title}</div>
                <div style="font-size: 12px; color: #94a3b8;">${item.city} / ${item.district} / ${item.neighborhood}</div>
            </td>
            <td><div style="font-weight: bold; color: #f59e0b;">${item.price}</div></td>
            <td>
                <div>${item.m2} m² (${item.rooms})</div>
                <div style="font-size: 11px; color: #94a3b8;">${m2Price} ₺/m²</div>
            </td>
            <td><div style="font-weight: bold; color: #10b981;">${rentNum.toLocaleString('tr-TR')} ₺</div></td>
            <td><span class="roi-tag">%${roi}</span></td>
            <td>
                <a href="${item.url}" target="_blank" class="link-btn">İlana Git</a>
                <button class="delete-btn" data-index="${index}">Sil</button>
            </td>
        `;
        tbody.appendChild(tr);
    });

    // Silme butonlarını bağla
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', deleteListing);
    });
}

async function deleteListing(e) {
    const index = e.target.getAttribute('data-index');
    const { my_listings = [] } = await chrome.storage.local.get('my_listings');
    
    my_listings.splice(index, 1);
    await chrome.storage.local.set({ my_listings });
    
    loadListings(); // Listeyi yenile
}
