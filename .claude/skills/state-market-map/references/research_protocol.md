# Research protocol

Work the state in this order. Acquisitions first - they tell you which names to strike
from the independent roster before you waste time researching a company that sold in 2023.

---

## 1. Acquisitions since 2015

Goal: every company headquartered in the state that was bought, absorbed, merged, or
rebranded under an acquirer since 1/1/2015.

### Source order (highest confidence first)

0. **Start with the master workbook.** `Target Research\Security_Fire_MA_2015_2026.xlsx`,
   built 7/28/26: 1,127 deals 2014-2026 with a pre-filtered **Northeast Targets** tab (175
   rows: Target, Acquirer, Year, City, State, Segment). Per state: NY 44, MA 37, PA 34,
   NJ 29, CT 17, RI 6, ME 5, NH 3. Filter to the state, then verify each row - the workbook
   is a lead list, not gospel. Rows with city "UNK" need a city before they can go on the
   map, and sprinkler-only names need a vertical ruling. Then continue with the sources
   below to catch anything added since.
1. **Acquirer newsrooms and "our brands" / "locations" pages.** The roll-ups list what they
   bought. Work the known consolidator list first - it is the highest-yield sweep in the
   whole build:
   Pye-Barker Fire & Safety, Pavion, Convergint, Encore Fire Protection, APi Group
   (Davis-Ulmer, Chubb), Summit Fire & Security, Impact Fire, Everon, Securitas Technology,
   Kastle, Minuteman Security & Life Safety, American Alarm & Communications, Sciens
   Building Solutions, Cook & Boardman, Fidelity Building Services Group, Knight Security,
   Hiller, Doyle Security, NSG-Norel, IML/Northwoods, Cobalt/Alpine, Bluejack.
   The live roster lives in `Target Research\Security_RollUps_Tracker_v4_2026-07-28.xlsx` -
   read it before sweeping, it is maintained and it changes.
2. **Trade press.** SecurityInfoWatch, Security Systems News, SDM Magazine, Security Sales &
   Integration, Fire Protection Contractor. Query pattern:
   `"<acquirer>" acquires <state>`, `<state> security company acquired 2015..2026`,
   `"joins <acquirer>" alarm <state>`.
3. **The target's own web presence.** A "now part of X" banner, a redirected domain, or a
   LinkedIn page renamed to "X, a Y company" is proof of sale even with no press release.
4. **State business registry.** Status changes, name changes, and merger filings date deals
   the press never covered. Free and authoritative for the year.
5. **ZoomInfo** company record: parent company field, `enrich_company_signals`, and
   `search_scoops` for M&A scoops.

### Rules

- Year comes from a dated source (press release, filing, dated post). LinkedIn "acquired"
  with no date is not a year - leave `year: null` and the page simply shows no year.
- Record the acquirer as the operating brand, not the fund. PE sponsor goes in `sponsor`
  (internal cut only) - e.g. acquirer "Pye-Barker Fire & Safety", sponsor "Altas Partners".
- Non-standard outcomes use `verb`: "now a brand of", "part of", "merged into".
- HQ relocations after the deal go in `note` ("HQ moved to North Carolina").
- Closures and dissolutions are NOT acquisitions. Keep them out of the list; mention in
  `notes` if the name is well known enough that its absence looks like an oversight.

---

## 2. The independent roster

Goal: every still-independent, in-state-HQ company in the four verticals above ~$1M revenue.

### Where they hide

- **ZoomInfo `search_companies`** by state + SIC/NAICS (7382 security systems services,
  561621 security systems installation, 238210 electrical contractors filtered by keyword)
  with revenue floor $1M. This is the backbone of the list.
- **State licensing boards.** Alarm installer, burglar/fire alarm contractor, and locksmith
  licenses are public in most Northeast states and catch companies with no web footprint.
  Fire alarm work also shows in state fire marshal contractor lists.
- **OEM dealer locators.** Brivo, Openpath/Motorola, LenelS2, Genetec, Milestone, ASSA
  ABLOY/Medeco distributor and dealer pages, Honeywell/Resideo, Napco, DMP, Alarm.com.
  These surface the real integrators and tell you the OEM affiliation for the description.
- **Associations.** PBFAA (PA), NEACC, NJELSA, NYELSA, CASIA (CT), ALOA chapters, NFPA
  member directories, and state ESA chapters. Membership lists are roster gold.
- **Distributor branch pages.** ADI, Anixter/Wesco, Norfolk Wire, Banner Solutions counter
  locations tell you where the density is.
- **Apollo** as fallback only, and never as the source of truth for LinkedIn pages.

### Inclusion test - all four must pass

1. HQ physically in the state (not a branch, not a satellite office of an out-of-state firm).
2. Independently owned - no PE platform, no strategic parent. PE-touched history alone does
   not disqualify a company as a target, but for THIS document "independent" means it is not
   currently owned by a platform or strategic.
3. Vertical fit: access control, locksmith/safe, fire & life safety, CCTV/video, alarm and
   integration.
4. Real company: ~$1M+ revenue estimate, a verifiable address or fleet, and an active
   footprint (site, licensing, reviews within ~18 months).

### Exclusions

Guard and manned-services firms. IT-only VARs and low-voltage cabling shops with no security
line. National branch offices. DIY/residential dealer-program resellers. One-truck mobile
locksmiths with a Google listing and nothing else. Wholesale central stations (they are
suppliers to this market, not participants in it).

Borderline calls get flagged in `notes`, never dropped silently.

### Sectioning

Section order drives the roster layout and the map has no opinion about it. Default three
sections, in this order:
1. Locksmiths & Safe Specialists
2. Fire & Life Safety
3. Security Integrators & Alarm Companies

Add a fourth ("Access Control Specialists" or "Video & Surveillance") only when the state has
enough pure-play names to justify it - roughly 6+. Otherwise those companies live in
Integrators & Alarm.

---

## 3. Verify and dedup

- **Live HubSpot CRM check** on every name (MCP portal 9c7432ec, never the stale snapshot
  CSV). The map is not a CRM export, but knowing what is already in the pipeline shapes what
  Lance does with it - note CRM overlap in `notes`, not on the page.
- **Cross-list check.** No company may appear in both `acquisitions` and `sections`. The
  build script hard-fails on this.
- **Ghost check.** An absorbed brand often keeps its old website for years. Before listing a
  company as independent, confirm no acquirer claims it: search `"<company>" "part of"`,
  `"<company>" acquired`, and check the company's LinkedIn "About" for a parent.
- **Dissolution check.** State registry status. Dissolved or "administratively dissolved"
  companies come off the roster.
- **Founding year.** Only from the company's own site/LinkedIn ("serving since 1948"), a
  state filing date, or ZoomInfo's founded field with corroboration. `~1955` is acceptable
  when the company itself says "mid-fifties" - the tilde is honest.
- **Count sanity.** Section counts print on the page automatically. Sanity-check the total
  against the prior version of the state file and explain any drop bigger than a couple of
  names.

---

## 4. What good looks like

Note on the shipped CT sample: it carries 13 acquisitions, all 2021-2026, because it was
built before the master workbook surfaced. The workbook has 17 CT rows including 2015, 2016
and 2020 deals, so CT is undercounted and needs a verification pass. Treat it as a format
example, not a finished state.

For Connecticut, July 2026: 13 acquisitions (4 to a single buyer, all falling 2021-2026), 80
remaining independents across three sections, every city spelled so it lands on the map, zero
overlap between the two lists, and a headline that states the trend without editorializing.

One extra field worth the effort: `city` on every row. It is what puts the company on the
map, and the map is the half of this document people remember.
