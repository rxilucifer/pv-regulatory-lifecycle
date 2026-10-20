"""Make a FAKE log of when each report was sent to the regulator.
Run:  python tools/make_submission_log.py
Writes data/submission_log.csv
"""
import random
import pandas as pd
from datetime import timedelta

random.seed(202)
df = pd.read_csv("data/reports_clean.csv", parse_dates=["receipt_date"])

rows = []
for _, r in df.iterrows():
    days = random.choice([3, 5, 7, 9, 11, 13, 14, 15, 18, 22, 28])
    sent = r["receipt_date"] + timedelta(days=days)
    rows.append({"report_id": r["report_id"], "sent_date": sent.date().isoformat()})

pd.DataFrame(rows).to_csv("data/submission_log.csv", index=False)
print(f"Wrote {len(rows)} submission records.")
