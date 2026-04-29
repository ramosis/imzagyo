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
    const currentRole = localStorage.getItem('imza_admin_role') || 'admin';
    const targetBtn = btnElement || document.querySelector(`button[onclick*="'${sectionId}'"]`);
    if (targetBtn && targetBtn.hasAttribute('data-access')) {
        const requiredAccess = targetBtn.getAttribute('data-access');
        if (requiredAccess === 'admin' && currentRole !== 'admin') {
            if (typeof showToast === 'function') showToast('Bu bölüme erişim yetkiniz yok.', 'error');
            return;
        }
        if (requiredAccess === 'broker' && currentRole === 'standart') {
            if (typeof showToast === 'function') showToast('Bu bölüm Broker ve üzeri yetki gerektirir.', 'error');
            return;
        }
    }

    // Section visibility
    const allSections = document.querySelectorAll('.content-section');
    allSections.forEach(s => s.classList.add('hidden'));

    const target = document.getElementById(targetId);
    if (target) {
        target.classList.remove('hidden');
    } else {
        console.warn("[İmza Portal] HATA: Hedef bölüm bulunamadı ->", targetId);
    }

    // Sidebar highlight
    document.querySelectorAll('#sidebar nav .nav-item').forEach(a => {
        a.classList.remove('bg-gold/10', 'text-gold', 'border-r-4', 'border-gold');
    });
    if (btnElement) {
        btnElement.classList.add('bg-gold/10', 'text-gold', 'border-r-4', 'border-gold');
    }

    // Dispatch a custom event so specific modules can load data when their section is shown
    const event = new CustomEvent('sectionShown', { detail: { sectionId: targetId } });
    document.dispatchEvent(event);
}

function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebar-overlay');
    
    if (sidebar) {
        sidebar.classList.toggle('-translate-x-full');
        if (overlay) overlay.classList.toggle('hidden');
        
        if (!sidebar.classList.contains('-translate-x-full') && window.innerWidth < 1024) {
            document.body.style.overflow = 'hidden';
        } else {
            document.body.style.overflow = '';
        }
    }
}
