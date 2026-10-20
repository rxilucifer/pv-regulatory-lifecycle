"""Check each fake report against the reporting deadlines in R-06.
Rule used (Indian MAH guidance v2.0, section 2.8): serious reports within
15 calendar days of receipt, non-serious within 30 calendar days.
Run:  python tools/reporting_clock.py
Writes data/reporting_clock.csv
"""
import pandas as pd

rep = pd.read_csv("data/reports_clean.csv", parse_dates=["receipt_date"])
log = pd.read_csv("data/submission_log.csv", parse_dates=["sent_date"])
df = rep.merge(log, on="report_id", how="left")

# Treat a Fatal outcome as serious even if the form says N (safer choice)
df["treated_serious"] = (df["serious"] == "Y") | (df["outcome"] == "Fatal")
df["limit_days"] = df["treated_serious"].map({True: 15, False: 30})
df["due_date"] = df["receipt_date"] + pd.to_timedelta(df["limit_days"], unit="D")
df["days_taken"] = (df["sent_date"] - df["receipt_date"]).dt.days
df["late"] = df["sent_date"] > df["due_date"]
df["days_late"] = (df["sent_date"] - df["due_date"]).dt.days.clip(lower=0)

cols = ["report_id", "receipt_date", "treated_serious", "limit_days",
        "due_date", "sent_date", "days_taken", "late", "days_late"]
df[cols].to_csv("data/reporting_clock.csv", index=False)

print(f"Reports checked: {len(df)}")
for label, sub in [("Serious", df[df['treated_serious']]),
                   ("Non-serious", df[~df['treated_serious']])]:
    late = sub["late"].sum()
    pct = 100 * (len(sub) - late) / len(sub)
    print(f"{label}: {len(sub)} reports, {late} late, {pct:.1f}% on time")
print(f"Overall late: {df['late'].sum()}")
print("\nMost overdue serious reports:")
print(df[df["late"] & df["treated_serious"]]
      .sort_values("days_late", ascending=False)
      [["report_id", "due_date", "sent_date", "days_late"]].head(5).to_string(index=False))
