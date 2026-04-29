// --- PORTFOLIO (CRUD) ---
async function fetchAllPortfolios() {
    try {
        const base = typeof API_BASE !== 'undefined' ? API_BASE : '/api/v1';
        const res = typeof apiFetch !== 'undefined' ? await apiFetch(`${base}/portfolios`) : await fetch(`${base}/portfolios`);
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
    } catch (err) {
        console.error('Fetch Portfolios error:', err);
    }
}

async function fetchPortfoliosForDashboard() {
    try {
        const base = typeof API_BASE !== 'undefined' ? API_BASE : '/api/v1';
        const res = typeof apiFetch !== 'undefined' ? await apiFetch(`${base}/portfolios`) : await fetch(`${base}/portfolios`);
        const data = await res.json();
        
        const tableBody = document.getElementById('dashboard-portfolio-list');
        if (!tableBody) return; // Null Check
        
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
    } catch (err) {
        console.error('Dashboard Portfolios error:', err);
    }
}

async function editPortfolio(id) {
    if (typeof showToast === 'function') {
        showToast('Portföy düzenleme özelliği hazırlanıyor...', 'info');
    }
    console.log('Editing portfolio:', id);
    // Modal açma vs eklenebilir
}

async function deletePortfolio(id) {
    if (!confirm('Bu portföyü silmek istediğinize emin misiniz?')) return;
    try {
        const base = typeof API_BASE !== 'undefined' ? API_BASE : '/api/v1';
        const res = typeof apiFetch !== 'undefined' ? await apiFetch(`${base}/portfolios/${id}`, { method: 'DELETE' }) : await fetch(`${base}/portfolios/${id}`, { method: 'DELETE' });
        
        if (res.ok) {
            if (typeof showToast === 'function') showToast('Portföy başarıyla silindi', 'success');
            fetchAllPortfolios();
            fetchPortfoliosForDashboard();
        } else {
            if (typeof showToast === 'function') showToast('Portföy silinemedi', 'error');
        }
    } catch (e) {
        console.error('Delete Portfolio error:', e);
    }
}