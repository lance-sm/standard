# Meeting Prep + Deal Hot List — routine prompt

Paste the block below as the prompt of the daily **Meeting Prep** scheduled routine.
Suggested schedule: `8 10 * * 1-5` UTC (~6:08am ET), so it lands before the 7am block.

---

Build Lance's daily meeting prep and deal hot list, then email both to lance@badlandssecurity.com with the subject "Meeting Prep — [date]". HubSpot portal 50955967. Run fast — this is a routine daily build, not a research project. No task list, no subagents, no clarifying questions (Lance is not necessarily watching at 6am). Do not repeat this brief back — just send the email.

THIS PROMPT IS THE COMPLETE SPEC. Scheduled cloud runs usually cannot reach project memory or Lance's OneDrive folders — both require his desktop app to be online, and it often is not this early. Do not stall, skip, or degrade the run trying to read them. Everything you need is below.

## REFERENCE DATA

Internal domains (never treat as external): `tuckersfarm.com`, `badlandssecurity.com`, `websterlock.com`.

HubSpot deal pipeline: `917378060`. Deal owner: `87401864`.

Deal stage IDs:
- Initial Meeting `1401758003`
- NDA Sent `1399091991`
- NDA Signed `1399091992`
- IOI `1399091994`
- Management Meeting `1399091993`
- Due Diligence `1399232681`
- LOI `1399091995`
- On Hold `1399238912`
- Closed `1399091996`
- Lost `1399091997`
- Pass `1399238471`

Live stages = Initial Meeting, NDA Sent, NDA Signed, IOI, Management Meeting, Due Diligence, LOI. Everything else is parked.

Two contact properties are MISSPELLED in HubSpot. Use the misspellings or the query returns nothing: `call_attepts` (sic) and `calll_back_date` (sic, three l's). The `banker` property carries the label "Contact Type"; values are Banker / Broker / Industry Contact / Seller.

Broker code names: read `meeting-prep/aliases.json` from the `lance-sm/standard` repo if reachable; otherwise use the mapping inline at the end of this prompt. Deals often appear in email under a broker's project code name while the HubSpot deal is filed under the target company's name. Always resolve code names before deciding a deal has no record.

## PART 1 — MEETING PREP

Pull today's calendar. Identify external meetings: any meeting where at least one attendee's domain is not an internal domain, or the title/context clearly signals a seller, broker, or industry contact. If unsure, include it. Skip internal-only and personal meetings.

For each external meeting, in chronological order, look up the attendee/company in HubSpot (contact, company, open deals — include stage and value if an open deal exists), pull relevant email thread history, and search Granola for past transcripts with that contact or company (full history, no date cutoff). If no HubSpot record exists, use web search for a company overview; only fall back to ZoomInfo/Apollo enrichment if web search is too thin, and report any credits spent. If multiple external companies are on one meeting, combine into a single note.

Format each note: (a) 3–5 bullet company overview, (b) open follow-ups and action items from the last touch across HubSpot/email/Granola, noting "no prior record" if none, (c) 2–3 highest-impact questions to ask.

If there are no external meetings today, say so in one line and go straight to Part 2.

## PART 2 — DEAL HOT LIST

Append a section titled "DEAL HOT LIST".

Pull all deals in live stages. For each, determine the **last real touch** by taking the most recent of:
- HubSpot `notes_last_contacted` / `hs_last_activity_date`
- any sent email to that contact or company domain
- any calendar event with them
- any Granola note referencing them

HubSpot alone is unreliable — Lance does not log everything. A deal whose only recent evidence is an email or a dinner is NOT stale.

**TOUCH TODAY** — deals with no real touch in 14+ days, oldest first. Give name, stage, days stale, and the date and source of the last touch. Suppress any deal that already has a future meeting booked.

**SCHEDULED — NO ACTION** — the suppressed ones, one line each with the meeting date, plus anything that HubSpot shows as stale but the blended evidence clears.

**NEEDS A HUBSPOT RECORD** — companies with real email or calendar activity in the last 30 days that have no deal record. Resolve broker code names against the alias list first. Skip vendors, IT suppliers, recruiters, and internal.

**FIX** — records whose stage contradicts observed activity (e.g. filed as Pass while an IOI is due).

**TIME-SENSITIVE** — conference travel inside 7 days with fewer than 5 meetings booked, IOI/LOI deadlines inside 7 days, and internal meetings that collide with conference days.

## PART 3 — REPLY-TO-LOG

Before building today's list, search for replies to yesterday's prep email. Parse any shorthand log lines — company name first, then free text, e.g.:

```
Abbey - dinner 9/8 w/ Webster + Cosmic, next: call Thurs
Precision Lock - dead, move to Pass
Able Fire - create deal, Initial Meeting, called 9/9
```

Write them to HubSpot as notes, stage changes, or new deals as appropriate. Associate new deals to the existing company record when one exists — search companies before creating one. Confirm what you wrote in a short block at the top of today's hot list. If a line is ambiguous, write nothing for it and list it under "couldn't parse".

## FALLBACK ALIASES

If `aliases.json` is unreachable:
- Project Firehouse (Flatirons Capital / Connor Slivocka) → New York City Alarm — UNCONFIRMED
- Fire Suppression Co (Hedgestone / Anthony Perrone) → STAT Fire Sprinkler — UNCONFIRMED
- Project Ignite (Dinan Capital / Aryan) → Boston Fire - Project Ignite — confirmed
