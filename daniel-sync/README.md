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
`revenue` / `ebitda` may be `null`. **Valuation Proposed** and **Multiple** are
always written blank; HubSpot has no such fields and they must never be inferred.

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
