function showToast(message, type = 'info') {
    let toast = document.getElementById('toast-container');
    if (!toast) {
        // Create container if it doesn't exist
        toast = document.createElement('div');
        toast.id = 'toast-container';
        toast.className = 'fixed bottom-4 right-4 z-50 flex flex-col gap-2';
        document.body.appendChild(toast);
    }
    
    const el = document.createElement('div');
    // Define base styles based on type
    let typeClasses = 'bg-gray-800 text-white';
    if (type === 'error') typeClasses = 'bg-red-500 text-white';
    else if (type === 'success') typeClasses = 'bg-emerald-500 text-white';
    else if (type === 'warning') typeClasses = 'bg-yellow-500 text-white';
    
    el.className = `toast px-4 py-3 rounded-lg shadow-lg text-sm font-medium transition-all ${typeClasses}`;
    el.textContent = message;
    toast.appendChild(el);
    
    setTimeout(() => {
        el.style.opacity = '0';
        setTimeout(() => el.remove(), 300);
    }, 3000);
}

function toggleModal(modalId, show = true) {
    const modal = document.getElementById(modalId);
    if (!modal) {
        console.warn(`Modal #${modalId} not found`);
        return;
    }
    if (show) {
        modal.classList.remove('hidden');
    } else {
        modal.classList.add('hidden');
    }
}

function formatCurrency(amount, currency = 'TRY') {
    if (isNaN(amount) || amount === null) return '-';
    return new Intl.NumberFormat('tr-TR', {
        style: 'currency',
        currency: currency,
        minimumFractionDigits: 0,
        maximumFractionDigits: 2
    }).format(amount);
}

function toggleLoading(elementId, loading = true) {
    const el = document.getElementById(elementId);
    if (!el) return;
    
    if (loading) {
        el.classList.add('opacity-70', 'cursor-wait');
        el.disabled = true;
    } else {
        el.classList.remove('opacity-70', 'cursor-wait');
        el.disabled = false;
    }
}

// Utility for formatting dates
function formatDate(dateString) {
    if (!dateString) return '-';
    const d = new Date(dateString);
    return d.toLocaleString('tr-TR', {
        day: '2-digit', month: '2-digit', year: 'numeric',
        hour: '2-digit', minute: '2-digit'
    });
}