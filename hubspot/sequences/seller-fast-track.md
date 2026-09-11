# Seller Fast-Track — building the Suleman 17-touch sequence in HubSpot

Source: `Suleman_17-touch_sequence_HS.pdf` (SAGARIS "SMB owner fast-track", template id `smb_fast_track`, 17 touches / 30 days, 60-day ice after breakup) and the companion `SEQUENCE-TEMPLATES-REVIEW.md` (full per-touch writing rules). This file is the HubSpot translation for Badlands portal 50955967 (Sales Hub Pro seat, so native Sequences are available).

Written 2026-09-11. Portal facts below were pulled that day.

## 1. The short version

- HubSpot Sequences can carry all 17 touches. Emails become automated-email steps; LinkedIn, SMS and phone become task steps. HubSpot has **no native SMS step**, so the 4 SMS touches are to-do tasks with the text pre-written in the task note.
- The sequence itself has to be built in the HubSpot UI (Automation → Sequences). The HubSpot MCP connector exposes no Sequence object. HubSpot's Sequences API (2026-09 version) does now have a create endpoint under `/automation/sequences/2026-09/serviceaccounts/sequences`, but it needs a private-app / service-account token that this environment does not hold. If Lance adds one as an environment variable, Claude can build the 17 steps by API instead of by hand.
- Everything around the sequence is Claude's job and can start now: the screened enrollment batch, per-contact personalization written into contact properties, the call-task queue folded into the Daily Dials brief, reply triage, and a weekly sequence report.

## 2. Touch-by-touch mapping

Day = calendar day in the SAGARIS spec. HubSpot step delays run in business days, so the same gaps stretch to roughly six calendar weeks; shorten the late gaps (touches 13–17) if 30 calendar days matters.

| # | Day | SAGARIS channel | HubSpot step | Content source | Notes |
|---|---|---|---|---|---|
| 1 | 1 | Email — short, punchy intro | Automated email | Template T1 + `personalization_hook` token | 3 sentences, one observation, one ask. |
| 2 | 2 | LinkedIn — next-day connect | Task (Sales Navigator connection request, or To-do) | Task note carries the 35–60 word note | Sales Navigator task type needs the LinkedIn integration; a To-do works without it. |
| 3 | 3 | SMS — day-three SMS | To-do task | Task note carries the one-line text | Send from Aircall (logs to timeline) or phone. |
| 4 | 4 | Phone — early call attempt | Call task | Pre-call brief from Daily Dials | 15-second voicemail script in the task note. |
| 5 | 5 | Email — value email | Automated email | Template T5 | One concrete result, one similar business. See proof-point gap in §6. |
| 6 | 6 | LinkedIn — message | Task (Sales Navigator InMail, or To-do) | Task note | If not connected, engage on their content. |
| 7 | 7 | SMS — week-one close attempt | To-do task | Task note | Offer a 10-minute call this week. |
| 8 | 9 | Email — problem email | Automated email | Template T8 + `seq_problem_line` token | Per-contact line written by Claude. |
| 9 | 11 | Phone — second call | Call task | Daily Dials brief shows whether T1/T5 were opened | |
| 10 | 13 | Email — social proof | Automated email | Template T10 | Needs a real testimonial or a named comparable. |
| 11 | 15 | SMS — mid-sequence | To-do task | Task note | "Worth 10 minutes?" |
| 12 | 17 | LinkedIn — follow-up | Task | Task note | Engage on a post if one is supplied; otherwise one observation. No pitch. |
| 13 | 19 | Email — offer something | Automated email | Template T13 + `seq_offer_line` token | Badlands version: a free, confidential valuation range or a market-map excerpt for their state. |
| 14 | 21 | Phone — third call | Call task | Daily Dials brief | Last high-effort call. |
| 15 | 24 | Email — long-term nurture | Automated email | Template T15 | No ask. The state market map's acquisition roster is the natural payload. |
| 16 | 27 | SMS — final SMS | To-do task | Task note | Door left open. |
| 17 | 30 | Email — breakup | Automated email | Template T17 | Clean close. Contact goes to a 60-day ice list. |

Channel mix: 7 email, 3 LinkedIn, 4 SMS, 3 phone.

## 3. Sequence settings

- Unenroll on reply: on. Unenroll when a meeting is booked: on.
- Send window: business days, 8:00–17:00 ET (portal timezone is US/Eastern).
- Every task step: tick **"Continue without completing task."** By default HubSpot pauses the whole sequence until a task is completed, which would stall the emails behind any LinkedIn or SMS task Lance did not get to. The portal already has 67 not-started call tasks and 34 not-started to-dos.
- Personalization tokens used in automated emails must resolve for every enrolled contact or HubSpot blocks the send. Give every token a default and have Claude fill the properties for the batch before enrollment.
- Threading: T5, T8, T10 reply in the T1 thread; T13, T15, T17 start new threads (matches the "different angle" rule in the SAGARIS prompts).

