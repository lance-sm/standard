# CLAUDE.md

Repo-wide instructions for Claude Code sessions on this repo (Badlands working repo, account: lance@badlandssecurity.com). Kept short on purpose: the rules for each recurring job live in a skill that loads only when that job comes up. Restructured 2026-09-11; nothing was dropped, only moved.

## Who this is for

Lance Smith, Corporate Development at Badlands Security: an M&A holdco buying independent access control, locksmith, and fire and life safety businesses in the Northeast and Mid-Atlantic. HubSpot portal 50955967 (Sales Hub Pro, timezone US/Eastern). Deals are sourced mostly by proprietary outreach: cold calls through Aircall, HubSpot sequences, and email.

## Read-before rules (these are not optional)

- **Any cold-call ask** — a list of phone numbers from HubSpot, a dial string, the daily dials, a call list, a call brief, who to call today — read `.claude/skills/cold-call/SKILL.md` in full before touching HubSpot. It is the complete spec, moved verbatim from this file. The live "Daily Dials" routine carries only a two-line prompt and depends on that skill for every rule.
- **Any outreach copy** — email, sequence step, SMS, voicemail, call opener, LinkedIn note, follow-up, breakup, re-engagement, template, HubSpot sequence build — read `.claude/skills/outreach-writing/SKILL.md`, then `outreach/SAGARIS-RULES.md`. Lance adopted those rules as gospel on 2026-09-11.
- **Any market map, state landscape, independents roster, or acquisition history** — the `state-market-map` skill in `.claude/skills/`.

## Invariants (never break these, whatever the ask)

- A refusal, "not selling", "out of business" or do-not-call written in a contact's `call_notes` is permanent. Nothing re-opens it.
- Open deals (contact **or** company; company level is authoritative) and customers are never dialed, emailed or sequenced.
- NYC metro is decided by `migration/routines/nyc_metro_cities.json`, matched on `city` within the contact's own `state`. Never re-derive it from memory; add missing cities to the file.
- HubSpot writes are limited to what a skill explicitly authorizes. For the cold-call list that is exactly two: `daily_call_list_date` on shipped contacts and `call_tier` = Excluded on notes-screen refusals.
- Third-party DNC registry flags (ZoomInfo, national registry) are irrelevant to M&A outreach: never drop a contact over one, never mention them.
- The daily call brief docx and its emailed link are mandatory on every cold-call run.

## Where things live

| Path | What it is | Verified |
|---|---|---|
| `.claude/skills/cold-call/SKILL.md` | Complete cold-call list spec (screening, cadence, brief, write-backs, delivery) | 2026-09-11 |
| `.claude/skills/outreach-writing/SKILL.md` + `outreach/SAGARIS-RULES.md` | Outreach writing standard, verbatim rules, five sequence shapes | 2026-09-11 |
| `.claude/skills/state-market-map/` | State market map skill | — |
| `hubspot/sequences/seller-fast-track.md` | HubSpot build plan for the 17-touch seller sequence | 2026-09-11 |
| `migration/routines/nyc_metro_cities.json` | Canonical NYC-metro city list per state | 2026-09-11 |
| `migration/routines/routines.json` | The old-account routine export. The "Cold Call Today" prompt inside it is still the strictest written spec and the cold-call skill tells you to read it. | exported 2026-08-31 |
| `routines/LIVE.md` | The routines actually running on this account, with trigger ids and crons | 2026-09-11 |
| `daniel-sync/` | Templates and scripts for the Tuesday Daniel sync routine | — |
| `migration/` | Historical: the account-move kit. Its routine inventory no longer matches the live account; see `routines/LIVE.md`. | 2026-08-31 |
