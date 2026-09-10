---
name: seller-call-list
description: Build Lance's cold-call list of seller phone numbers from HubSpot - sellers only, ranked by call tier, with nobody dialed in the last 30 days - then stamp the call date back onto the records. Use when Lance asks for call numbers, a dial list, a daily call list, "who am I calling today", or runs the scheduled call-list task. Covers the 9-state Northeast.
---

# Seller Call List

Daily cold-call list for Badlands M&A outreach: independent security, locksmith, fire/life
safety and CCTV owners in the Northeast who might sell.

Every rule below exists because it was gotten wrong once. Do not re-derive them.

## Output contract

- **A comma-separated string in chat. Not a CSV file, not a table, not an attachment.**
  Lance copy-pastes it into the dialer.
- 10 digits each, no punctuation, no country code, deduped.
- Default 50 numbers unless he says otherwise.
- After delivering, **write the call date back to HubSpot** (see *Write-back*).

## Who qualifies

| Filter | Value |
|---|---|
| `banker` (labeled **Contact Type**) | `Seller` only — never Banker, Broker, or Industry Contact |
| State | NY, NJ, CT, MA, PA, NH, RI, VT, ME |

A contact carried over from a prior day's queue keeps its slot even if `state` is blank or
out-of-area. Only apply the state filter to newly added contacts.

## Call tiers — `call_tier`

Priority order: **Platform Target > A > B > C**. (No seller currently carries Platform Target;
check anyway rather than assuming.)

- **`Excluded` is a hard stop.** Never include, never fill from, no exceptions. ~127 sellers.
- **Tier outranks number type.** A Tier A landline beats a Tier B mobile.
- ~600 sellers have **no tier assigned** — untriaged, ranks below C. Don't quietly pull from
  this pool to hit a count; surface the backlog to Lance instead.

## The 30-day rule

**Nobody contacted in the last 30 days.** Not "4 weeks" — 28 vs 30 has bitten before, because
call blocks cluster right at the boundary (a 28-day cutoff once shipped three people who had
been dialed 29 days earlier).

Verify two ways and suppress if *either* trips:

**1. The CALL object — this is the authoritative check.**

```sql
SELECT hs_object_id, hs_timestamp, hs_call_to_number, hs_call_direction, hs_call_status
FROM CALL WHERE hs_timestamp BETWEEN '<today-32d>' AND '<today+1d>' LIMIT 500
```

Normalize `hs_call_to_number` to 10 digits and match against every number on the contact.
**Many CALL records carry no contact association at all** — a contact can look clean on every
rollup field and still have been dialed yesterday. This check alone caught 90 contacts that the
contact-level fields passed.

**2. Contact-level rollups** — take the max of `notes_last_contacted`,
`aircall_last_call_at`, `aircall_last_sms_at`.

## Property gotchas

- **`aircall_last_call_at` is the field HubSpot displays as "Last Aircall call timestamp (EDT)".**
  HubSpot appends the `(EDT)`/`(EST)` display-timezone suffix to datetime column headers. There
  is no separate EDT property — do not go looking for one. Stored UTC, displayed Eastern;
  convert to ET for any date-exact comparison (a 8:30pm ET call stores as the next day in UTC).
  Verified: it never post-dates `notes_last_contacted`, because Aircall syncs in as logged
  activity. It is not an independent signal, but include it in the max anyway.

- **`daily_call_list_date` means QUEUED, not called.** Never suppress on it. People queued on a
  previous day who were never actually dialed should be *mixed back in* to today's list — check
  them against the CALL object and carry forward the ones with no real dial.