## 4. Contact properties to add (Settings → Properties → Contact)

| Property | Type | Used by | Written by |
|---|---|---|---|
| `personalization_hook` | exists | T1, T2 note | Claude / existing |
| `seq_problem_line` | single-line text | T8 | Claude, per contact, before enrollment |
| `seq_offer_line` | single-line text | T13 | Claude, per contact |
| `fast_track_ready` | date | enrollment list | Claude, on the screened batch |
| `fast_track_ice_until` | date | ice list / re-enrollment guard | Claude, on breakup (T17 + 60 days) |

Claude cannot create properties through the connector; it can only read and write values. Creating the four new ones is a two-minute UI job.

## 5. Enrollment: who goes in

Same screen as the cold-call routine (`migration/routines/routines.json`, "Cold Call Today", Steps 2–3), plus email-specific checks:

- `banker` = Seller; `call_tier` in A, B, C (Platform Target handled by hand).
- NYC-metro city per `migration/routines/nyc_metro_cities.json`, matched within state.
- `email` present; ZeroBounce `zb_status` valid where available (the ZeroBounce connector needs authorizing before Claude can validate new addresses).
- No deals at contact or company; lifecycle not customer/opportunity.
- `call_notes` refusal screen (permanent), Aircall tags, strategic-domain screen — all as in the routine.
- `hs_sequences_is_enrolled` = false; `fast_track_ice_until` empty or past.
- Not on the daily call list in the last 4 weeks, so the sequence's own call tasks are the first dials.

Pool on 2026-09-11 (Seller, tier A/B/C/Platform Target, email present):

| | NY | NJ | CT | Tri-state | Everywhere |
|---|---|---|---|---|---|
| Email on file | 363 | 161 | 86 | 610 | ~850 |
| Email + mobile (SMS-capable) | 226 | 112 | 57 | 395 | ~480 |
| Already been through a HubSpot sequence | 225 | 98 | 66 | 389 | ~610 |
| Never sequenced | 138 | 63 | 20 | 221 | ~240 |
| LinkedIn URL on file | | | | | 624 |

State counts overstate NYC-metro; the city filter cuts them further. 63 contacts are live in the existing "NYC Targets" sequence today.

Pace: 5 enrollments per business day (25/week). Each contact generates 3 call tasks over the run, so steady state is about 15 sequence call tasks per day, leaving room in the 50-dial list for cold dials. 10/day would make the sequence consume roughly 30 of the 50 dials.

## 6. Decisions Lance owns before build

1. **Proof points for T5 and T10.** The pipeline has one Closed deal. Options: a named comparable acquisition from the state market maps ("since 2020, 14 CT integrators have sold; here is who bought them"), or an owner reference Lance can quote. Without one of these, T5/T10 fall back to the platform thesis and lose most of their punch.
2. **SMS channel.** Aircall (texts land on the HubSpot timeline) or personal phone (no log; Claude cannot see it happened).
3. **LinkedIn.** Sales Navigator integration on or off. On: native task types and one-click InMail. Off: To-do tasks with the message text.
4. **Enrollment pace**: 5/day recommended.
5. **API build.** If Lance creates a HubSpot private app with `automation.sequences.read` and `automation.sequences.enrollments.write` scopes and adds the token to the Claude environment (never in chat), Claude builds and updates the 17 steps by API. Otherwise the UI build is about 45 minutes with the templates supplied.
6. **Cadence carve-out** in the Daily Dials routine: contacts with an open sequence call task bypass the 4-week `daily_call_list_date` rule and the Tier A 21-day rule, because the sequence calls on days 4, 11 and 21.

## 7. What Claude runs around the sequence

| Job | Cadence | Mechanism |
|---|---|---|
| Screened enrollment batch: 5 contacts, all rules in §5, `fast_track_ready` stamped, `seq_problem_line` / `seq_offer_line` / `personalization_hook` written | Daily, before Daily Dials | HubSpot connector search + `manage_crm_objects`; Lance enrolls from the active list in one click |
| Sequence call tasks at the top of the dial string, with the T1/T5 open/click state and the prior-conversation block already in the brief | Daily | Extend the "Cold Call Today" routine: pull `TASK` where type = CALL, due today, from the sequence; close the task when Aircall logs the dial |
| Reply triage: interested / not now / refusal. Refusal → `call_notes` + `call_tier` = Excluded + note to unenroll. Not now → `calll_back_date`. | Daily | Extend the Weekly Email Scan routine to daily; write-backs are the two already authorized plus the new date fields |
| Sequence report: enrolled, replied, meetings, unenrolled, opens/clicks by step, refusals caught | Weekly (Mon) | `hs_sequences_*`, `hs_sales_email_last_*`, EMAIL and MEETING_EVENT counts |
| Ice-list release: 60 days after T17, contacts return to the cold-call pool or to a re-engagement sequence | Weekly | `fast_track_ice_until` |
| Task hygiene: re-date or close stale sequence tasks so the queue stays honest | Weekly | `manage_crm_objects` on TASK |

