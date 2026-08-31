---
name: state-market-map
description: Build a Badlands state market map - a dark landscape PDF showing every independent security, locksmith, fire and life safety and CCTV company headquartered in one state on a dot map, plus every acquisition of an in-state company since 2015 (company, city, year acquired, acquirer). Use when Lance asks for a market map, a state landscape, an independents roster, a consolidation wave, or who has been bought in a given state. Covers the 9-state Northeast: CT, MA, ME, NH, NJ, NY, PA, RI, VT.
---

# Badlands State Market Map

## What this produces

From one researched dataset, three artifacts:

| File | Purpose |
|---|---|
| `data/<state>.json` | The verified dataset. Durable asset - kept and diffed on every refresh so the map becomes a time series. |
| `Badlands_<ST>_Market_Map_<Month_Year>.pdf` | External cut. Shareable with owners, brokers, OEM reps. |
| `..._INTERNAL.pdf` | Internal cut. Same data plus PE sponsors, succession flags, revenue bands. Never send this out. |

Page 1 is the argument: headline, KPI strip, who is doing the buying, and a dot map of where
the companies actually are. Page 2+ are the rosters - the ones that went, and the ones still
standing.

## Rule zero: research fills a JSON, code draws the map

Do not hand the roster to a design step. Two failure modes, both seen in this project: a
design pass silently rewrites numbers it does not understand, and a hand-built page overflows
the bottom edge mid-list with no warning. `scripts/build_map.py` measures the real rendered
document and re-lays it out until nothing crosses the footer rule.

Design decisions still belong to a human - color, hierarchy, what the page argues. Make them
once, in the script, and every state inherits them. See `references/design_spec.md`.

## Workflow

**1. Frame it.** Confirm the state and the as-of month. If `data/<state>.json` already
exists this is a refresh: research what changed, then lead the summary with the delta.

**2. Acquisitions since 2015.** Every company HQ'd in the state bought, absorbed, or
rebranded under an acquirer. `references/research_protocol.md` section 1 for source order.
Required: company, city, acquirer, source. Year where verifiable - `null` if not.

**3. Independent roster.** Still-independent, in-state-HQ companies in the four verticals.
Section 2 for inclusion tests. Required: company, city. Founding year where verified.

**4. Verify and dedup.** Section 3. Live HubSpot cross-check, no company on both lists, kill
the ghosts (absorbed brands still running an old website).

**5. Build.**
```bash
python3 scripts/build_map.py data/connecticut.json                      # external
python3 scripts/build_map.py data/connecticut.json --audience internal  # internal
```
Validation runs first and refuses to render on a structural error. Watch stderr for
`[OVERFLOW]` (a layout bug - report it, do not ship around it) and for towns with no
coordinate match (usually a misspelled city).

**6. QC and deliver.** Run `references/qc_checklist.md`. Ship both PDFs, save the JSON, and
lead the summary with: independents remaining, absorbed since 2015, most active acquirer.

**7. Send it.** The map is a door opener - `references/outreach_email.md` has the two emails
that carry it, numbers swapped per state. Attach the external cut only.

## Hard rules

- **2015 cutoff** on acquisition history. The page auto-labels the window from the earliest
  verified year, so a state whose deals all fall after 2021 reads "absorbed since 2021".
- **Never guess a year.** Unverified prints as nothing rather than a number that a founder
  will notice is wrong.
- **In-state HQ only.** A national with a branch in Hartford is not a Connecticut company.
- **No company on both lists.** The validator hard-fails. This is the single most
  embarrassing failure mode - pitching a shop that sold two years ago.
- **Every row traceable.** Fill `source` on acquisitions. Unsourced does not ship.
- **Verticals:** access control, locksmith/safe, fire & life safety, CCTV/video, alarm and
  integration. Excluded: guard services, IT-only VARs, national branches, DIY dealer
  programs, one-truck locksmiths with no verifiable footprint, wholesale central stations.
- **Revenue floor** ~$1M ZoomInfo estimate. Flag borderline names in `notes`, never drop silently.
- **Founding years are optional.** They add texture and drive the "oldest shop still
  owner-run" KPI, but they are the softest number on the page. `"show_founded": false` drops
  every one of them and swaps that KPI for the town count. Use it for any state where the
  years cannot be sourced confidently.
- **House style:** hyphens, never em dashes. No pitch language in the external cut.

## Reference files

- `references/research_protocol.md` - where to look, in what order, what counts as verified
- `references/data_schema.md` - the JSON contract, field by field
- `references/design_spec.md` - the locked look and what may vary per state
- `references/outreach_email.md` - the two emails that carry the map (Industry Contact / Seller)
- `references/qc_checklist.md` - the pre-ship gates
- `examples/connecticut.json` - a complete, real state file to copy

## Assets

`assets/geo/*.json` county outlines for the 9 Northeast states, `assets/places_ne.csv` town
coordinates (8,221 places, covers villages like Plantsville), `assets/fonts/*.woff2` subset
Inter and JetBrains Mono embedded in the output. No network access needed at build time.

## Where files live

`Target Research\Market Maps\` on OneDrive, JSONs under `data\`. Keep prior versions - the
quarter-over-quarter diff ("three more absorbed since March") is the most persuasive line in
the document and it only exists if the old file was saved.

## Refresh cadence

Quarterly per state, or immediately when the weekly M&A scan flags an in-state deal.
