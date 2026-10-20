"""Quality-check the fake DMX-101 reports. Does NOT look at the answer key.
Run:  python tools/qc_reports.py
Writes data/qc_findings.csv and data/reports_clean.csv
"""
import pandas as pd

df = pd.read_csv("data/reports.csv", dtype={"patient_age": "float"})
for col in ["receipt_date", "start_date", "onset_date"]:
    df[col] = pd.to_datetime(df[col], errors="coerce")

findings = []


def flag(rows, problem, note):
    for rid in rows["report_id"]:
        findings.append({"report_id": rid, "problem": problem, "note": note})


# 1. Duplicates: same case details, different report_id (keep the first one)
same_cols = [c for c in df.columns if c != "report_id"]
dups = df[df.duplicated(subset=same_cols, keep="first")]
flag(dups, "duplicate", "same details as an earlier report")

# 2. Missing data
flag(df[df["patient_age"].isna()], "missing_age", "patient_age blank")
flag(df[df["onset_date"].isna()], "missing_onset", "onset_date blank")

# 3. Impossible values
age_bad = df[(df["patient_age"] < 18) | (df["patient_age"] > 100)]
flag(age_bad, "impossible_age", "age outside 18-100")

# 4. Impossible date order
flag(df[df["onset_date"] < df["start_date"]], "onset_before_start",
     "event began before the drug was started")
flag(df[df["receipt_date"] < df["onset_date"]], "receipt_before_onset",
     "report received before the event began")

# 5. Seriousness conflict
flag(df[(df["serious"] == "N") & (df["outcome"] == "Fatal")],
     "seriousness_conflict", "marked not serious but outcome is Fatal")

out = pd.DataFrame(findings)
out.to_csv("data/qc_findings.csv", index=False)

# Clean file = remove duplicates only. Other problems need follow-up
# with the reporter, so those rows stay but are listed in qc_findings.csv.
clean = df[~df["report_id"].isin(dups["report_id"])]
clean.to_csv("data/reports_clean.csv", index=False)

print(f"Reports checked: {len(df)}")
print(f"Problems found:  {len(out)}")
print(out["problem"].value_counts().to_string())
print(f"Clean file rows: {len(clean)}")
