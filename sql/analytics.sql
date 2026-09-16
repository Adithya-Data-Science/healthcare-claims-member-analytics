-- Monthly claim and cost trend
SELECT d.year_month, COUNT(*) AS claims, ROUND(SUM(f.allowed_amount),2) AS allowed_amount,
       ROUND(SUM(f.paid_amount),2) AS paid_amount,
       ROUND(SUM(f.member_cost_share),2) AS member_cost_share
FROM fact_claims f JOIN dim_dates d USING(date_key)
GROUP BY d.year_month ORDER BY d.year_month;

-- Service mix and denial rate
SELECT s.service_category, COUNT(*) AS claims, ROUND(SUM(f.allowed_amount),2) AS allowed_amount,
       ROUND(AVG(CASE WHEN f.claim_status='Denied' THEN 1.0 ELSE 0.0 END)*100,2) AS denial_rate_pct
FROM fact_claims f JOIN dim_services s USING(service_code)
GROUP BY s.service_category ORDER BY allowed_amount DESC;

-- Inpatient 30-day readmission rate by member segment
SELECT m.age_band, m.plan_type, COUNT(*) AS paid_inpatient_claims,
       ROUND(AVG(f.readmission_30d)*100,2) AS readmission_rate_pct
FROM fact_claims f JOIN dim_members m USING(member_id)
WHERE f.service_code='INP' AND f.claim_status='Paid'
GROUP BY m.age_band,m.plan_type ORDER BY readmission_rate_pct DESC;

