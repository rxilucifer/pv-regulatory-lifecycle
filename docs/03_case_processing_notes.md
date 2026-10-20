# Case Processing and Data Quality Notes

| Field | Value |
|---|---|
| Document ID | PV-004 |
| Title | Case Processing and Data Quality Notes |
| Version | 0.1 |
| Status | Draft |
| Date | 2026-10-20 |
| Author | Dr. Raj Akil Nomani |

## Purpose
Describes how the 512 fictional DMX-101 reports were checked before any analysis.

## Checks applied
| Check | What it looks for | Action |
|---|---|---|
| Duplicate | Same case details under a different report ID | Remove later copy, keep the first |
| Missing age | Age blank | Keep, list for follow-up |
| Missing onset date | Onset date blank | Keep, list for follow-up |
| Impossible age | Age under 18 or over 100 | Keep, list for follow-up |
| Onset before start | Event began before the drug was started | Keep, list for follow-up |
| Receipt before onset | Report received before the event began | Keep, list for follow-up |
| Seriousness conflict | Marked not serious but outcome is Fatal | Keep, list for follow-up |

## Result
All 50 planted problems were found, with no false alarms. The checks were written for known problems, so real data would need more checks.

## Limits
- All data is invented. No real patient is involved.
- Duplicates were found only by exact match. Real duplicate detection also needs near matches, such as a different date format or a missing field.
