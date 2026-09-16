# Validation controls

The pipeline stops if any control fails:

- Exactly 50,000 claim rows
- Unique and nonmissing claim identifiers
- Complete required fields
- Valid member, provider, and service foreign keys
- Accepted claim status values
- Nonnegative financial measures
- Service dates within the documented analysis window
- Paid claims reconcile: paid amount plus member cost share equals allowed amount within one cent
- Denied claims have zero paid amount and member cost share
- Readmission indicator is binary

The executed results are written to `data/validation_report.json`.

