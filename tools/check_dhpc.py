"""Check the draft letter (PV-011): required headings are present and the
numbers in the letter match the data. Run:  python tools/check_dhpc.py
"""
import sys
import pandas as pd

TEXT = open("docs/10_dhpc_draft.md").read()
HEADINGS = ["## Summary", "## Background on the safety concern",
            "## Follow-up", "## Call for reporting", "## Company contact point"]

problems = []
for h in HEADINGS:
    if h not in TEXT:
        problems.append(f"Missing heading: {h}")

df = pd.read_csv("data/reports_clean.csv", parse_dates=["receipt_date"])
cum = df[df["receipt_date"] <= "2026-06-30"]
rash = cum[cum["event_term"] == "Rash"]
serious = ((rash["serious"] == "Y") | (rash["outcome"] == "Fatal")).sum()
expected = (f"{len(rash)} reports of rash had been received among "
            f"{len(cum)} reports in total, {serious} of them serious")
if expected not in TEXT:
    problems.append(f"Numbers do not match the data. Expected: {expected}")

if "caused" in TEXT.lower().replace("is the cause", ""):
    problems.append("Contains 'caused'. Do not state causality.")

for p in problems:
    print("ERROR  ", p)
print(f"\n{len(problems)} problem(s)")
sys.exit(1 if problems else 0)
