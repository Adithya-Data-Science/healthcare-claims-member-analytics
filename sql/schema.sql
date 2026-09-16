CREATE TABLE dim_members (member_id TEXT PRIMARY KEY, age_band TEXT NOT NULL, region TEXT NOT NULL, plan_type TEXT NOT NULL);
CREATE TABLE dim_providers (provider_id TEXT PRIMARY KEY, provider_type TEXT NOT NULL, region TEXT NOT NULL);
CREATE TABLE dim_services (service_code TEXT PRIMARY KEY, service_category TEXT NOT NULL);
CREATE TABLE dim_dates (date_key INTEGER PRIMARY KEY, service_date TEXT NOT NULL, year INTEGER NOT NULL, month INTEGER NOT NULL, month_name TEXT NOT NULL, year_month TEXT NOT NULL);
CREATE TABLE fact_claims (claim_id TEXT PRIMARY KEY, member_id TEXT NOT NULL, provider_id TEXT NOT NULL, service_code TEXT NOT NULL, claim_status TEXT NOT NULL, allowed_amount REAL NOT NULL CHECK(allowed_amount>=0), paid_amount REAL NOT NULL CHECK(paid_amount>=0), member_cost_share REAL NOT NULL CHECK(member_cost_share>=0), readmission_30d INTEGER NOT NULL CHECK(readmission_30d IN (0,1)), date_key INTEGER NOT NULL, FOREIGN KEY(member_id) REFERENCES dim_members(member_id), FOREIGN KEY(provider_id) REFERENCES dim_providers(provider_id), FOREIGN KEY(service_code) REFERENCES dim_services(service_code), FOREIGN KEY(date_key) REFERENCES dim_dates(date_key));

