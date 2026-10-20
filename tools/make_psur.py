"""Build a DRAFT periodic safety update report (PSUR) for fictional DMX-101.
Section order follows the Indian MAH guidance (R-11). All data is invented.
Run:  python tools/make_psur.py
Writes docs/06_psur_draft.md and data/psur_line_listing.csv
"""
import pandas as pd

START, END = pd.Timestamp("2026-01-01"), pd.Timestamp("2026-06-30")
LISTED = ["Nausea", "Headache", "Dizziness"]

df = pd.read_csv("data/reports_clean.csv", parse_dates=["receipt_date"])
clock = pd.read_csv("data/reporting_clock.csv")
df = df.merge(clock[["report_id", "late"]], on="report_id")
df["serious_flag"] = (df["serious"] == "Y") | (df["outcome"] == "Fatal")
inter = df[(df["receipt_date"] >= START) & (df["receipt_date"] <= END)]
cum = df[df["receipt_date"] <= END]

# Appendix: line listing of interval cases
cols = ["report_id", "patient_age", "sex", "strength_mg", "start_date",
        "onset_date", "event_term", "serious", "outcome"]
ll = inter[cols].copy()
ll["causality"] = "Not assessed"
ll.to_csv("data/psur_line_listing.csv", index=False)


def tab(frame):
    t = frame.groupby("event_term").agg(reports=("report_id", "count"),
                                        serious=("serious_flag", "sum"))
    t["listed"] = ["Yes" if e in LISTED else "No" for e in t.index]
    return t


ti, tc = tab(inter), tab(cum)
tt = tc.join(ti, lsuffix="_cum", rsuffix="_int").fillna(0)
tt = tt.sort_values("reports_cum", ascending=False)
rows = "\n".join(
    f"| {e} | {r.listed_cum} | {int(r.reports_int)} | {int(r.serious_int)} "
    f"| {int(r.reports_cum)} | {int(r.serious_cum)} |" for e, r in tt.iterrows())

rash_i = int((inter["event_term"] == "Rash").sum())
rash_c = int((cum["event_term"] == "Rash").sum())
late_i = int(inter[inter["serious_flag"]]["late"].sum())
ser_i = int(inter["serious_flag"].sum())

md = f"""# Periodic Safety Update Report (Draft): DMX-101

| Field | Value |
|---|---|
| Document ID | PV-007 |
| Title | Periodic Safety Update Report (Draft): DMX-101 |
| Version | 0.1 |
| Status | Draft |
| Date | 2026-10-20 |
| Author | Dr. Raj Akil Nomani |

This is a practice document. DMX-101 is a fictional drug and all data is invented. Section order follows the Indian MAH guidance (R-11).

## 1. Title page
Product: DMX-101 tablets, 10 mg and 25 mg. MAH: Example Pharma Ltd (fictional). Reporting interval: {START.date()} to {END.date()}. Data lock point: {END.date()}. Submission due 30 calendar days after the end of the interval.

## 2. Introduction
DMX-101 is a once-daily add-on tablet for type 2 diabetes (PV-001). This report covers the interval above and also gives cumulative figures.

## 3. Current worldwide marketing authorisation status
Not applicable. DMX-101 is fictional and has no authorisation.

## 4. Actions taken in the reporting interval for safety reasons
None. No regulatory or company safety action has been taken in this exercise.

## 5. Changes to reference safety information
None. The reference safety information lists nausea, headache and dizziness (PV-001). Rash is not listed.

## 6. Estimated patient exposure
Not available. This exercise has no sales or patient exposure data, so no reporting rates can be calculated.

## 7. Individual case histories
### 7.2 Cases received from India
{len(inter)} reports were received in the interval ({len(cum)} cumulative). The line listing is in data/psur_line_listing.csv. Causality has not yet been assessed for these cases.

### 7.5 Summary tabulation of post-marketing reports
Serious means marked serious or with a Fatal outcome.

| Event | Listed in label | Reports (interval) | Serious (interval) | Reports (cumulative) | Serious (cumulative) |
|---|---|---|---|---|---|
{rows}

## 8. Studies
No studies are included in this exercise.

## 9. Other information
### 9.3 Overview of signals
| Signal | Status | Source |
|---|---|---|
| Rash | New, ongoing | PV-005 |

Rash had {rash_i} reports in the interval and {rash_c} cumulatively. It met the screening rule, mainly at 25 mg and in patients aged 65 and over (PV-005). PV-005 used all reports in the database, including some received after the data lock point. It has not been confirmed as caused by DMX-101.

### Timeliness of reporting
{late_i} of {ser_i} serious reports in the interval were sent after the 15-day limit (PV-006).

## 10. Overall safety evaluation
Safety: the main finding is the rash signal above. Benefit: no efficacy data is included, so benefit has not been evaluated and a benefit-risk analysis cannot be completed.

## 11. Conclusion
The rash signal needs case-by-case review and a decision on validation. Late submission of serious reports needs a corrective action. The reference safety information has not been changed.

## 12. Appendix
Line listing of cases in the interval: data/psur_line_listing.csv.
"""
with open("docs/06_psur_draft.md", "w") as f:
    f.write(md)
print(f"Interval reports: {len(inter)}, cumulative: {len(cum)}")
print(f"Rash interval/cumulative: {rash_i}/{rash_c}")
print(f"Serious in interval: {ser_i}, late: {late_i}")
