CREATE TABLE rcm_clean.fact_claim_financial (
    claim_financial_key BIGINT IDENTITY PRIMARY KEY,
    claim_id NVARCHAR(60) NOT NULL,
    service_date DATE NOT NULL,
    payer NVARCHAR(255) NOT NULL,
    provider NVARCHAR(255) NOT NULL,
    cpt VARCHAR(10) NOT NULL,
    claim_status NVARCHAR(60) NOT NULL,
    charge_amount DECIMAL(18,2) NOT NULL,
    payment_amount DECIMAL(18,2) NOT NULL,
    adjustment_amount DECIMAL(18,2) NOT NULL,
    balance_amount DECIMAL(18,2) NOT NULL,
    source_file_id BIGINT NOT NULL,
    ingestion_run_id UNIQUEIDENTIFIER NOT NULL,
    CONSTRAINT CK_claim_reconciliation CHECK (ABS(charge_amount-payment_amount-adjustment_amount-balance_amount) <= 0.01),
    CONSTRAINT FK_claim_file FOREIGN KEY (source_file_id) REFERENCES rcm_ctl.source_file_registry,
    CONSTRAINT FK_claim_run FOREIGN KEY (ingestion_run_id) REFERENCES rcm_ctl.ingestion_run
);
GO
