# Data dictionary

| Table | Field | Definition |
|---|---|---|
| fact_claims | claim_id | Synthetic unique claim identifier |
| fact_claims | member_id | Synthetic member key |
| fact_claims | provider_id | Synthetic provider key |
| fact_claims | service_code | Service-category key |
| fact_claims | service_date/date_key | Date of synthetic service and date-dimension key |
| fact_claims | claim_status | Paid or Denied |
| fact_claims | allowed_amount | Synthetic amount allowed under the plan, USD |
| fact_claims | paid_amount | Synthetic plan-paid amount, USD |
| fact_claims | member_cost_share | Synthetic member responsibility, USD |
| fact_claims | readmission_30d | Synthetic inpatient readmission indicator, 0/1 |
| dim_members | age_band | Synthetic member age category |
| dim_members | region | Synthetic Nebraska-area category |
| dim_members | plan_type | PPO, HMO, or HDHP |
| dim_providers | provider_type | Hospital, Clinic, Specialist, or Urgent Care |
| dim_services | service_category | Human-readable service category |

