"""Make a FAKE safety database for the fictional drug DMX-101.
Everything here is invented. Run:  python tools/make_reports.py
Writes data/reports.csv and data/answer_key.csv
"""
import csv
import random
from datetime import date, timedelta

random.seed(101)  # same seed = same fake data every time

N = 500
EVENTS = ["Nausea", "Headache", "Dizziness", "Diarrhoea", "Fatigue",
          "Back pain", "Cough", "Constipation", "Insomnia", "Hypoglycaemia",
          "Urinary tract infection", "Vomiting"]
WEIGHTS = [20, 18, 6, 9, 8, 6, 5, 5, 4, 5, 6, 4]
REPORTERS = ["Physician", "Pharmacist", "Nurse", "Patient"]
OUTCOMES = ["Recovered", "Recovering", "Not recovered", "Unknown"]


def rand_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))


rows = []
for i in range(1, N + 1):
    age = max(18, min(90, int(random.gauss(58, 14))))
    strength = random.choice([10, 25])
    # Planted signal: rash is far more common at 25 mg in people aged 65+
    p_rash = 0.04
    if strength == 25 and age >= 65:
        p_rash = 0.45
    elif strength == 25:
        p_rash = 0.08
    if random.random() < p_rash:
        event = "Rash"
    else:
        event = random.choices(EVENTS, WEIGHTS)[0]
    start = rand_date(date(2025, 6, 1), date(2026, 3, 31))
    onset = start + timedelta(days=random.randint(2, 60))
    receipt = onset + timedelta(days=random.randint(3, 90))
    serious = "Y" if random.random() < (0.30 if event == "Rash" else 0.10) else "N"
    outcome = random.choices(OUTCOMES, [45, 25, 15, 15])[0]
    rows.append({
        "report_id": f"DMX-{i:04d}",
        "receipt_date": receipt.isoformat(),
        "patient_age": age,
        "sex": random.choice(["F", "M"]),
        "strength_mg": strength,
        "start_date": start.isoformat(),
        "onset_date": onset.isoformat(),
        "event_term": event,
        "serious": serious,
        "outcome": outcome,
        "reporter_type": random.choice(REPORTERS),
    })

key = []
ids = list(range(N))
random.shuffle(ids)
pool = iter(ids)


def log(idx, problem, note):
    key.append({"report_id": rows[idx]["report_id"], "problem": problem, "note": note})


for _ in range(10):          # missing age
    idx = next(pool); rows[idx]["patient_age"] = ""
    log(idx, "missing_age", "patient_age left blank")
for _ in range(8):           # missing onset date
    idx = next(pool); rows[idx]["onset_date"] = ""
    log(idx, "missing_onset", "onset_date left blank")
for _ in range(6):           # onset before drug start
    idx = next(pool)
    s = date.fromisoformat(rows[idx]["start_date"])
    rows[idx]["onset_date"] = (s - timedelta(days=10)).isoformat()
    log(idx, "onset_before_start", "onset 10 days before drug start")
for _ in range(5):           # receipt before onset
    idx = next(pool)
    o = rows[idx]["onset_date"] or rows[idx]["start_date"]
    rows[idx]["receipt_date"] = (date.fromisoformat(o) - timedelta(days=5)).isoformat()
    rows[idx]["onset_date"] = o
    log(idx, "receipt_before_onset", "report received 5 days before onset")
for _ in range(5):           # serious = N but outcome says a death
    idx = next(pool)
    rows[idx]["serious"] = "N"; rows[idx]["outcome"] = "Fatal"
    log(idx, "seriousness_conflict", "serious=N but outcome=Fatal")
for _ in range(4):           # impossible age
    idx = next(pool); rows[idx]["patient_age"] = random.choice([0, 150, 212])
    log(idx, "impossible_age", "age outside 18-100")

dups = []
for _ in range(12):          # duplicate reports (new id, same case)
    idx = next(pool)
    d = dict(rows[idx])
    d["report_id"] = f"DMX-{N + len(dups) + 1:04d}"
    dups.append(d)
    key.append({"report_id": d["report_id"], "problem": "duplicate",
                "note": f"duplicate of {rows[idx]['report_id']}"})
rows.extend(dups)

fields = list(rows[0].keys())
with open("data/reports.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
with open("data/answer_key.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["report_id", "problem", "note"])
    w.writeheader(); w.writerows(key)
print(f"Wrote {len(rows)} reports and {len(key)} planted problems.")
