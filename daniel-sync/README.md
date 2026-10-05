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
    live-deals-template.xlsx    <- copy of "Live Deals Aug 19.xlsx"
  scripts/
    build_agenda_docx.py
    build_live_deals_xlsx.py
```

Both templates are committed and verified present as of 2026-10-05. (An earlier
version of this file claimed `live-deals-template.xlsx` was missing; it is not.)
If either template is ever deleted, `build_live_deals_xlsx.py` falls back to
constructing a fresh workbook from the style spec recorded in the script (Aptos
Narrow 11, accounting format on D/E/F, wrapped column H, the exact column
widths). That output is visually correct but is *not* the template-derived file,
and the script prints `[FRESH-WORKBOOK FALLBACK]` plus a stderr warning so the
run reports it honestly. `build_agenda_docx.py` aborts outright rather than emit
a mis-styled document.

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

## Where the deliverables go  (corrected 2026-10-05)

**Primary destination — Acquisitions SharePoint, one folder per meeting date.**

Drive id `b!AjvqY5-7oUGnL66ShD9sTLE9RuTBi5tMkq6crSzvqU3pO6DGZYzaQ72XNf-pUIpX`

| Folder | Item id |
|---|---|
| `Biz Dev` | `01ATLQUZBDEWY24DOKHJBLTWWUL2GZB5LW` |
| `Biz Dev/Weekly Agendas & Docs` | `01ATLQUZEOATC35R5DHJBYXGALCYGTZ5XS` |
| `Biz Dev/Weekly Agendas & Docs/October 5` | `01ATLQUZGDYJ5TNIN5DRGJHC3QPLP5RARB` |

Each run creates a **new dated subfolder directly under `Weekly Agendas & Docs`**,
named `"<Month> <Day>"` — e.g. `October 5`, matching the existing `September 28`.
Use `sharepoint_create_folder` with `parentItemId` =
`01ATLQUZEOATC35R5DHJBYXGALCYGTZ5XS`. Do **not** nest under a month folder: July
and August did that, September 28 onward is flat, and flat is the current
convention.

All three deliverables go in that dated folder: the agenda `.docx`, the live
deals `.xlsx`, and the current BD scorecard.

**OneDrive `0 Inbox`** (secondary / staging only)

Drive id `b!sRY4CJgKn0ue4_YulSpe6Vi0hWolvkdPjEqf1z-VtlIq9yYGd7DER477LYoouoxm`

| Folder | Item id |
|---|---|
| `0 Inbox` | `01XYRJS5B47CCG5ILBT5HLRX56JSBD6ZHM` |
| `4 Admin/Calendar & Meetings` | `01XYRJS5BFPCX4RDSE6BCYREJB6QQWQJDE` |

⚠ The id `01XYRJS5DJDOILEMV4OZBK6FZV3DAOKL3J`, which the routine prompt carried
for `0 Inbox`, is **dead** — it returns `NOT_FOUND`. The live id is the one
above, and it is also in `.claude/skills/file-inbox/SKILL.md`, which is the
authoritative list. Never hardcode a folder id in the routine prompt; read it
from that skill.

## Known tooling limit: binary upload

`mcp__Microsoft-365__sharepoint_upload_file` has **no file-path parameter**. It
accepts only `content` (UTF-8 text) or `contentBase64`. A `.docx` / `.xlsx`
therefore has to be base64-encoded into the model's own context and re-emitted
by hand, which for a ~10-20 KB file is 13k-26k characters and is **not reliably
transcribable** — a single dropped or duplicated character fails validation.

So the routine instruction "pass the local file path to the upload tool" cannot
be followed: no such parameter exists.

What does work without any transcription:

- **`sharepoint_copy_item`** — server-side, cross-drive, no bytes through
  context. Use it for anything that already lives in OneDrive or SharePoint
  (e.g. the BD scorecard from `4 Admin/Calendar & Meetings`).
- **`sharepoint_create_folder`**, `sharepoint_move_item`, `sharepoint_rename_item`
  — all metadata-only.

The two *generated* files (agenda, live deals) have no server-side source to copy
from, so until the connector grows a path-based upload they must be placed by
hand, or generated into a location the connector can already see. They are
committed to this folder each week so the run always leaves a durable copy.

### Do not attempt a base64 upload of a generated file

Proven the hard way on 2026-10-05. Two hand-transcription attempts at
`Live Deals Oct 5.xlsx` (10,096 bytes / 13,464 base64 chars):

- Attempt 1 **with** `expectedBytes` — rejected, `bad_length`, 13,493 chars
  received (29 too many). Nothing was written. Correct outcome.
- Attempt 2 **without** `expectedBytes` — **accepted, and wrote 18,001 bytes**,
  i.e. a duplicated chunk, a silently corrupt workbook sitting in the deal
  folder under a name that looks right. It had to be found by comparing the
  reported byte count against the local file and then deleted.

So: `expectedBytes` is the only thing standing between a dropped character and
a corrupt file that nobody notices until Daniel opens it. Never omit it. And
treat the byte count in the success message as something to check, not to
trust — compare it against `stat -c%s` on the source before moving on.

**Correction, same day.** A third attempt was made using indexed 1000-character
blocks (`print('%05d|%s' % (i, b[i:i+1000]))`) to make the ordering verifiable,
**and passing `expectedBytes=10096`**. It uploaded **18,004 bytes anyway** — the
guard did not reject it. So:

- `expectedBytes` catches a *malformed* payload (attempt 1, `bad_length`, nothing
  written) but did **not** catch a well-formed payload of the wrong length.
  Do not rely on it.
- Three attempts, three failures; two of them wrote a corrupt workbook into the
  deal folder that had to be deleted.
- The payload keeps arriving at roughly 24,000 characters instead of 13,464,
  i.e. something in the path is duplicating content, and no amount of care in
  the re-emission fixes it.

**Conclusion: a generated `.docx`/`.xlsx` cannot be uploaded through this
connector. Do not try.** Build the files, commit them here, and hand them to
Lance to drop into the dated SharePoint folder — that is the supported path
until the connector gains a file-path upload. Everything that already exists in
OneDrive or SharePoint (the BD scorecard) goes across fine with
`sharepoint_copy_item`, which touches no bytes.
