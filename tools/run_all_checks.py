"""Final quality check for the whole project. Run:  python tools/run_all_checks.py
Runs every checker, checks cross-references, and confirms the results can be
reproduced by re-running the pipeline from scratch.
"""
import hashlib
import re
import subprocess
import sys
from pathlib import Path

import pandas as pd

results = []  # (name, passed, detail)


def record(name, passed, detail=""):
    results.append((name, passed, detail))


def run(script):
    p = subprocess.run([sys.executable, script], capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


# 1. Files are not empty and contain no pasted wrapper lines
bad = []
for folder in ["docs", "registers", "tools", "data"]:
    for f in Path(folder).rglob("*"):
        if f.is_file() and f.suffix in {".md", ".csv", ".py"}:
            if f.stat().st_size == 0:
                bad.append(f"{f} is empty")
                continue
            for line in f.read_text().splitlines():
                if line.startswith("cat > ") or line.strip() == "EOF":
                    bad.append(f"{f} has a pasted wrapper line")
                    break
readme = Path("README.md").read_text()
if len(readme.strip()) == 0 or "cat > README" in readme:
    bad.append("README.md is empty or has a wrapper line")
record("Files are not empty and have no wrapper lines", not bad, "; ".join(bad))

# 2. The three checkers
for script in ["tools/check_docs.py", "tools/check_dossier.py", "tools/check_dhpc.py"]:
    code, out = run(script)
    record(f"{script} passes", code == 0, "" if code == 0 else out.strip()[-300:])

# 3. Cross-references: every PV-nnn and R-nn mentioned must exist
doc_ids = set(pd.read_csv("registers/document_register.csv", dtype=str)["doc_id"])
ref_ids = set(pd.read_csv("registers/regulatory_references.csv", dtype=str)["ref_id"])
missing = []
for f in list(Path("docs").glob("*.md")) + [Path("README.md")]:
    text = f.read_text()
    for pv in set(re.findall(r"\bPV-\d{3}\b", text)):
        if pv not in doc_ids:
            missing.append(f"{f.name}: {pv}")
    for r in set(re.findall(r"\bR-\d{2}\b", text)):
        if r not in ref_ids:
            missing.append(f"{f.name}: {r}")
record("Every PV-nnn and R-nn mentioned exists in a register", not missing,
       "; ".join(sorted(missing)))

# 4. References that are cited in documents should have been looked up
refs = pd.read_csv("registers/regulatory_references.csv", dtype=str).fillna("")
cited = set()
for f in Path("docs").glob("*.md"):
    cited |= set(re.findall(r"\bR-\d{2}\b", f.read_text()))
not_looked_up = sorted(
    r for r in cited
    if refs.loc[refs["ref_id"] == r, "date_checked"].eq("").all())
record("Every reference cited in a document has a date checked", not not_looked_up,
       "not yet looked up: " + ", ".join(not_looked_up))

# 5. README: Modules 0 to 9 ticked
unticked = [m for m in re.findall(r"- \[ \] Module (\d+)", readme) if int(m) < 10]
record("README shows Modules 0 to 9 as done", not unticked,
       "unticked: " + ", ".join(unticked))

# 6. Reproducibility: re-run the pipeline and compare every output
outputs = ["data/reports.csv", "data/answer_key.csv", "data/qc_findings.csv",
           "data/reports_clean.csv", "data/submission_log.csv",
           "data/reporting_clock.csv", "data/signal_results.csv",
           "data/psur_line_listing.csv", "docs/06_psur_draft.md"]
before = {o: sha(o) for o in outputs}
pipeline = ["tools/make_reports.py", "tools/qc_reports.py",
            "tools/make_submission_log.py", "tools/reporting_clock.py",
            "tools/signal_detection.py", "tools/make_psur.py"]
failed = [s for s in pipeline if run(s)[0] != 0]
after = {o: sha(o) for o in outputs}
changed = [o for o in outputs if before[o] != after[o]]
record("Pipeline re-runs and every output is identical", not failed and not changed,
       "failed: " + ", ".join(failed) + " changed: " + ", ".join(changed))

# 7. QC scoring against the answer key
code, out = run("tools/score_qc.py")
ok = code == 0 and "Missed:           0" in out and "False alarms:     0" in out
record("QC finds all planted problems with no false alarms", ok,
       "" if ok else out.strip()[-300:])

# 8. No .DS_Store tracked by git
g = subprocess.run(["git", "ls-files"], capture_output=True, text=True)
if g.returncode == 0:
    record("No .DS_Store file is tracked", ".DS_Store" not in g.stdout)

print("\nFINAL QUALITY CHECK\n")
for name, passed, detail in results:
    print(("PASS  " if passed else "FAIL  ") + name)
    if not passed and detail:
        print("      " + detail)
n_fail = sum(1 for r in results if not r[1])
print(f"\n{len(results) - n_fail} of {len(results)} checks passed")
sys.exit(1 if n_fail else 0)
