# CLAUDE.md

Repo-wide instructions for Claude Code sessions on this repo (Badlands working repo, account: lance@badlandssecurity.com).

## Cold-call phone list (HubSpot seller outreach)

The recurring "50 phone numbers from HubSpot" routine. Follow all of this without being asked.

### Output format
- Paste the CSV directly in the chat reply as plain text Lance can copy-paste — never a file attachment alone.
- Prefix every phone number with `+1`.
- Comma-separated on one line (not one per line), no header row, no extra columns.

### Who goes on the list
- Sellers only (Contact Type / `banker` = `Seller`; exclude Broker, Banker, Industry Contact).
- Prefer mobile (`mobilephone`) over landline (`phone`); landline only when no mobile is on file.
- **NYC metro only.** The target is anyone who could reasonably service NYC. Filter on the company's `city`, not just `state` — a NY/NJ/CT state filter is far too broad and pulls in Buffalo, Syracuse, Albany, Hartford and South Jersey, none of which can service NYC.
  - **In:** the 5 boroughs (Manhattan, Brooklyn, Queens, Bronx, Staten Island); Long Island (Nassau, Suffolk); Westchester, Rockland, Putnam, lower Hudson Valley; northern NJ (Bergen, Hudson, Essex, Passaic, Union, Morris, and Middlesex up to about Edison/New Brunswick); southern CT, meaning Fairfield County (Greenwich, Stamford, Norwalk, Bridgeport, Danbury).
  - **Out:** upstate NY (Albany, Syracuse, Rochester, Buffalo, and towns near them such as Delmar, Selkirk, Clifton Park); CT beyond Fairfield County (Hartford, New Haven, Wallingford, Milford); NJ shore and South Jersey (Brick, Manasquan, Mullica Hill); PA and MA entirely.
  - Watch for name collisions when filtering on city — Clifton NJ is in, Clifton Park NY is out.
- Exclude `call_tier = Excluded`.
- **DNC — two different things, treat them differently.**
  - **Third-party registry flags (ZoomInfo `mobilePhoneDoNotCall`, national DNC registry): ignore them.** Those govern telephone solicitation — selling goods or services. B2B M&A outreach asking an owner whether he would sell his business is not solicitation, and B2B is broadly exempt anyway. Do not drop a contact or a number over one, and do not raise it as a concern.
  - **Do-not-call recorded in Lance's own CRM: always honor.** That means `[DNC]` written into a phone field, the Aircall tag `Do not call back`, and any refusal or removal request in `call_notes`. These are people who personally told Lance to stop. They stay excluded permanently.

### Cadence
- 4–8 week cadence. Exclude anyone whose `daily_call_list_date` is within the last 4 weeks — that field is the source of truth for when a contact was last put on a list.
- Also respect `notes_last_contacted` as a secondary staleness check.

### Prioritization
1. Sequence email engagement: opened + clicked first, then opened only, most recent engagement first (`hs_sales_email_last_opened` / `hs_sales_email_last_clicked`). Note `hs_email_open` is a Marketing Hub metric and is empty in this portal — do not rely on it.
2. Fallback for contacts with no tracked engagement: call tier (A > B > C), then touchpoint count (`num_contacted_notes`), then oldest-contacted first.

### Source of truth
`migration/routines/routines.json` holds the authoritative cold-call spec (the "Cold Call Today" routine prompt). It is stricter and more complete than this file. Read it before every build; where the two disagree, it wins.

### Screening — every one of these, on every candidate
Verified on 2026-09-10: skipping these put 16 of 50 contacts on a list who should not have been dialed.
- **Open deals** — `num_associated_deals` > 0 on the contact **or** its company. Company level is authoritative. Coverage unit is the company.
- **Customers** — `lifecyclestage` = customer at either level. Opportunity stage is also a drop.
- **`call_notes`, read in full on every candidate.** Free text, strongest signal in the record. Refusals, "not selling", "out of business", DNC, bad number. A refusal written in notes is permanent — the 60-day cooldown applies only to the Aircall *tag*, never to a note. Booked meetings and callbacks are live threads: exclude if `aircall_last_call_at` is within 60 days.
- **Aircall tags** — `last_used_aircall_tags` containing Do not call back, Bad number, Wrong person, or Booked meeting.
- **Already dialed** — `aircall_last_call_at` = today, or on/after the most recent `daily_call_list_date` stamp.
- **Strategic email-domain screen** — OEMs, roll-up competitors, bankers and brokers. Full list in routines.json. Match on email domain, never the company-name field.
- **Out of ICP** — cyber/MDR firms, manned guarding, distributors-only, gate automation.

### Cadence — use `aircall_last_call_at`, not `notes_last_contacted`
Tier A: never called or >21 days. Tier B: >84 days. Tier C: >182 days. `notes_last_contacted` is a secondary check only.

### Daily call brief (Word doc) — every run
**Filename: `Cold call report <Mon> <D>.docx`** — the run's own date, e.g. `Cold call report Sept 10.docx`. AP-style month abbreviations (Jan, Feb, Mar, Apr, May, June, July, Aug, Sept, Oct, Nov, Dec — note `Sept`, not `Sep`), no leading zero on the day, no year.

Alongside the dial string, build a `.docx` brief covering every contact shipped:
- Name, title, company, city/state, and the number being dialed.
- Prior contact history: last Aircall call, touch count, verbatim `call_notes`, last Aircall tag.
- **1–2 sentences on who they are and why Lance is calling** — a specific, concrete reason that will hold the person on the phone. Build it from `personalization_hook` plus company detail (founding year, generation, marquee jobs, niche, awards, recent expansion). Never generic.
- Flag anything Lance should know before dialing: wrong-seniority contact, questionable geography, suspect phone number, franchise vs. independent.
- Close with a "Struck from today's list" section naming everyone screened out and the rule that caught them.

`docx` (npm) is NOT preinstalled in the cloud container despite what the docx skill says — `npm install docx` in the scratchpad first. LibreOffice and pdftoppm are also unavailable, so the skill's render-and-look verification step cannot run; validate by checking the zip contains `[Content_Types].xml` and grepping `word/document.xml` for expected content instead.

### Required write-back — do this every time
After generating the list, stamp `daily_call_list_date` = today's date on every contact on it, via `manage_crm_objects` (max 10 objects per call, so batch it). This is pre-authorized standing work: do not ask for confirmation, and do not skip it. Without the stamp the cadence math breaks on the next run.
