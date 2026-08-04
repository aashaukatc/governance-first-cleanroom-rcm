CREATE TABLE rcm_ctl.source_file_registry (
    source_file_id BIGINT IDENTITY PRIMARY KEY,
    source_file_name NVARCHAR(260) NOT NULL,
    sha256 CHAR(64) NOT NULL,
    report_family NVARCHAR(80) NULL,
    disposition NVARCHAR(40) NOT NULL,
    schema_signature CHAR(64) NULL,
    received_at_utc DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    UNIQUE (sha256)
);
CREATE TABLE rcm_ctl.ingestion_run (
    ingestion_run_id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWSEQUENTIALID(),
    started_at_utc DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME(),
    completed_at_utc DATETIME2 NULL,
    final_status VARCHAR(10) NOT NULL DEFAULT 'YELLOW'
);
CREATE TABLE rcm_ctl.row_lineage (
    lineage_id BIGINT IDENTITY PRIMARY KEY,
    ingestion_run_id UNIQUEIDENTIFIER NOT NULL,
    source_file_id BIGINT NOT NULL,
    source_row_number INT NOT NULL,
    target_schema SYSNAME NOT NULL,
    target_table SYSNAME NOT NULL,
    target_business_key NVARCHAR(200) NOT NULL,
    transformation_version NVARCHAR(40) NOT NULL,
    CONSTRAINT FK_lineage_run FOREIGN KEY (ingestion_run_id) REFERENCES rcm_ctl.ingestion_run,
    CONSTRAINT FK_lineage_file FOREIGN KEY (source_file_id) REFERENCES rcm_ctl.source_file_registry
);
GO