- `calll_back_date` (three l's) — scheduled callback. `call_attepts` (misspelled) — attempt count.
  `call_notes` — free text, often `LVM 6/3` style.

## Number selection

- **Mobile strongly preferred**; landline is acceptable but not preferred.
- **Mobile means the `mobilephone` field only.** A number sitting in `phone` is not a mobile —
  classifying it as one inflates the mobile count badly.
- `(co. line)` inside a number's text demotes it to landline even in the `mobilephone` field.
- **Drop toll-free numbers entirely** — 800/833/844/855/866/877/888. They route to a receptionist,
  never the owner. 17 sellers have *only* a toll-free number on file.
- **85 sellers carry the identical number in both `mobilephone` and `phone`.** That is one number,
  not a mobile plus a landline — do not count it as mobile coverage.
- **`[DNC]` free-text tags: ignore them.** Standing instruction from Lance, 2026-09-09. Every
  known tag sits on an office line with a clean mobile alongside, consistent with a vendor scrub
  against the national registry — which does not apply to B2B calls to business owners.
  *One exception:* if a tag or call note records that the person **themselves** asked to stop
  being called, still include the number, but flag it in the summary so Lance decides knowingly.
  Never silently drop it, and never silently include it either.

## The blocklist MUST be number-level, never record-level

This is the most dangerous failure mode in the whole process. **Duplicate contact records exist** —
the same human under two records, sometimes with a name typo, often with different tiers. Filtering
on record ID lets the clean twin through and you dial someone who already said no.

Build the blocklist by **phone number across every contact in the portal**, from any record with:
- `call_tier` = `Excluded`
- `last_used_aircall_tags` matching `do not call back` or `bad number`
- `call_notes` matching a rejection

Real cases that defeated record-level filtering:
- **Bart Didden** — Excluded + "not interested" on one record, Tier B on another, same mobile.
- **Steven Guardiani / "Seteven Guardiani"** — typo duplicate, Excluded, note `shut dwn` (business
  closed), same mobile as the live Tier A record. Shipped on a delivered list before it was caught.

**Rejection language is far wider than "not interested".** Also catch: `pass`, `shut dwn` /
shut down, `closed`, `out of business`, `retired`, `too small`, `hung up`, `declined`,
`already sold`, `wrong number`. Notes are terse and misspelled — match loosely.

**`booked meeting` in the aircall tags means an active conversation.** Exclude from cold-call
lists and say so — cold-calling someone mid-deal is the worst error this list can make.

## Geography: trust area codes, not the `state` field

`state` is unreliable and must never be the only geographic filter:
- **73 sellers** have a `state` contradicting every area code on the record.
- **14 sellers** have no `state` at all — invisible to any `state IN (...)` query.
- Observed: a Staten Island alarm company filed under VA; a CT/RI operator under OR; a NY owner
  under KY.

Filter NYC metro on **area code first**, city as support:
NY `212 646 332 917 718 347 929 516 631 914 845` · NJ `201 551 973 862 908 732 848` ·
CT Fairfield `203 475`. Exclude upstate NY (`315 585 716 518 607`), Philly/Trenton NJ
(`856 609`), Hartford CT (`860 959`).

## Ranking

1. Tier (Platform Target > A > B > C)
2. Carry-over from a prior uncalled queue ranks ahead of fresh contacts *at the same tier*
3. Mobile before landline
4. Most overdue first (longest since last contact; never-contacted counts as most overdue)

Keep the blend tier-dominant. A carry-over queue skewed to Tier B must not crowd out Tier A —
cap the low-tier carry-over rather than filling the list with it.

## Write-back

After delivering the numbers, stamp every delivered contact:

```
manage_crm_objects → updateRequest → { objectType: "CONTACT", objectId: <id>,
                                       properties: { daily_call_list_date: "YYYY-MM-DD" } }
```

Max 10 objects per call, so batch. Date format `YYYY-MM-DD` works. This is what Lance filters
on to pull up the day's list. Verify with `get_crm_objects` afterward — not with a GROUP BY
(see below).

## HubSpot MCP tool quirks

- **`search_properties` on CONTACT returns a capped ~316 properties and ignores `searchTerms`
  entirely** — the same alphabetical list every time. Never treat it as the complete property
  set. To check a specific property, use `get_properties` with candidate names, or
  `get_crm_objects` with no `properties` argument to dump a live record's populated fields.
- `get_properties` with no `propertyNames` returns empty — it cannot enumerate.
- **`GROUP BY` on a date property mislabels the bucket** (a `= '2026-09-09'` filter reported
  back as `2026-09-01`). The counts are right; the label is not. Verify values with
  `get_crm_objects`.
- Large `query_crm_data` results spill to a file instead of returning — parse it with python
  rather than re-querying with fewer columns.
- `query_crm_data` returns some default properties (name, email) regardless of the SELECT list.

## Report back

Alongside the number string, state: tier mix, mobile/landline split, state spread, the tightest
days-since-contact on the list, how many were carried over vs newly added, and anything
suppressed with the reason. If a judgment call was made on blend or tier trade-offs, say so
explicitly and offer the alternative.
