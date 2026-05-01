export const API_BASE = '/api/v1';

/**
 * Core fetch wrapper with authentication and common error handling.
 * @param {string} url - The endpoint URL
 * @param {Object} options - Fetch options
 * @returns {Promise<Response>}
 */
export async function apiFetch(url, options = {}) {
    const token = localStorage.getItem('imza_admin_token');
    
    // Auto-prefix relative URLs with API_BASE
    const finalUrl = url.startsWith('http') || url.startsWith('/') ? url : `${API_BASE}/${url}`;
    
    const defaultHeaders = {
        'Authorization': token ? `Bearer ${token}` : '',
        'Content-Type': 'application/json'
    };
    
    const fetchOptions = { 
        ...options, 
        headers: { 
            ...defaultHeaders, 
            ...options.headers 
        } 
    };
    
    try {
        const response = await fetch(finalUrl, fetchOptions);
        
        if (response.status === 401) {
            console.warn('[İmza API] Oturum geçersiz. Login sayfasına yönlendiriliyor.');
            localStorage.removeItem('imza_admin_token');
            // If we are in the portal, we might want to reload to show login screen
            if (window.location.pathname.includes('/portal')) {
                window.location.reload();
            }
        }
        
        return response;
    } catch (error) {
        console.error(`[İmza API] Fetch hatası (${finalUrl}):`, error);
        throw error;
    }
}
