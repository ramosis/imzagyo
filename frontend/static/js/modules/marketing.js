import { apiFetch } from '../core/api.js';

export async function initMarketing() {
    console.log('[İmza Marketing] Başlatılıyor...');
    await loadCampaigns();
    await loadAutomationRules();
    await loadTemplates();
}

// --- KAMPANYALAR ---
async function loadCampaigns() {
    try {
        const response = await apiFetch('marketing/campaigns');
        const campaigns = await response.json();
        const tbody = document.getElementById('campaigns-table-body');
        
        if (!tbody) return;
        
        if (campaigns.length === 0) {
            tbody.innerHTML = '<tr><td colspan="6" class="p-8 text-center text-gray-400">Henüz kampanya bulunmuyor.</td></tr>';
            return;
        }

        tbody.innerHTML = campaigns.map(c => `
            <tr class="hover:bg-gray-50 transition-colors">
                <td class="p-6">
                    <div class="font-bold text-navy">${c.title}</div>
                    <div class="text-[10px] text-gray-400 uppercase tracking-widest">${c.channel}</div>
                </td>
                <td class="p-6">
                    <span class="px-3 py-1 rounded-full text-[10px] font-bold uppercase ${c.type === 'automated' ? 'bg-purple-100 text-purple-600' : 'bg-blue-100 text-blue-600'}">
                        ${c.type === 'automated' ? 'Otomatik' : 'Manuel'}
                    </span>
                </td>
                <td class="p-6 font-medium text-gray-600">${c.target_group}</td>
                <td class="p-6 font-bold text-navy">${c.sent_count} Kişi</td>
                <td class="p-6 text-gray-400">${new Date(c.created_at).toLocaleDateString('tr-TR')}</td>
                <td class="p-6 text-right">
                    <span class="px-3 py-1 rounded-full text-[10px] font-bold uppercase ${c.status === 'completed' ? 'bg-green-100 text-green-600' : 'bg-gray-100 text-gray-400'}">
                        ${c.status}
                    </span>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('[İmza Marketing] Kampanya yükleme hatası:', error);
    }
}

// --- KURALLAR ---
async function loadAutomationRules() {
    try {
        const response = await apiFetch('marketing/rules');
        const rules = await response.json();
        const tbody = document.getElementById('automation-rules-table-body');
        
        if (!tbody) return;
        
        if (rules.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" class="p-8 text-center text-gray-400">Aktif kural bulunmuyor.</td></tr>';
            return;
        }

        tbody.innerHTML = rules.map(r => `
            <tr class="hover:bg-gray-50 transition-colors">
                <td class="p-6 font-bold text-navy">${r.name}</td>
                <td class="p-6 text-gray-600 font-medium">${r.trigger}</td>
                <td class="p-6 text-gold font-bold uppercase tracking-tighter text-xs">${r.action}</td>
                <td class="p-6">
                    <div class="flex items-center gap-2">
                        <div class="w-2 h-2 rounded-full ${r.is_active ? 'bg-green-500' : 'bg-red-500'}"></div>
                        <span class="text-xs font-bold">${r.is_active ? 'Aktif' : 'Pasif'}</span>
                    </div>
                </td>
                <td class="p-6 text-right">
                    <button class="text-navy hover:text-gold transition-colors"><i class="fa-solid fa-ellipsis-vertical"></i></button>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('[İmza Marketing] Kural yükleme hatası:', error);
    }
}

// --- ŞABLONLAR ---
async function loadTemplates() {
    try {
        const response = await apiFetch('marketing/templates');
        const templates = await response.json();
        const grid = document.getElementById('templates-grid');
        
        if (!grid) return;
        
        if (templates.length === 0) {
            grid.innerHTML = '<div class="p-8 text-center text-gray-400 col-span-full">Henüz şablon oluşturulmamış.</div>';
            return;
        }

        grid.innerHTML = templates.map(t => `
            <div class="bg-white p-6 rounded-3xl border border-gray-100 hover:shadow-xl transition-all group relative overflow-hidden">
                <div class="absolute top-0 right-0 p-4 opacity-0 group-hover:opacity-100 transition-opacity">
                    <button class="text-gray-400 hover:text-navy"><i class="fa-solid fa-pen-to-square"></i></button>
                </div>
                <div class="w-12 h-12 bg-gray-50 rounded-2xl flex items-center justify-center text-navy mb-4 shadow-inner">
                    <i class="fa-solid ${t.type === 'email' ? 'fa-envelope' : 'fa-comment-sms'}"></i>
                </div>
                <h4 class="font-bold text-navy mb-1">${t.name}</h4>
                <p class="text-[10px] text-gray-400 uppercase tracking-widest font-black mb-4">${t.type}</p>
                <div class="text-xs text-gray-500 line-clamp-3 mb-4">${t.content}</div>
                <button class="w-full py-3 bg-gray-50 group-hover:bg-navy group-hover:text-gold rounded-xl text-[10px] font-bold uppercase tracking-widest transition-all">Şablonu Önizle</button>
            </div>
        `).join('');
    } catch (error) {
        console.error('[İmza Marketing] Şablon yükleme hatası:', error);
    }
}

// --- GLOBAL EVENTS ---
window.switchCampaignTab = function(tab) {
    document.querySelectorAll('.campaign-tab-btn').forEach(btn => {
        btn.classList.remove('active', 'bg-white', 'shadow-sm', 'text-navy');
        btn.classList.add('text-gray-500');
    });
    document.querySelectorAll('.campaign-tab-content').forEach(content => content.classList.add('hidden'));
    
    const activeBtn = document.getElementById(`campaign-tab-btn-${tab}`);
    activeBtn.classList.add('active', 'bg-white', 'shadow-sm', 'text-navy');
    activeBtn.classList.remove('text-gray-500');
    
    document.getElementById(`campaign-tab-content-${tab}`).classList.remove('hidden');
};
