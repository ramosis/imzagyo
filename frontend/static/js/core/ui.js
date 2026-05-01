/**
 * Shows a toast notification.
 * @param {string} message - Message to display
 * @param {string} type - 'success', 'error', 'info', 'warning'
 */
export function showToast(message, type = 'info') {
    const container = document.getElementById('toast-container');
    if (!container) return;

    const toast = document.createElement('div');
    const colors = {
        success: 'bg-emerald-500 text-white',
        error: 'bg-red-500 text-white',
        info: 'bg-navy text-gold',
        warning: 'bg-amber-500 text-white'
    };

    toast.className = `${colors[type] || colors.info} px-6 py-4 rounded-xl shadow-2xl flex items-center gap-3 animate-fade-in z-[999]`;
    toast.innerHTML = `
        <i class="fa-solid ${type === 'success' ? 'fa-check-circle' : 'fa-circle-info'}"></i>
        <span class="font-bold text-sm">${message}</span>
    `;

    container.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(-20px)';
        setTimeout(() => toast.remove(), 300);
    }, 4000);
}

export function toggleModal(id, show = true) {
    const modal = document.getElementById(id);
    if (!modal) return;
    
    if (show) {
        modal.classList.remove('hidden');
        if (id.includes('modal')) modal.classList.add('flex');
    } else {
        modal.classList.add('hidden');
        modal.classList.remove('flex');
    }
}

export function formatCurrency(amount, currency = 'TRY') {
    return new Intl.NumberFormat('tr-TR', { 
        style: 'currency', 
        currency: currency 
    }).format(amount);
}

export function toggleLoading(element, isLoading, originalText = '') {
    if (!element) return;
    if (isLoading) {
        element.disabled = true;
        element.dataset.originalText = element.innerHTML;
        element.innerHTML = '<i class="fa-solid fa-spinner fa-spin mr-2"></i> Yükleniyor...';
    } else {
        element.disabled = false;
        element.innerHTML = originalText || element.dataset.originalText || 'Tamam';
    }
}

// Global expose for transition period
window.showToast = showToast;
window.toggleModal = toggleModal;
