"""Look for safety signals in the cleaned fake DMX-101 reports.
Run:  python tools/signal_detection.py
Writes data/signal_results.csv
"""
import pandas as pd

df = pd.read_csv("data/reports_clean.csv")
LISTED = ["Nausea", "Headache", "Dizziness"]  # events in the fictional label

# Only use rows where age is believable (the others are for follow-up)
df = df[df["patient_age"].between(18, 100)].copy()
df["event_listed"] = df["event_term"].isin(LISTED)

groups = {
    "25 mg": df["strength_mg"] == 25,
    "Age 65+": df["patient_age"] >= 65,
    "25 mg and age 65+": (df["strength_mg"] == 25) & (df["patient_age"] >= 65),
}


def prr_table(in_group):
    """PRR of each event: group vs everyone else."""
    rows = []
    n_in, n_out = in_group.sum(), (~in_group).sum()
    for event in sorted(df["event_term"].unique()):
        is_ev = df["event_term"] == event
        a = (is_ev & in_group).sum()          # event, in group
        b = n_in - a                          # other events, in group
        c = (is_ev & ~in_group).sum()         # event, not in group
        d = n_out - c                         # other events, not in group
        if a == 0 or c == 0:
            continue
        prr = (a / (a + b)) / (c / (c + d))
        n = a + b + c + d
        chi2 = n * (a * d - b * c) ** 2 / ((a + b) * (c + d) * (a + c) * (b + d))
        rows.append({"event": event, "n_in_group": a, "PRR": round(prr, 2),
                     "chi2": round(chi2, 1)})
    return pd.DataFrame(rows)


results = []
for name, mask in groups.items():
    t = prr_table(mask)
    t["group"] = name
    t["listed_in_label"] = t["event"].isin(LISTED)
    # Screening rule: at least 3 reports, PRR >= 2 and chi2 >= 4
    t["signal"] = (t["n_in_group"] >= 3) & (t["PRR"] >= 2) & (t["chi2"] >= 4)
    results.append(t)

res = pd.concat(results)
res.to_csv("data/signal_results.csv", index=False)

print(f"Reports used: {len(df)}")
print("\nUnlisted events by number of reports:")
unl = df[~df["event_listed"]]["event_term"].value_counts().head(5)
print(unl.to_string())
print("\nEvents that meet the screening rule:")
print(res[res["signal"]].sort_values(["group", "PRR"], ascending=[True, False])
      [["group", "event", "n_in_group", "PRR", "chi2", "listed_in_label"]]
      .to_string(index=False))
