CREATE TABLE rcm_qa.control_result (
    control_result_id BIGINT IDENTITY PRIMARY KEY,
    ingestion_run_id UNIQUEIDENTIFIER NOT NULL,
    control_id VARCHAR(20) NOT NULL,
    control_name NVARCHAR(255) NOT NULL,
    status VARCHAR(10) NOT NULL CHECK (status IN ('GREEN','YELLOW','RED')),
    exception_count INT NOT NULL DEFAULT 0,
    evidence_json NVARCHAR(MAX) NULL,
    evaluated_at_utc DATETIME2 NOT NULL DEFAULT SYSUTCDATETIME()
);
GO

CREATE OR ALTER PROCEDURE rcm_qa.usp_evaluate_publish_gate @ingestion_run_id UNIQUEIDENTIFIER AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @red INT=(SELECT COUNT(*) FROM rcm_qa.control_result WHERE ingestion_run_id=@ingestion_run_id AND status='RED');
    DECLARE @yellow INT=(SELECT COUNT(*) FROM rcm_qa.control_result WHERE ingestion_run_id=@ingestion_run_id AND status='YELLOW');
    DECLARE @status VARCHAR(10)=CASE WHEN @red>0 THEN 'RED' WHEN @yellow>0 THEN 'YELLOW' ELSE 'GREEN' END;
    UPDATE rcm_ctl.ingestion_run SET final_status=@status, completed_at_utc=SYSUTCDATETIME() WHERE ingestion_run_id=@ingestion_run_id;
    SELECT @status AS publish_gate_status, @red AS red_controls, @yellow AS yellow_controls;
END;
GO