## 8. Beyond this sequence: what else is worth doing

Grounded in the portal as of 2026-09-11.

- **Proprietary sourcing is the business.** 81 of 105 deals are `deal_source` = Proprietary, 20 Broker. Outbound cadence quality is the main lever, which is why this sequence matters more than any list purchase.
- **Re-engagement sequence next.** 25 deals sit On Hold and about 600 sellers have been through a HubSpot sequence without converting. The SAGARIS "Re-engagement" template (12 touches / 30 days) is the right shape for them, run quarterly. Build it second.
- **Company sector is half blank.** 840 of 1,648 companies have no `lock` (Sector) value; 428 AC, 137 Ancillary, 114 Lock, 69 Fire, 60 Broker. Claude can classify the blanks from website, name and ZoomInfo/Apollo firmographics in one pass, which makes every list and report cleaner.
- **`acquired` is under-used.** Only 16 companies are flagged acquired, while the state-market-map skill tracks every in-state acquisition since 2015. Syncing those into `acquired` turns a `call_notes` guess ("sold to…") into a hard filter and stops dials to companies that are already someone's platform.
- **Net-new owners.** The tri-state seller pool with a working email is ~610 and ~390 of them have already been sequenced. The next well is the market-map independents not yet in HubSpot: diff the roster against companies, then enrich owners through ZoomInfo/Apollo (credits) and validate emails through ZeroBounce before they touch the sequence.
- **Deliverability protection.** The Badlands mail domain is fresh from the tenant migration. Keep sequence volume ramped (25/week), validate every address, and keep bounces out of the automated emails.
- **Meeting capture.** Granola and Plaud are connected. Post-meeting: transcript → deal note, next step, stage move. A routine can do this the morning after each meeting.
- **Task backlog.** 67 not-started call tasks and 34 to-dos already exist. Clear them before the sequence adds more, or they bury the sequence's tasks.
- **Routines already live on this account:** Daily Dials (09:00 UTC weekdays), Daily Calendar Prep (10:00 UTC), Mass Email Digest (10:30 UTC weekdays), Weekly Email Scan (Mon 10:00 UTC), Tuesday prep — Daniel sync (Tue 11:00 UTC), HubSpot CRM Audit (first Monday, 10:00 UTC). The sequence jobs in §7 extend Daily Dials and Weekly Email Scan rather than adding new routines.

## 9. Sample copy (Badlands voice, HubSpot token syntax)

Full 17-touch copy is written once the §6 decisions are made. Three samples so the voice is agreed first. Rules from the SAGARIS prompts apply: open on something true about them, one ask, no consultant vocabulary, no exclamation marks, no "just following up".

**T1 — automated email**

Subject: `a question about {{ company.name }}`

```
{{ contact.firstname }},

{{ contact.personalization_hook }}

I run acquisitions at Badlands. We are building a group of independent access control, fire and locksmith businesses across the tri-state area, and {{ company.name }} is the kind of operator we want in it.

Would 15 minutes next week to hear what a sale could look like for you be worth your time? A one-line no is fine.

Lance
```

`personalization_hook` default (used only if the property is empty): `Your team has been servicing {{ contact.city }} accounts for a long time, and that kind of base is rare.`

**T3 — SMS task note (day 3)**

```
{{ contact.firstname }}, Lance from Badlands. I emailed Tuesday about {{ company.name }}. Is a sale something you would ever think about, yes or no?
```

**T4 — call task note, voicemail (day 4, 15 seconds)**

```
{{ contact.firstname }}, Lance at Badlands. We buy independent security businesses in the New York area. I sent a note about {{ company.name }} this week. My number is [Aircall number]. No pitch, just a conversation when it suits you.
```

## 10. Build checklist (HubSpot UI, ~45 minutes)

1. Settings → Properties → Contact: create `seq_problem_line`, `seq_offer_line` (single-line text), `fast_track_ready`, `fast_track_ice_until` (date).
2. Sales → Templates: create T1, T5, T8, T10, T13, T15, T17 from the copy Claude supplies. Set a default value on every token.
3. Automation → Sequences → Create sequence → Start from scratch → name it `Seller Fast-Track (NYC metro)`.
4. Add the 17 steps in the order of §2, with the delays from the Day column. Email steps: pick the template. Task steps: type Call / To-do / Sales Navigator, paste the task note, tick "Continue without completing task".
5. Settings tab: business days only, 8:00–17:00 ET, unenroll on reply and on meeting booked.
6. Contacts → Lists: active list `Fast-Track ready` = `fast_track_ready` is known AND `hs_sequences_is_enrolled` = false. Claude keeps this list fed; Lance enrolls from it.
7. Tell Claude the sequence is live. The Daily Dials and Weekly Email Scan routines get the §7 extensions the same day.
