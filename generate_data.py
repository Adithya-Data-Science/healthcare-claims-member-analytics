from pathlib import Path
import numpy as np
import pandas as pd

SEED = 2027
N_CLAIMS = 50_000
OUT = Path("data/raw")

def main():
    rng = np.random.default_rng(SEED)
    OUT.mkdir(parents=True, exist_ok=True)
    members = pd.DataFrame({
        "member_id": [f"M{i:06d}" for i in range(1, 5001)],
        "age_band": rng.choice(["0-17", "18-34", "35-49", "50-64", "65+"], 5000, p=[.15,.24,.22,.25,.14]),
        "region": rng.choice(["Omaha", "Lincoln", "Central", "Western", "Northeast"], 5000, p=[.38,.22,.16,.11,.13]),
        "plan_type": rng.choice(["PPO", "HMO", "HDHP"], 5000, p=[.48,.27,.25]),
    })
    providers = pd.DataFrame({
        "provider_id": [f"P{i:04d}" for i in range(1, 301)],
        "provider_type": rng.choice(["Hospital", "Clinic", "Specialist", "Urgent Care"], 300, p=[.15,.4,.32,.13]),
        "region": rng.choice(["Omaha", "Lincoln", "Central", "Western", "Northeast"], 300, p=[.38,.22,.16,.11,.13]),
    })
    service = pd.DataFrame({
        "service_code": ["INP", "OUT", "ER", "RX", "IMG", "LAB", "PCP", "SPEC"],
        "service_category": ["Inpatient", "Outpatient", "Emergency", "Pharmacy", "Imaging", "Laboratory", "Primary Care", "Specialist"],
    })
    dates = pd.date_range("2024-01-01", "2025-12-31", freq="D")
    service_codes = rng.choice(service.service_code, N_CLAIMS, p=[.07,.18,.08,.25,.08,.10,.13,.11])
    base = {"INP":9000,"OUT":900,"ER":1800,"RX":140,"IMG":650,"LAB":120,"PCP":180,"SPEC":320}
    allowed = np.array([rng.lognormal(np.log(base[x]), .55) for x in service_codes]).round(2)
    denied = rng.random(N_CLAIMS) < .055
    member_share = np.where(denied, 0, allowed * rng.uniform(.08,.28,N_CLAIMS)).round(2)
    paid = np.where(denied, 0, allowed-member_share).round(2)
    claims = pd.DataFrame({
        "claim_id": [f"C{i:07d}" for i in range(1,N_CLAIMS+1)],
        "member_id": rng.choice(members.member_id,N_CLAIMS),
        "provider_id": rng.choice(providers.provider_id,N_CLAIMS),
        "service_code": service_codes,
        "service_date": rng.choice(dates,N_CLAIMS),
        "claim_status": np.where(denied,"Denied","Paid"),
        "allowed_amount": allowed,
        "paid_amount": paid,
        "member_cost_share": member_share,
    })
    inpatient = claims.service_code.eq("INP") & claims.claim_status.eq("Paid")
    claims["readmission_30d"] = 0
    claims.loc[inpatient,"readmission_30d"] = (rng.random(inpatient.sum()) < .118).astype(int)
    members.to_csv(OUT/"members.csv",index=False)
    providers.to_csv(OUT/"providers.csv",index=False)
    service.to_csv(OUT/"services.csv",index=False)
    claims.to_csv(OUT/"claims.csv",index=False,date_format="%Y-%m-%d")
    print(f"Generated {len(claims):,} synthetic claims with seed {SEED}.")

if __name__ == "__main__": main()

