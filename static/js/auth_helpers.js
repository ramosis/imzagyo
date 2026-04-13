/**
 * Unified Identity Management UI Helpers
 * Handles linking, unlinking (soft delete), and primary identity selection.
 */

export const IdentityHelpers = {
    /**
     * Fetch user's connected identities
     */
    async fetchIdentities(token) {
        try {
            const response = await fetch('/api/v1/auth/identities', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (!response.ok) throw new Error('Kimlikler getirilemedi.');
            return await response.json();
        } catch (err) {
            console.error('Failed to fetch identities', err);
            return [];
        }
    },

    /**
     * Unlink an identity (triggers backend soft delete and audit log)
     */
    async unlinkIdentity(token, identityId) {
        const msg = "Bu kimliği hesabınızdan ayırmak istediğinize emin misiniz?\n(Güvenlik amacıyla işlem kaydı tutulacaktır, ancak hesap erişimi sonlandırılacaktır.)";
        if (!confirm(msg)) {
            return false;
        }

        try {
            const response = await fetch(`/api/v1/auth/identities/unlink/${identityId}`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}` }
            });
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'İşlem başarısız');
            alert(data.message);
            return true;
        } catch (err) {
            alert(err.message);
            return false;
        }
    },

    /**
     * Set a primary identity
     */
    async setPrimaryIdentity(token, identityId) {
        try {
            const response = await fetch(`/api/v1/auth/identities/set-primary/${identityId}`, {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${token}` }
            });
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || 'İşlem başarısız');
            alert(data.message);
            return true;
        } catch (err) {
            alert(err.message);
            return false;
        }
    },

    /**
     * Start the linking flow for a new provider (Google/Facebook)
     */
    linkNewProvider(provider) {
        window.location.href = `/api/v1/auth/social/login/${provider}`;
    }
};

export const AuditHelpers = {
    /**
     * Fetch the security audit logs for identity changes (Admin / Super Admin view)
     */
    async fetchAuditLogs(token) {
        try {
            const response = await fetch('/api/v1/auth/audit-log', {
                headers: { 'Authorization': `Bearer ${token}` }
            });
            if (!response.ok) throw new Error('Audit log getirilemedi.');
            return await response.json();
        } catch (err) {
            console.error('Failed to fetch audit logs', err);
            return [];
        }
    }
};
