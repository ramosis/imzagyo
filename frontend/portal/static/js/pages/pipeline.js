// --- PIPELINE PAGE JS ---
document.addEventListener('DOMContentLoaded', () => {
    // Sadece pipeline.html yüklendiğinde çalışacak özel kodlar
    const pipelineContainer = document.getElementById('pipeline-container');
    if (pipelineContainer) {
        console.log('[İmza Portal] Pipeline sayfası algılandı, eventler bağlanıyor...');
        if (typeof initPipelineEvents === 'function') {
            initPipelineEvents();
        }
        
        // Load initial leads specifically for pipeline
        if (typeof fetchLeads === 'function') {
            fetchLeads('pipeline');
        }
    }
});

function switchLeadsView(view) {
    const listView = document.getElementById('leads-list-view');
    const pipeView = document.getElementById('leads-pipeline-view');
    const listBtn = document.getElementById('leads-list-btn');
    const pipeBtn = document.getElementById('leads-pipeline-btn');

    if (!listView || !pipeView || !listBtn || !pipeBtn) {
        console.warn('Lead view elements not found');
        return;
    }

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
    if (typeof showSection === 'function') {
        showSection('leads');
    }
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