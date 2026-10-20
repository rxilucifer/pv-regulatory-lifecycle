# Style guide

| Field | Value |
|---|---|
| Document ID | PV-002 |
| Title | Style guide |
| Version | 0.1 |
| Status | Draft |
| Date | 2026-10-20 |
| Author | Dr. Raj Akil Nomani |

This guide sets the wording and layout used in every document in this project. The checker (`tools/check_docs.py`) warns about some of these rules.

## 1. General rules

- Write plainly. Short sentences, active voice, one idea per sentence.
- Use sentence case for headings.
- Say what you know and what you do not know. Do not use filler such as obviously or clearly.
- Every number in a document must come from a script or a cited source, and not from memory.
- Leave no unfinished markers in a document that is marked Approved.

## 2. Terms to use

| Use | Avoid | Reason |
|---|---|---|
| Adverse event | Side effect | An adverse event is any untoward medical occurrence, whether or not the medicine is the cause |
| Adverse reaction | Side effect | Use this only when a causal link to the medicine is at least a reasonable possibility |
| Serious | Very serious | Seriousness is yes or no, based on set criteria. It is not a degree |
| Severe | Serious (for intensity) | Severe describes how intense an event is. Serious describes the outcome or criteria met |
| Reported | Complained of | Neutral wording for what the patient or reporter said |
| Experienced | Suffered from | Neutral wording |
| Is associated with | Caused | Do not state causality unless it was formally assessed |
| Participant | Patient (in a trial) | Use participant for people in a clinical trial and patient for people who take a marketed medicine |

## 3. Seriousness criteria

An event is serious if it meets at least one of these criteria. Confirm the wording against the current guideline in the references register before using it in a regulatory document.

1. Results in death
2. Is life-threatening
3. Requires hospitalisation or prolongs existing hospitalisation
4. Results in persistent or significant disability or incapacity
5. Is a congenital anomaly or birth defect
6. Is another medically important event

## 4. Outcome terms

Describe the outcome of an event with one of these terms: recovered or resolved, recovering or resolving, not recovered or not resolved or ongoing, recovered or resolved with sequelae, fatal, unknown.

## 5. Causality terms

Causality assessments use the WHO-UMC categories: Certain, Probable or likely, Possible, Unlikely, Conditional or unclassified, and Unassessable or unclassifiable. Write the category name exactly, and give the reason for the choice in one sentence.

## 6. Dates, numbers and units

- Write dates as 1 January 2026 in text, and as 2026-01-01 in tables and data files.
- Use the 24-hour clock.
- Write numbers below ten in words, except for measurements, ages, doses and percentages.
- Give a unit with every dose, and write the dose form in full on first use.
- Write the percentage sign without a space, for example 8%.

## 7. Abbreviations

Write the full term at first use with the abbreviation in brackets, for example individual case safety report (ICSR). Add every abbreviation to the [glossary](02_glossary.md).

## 8. Case narratives

- Write in the past tense, in time order.
- Include, in this order: the reporter and the source, the patient (age group and sex only), the suspect medicine with dose and dates, the medical history and other medicines, the event with onset date and course, treatment given, outcome, and the causality assessment with the reason.
- Never include a name, a full date of birth or any detail that could identify a real person. All patients in this project are fictional.

## 9. Citing sources

- Name the document and the version, and record it in `registers/regulatory_references.csv` with the date you checked it.
- Summarise in your own words. Do not copy text from a label or a guideline.

## 10. Document control

- Every document has a control table with a document ID, title, version, status and date.
- The ID, title, version and status must match `registers/document_register.csv`.
- Allowed statuses: Draft, In review, Approved, Superseded.
- Change the version and the date whenever the content changes.
