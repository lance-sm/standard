# DECISIONS.md — CRM audit decisions ledger

Standing decisions Lance has made about findings in the monthly HubSpot audit. The audit routine reads this file before each run and **does not re-propose anything recorded here**. One line per decision. Add entries in an attended session; the audit itself never writes here.

Format: `YYYY-MM-DD | finding (property / record / rule) | decision (accepted / rejected / deferred until …) | note`

| Date | Finding | Decision | Note |
|---|---|---|---|
| — | No decisions recorded yet. First ledger created by the 2026-11-02 run; the 2026-09-09 baseline run left no ledger in this repo. | — | — |

Candidate decisions from AUDIT-2026-11-02.md that only Lance can make (record the answer here):
- Keep or archive `deal_stage` ("Deal Stage.") after reconciling the 10 conflicts.
- Delete the "ARCHIVE - Do Not Use" pipeline (irreversible; 27 deals still carry archive-stage dates).
- Owner-seat display name: "Badlands Security Company" vs "Lance Smith".
- Whether conference-contact companies (GSX, NFPA, ALOA imports) belong in COMPANY at all, or should be tagged Ancilary on import.
- Whether sequence steps should keep auto-creating tasks.
