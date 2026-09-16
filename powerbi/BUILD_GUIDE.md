# Power BI build guide

## Load and transform

Load the five CSVs in `data/prepared`. Use the transformations in `power_query.m` for the claims fact table. Set identifiers to text, `date_key` to whole number, and amounts to fixed decimal number.

## Relationships

- `dim_members[member_id]` 1:* `fact_claims[member_id]`
- `dim_providers[provider_id]` 1:* `fact_claims[provider_id]`
- `dim_services[service_code]` 1:* `fact_claims[service_code]`
- `dim_dates[date_key]` 1:* `fact_claims[date_key]`

Use single-direction filters from each dimension to the fact table. Mark `dim_dates[service_date]` as the date table.

## Measures

Create the measures in `measures.dax`. Reconcile Total Claims, Total Allowed, Total Paid, Denial Rate, and Inpatient Readmission Rate with `data/validation_report.json`.

## Report pages

1. **Member and cost overview**: KPI cards for claims, members, allowed amount, paid amount, member cost share, and denial rate; monthly allowed/paid line chart; service-category allowed-amount bar chart.
2. **Utilization and quality**: claims per 1,000 members; inpatient utilization; readmission rate by age band and plan; denial rate by service category.
3. **Provider variation**: allowed amount per claim and denial rate by provider type and region; drill-through table for provider-level review.
4. **Data quality**: validation-rule status and reconciliation totals from the pipeline report.

Add slicers for year, region, plan type, age band, provider type, and service category. Do not display individual member identifiers on report pages.

## Publication checklist

- Refresh succeeds without errors.
- Every relationship has the expected 1:* cardinality.
- KPI totals match the validation report.
- No member-level identifiers appear in visuals or tooltips.
- Titles specify metric, unit, and period where needed.

