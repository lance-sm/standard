# Daniel sync — weekly prep assets

Supporting files for the cloud routine **"Tuesday prep — Daniel sync"**
(`trig_01B4fUrWUecWNfZHLc34DQ2h`), which runs Tuesdays at 11:00 UTC.

The routine runs in a cloud sandbox with **no access to Lance's local disk**, and
the Microsoft 365 connector returns extracted *text* rather than raw `.docx` /
`.xlsx` bytes. The templates therefore cannot be fetched from OneDrive at run
time — they have to live here, in the repo the routine checks out.

## Layout

```
daniel-sync/
  templates/
    agenda-template.docx        <- copy of "August 26 Agenda.docx"
    live-deals-template.xlsx    <- copy of "Live Deals Aug 19.xlsx"   (MISSING - see below)
  scripts/
    build_agenda_docx.py
    build_live_deals_xlsx.py
```

## ⚠ Missing file

`templates/live-deals-template.xlsx` is **not yet committed**. Copy
`Live Deals Aug 19.xlsx` from OneDrive `0 Inbox/` to that path and commit it.

Until it lands, `build_live_deals_xlsx.py` falls back to constructing a fresh
workbook from the style spec recorded in the script (Aptos Narrow 11, accounting
format on D/E/F, wrapped column H, the exact column widths). That output is
visually correct but is *not* the template-derived file, and the script prints
`[FRESH-WORKBOOK FALLBACK]` plus a stderr warning so the run reports it honestly.

## Usage

```bash
pip install openpyxl

python3 scripts/build_agenda_docx.py items.json "September 15 Agenda.docx"
python3 scripts/build_live_deals_xlsx.py deals.json "Live Deals Sep 15.xlsx" 2026-09-15
```

`items.json` — `[[level, text], ...]`, level `0` top-level, `1` sub-item.

`deals.json` — list of
`{dealname, stage, location, revenue, ebitda, description, deal_source}`.
`revenue` / `ebitda` may be `null`.

Column order (11 columns, one tab):

| A | B | C | D | E | F | G | H | I | J | K |
|---|---|---|---|---|---|---|---|---|---|---|
| Deal Name | Deal Stage | Last Contacted | Notes | Location | Revenue | EBITDA | Valuation Proposed | Multiple | Deal Description | Deal Source |

**Always written blank** — never inferred, never auto-filled:

- **Valuation Proposed** and **Multiple** — HubSpot has no such fields.
- **Last Contacted** (date, `m/d/yyyy`) and **Notes** — added 2026-10-12 at
  Lance's request, maintained by hand. HubSpot's `notes_last_contacted` is *not*
  a safe source: it only moves when an engagement is logged, so on 2026-10-12 it
  read 8/28 for New York City Alarm even though the LOI went out 10/6. Writing it
  would understate real contact and hide exactly the staleness the column exists
  to expose. The builder will pass through optional `last_contacted` / `notes`
  keys if they are ever present in `deals.json`, but the routine does not set them.

## Guarantees

`build_agenda_docx.py` copies the template package and replaces only the body
paragraphs. Verified: output namelist identical to the template, every
non-`document.xml` entry byte-identical, `sectPr` preserved, paragraph text and
`ilvl` reproduced exactly when fed the template's own content. If the
`w14:paraId="45034E33"` tail anchor is ever absent it aborts rather than emit a
mis-styled file — if that happens the template changed, and the script needs
updating, not the document.

`build_live_deals_xlsx.py` loads the template workbook itself, captures row 2's
per-column font / fill / number-format / alignment / border, clears the old data
rows and reapplies those styles cell by cell. Row heights follow the template
rule `ceil(len(description)/88) * 14.4`, floor `28.8`. Deals sort by stage
(Initial Meeting → NDA Sent → NDA Signed → Management Meeting → IOI → LOI → Due
Diligence), then alphabetically within a stage so week-to-week ordering is
stable.

## Handling note

Deal descriptions come verbatim from HubSpot and regularly contain internal
`KILL` diligence notes and price anchors. The generated spreadsheet is an
internal document — it must not be sent to a broker or seller as-is.
