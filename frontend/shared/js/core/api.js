const API_BASE = '/api/v1';

async function apiFetch(endpoint, options = {}) {
    const token = localStorage.getItem('imza_admin_token') || sessionStorage.getItem('imza_admin_token');
    // Eğer endpoint / ile başlamıyorsa ve API_BASE ile başlamıyorsa
    const url = endpoint.startsWith('http') ? endpoint : (endpoint.startsWith('/api') ? endpoint : `${API_BASE}${endpoint.startsWith('/') ? endpoint : '/' + endpoint}`);
    
    const defaultOptions = {
        headers: {
            'Content-Type': 'application/json',
            ...(token && { 'Authorization': `Bearer ${token}` })
        }
    };
    
    const fetchOptions = { ...defaultOptions, ...options };
    // Merge headers carefully if options provided headers
    if (options.headers) {
        fetchOptions.headers = { ...defaultOptions.headers, ...options.headers };
    }

    try {
        const response = await fetch(url, fetchOptions);
        
        if (response.status === 401) {
            alert('Oturum süreniz doldu. Lütfen tekrar giriş yapın.');
            window.location.reload();
            return;
        }
        
        return response;
    } catch (error) {
        console.error('API Fetch Error:', error);
        throw error;
    }
}

function getAuthHeaders() {
    const token = localStorage.getItem('imza_admin_token');
    return token ? { 'Authorization': `Bearer ${token}` } : {};
}