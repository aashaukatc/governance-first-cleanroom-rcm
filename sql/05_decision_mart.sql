CREATE OR ALTER VIEW rcm_mart.vw_payer_financial_performance AS
SELECT payer,
       COUNT(DISTINCT claim_id) AS claim_count,
       SUM(charge_amount) AS charges,
       SUM(payment_amount) AS payments,
       SUM(balance_amount) AS outstanding_balance,
       CAST(SUM(payment_amount) / NULLIF(SUM(charge_amount-adjustment_amount),0) AS DECIMAL(18,4)) AS net_collection_rate
FROM rcm_clean.fact_claim_financial
GROUP BY payer;
GO
