# Dossier Tracker Notes

| Field | Value |
|---|---|
| Document ID | PV-012 |
| Title | Dossier Tracker Notes |
| Version | 0.1 |
| Status | Draft |
| Date | 2026-10-20 |
| Author | Dr. Raj Akil Nomani |

This is a practice document. DMX-101 is a fictional drug and all data is invented.

## Purpose
Explains the dossier tracker (registers/dossier_tracker.csv), which shows how the documents in this project map onto the sections of a Common Technical Document (CTD).

## Structure used
The CTD has five modules (R-06, ICH M4):

| Module | Content | Common to all regions |
|---|---|---|
| 1 | Administrative and prescribing information | No. Set by each regulator |
| 2 | Summaries and overviews | Yes |
| 3 | Quality | Yes |
| 4 | Nonclinical study reports | Yes |
| 5 | Clinical study reports | Yes |

## Result
13 sections are tracked: 2 have a draft, 4 are not started and 7 are outside this project (no manufacturing, nonclinical or clinical study data exists here).

| Section | Drafted from |
|---|---|
| 1.2 Region-specific documents and prescribing information | PV-009 (proposed label wording) |
| 2.7 Clinical summary: safety | PV-005 and PV-007 (post-marketing reports only) |

## How the check works
tools/check_dossier.py confirms that every status is one of three allowed values, that every section sits in the right module, that every source document is in the document register, and that a draft section always has a source document.

## Limits
- Only the section numbers and titles shown in ICH M4 were used. Their detailed content requirements were not reviewed.
- Which Indian authority requires the CTD, and what Module 1 must contain in India, was not looked up.
- A draft status means a practice document exists. It does not mean the section is complete or ready to submit.
- Safety information in a real dossier would also draw on clinical trial data, which this project does not have.
