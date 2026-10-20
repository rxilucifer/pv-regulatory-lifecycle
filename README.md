# Pharmacovigilance and Regulatory Lifecycle Suite

A learning project that follows one **fictional** drug, DMX-101, through its safety and regulatory life: safety reports, case processing, signal detection, periodic reporting, risk management, labelling, communications and a regulatory dossier tracker. Documents are written by hand and checked by code wherever possible.

**Fictional and educational.** DMX-101 does not exist. Nothing here is a real label, a real regulatory submission or medical advice, and no real patient data is used.

## Status
- [x] Module 0: Foundation (product profile, style guide, glossary, registers, document checks)
- [x] Module 1: Synthetic safety database
- [ ] Module 2: Case processing
- [ ] Module 3: Reporting clock
- [ ] Module 4: Signal management
- [ ] Module 5: Periodic safety report
- [ ] Module 6: Risk management plan summary
- [ ] Module 7: Labelling
- [ ] Module 8: Communications
- [ ] Module 9: Dossier tracker
- [ ] Module 10: Final quality check and portfolio page

## How to run
1. `pip install -r requirements.txt`
2. `python tools/check_docs.py` checks document control and style

## Documents
- [Product profile](docs/00_product_profile.md)
- [Style guide](docs/01_style_guide.md)
- [Glossary](docs/02_glossary.md)

## Registers
- `registers/document_register.csv` lists every document with its version and status
- `registers/regulatory_references.csv` records each guideline used, with the version and the date it was checked
- `registers/style_rules.csv` lists wording the checker warns about
