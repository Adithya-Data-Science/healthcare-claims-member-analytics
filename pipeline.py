from pathlib import Path
import json, sqlite3
import pandas as pd

ROOT=Path(__file__).parent; RAW=ROOT/"data/raw"; PREP=ROOT/"data/prepared"

def load():
    c=pd.read_csv(RAW/"claims.csv",parse_dates=["service_date"])
    m=pd.read_csv(RAW/"members.csv"); p=pd.read_csv(RAW/"providers.csv"); s=pd.read_csv(RAW/"services.csv")
    return c,m,p,s

def validate(c,m,p,s):
    checks={
      "claim_rows_50000":len(c)==50000,
      "claim_id_unique":c.claim_id.is_unique,
      "required_fields_complete":not c.isna().any().any(),
      "member_fk_valid":c.member_id.isin(m.member_id).all(),
      "provider_fk_valid":c.provider_id.isin(p.provider_id).all(),
      "service_fk_valid":c.service_code.isin(s.service_code).all(),
      "status_valid":c.claim_status.isin(["Paid","Denied"]).all(),
      "amounts_nonnegative":(c[["allowed_amount","paid_amount","member_cost_share"]]>=0).all().all(),
      "date_window_valid":c.service_date.between("2024-01-01","2025-12-31").all(),
      "paid_reconciles":((c.claim_status.eq("Paid") & ((c.paid_amount+c.member_cost_share-c.allowed_amount).abs()<=.01)) | (c.claim_status.eq("Denied") & c.paid_amount.eq(0) & c.member_cost_share.eq(0))).all(),
      "readmission_binary":c.readmission_30d.isin([0,1]).all(),
    }
    checks={k:bool(v) for k,v in checks.items()}
    if not all(checks.values()): raise ValueError({k:v for k,v in checks.items() if not v})
    return checks

def main():
    c,m,p,s=load(); checks=validate(c,m,p,s); PREP.mkdir(parents=True,exist_ok=True)
    fact=c.copy(); fact["date_key"]=fact.service_date.dt.strftime("%Y%m%d").astype(int)
    dates=pd.DataFrame({"service_date":pd.date_range("2024-01-01","2025-12-31")}); dates["date_key"]=dates.service_date.dt.strftime("%Y%m%d").astype(int); dates["year"]=dates.service_date.dt.year; dates["month"]=dates.service_date.dt.month; dates["month_name"]=dates.service_date.dt.strftime("%b"); dates["year_month"]=dates.service_date.dt.strftime("%Y-%m")
    fact.drop(columns="service_date").to_csv(PREP/"fact_claims.csv",index=False)
    m.to_csv(PREP/"dim_members.csv",index=False); p.to_csv(PREP/"dim_providers.csv",index=False); s.to_csv(PREP/"dim_services.csv",index=False); dates.to_csv(PREP/"dim_dates.csv",index=False,date_format="%Y-%m-%d")
    db=ROOT/"data/analytics.db"; con=sqlite3.connect(db)
    fact.drop(columns="service_date",errors="ignore").to_sql("fact_claims",con,if_exists="replace",index=False)
    m.to_sql("dim_members",con,if_exists="replace",index=False); p.to_sql("dim_providers",con,if_exists="replace",index=False); s.to_sql("dim_services",con,if_exists="replace",index=False); dates.to_sql("dim_dates",con,if_exists="replace",index=False); con.close()
    metrics={"claims":int(len(c)),"members":int(c.member_id.nunique()),"providers":int(c.provider_id.nunique()),"allowed_amount":round(float(c.allowed_amount.sum()),2),"paid_amount":round(float(c.paid_amount.sum()),2),"denial_rate":round(float(c.claim_status.eq('Denied').mean()),4),"inpatient_readmission_rate":round(float(c.loc[(c.service_code=='INP') & (c.claim_status=='Paid'),'readmission_30d'].mean()),4)}
    (ROOT/"data/validation_report.json").write_text(json.dumps({"checks":checks,"metrics":metrics},indent=2))
    print(json.dumps(metrics,indent=2))

if __name__=="__main__": main()
