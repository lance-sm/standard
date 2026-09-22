# BDO intro target list — combined send file

Build of the combined BDO send file, 2026-09-21. Picks up the work paused in
`BDO Target List - Handoff.md` (2026-09-21) and completes agreed next steps 1, 2, 4 and 5.
Step 3 (URL verification) is only partly done — see **Known gaps**.

Output: `BDO Target List - Combined Send File.xlsx`, saved flat in `~/Desktop/Claude Files/`.

## Tabs

| Tab | Rows | For BDO? |
|---|---|---|
| Summary | — | counts, method, caveats |
| BDO Send List | 1,246 | **yes** — company-level columns only |
| Send List - Internal Detail | 1,246 | no — per-row provenance |
| Hold Back - Live Deals | 41 | no — Lance decides |
| Adjacent - Review | 63 | no — Lance decides |
| NYC Unclassified - Review | 77 | no — Lance decides |
| Removed | 321 | no — audit trail |

Send List columns are exactly the ones decision 4 of the handoff allows:
Company | Website | City | State | Vertical | Size Tier | In HubSpot.
No owner names, no revenue estimates, no ownership notes, no sources.

## Inputs

- `NYC Metro Target List - Organized.xlsx` → Qualified (712) and Unclassified (77)
- `NE Security Target Universe - BDO.xlsx` → Send List (358), Review-Adjacent (34),
  and the PE-Owned / Above Buy-Box / Excluded tabs used as the blocklist
- Fresh HubSpot company export, 1,649 records, pulled 2026-09-21 via the HubSpot MCP
  (`hs_object_id, name, domain, city, state, numberofemployees, annualrevenue, lifecyclestage`)
- HubSpot deal pipeline, 112 deals in "M&A Pipeline" → `hubspot_deal_companies.tsv`

Nothing was written to HubSpot.

## What the scripts hold

- `lib.py` — the two normalizers. `norm_name` is the loose one the handoff specified
  (strips inc/llc/corp/co/company/the/and/systems/services/group). `norm_name_strict`
  keeps systems/services/group and is used whenever a domain or headcount is carried
  onto a row, because the loose one joins different companies — it merged
  "Excel Security Systems Inc." (Brooklyn) into "Excel Security" (Manhattan, 900 employees).
- `screen.py` — the first-pass call on all 636 in-footprint HubSpot records that were on
  neither prior list: 257 target, 253 non-target, 106 uncertain, 17 adjacent, 3 duplicate.
- `resolved.py` — the 106 uncertain records after ZoomInfo enrichment
  (industry, headcount, parent, defunct flag): 44 target, 46 non-target, 12 adjacent, 4 duplicate.
- `zi_nyc.py` — ZoomInfo data for the 77 NYC "Unclassified" names, carried onto their review tab.
- `build.py` — merge, blocklist, hold-back, dedupe, tiering and workbook writer.

## Screening rules applied

1. Blocklist: universe PE-Owned, Above Buy-Box and Excluded tabs plus the NYC Excluded tab,
   matched on normalized name and on domain.
2. Removed outright: broker/advisor companies attached to deals (Flatirons, Hedgestone, DGP,
   Corum, The Advisory IB, SEMM) and Cosmic Fischer, which Badlands owns.
3. Held back: every company with a deal in an active stage — Initial Meeting, Management
   Meeting, IOI, Due Diligence, On Hold. "Pass" deals stay on the send list; they are dead
   and carry no NDA. The hold-back tab is built from the pipeline itself, so an active deal
   appears whether or not it sat on a source list.
4. Deduped by domain, then by normalized name **within a state**. A domain match always
   means one company; a loose-name match only does when the state agrees too. Keeping the
   two apart matters — "American Alarm" is three different companies, in MA, CT and NY.
5. `lookup_hs()` disambiguates on state, then city, when several HubSpot records share a
   name, and leaves the domain blank rather than guess when it still can't tell. 15 names
   in HubSpot are shared by more than one distinct domain.
6. A guard at the end asserts that no in-footprint HubSpot record ends up on no tab at all.

## Verified corrections

Each row in the top two size tiers was checked individually, since that is what BDO reads first.
Four were wrong and are now on the Removed tab:

- **Winfield Security Corporation** — guard/officer services, and has joined Tarian, a PE platform
  already on the PE-Owned tab.
- **Building Security Services** — guard/officer services (unarmed guards, concierge, mobile patrol).
- **AccessIT Group** — cybersecurity VAR, not physical security.
- **DTiQ** — PE-owned; Digital Alpha holds the majority and Bain Capital Credit invested in 2024.
  The universe build had it as "Independent" because ZoomInfo returned no parent.

Two more were corrected rather than removed:

- **Mac Security Systems** — ZoomInfo had it on `macsecurity.com.ec`, an Ecuador domain. Cleared.
  (This was one of the three rows the handoff flagged for checking.)
- **Security 101 - Rochester** — the 620 headcount in HubSpot is the national franchise network,
  not the Rochester franchisee. Size tier set to Unknown.

Of the handoff's three flagged rows, **Northstar Protection** is confirmed a genuine alarm, fire
and access integrator in Hermon ME, not a guard company — it stays. **Wayman Fire Protection**
($118M ZoomInfo revenue at 130 employees) is still unverified.

## Known gaps

- **URL verification is not complete.** This session's network policy blocks outbound access to
  company websites, so homepages could not be fetched and matched against company names. Domains
  from the universe build are ZoomInfo-sourced; domains taken from HubSpot are unverified. The
  `URL Check` column on the internal detail tab says which is which. Roughly 1,000 rows still
  need a real URL check. To do it properly, set the cloud environment's **Network access** to
  **Full** (claude.ai/code → cloud icon → edit environment); the default **Trusted** level
  allows package registries and GitHub only. ZoomInfo bulk enrichment is the alternative.
- **Size tier is incomplete:** 785 of 1,246 rows have no headcount. The NYC metro list carried no
  size data and most HubSpot records have no employee count.
- The NYC "Unclassified" names were left on their own review tab rather than guessed onto the send
  list. ZoomInfo's industry codes do not separate low-voltage installers from IT shops in that
  group, and the earlier NYC cleanup had deliberately left them unclassified. Six are Badlands
  deal companies, so the group does contain real targets.
- The universe Review-Adjacent rows are on their own tab, not the send list, matching the intent
  of that tab in the universe build.

## Name collisions

Three separate defects all traced to the loose normalizer the handoff specified, which strips
`systems`, `services` and `group`:

1. It joined **Excel Security Systems Inc.** (Brooklyn) to **Excel Security** (Manhattan),
   handing the Brooklyn company the wrong domain and a 900-employee headcount.
2. It hid HubSpot records from screening whenever any other company shared their name.
   **American Alarm** (Norwalk CT) and **Approved Fire Protection** (Somerset NJ) were
   recovered by hand; the guard now fails the build if this recurs.
3. It merged distinct same-name companies across states. Seven pairs are now kept apart,
   among them Integrated Security (NY) vs Integrated Security Group (CT), and the three
   American Alarms.

The loose normalizer is still used for the `In HubSpot` flag, where a fuzzy match is what you
want. It is no longer trusted on its own to decide that two rows are the same company.
