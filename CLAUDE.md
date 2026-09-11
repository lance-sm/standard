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
  - **Use the committed city list, don't re-derive it from memory.** `migration/routines/nyc_metro_cities.json` holds the canonical metro town list per state. Read it; match case-insensitively on `city` within the contact's own `state`. Deriving this from scratch each morning is how Edison NJ — the town literally named as the Middlesex boundary above — got filed as band 2 on 2026-09-11, costing two undialed rollovers their slot. If you hit a city that isn't in the file, look up its county, classify it, **add it to the file**, and note it in the run summary.
- Exclude `call_tier = Excluded`.
- Registry flags (ZoomInfo `mobilePhoneDoNotCall`, national registry) are irrelevant to this work — they govern telephone solicitation, not M&A outreach. Never drop a contact over one, never mention them in a report or a reply.
- Someone who has personally asked Lance to stop contacting them stays excluded permanently — caught by the `call_notes` refusal screen below. Screen it silently; do not call it out as a category in the report.

### Cadence
- 4–8 week cadence. Exclude anyone whose `daily_call_list_date` is within the last 4 weeks — that field is the source of truth for when a contact was last put on a list.
- Also respect `notes_last_contacted` as a secondary staleness check.

### Prioritization
1. Sequence email engagement: opened + clicked first, then opened only, most recent engagement first (`hs_sales_email_last_opened` / `hs_sales_email_last_clicked`). Note `hs_email_open` is a Marketing Hub metric and is empty in this portal — do not rely on it.
2. Fallback for contacts with no tracked engagement: call tier (A > B > C), then touchpoint count (`num_contacted_notes`), then oldest-contacted first.

### Source of truth
`migration/routines/routines.json` holds the authoritative cold-call spec (the "Cold Call Today" routine prompt). It is stricter and more complete than this file. Read it before every build; where the two disagree, it wins.

**Standing exception, confirmed by Lance 2026-09-11:** the routine prompt's "no spreadsheet or file unless Lance asks" line in its Step 5/6 no longer applies. He has asked, permanently. The Daily call brief docx below (and its email delivery) is mandatory on every run, full stop — this file's instruction on that point overrides routines.json, not the other way around.

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

### Daily call brief (Word doc) — every run, mandatory, no exceptions
**Filename: `Cold call report <Mon> <D>.docx`** — the run's own date, e.g. `Cold call report Sept 10.docx`. AP-style month abbreviations (Jan, Feb, Mar, Apr, May, June, July, Aug, Sept, Oct, Nov, Dec — note `Sept`, not `Sep`), no leading zero on the day, no year. Get the date right — it's the run's own date, not the date of some prior list being referenced.

**Delivery: email it, don't just drop it in chat.** The Microsoft-365 mail tools available in this environment (`outlook_send_mail`, `outlook_create_draft`) have no attachment parameter — confirmed 2026-09-11, `outlook_send_draft` even explicitly refuses drafts with attachments. So: upload the .docx via `sharepoint_upload_file` to **`1 Pipeline/Cold Call Reports`** in Lance's OneDrive — driveId `b!sRY4CJgKn0ue4_YulSpe6Vi0hWolvkdPjEqf1z-VtlIq9yYGd7DER477LYoouoxm`, `parentItemId` `01XYRJS5CJGIH5PNHJFBHKNOQ675GCPLUZ` — then email the resulting `webUrl` as a link — not a literal attachment — to lance@badlandssecurity.com via `outlook_send_mail`. Never drop these in the drive root; that folder is the standing home so the reports accumulate in one place. Do not rely on SendUserFile/chat alone, since nobody may be watching the session. Target landing in his inbox by **7:00 AM ET**. Subject line: `Cold call report <Mon> <D>`. Body: the link, plus a one-line summary (count shipped, geo mix) — the doc itself carries the detail. If a genuine attachment tool becomes available later, switch to that instead of the link.

Alongside the dial string, build a single `.docx` brief covering every contact shipped — this is one document, not two:
- **Name, hyperlinked to the HubSpot contact record** — `https://app.hubspot.com/contacts/50955967/record/0-1/<contactId>`. Plus title, company, city/state.
- **The number being dialed, tagged `(M)` or `(D)`.** `M` = a distinct mobile is on file. `D` = `mobilephone` duplicates `phone`, so there is only one number and it is the office line. Compare the two fields on normalized digits — many records copy the office line into the mobile field, and calling that `M` is misleading.
- **Activity counts on their own line: `Emails: X (last M/D) · Dials: X · Meetings: X`.** Omit Meetings entirely when zero. Omit the `(last M/D)` parenthetical only when the email count is zero — a count with no recency doesn't tell Lance whether the thread is warm or a year cold. Date format is bare month/day, no year (`6/19`), matching the `call_notes` style already in the doc. Sources:
  - Dials — `SELECT CONTACT.hs_object_id, COUNT(*) FROM CALL WHERE CONTACT.hs_object_id IN (...) GROUP BY CONTACT.hs_object_id`. One query for the whole list.
  - Meetings — same shape against `MEETING_EVENT`. One query for the whole list.
  - Emails — the `EMAIL` object is hidden from the reporting API, so SQL fails. Use `search_crm_objects` with `objectType: EMAIL`, an `associatedWith` contacts filter, `limit: 1`, **and `sorts: [{propertyName: "hs_timestamp", direction: "DESCENDING"}]`**. Read `total` for the count and the single returned row's `hs_timestamp` for the last-email date — the sort means both come back from the SAME call, so this stays one call per contact (~50 per run), not two. A contact with no emails returns an empty `results` array with `total: 0`; drop the parenthetical rather than printing a placeholder. Counts include inbound replies; a reply is a strong signal worth surfacing in the flag line.
- Prior contact history on its own line: last Aircall call, verbatim `call_notes`, last Aircall tag.
- **1–2 sentences on who they are and why Lance is calling** — a specific, concrete reason that will hold the person on the phone. Build it from `personalization_hook` plus company detail (founding year, generation, marquee jobs, niche, awards, recent expansion). Never generic.
- Flag anything Lance should know before dialing: wrong-seniority contact, questionable geography, suspect phone number, franchise vs. independent.
- Close with a "Struck from today's list" section naming everyone screened out and the rule that caught them.

`docx` (npm) is NOT preinstalled in the cloud container despite what the docx skill says — `npm install docx` in the scratchpad first. LibreOffice and pdftoppm are also unavailable, so the skill's render-and-look verification step cannot run; validate by checking the zip contains `[Content_Types].xml` and grepping `word/document.xml` for expected content instead.

### Required write-back — do this every time
After generating the list, stamp `daily_call_list_date` = today's date on every contact on it, via `manage_crm_objects` (max 10 objects per call, so batch it). This is pre-authorized standing work: do not ask for confirmation, and do not skip it. Without the stamp the cadence math breaks on the next run.

### Schedule — 7am ET delivery deadline
The routine's cron (`migration/routines/routines.json`, "Cold Call Today") fires early enough to build the list, run the activity-count queries, generate the docx, and email it before 7:00 AM ET — currently `10:00 UTC` (6:00 AM EDT), a 1-hour buffer. **DST caveat:** the cron is a fixed UTC time; ET's offset from UTC shifts by an hour at the March/November changeovers, so the buffer shrinks to 0 or grows to 2 hours seasonally. Nudge the cron by an hour at each changeover if the buffer matters, or leave it — a 1-hour miss either way is not worth obsessing over.
