# Healthcare Claims Analytics and Member Insights

An end-to-end portfolio project for analyzing de-identified synthetic healthcare claims with R, SQL, and Power BI-ready assets. The workflow generates reproducible data, validates data quality, builds a SQLite analytics layer, produces R summaries, and documents a Power BI dashboard model.

## Business questions

- How do claim volume, allowed amount, paid amount, and member cost share change by month?
- Which service categories and providers account for the largest allowed amounts?
- How do inpatient utilization and 30-day readmission rates vary by member segment?
- Which records fail completeness, accepted-value, or reconciliation rules?

## Data and privacy

All records are synthetic and generated locally. The repository contains no protected health information and should not be used for clinical decisions. Member, provider, and claim identifiers are artificial.

## Start-to-finish workflow

1. Generate 50,000 deterministic synthetic claims and supporting dimensions.
2. Validate required fields, unique claim IDs, foreign keys, accepted values, dates, and financial reconciliation.
3. Load a SQLite star schema with claims as the fact table and member, provider, service, and date dimensions.
4. Run SQL analyses for monthly trends, service mix, provider variation, member cost share, and readmissions.
5. Run the R analysis to produce independent summary tables and charts.
6. Import the prepared CSV outputs into Power BI using the documented Power Query steps, relationships, and DAX measures.
7. Compare dashboard totals with the validation report before publishing.

## Repository structure

```text
data/                 Generated synthetic source and prepared output files
docs/                 Data dictionary, methodology, findings, and validation notes
powerbi/              Power Query, DAX, model, and dashboard build specification
r/                    Reproducible R analysis
sql/                  Schema and analytical queries
tests/                Automated validation tests
generate_data.py      Deterministic synthetic-data generator
pipeline.py           Validation, transformation, SQLite load, and output pipeline
requirements.txt      Python dependencies
```

## Run locally

```bash
python -m venv .venv
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python generate_data.py
python pipeline.py
python -m unittest discover -s tests -v
Rscript r/analysis.R
```

The Python pipeline writes `data/analytics.db`, prepared CSVs, and `data/validation_report.json`. The R script writes summary CSVs and PNG charts to `outputs/r`.

## Power BI build

Follow `powerbi/BUILD_GUIDE.md`. The folder includes the Power Query transformation, star-schema relationships, DAX measures, report-page specification, and reconciliation checklist needed to reproduce the report in Power BI Desktop.

## Reproducibility

- Fixed random seed: `2027`
- Synthetic claims: `50,000`
- Analysis period: January 2024 through December 2025
- Automated tests cover row counts, primary keys, foreign keys, accepted values, nonnegative amounts, date logic, and paid/denied reconciliation.

## Limitations

The data are synthetic and intentionally simplified. Results demonstrate analytics, data-quality, governance, and reporting practices; they do not represent BCBSNE or any real insurer, provider, or member population.

