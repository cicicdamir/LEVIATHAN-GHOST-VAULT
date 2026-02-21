-- ==========================================
-- LEVIATHAN GHOST-VAULT | DATABASE ARCHITECTURE
-- Lead Architect: cicicdamir
-- Domain: Data Integration & Cybersecurity
-- ==========================================

-- Primary Registry for Chromatic Matrices
CREATE TABLE IF NOT EXISTS ghost_vault_registry (
    vault_id BINARY(16) PRIMARY KEY,              -- UUID for stealth indexing
    matrix_hash CHAR(64) UNIQUE NOT NULL,         -- SHA-256 hash of the output matrix
    carrier_type ENUM('JPG', 'PNG', 'WEBP'),      -- Metadata camouflage targets
    encryption_standard VARCHAR(20) DEFAULT 'AES-256-CBC',
    payload_size_kb DECIMAL(10, 2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_matrix_lookup (matrix_hash)         -- High-speed query optimization
) ENGINE=InnoDB;

-- Secure Integration Logs (Acid Compliant)
CREATE TABLE IF NOT EXISTS vault_access_audit (
    audit_id INT AUTO_INCREMENT PRIMARY KEY,
    vault_id BINARY(16),
    action_signature VARCHAR(50),                 -- ENCRYPT_DATA / RECOVER_METADATA
    integrity_check BIT(1) DEFAULT 1,             -- Status of data consistency
    access_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (vault_id) REFERENCES ghost_vault_registry(vault_id) ON DELETE CASCADE
) ENGINE=InnoDB;
