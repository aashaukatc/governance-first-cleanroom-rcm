CREATE TABLE rcm_xref.map_payer (
    raw_value NVARCHAR(255) PRIMARY KEY,
    canonical_value NVARCHAR(255) NOT NULL,
    payer_type NVARCHAR(60) NOT NULL,
    mapping_status VARCHAR(20) NOT NULL DEFAULT 'APPROVED',
    approved_by NVARCHAR(120) NULL,
    approved_at_utc DATETIME2 NULL
);
CREATE TABLE rcm_xref.map_provider (
    raw_value NVARCHAR(255) PRIMARY KEY,
    canonical_value NVARCHAR(255) NOT NULL,
    specialty NVARCHAR(100) NULL,
    mapping_status VARCHAR(20) NOT NULL DEFAULT 'APPROVED'
);
CREATE TABLE rcm_xref.map_cpt (
    raw_value VARCHAR(10) PRIMARY KEY,
    canonical_value VARCHAR(10) NOT NULL,
    cpt_family NVARCHAR(100) NOT NULL,
    mapping_status VARCHAR(20) NOT NULL DEFAULT 'APPROVED'
);
CREATE TABLE rcm_xref.map_denial (
    raw_value VARCHAR(20) PRIMARY KEY,
    canonical_value VARCHAR(20) NOT NULL,
    denial_category NVARCHAR(120) NOT NULL,
    mapping_status VARCHAR(20) NOT NULL DEFAULT 'APPROVED'
);
GO
