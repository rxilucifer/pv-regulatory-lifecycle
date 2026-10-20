"""Compare my QC findings with the answer key. Run AFTER qc_reports.py."""
import pandas as pd

found = pd.read_csv("data/qc_findings.csv")
key = pd.read_csv("data/answer_key.csv")

f = set(zip(found["report_id"], found["problem"]))
k = set(zip(key["report_id"], key["problem"]))

print(f"Planted problems: {len(k)}")
print(f"Found correctly:  {len(f & k)}")
print(f"Missed:           {len(k - f)}")
print(f"False alarms:     {len(f - k)}")
for item in sorted(k - f):
    print("  missed:", item)
for item in sorted(f - k):
    print("  false alarm:", item)
