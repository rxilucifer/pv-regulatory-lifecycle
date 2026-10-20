"""Check the dossier tracker and show a status summary.
Run:  python tools/check_dossier.py
"""
import sys
import pandas as pd

STATUSES = ["Not started", "Draft", "Not in scope"]

tracker = pd.read_csv("registers/dossier_tracker.csv", dtype=str).fillna("")
register = pd.read_csv("registers/document_register.csv", dtype=str).fillna("")
known_ids = set(register["doc_id"])

problems = []
for _, r in tracker.iterrows():
    sec = r["ctd_section"]
    if r["status"] not in STATUSES:
        problems.append(f"{sec}: status '{r['status']}' is not one of {STATUSES}")
    if sec.split(".")[0] != r["module"]:
        problems.append(f"{sec}: section does not belong to module {r['module']}")
    ids = [i.strip() for i in r["source_documents"].split(";") if i.strip()]
    for i in ids:
        if i not in known_ids:
            problems.append(f"{sec}: source document {i} is not in the document register")
    if r["status"] == "Draft" and not ids:
        problems.append(f"{sec}: status is Draft but no source document is listed")
    if r["status"] != "Draft" and ids:
        problems.append(f"{sec}: has source documents but status is {r['status']}")
if tracker["ctd_section"].duplicated().any():
    problems.append("A CTD section is listed more than once")

print(f"Sections tracked: {len(tracker)}")
print(tracker["status"].value_counts().to_string())
print("\nBy module:")
print(pd.crosstab(tracker["module"], tracker["status"]).to_string())
for p in problems:
    print("ERROR  ", p)
print(f"\n{len(problems)} problem(s)")
sys.exit(1 if problems else 0)
