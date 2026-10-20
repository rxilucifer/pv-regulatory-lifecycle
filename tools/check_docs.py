"""
Module 0: document control and style checks.

Reads registers/document_register.csv and registers/style_rules.csv and checks
every Markdown file in docs/.

Errors (stop the build): missing or empty files, missing control fields,
values that disagree with the register, unregistered files, leftover placeholders.
Warnings (advice): wording that the style rules say to avoid.
"""
import re
import sys
from pathlib import Path

import pandas as pd

DOCS = Path("docs")
FIELDS = ["Document ID", "Title", "Version", "Status", "Date"]
MATCH_FIELDS = {"Document ID": "doc_id", "Title": "title",
                "Version": "version", "Status": "status"}
ALLOWED_STATUS = {"Draft", "In review", "Approved", "Superseded"}
PLACEHOLDERS = ["TODO", "XXX", "(write your name)", "WRITE HERE", "lorem ipsum", "Your Name Here", "cat >"]
EXEMPT_FROM_STYLE = {"01_style_guide.md", "02_glossary.md"}

register = pd.read_csv("registers/document_register.csv", dtype=str).fillna("")
rules = pd.read_csv("registers/style_rules.csv", dtype=str).fillna("")

errors, warnings = [], []


def field_value(text, field):
    match = re.search(rf"\|\s*{re.escape(field)}\s*\|\s*(.+?)\s*\|", text)
    return match.group(1) if match else None


# ---------- Register checks ----------
if register["doc_id"].duplicated().any():
    errors.append("The register has a repeated document ID")

for row in register.itertuples(index=False):
    if row.status not in ALLOWED_STATUS:
        errors.append(f"{row.doc_id}: status '{row.status}' is not one of {sorted(ALLOWED_STATUS)}")

registered_files = set(register["file"])
for path in sorted(DOCS.glob("*.md")):
    if path.name not in registered_files:
        errors.append(f"{path.name}: not listed in registers/document_register.csv")

# ---------- Document checks ----------
for row in register.itertuples(index=False):
    path = DOCS / row.file
    if not path.exists():
        errors.append(f"{row.doc_id}: file docs/{row.file} does not exist")
        continue

    text = path.read_text(encoding="utf-8")
    if len(text) < 300:
        errors.append(f"{row.doc_id}: docs/{row.file} looks empty or too short ({len(text)} characters)")
        continue

    for field in FIELDS:
        value = field_value(text, field)
        if value is None:
            errors.append(f"{row.doc_id}: the control table is missing '{field}'")
        elif field in MATCH_FIELDS:
            expected = getattr(row, MATCH_FIELDS[field])
            if value != expected:
                errors.append(f"{row.doc_id}: '{field}' is '{value}' in the document but '{expected}' in the register")

    for number, line in enumerate(text.splitlines(), start=1):
        for placeholder in PLACEHOLDERS:
            if placeholder.lower() in line.lower():
                errors.append(f"{row.doc_id}: line {number} still contains '{placeholder}'")
        if path.name not in EXEMPT_FROM_STYLE:
            for rule in rules.itertuples(index=False):
                if re.search(rf"\b{re.escape(rule.phrase)}\b", line, flags=re.IGNORECASE):
                    warnings.append(f"{row.doc_id}: line {number}: '{rule.phrase}' -> {rule.preferred} ({rule.reason})")

# ---------- Report ----------
print(f"Documents in the register: {len(register)}")
print(f"Markdown files found in docs/: {len(list(DOCS.glob('*.md')))}\n")
for message in errors:
    print("ERROR  ", message)
for message in warnings:
    print("WARNING", message)
print(f"\n{len(errors)} error(s), {len(warnings)} warning(s)")
if errors:
    sys.exit(1)
print("Document control checks passed.")
