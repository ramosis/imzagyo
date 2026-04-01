-- Migration Script for Unified Identity Management

-- Create new tables if they do not exist
CREATE TABLE IF NOT EXISTS user_identities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    provider VARCHAR(20) NOT NULL CHECK(provider IN ("local","google","facebook")),
    provider_id VARCHAR(255),
    email VARCHAR(255) NOT NULL,
    is_verified BOOLEAN DEFAULT FALSE,
    is_primary BOOLEAN DEFAULT FALSE,
    deleted_at TIMESTAMP NULL
);

CREATE INDEX IF NOT EXISTS idx_user_identities_user ON user_identities(user_id);
CREATE INDEX IF NOT EXISTS idx_user_identities_email ON user_identities(email);
CREATE INDEX IF NOT EXISTS idx_user_identities_provider ON user_identities(provider, provider_id);

CREATE TABLE IF NOT EXISTS auth_audit_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id),
    action TEXT NOT NULL,
    details TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_auth_audit_user ON auth_audit_log(user_id);

-- Migrate Local Identities (Password-based users)
INSERT INTO user_identities (user_id, provider, provider_id, email, is_verified, is_primary)
SELECT 
    id, 
    'local', 
    id, -- Use user id as provider_id for local 
    email, 
    email_verified, 
    1 -- Primary identity 
FROM users 
WHERE email IS NOT NULL AND email != ''
AND id NOT IN (SELECT user_id FROM user_identities WHERE provider = 'local');

-- Migrate Social Identities
INSERT INTO user_identities (user_id, provider, provider_id, email, is_verified, is_primary)
SELECT 
    id, 
    social_provider, 
    social_id, 
    email, 
    1, -- verified
    CASE WHEN id NOT IN (SELECT user_id FROM user_identities WHERE provider = 'local') THEN 1 ELSE 0 END
FROM users 
WHERE social_provider IS NOT NULL AND social_provider IN ('google', 'facebook')
AND id NOT IN (SELECT user_id FROM user_identities WHERE provider = social_provider);

-- Audit Logs for Migrated Identities
INSERT INTO auth_audit_log (user_id, action, details)
SELECT user_id, 'migration', '{"provider": "' || provider || '", "migration_type": "initial"}'
FROM user_identities
WHERE user_id NOT IN (SELECT user_id FROM auth_audit_log WHERE action = 'migration');
