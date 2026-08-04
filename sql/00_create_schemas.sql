IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name='rcm_ctl') EXEC('CREATE SCHEMA rcm_ctl');
IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name='rcm_stg') EXEC('CREATE SCHEMA rcm_stg');
IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name='rcm_xref') EXEC('CREATE SCHEMA rcm_xref');
IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name='rcm_clean') EXEC('CREATE SCHEMA rcm_clean');
IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name='rcm_qa') EXEC('CREATE SCHEMA rcm_qa');
IF NOT EXISTS (SELECT 1 FROM sys.schemas WHERE name='rcm_mart') EXEC('CREATE SCHEMA rcm_mart');
GO
