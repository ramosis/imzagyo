import { apiFetch } from '../core/api.js';
import { showToast, toggleLoading } from '../core/ui.js';

export async function fetchPortfolios() {
    const container = document.getElementById('portfolio-grid');
    const tableBody = document.getElementById('portfolios-table-body');
    
    try {
        if (container) container.innerHTML = '<div class="col-span-full text-center py-12"><i class="fa-solid fa-spinner fa-spin text-3xl text-gold"></i></div>';
        
        const res = await apiFetch('portfolios');
        if (!res.ok) throw new Error('Portföyler yüklenemedi');
        
        const data = await res.json();
        renderPortfolios(data);
    } catch (err) {
        console.error('[Portfolio] Hata:', err);
        showToast('Portföyler yüklenirken bir hata oluştu', 'error');
    }
}

export function renderPortfolios(data) {
    const container = document.getElementById('portfolio-grid');
    const tableBody = document.getElementById('portfolios-table-body');

    if (container) {
        container.innerHTML = data.length === 0 ? '<div class="col-span-full text-center py-12 text-gray-400">Henüz portföy bulunmuyor.</div>' : '';
        data.forEach(p => {
            container.innerHTML += `
                <div class="bg-white rounded-2xl border border-gray-100 overflow-hidden hover:shadow-xl transition-all group">
                    <div class="h-48 bg-cover bg-center relative" style="background-image: url('${p.image_hero || '/static/img/placeholder.jpg'}')">
                        <div class="absolute top-4 right-4 bg-navy/80 backdrop-blur-md text-white px-3 py-1 rounded-full text-[10px] font-bold uppercase tracking-widest border border-white/10">
                            ${p.ref_no}
                        </div>
                    </div>
                    <div class="p-5">
                        <div class="flex justify-between items-start mb-2">
                            <h4 class="font-bold text-navy text-sm leading-tight group-hover:text-gold transition-colors truncate w-full" title="${p.title}">${p.title}</h4>
                        </div>
                        <p class="text-[10px] text-gray-400 mb-4 flex items-center gap-1 uppercase tracking-wider">
                            <i class="fa-solid fa-location-dot text-gold/60"></i> ${p.location}
                        </p>
                        <div class="flex justify-between items-center pt-4 border-t border-gray-50">
                            <span class="text-gold font-bold text-base">${p.price}</span>
                            <button class="edit-portfolio-btn text-xs font-bold text-navy hover:text-gold transition-colors" data-id="${p.id}">
                                İNCELE <i class="fa-solid fa-arrow-right ml-1"></i>
                            </button>
                        </div>
                    </div>
                </div>`;
        });
    }

    if (tableBody) {
        tableBody.innerHTML = data.length === 0 ? '<tr><td colspan="6" class="text-center py-8 text-gray-400">Sonuç bulunamadı.</td></tr>' : '';
        data.forEach(item => {
            tableBody.innerHTML += `
                <tr class="border-b border-gray-100 hover:bg-gray-50/50 transition-colors group">
                    <td class="py-4 px-6">
                        <div class="w-14 h-14 rounded-xl bg-cover bg-center border border-gray-100 shadow-sm" style="background-image: url('${item.image_hero || '/static/img/placeholder.jpg'}')"></div>
                    </td>
                    <td class="py-4 px-6">
                        <span class="bg-gray-100 text-gray-600 px-3 py-1 rounded-lg text-[10px] font-mono font-bold border border-gray-200">
                            ${item.ref_no}
                        </span>
                    </td>
                    <td class="py-4 px-6">
                        <span class="text-[10px] font-black uppercase tracking-widest px-2 py-1 rounded-md bg-gold/10 text-gold">
                            ${item.koleksiyon || 'GENEL'}
                        </span>
                    </td>
                    <td class="py-4 px-6 font-bold text-navy text-sm max-w-[250px] truncate" title="${item.title}">
                        ${item.title}
                    </td>
                    <td class="py-4 px-6 font-bold text-slate-700 text-sm">
                        ${item.price}
                    </td>
                    <td class="py-4 px-6 text-right">
                        <div class="flex gap-2 justify-end opacity-0 group-hover:opacity-100 transition-opacity">
                            <button class="media-portfolio-btn w-9 h-9 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center hover:bg-emerald-600 hover:text-white transition-all shadow-sm" data-id="${item.id}" title="Medya">
                                <i class="fa-solid fa-camera"></i>
                            </button>
                            <button class="edit-portfolio-btn w-9 h-9 rounded-xl bg-blue-50 text-blue-600 flex items-center justify-center hover:bg-blue-600 hover:text-white transition-all shadow-sm" data-id="${item.id}" title="Düzenle">
                                <i class="fa-solid fa-pen"></i>
                            </button>
                            <button class="delete-portfolio-btn w-9 h-9 rounded-xl bg-red-50 text-red-600 flex items-center justify-center hover:bg-red-600 hover:text-white transition-all shadow-sm" data-id="${item.id}" title="Sil">
                                <i class="fa-solid fa-trash-can"></i>
                            </button>
                        </div>
                    </td>
                </tr>`;
        });
    }
}

export function initPortfolioEvents() {
    console.log("[Portfolio] Event listener'lar kuruluyor...");
    
    // Global event delegation for portfolio buttons
    document.addEventListener('click', (e) => {
        const editBtn = e.target.closest('.edit-portfolio-btn');
        const deleteBtn = e.target.closest('.delete-portfolio-btn');
        const mediaBtn = e.target.closest('.media-portfolio-btn');
        
        if (editBtn) {
            const id = editBtn.dataset.id;
            if (window.editPortfolio) window.editPortfolio(id);
        }
        
        if (deleteBtn) {
            const id = deleteBtn.dataset.id;
            if (confirm('Bu portföyü silmek istediğinize emin misiniz?')) {
                deletePortfolio(id);
            }
        }

        if (mediaBtn) {
            const id = mediaBtn.dataset.id;
            if (window.openMediaManager) window.openMediaManager(id);
        }
    });
}

async function deletePortfolio(id) {
    try {
        const res = await apiFetch(`portfolios/${id}`, { method: 'DELETE' });
        if (res.ok) {
            showToast('Portföy başarıyla silindi', 'success');
            fetchPortfolios();
        } else {
            const data = await res.json();
            showToast(data.error || 'Silme işlemi başarısız', 'error');
        }
    } catch (err) {
        console.error('[Portfolio] Silme hatası:', err);
        showToast('Sunucu bağlantı hatası', 'error');
    }
}

// Auto-init if section is shown
window.addEventListener('sectionShown', (e) => {
    if (e.detail.sectionId === 'portfolios') {
        fetchPortfolios();
    }
});
