# CLAUDE.md

Repo-wide instructions for Claude Code sessions on this repo (Badlands working repo, account: lance@badlandssecurity.com).

## Known personal context (applies to any routine, e.g. daily Meeting Prep)

- **Mark Smith (msmith@kithkitchens.com)** is Lance's father, not a business contact needing a company-overview writeup. He's been in private equity for ~30 years and is a helpful thought partner. For meetings with him, skip the "who is he" background and instead suggest what to discuss — deal strategy, pipeline questions, or anything he could bring his PE experience to bear on — rather than treating him as an external prospect needing enrichment/CRM flags.

## Diligence request list for seller meetings (every Meeting Prep run)

For any meeting today tagged/identified as a **Seller** meeting (calendar category "Seller - Virtual"/"Seller - IP", or `banker`/Contact Type = Seller in HubSpot), generate a Badlands-branded Initial Diligence Request List.

- **Template source of truth**: `Badlands_Initial Request List.docx`, canonical blank copy at `https://thebadlandssecuritycompany.sharepoint.com/sites/Acquisitions/Shared Documents/Badlands Deal Folder/Admin & Ops/NDA and Request List/Badlands_Initial Request List.docx` (also mirrored under `TheBadlandsDrive/.../NDA and Request List/`). Read it fresh each time rather than hardcoding the text below, in case it's revised. Do NOT save the generated file back into that Admin & Ops folder — see Delivery below.
- **Fixed structure** (single page, header "BADLANDS SECURITY COMPANY", title line `[Target Company] – Initial Diligence Request List – [Date]`), four sections in this order:
  1. **Corporate Structure** — entity structure (C-Corp/S-Corp/LLC/partnership); cap table / shareholder list with ownership %.
  2. **Business Description** — corporate overview/marketing materials; services & products; geographies served; tech headcount; union status; total employees; owned/leased service trucks; self-performed vs. sub-contracted work.
  3. **Customers** — revenue by customer for last 3 years (redacted names OK); core customer base description.
  4. **Financial** — financials for last 3 years; revenue by segment; average revenue per project/service call/job.
- When a CIM or other deal material already exists for that target (check HubSpot deal notes/description and SharePoint), tailor bullets the way past examples do (e.g. NYC Alarm's filled list adds specific sub-bullets like license/cert rosters, RMR register, margin-change questions) — pull real numbers in as sub-bullets rather than leaving the generic question bare. When nothing is known yet (early-stage/no CIM), ship the generic template as-is with just company name and date filled in.
- **Delivery — send the file, don't just link/describe it:**
  - Deliver the actual `.docx` to Lance directly (`SendUserFile`) — not a SharePoint link pasted into prose. The Outlook MCP tools here have no attachment support (`outlook_send_mail`/`outlook_create_draft`/`outlook_send_draft` all reject attachments), so the morning Meeting Prep email itself stays link-free; the file goes out via direct delivery alongside it.
  - Also save a copy to Lance's OneDrive at the top-level **`0- Inbox`** folder (`personal/lance_badlandssecurity_com/Documents/0- Inbox`, sibling to `1 Pipeline`, `2 Deals`, etc.) — not `Admin & Ops/NDA and Request List` (that's the template's own home, not a save destination for generated lists).
  - **Known trap — large base64 uploads silently corrupt.** `sharepoint_upload_file`'s `contentBase64` gets mangled in this environment once the string runs long (a 9KB docx → ~12,500 base64 chars reliably corrupted on relay, even though the upload call "succeeded"). Keep generated diligence-list `.docx` files minimal — hand-roll the OOXML (bare `[Content_Types].xml` + `_rels/.rels` + `word/document.xml` + `word/_rels/document.xml.rels`, no styles/numbering/footnotes/endnotes/comments parts) rather than using the `docx` npm package's default output, to stay well under ~3,000 base64 chars. After uploading, always confirm the returned byte count matches the local file's actual size before trusting the copy — a mismatch means it silently corrupted.

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
- **Name, hyperlinked to the HubSpot contact record** — `https://app.hubspot.com/contacts/50955967/record/0-1/<contactId>`. Plus title, company, city/state.
- **The number being dialed, tagged `(M)` or `(D)`.** `M` = a distinct mobile is on file. `D` = `mobilephone` duplicates `phone`, so there is only one number and it is the office line. Compare the two fields on normalized digits — many records copy the office line into the mobile field, and calling that `M` is misleading.
- **Activity counts on their own line: `Emails: X · Dials: X · Meetings: X`.** Omit Meetings entirely when zero. Sources:
  - Dials — `SELECT CONTACT.hs_object_id, COUNT(*) FROM CALL WHERE CONTACT.hs_object_id IN (...) GROUP BY CONTACT.hs_object_id`. One query for the whole list.
  - Meetings — same shape against `MEETING_EVENT`. One query for the whole list.
  - Emails — the `EMAIL` object is hidden from the reporting API, so SQL fails. Use `search_crm_objects` with `objectType: EMAIL` and an `associatedWith` contacts filter, `limit: 1`, and read `total`. This is one call per contact, so budget ~50 calls per run. Counts include inbound replies; a reply is a strong signal worth surfacing in the flag line.
- Prior contact history on its own line: last Aircall call, verbatim `call_notes`, last Aircall tag.
- **1–2 sentences on who they are and why Lance is calling** — a specific, concrete reason that will hold the person on the phone. Build it from `personalization_hook` plus company detail (founding year, generation, marquee jobs, niche, awards, recent expansion). Never generic.
- Flag anything Lance should know before dialing: wrong-seniority contact, questionable geography, suspect phone number, franchise vs. independent.
- Close with a "Struck from today's list" section naming everyone screened out and the rule that caught them.

`docx` (npm) is NOT preinstalled in the cloud container despite what the docx skill says — `npm install docx` in the scratchpad first. LibreOffice and pdftoppm are also unavailable, so the skill's render-and-look verification step cannot run; validate by checking the zip contains `[Content_Types].xml` and grepping `word/document.xml` for expected content instead.

### Required write-back — do this every time
After generating the list, stamp `daily_call_list_date` = today's date on every contact on it, via `manage_crm_objects` (max 10 objects per call, so batch it). This is pre-authorized standing work: do not ask for confirmation, and do not skip it. Without the stamp the cadence math breaks on the next run.
