# meeting-prep

The daily **Meeting Prep + Deal Hot List** routine: what runs, why it works this way, and how to change it.

## What it does

Every weekday morning it emails `lance@badlandssecurity.com` one message with two parts:

1. **Meeting prep** — for each external meeting on today's calendar: a company overview, open follow-ups from the last touch, and 2–3 questions to ask.
2. **Deal hot list** — live deals that have gone cold, deals missing from HubSpot entirely, and stage errors.

It also parses replies to yesterday's email and writes them back to HubSpot, so logging costs a 30-second reply instead of a CRM session.

## Files

| File | Purpose |
|---|---|
| `prompt.md` | The complete routine prompt. Paste into the scheduled task. |
| `aliases.json` | Broker code name → HubSpot deal. Prevents false "missing record" hits. |

## Why staleness is blended, not read from HubSpot

`notes_last_contacted` lags badly because not every touch gets logged. Measured on 2026-09-10 against the live pipeline:

- **12 of 14** live deals showed 13+ days stale in HubSpot.
- After cross-checking sent mail, calendar and Granola, only **9** were genuinely cold.
- **IDR Technology** showed 9 days stale but had a meeting booked for Sep 17.
- **Paragon** showed no logged contact ever, with a meeting booked Sep 15.
- **Abbey Locksmiths** showed 27 days; Lance had dinner with them Sep 8.
- **6 deals didn't exist in HubSpot at all** — Able Fire, Ambush Alarm, Lock City and Zebra Lock were created 2026-09-10; the other two turned out to be broker code names for deals that already existed.

Ranking on the HubSpot field alone produces a list that is mostly noise. Hence the blend, the suppression rule, and `aliases.json`.

## Broker code names

Bankers run processes under project names. The email thread says "Project Firehouse"; the HubSpot deal says "New York City Alarm". Without the alias map the hot list reports a live deal as an orphaned record every single day.

Two entries in `aliases.json` are marked `"confirmed": false` — the pair is right but which-maps-to-which is inferred. A third (Project Phoenix → Telenet VoIP) is inferred from the DGP Capital call on 2026-08-27. Fix and flip `confirmed` as they're verified.

## Installing

Paste the block in `prompt.md` into the Meeting Prep scheduled routine on Lance's account. Suggested cron: `8 10 * * 1-5` UTC (~6:08am ET), landing before the 7am block.

## Note on routines.json

`migration/routines/routines.json` holds a snapshot of six scheduled routines. **Meeting Prep is not among them** — it was created after that snapshot and has been running unversioned. Anything added to the account since then is in the same position. Worth re-syncing that file, and adding this routine to it, so the account and the repo agree.

## Related

- `../daniel-sync/` — agenda and live-deal spreadsheet builders.
- *Cold Call Today* (in `routines.json`) builds a 50-contact Aircall list each weekday at 9am ET. That's the queue for the 10–11am and 4–5pm call blocks; this routine covers follow-up on deals already in flight.
