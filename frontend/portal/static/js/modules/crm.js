function initPipelineEvents() {
    const container = document.getElementById('pipeline-container');
    if (!container) return;
    
    container.addEventListener('click', (e) => {
        const btn = e.target.closest('button, a');
        if (!btn) return;
        
        if (btn.classList.contains('whatsapp-btn')) {
            const phone = btn.dataset.phone;
            if (phone) window.open(`https://wa.me/${phone}`, '_blank');
        }
        
        if (btn.classList.contains('edit-lead-btn')) {
            const leadId = btn.dataset.leadId;
            // Assuming openLeadEditModal is defined or will be migrated
            if (typeof openLeadEditModal === 'function') openLeadEditModal(leadId);
        }
        
        if (btn.classList.contains('move-stage-btn')) {
            const leadId = btn.dataset.leadId;
            const stageId = btn.dataset.stageId;
            moveLeadStage(leadId, stageId);
        }
    });
}

async function fetchLeads(filterType = 'all') {
    try {
        let url = `/api/v1/leads`;
        if (filterType === 'pipeline') url += '?pipeline=true';
        else if (filterType === 'standby') url += '?pipeline=false';

        // using global apiFetch if available
        const res = typeof apiFetch !== 'undefined' ? await apiFetch(url) : await fetch(url);
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
                const segment = l.segment || l.tags || 'Genel'; // 4E.2: Duplicate column handling
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
                            ${segment}
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
        if (typeof renderLeadPipeline === 'function') {
            renderLeadPipeline(data);
        }

        // Highlight pending lead if any
        if (window._pendingLeadId) {
            setTimeout(() => {
                if (typeof highlightLeadInPipeline === 'function') highlightLeadInPipeline(window._pendingLeadId);
            }, 500);
            window._pendingLeadId = null;
        }

    } catch (err) { console.error('Fetch Leads error:', err); }
}

function renderLeadPipeline(leads) {
    const container = document.getElementById('pipeline-container');
    if (!container) return;

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
                ${stageLeads.map(l => {
                    const segment = l.segment || l.tags || 'Genel'; // 4E.2 Fix
                    return `
                    <div class="kanban-card bg-white p-4 rounded-xl border border-gray-100 shadow-sm hover:shadow-md hover:border-gold/30 transition-all cursor-pointer group relative" 
                         id="lead-card-${l.id}" data-lead-id="${l.id}">
                        <div class="flex justify-between items-start mb-2">
                            <span class="font-bold text-navy text-sm leading-tight">${l.name}</span>
                            <span class="text-[10px] font-black ${l.ai_score >= 80 ? 'text-emerald-500' : 'text-gold'}">%${l.ai_score || 0}</span>
                        </div>
                        <p class="text-[10px] text-gray-500 line-clamp-2 mb-3 font-medium">${l.notes || 'Not bulunmuyor.'}</p>
                        <div class="flex items-center justify-between">
                            <div class="flex -space-x-2">
                                <div class="w-6 h-6 rounded-full bg-navy/10 border-2 border-white flex items-center justify-center text-[8px] font-bold text-navy uppercase">${l.name ? l.name[0] : '?'}</div>
                            </div>
                            <span class="text-[10px] font-bold text-gray-400 bg-gray-50 px-2 py-1 rounded">${segment}</span>
                        </div>
                    </div>
                `}).join('')}
            </div>
        `;
        container.appendChild(stageEl);
    });
}

// 4E.1: Pipeline Stage Default Değerleri
async function fetchPipelineStages() {
    try {
        const base = typeof API_BASE !== 'undefined' ? API_BASE : '/api/v1';
        const stages = typeof apiFetch !== 'undefined' ? await apiFetch(`${base}/crm/pipeline-stages/`) : await fetch(`${base}/crm/pipeline-stages/`).then(r => r.json());
        if (!stages || stages.length === 0) {
            console.warn('No pipeline stages found');
            return [];
        }
        return stages;
    } catch (err) {
        console.error('Failed to load pipeline stages:', err);
        return [];
    }
}

async function createLead(leadData) {
    const stages = await fetchPipelineStages();
    const defaultStage = stages.find(s => s.is_default) || stages[0];
    
    if (!defaultStage) {
        if (typeof showToast === 'function') showToast('Pipeline stage bulunamadı', 'error');
        return;
    }
    
    leadData.pipeline_stage_id = defaultStage.id;
    
    try {
        const base = typeof API_BASE !== 'undefined' ? API_BASE : '/api/v1';
        return typeof apiFetch !== 'undefined' ? await apiFetch(`${base}/crm/leads/`, {
            method: 'POST',
            body: JSON.stringify(leadData)
        }) : await fetch(`${base}/crm/leads/`, {
            method: 'POST',
            body: JSON.stringify(leadData),
            headers: { 'Content-Type': 'application/json' }
        });
    } catch (err) {
        console.error('Create Lead error:', err);
    }
}