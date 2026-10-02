# Recovering the 796 unreadable sites — local run

The cloud container routes HTTPS through a proxy that re-terminates TLS, so
Chromium there refuses to load any page and the JS-rendered sites could not be
read. On a normal machine there is no such interception and a real browser just
works. This is the kit for that run.

## What it recovers

Of 1,204 rows that came back `Unknown`:

| Cause | Rows | Recoverable here? |
|---|---|---|
| Thin / JS-only site | 639 | yes |
| Blocked by bot protection | 157 | yes — real Chrome passes the challenge |
| Not reachable (dead domain) | 333 | no, the site is gone |
| Site down / parked | 43 | no |
| No domain on the row | 31 | nothing to fetch |

So **796 rows**, carrying **1,806 contacts**. Expect to convert most of them;
some will still fail (a few are dead behind a JS shell).

## What is already here

- `recrawl-worklist.csv` — the 796 domains, with why each failed
- `base-classified.jsonl` — all 6,418 verdicts from the cloud run, so the browser
  pass only has to do the 796 and merge. Nothing else re-crawls.
- `pipeline/render_pass.py` — renders with Playwright, then hands the rendered
  HTML to the same parsing code the static crawler used, so classification
  behaves identically; only the fetch differs
- `pipeline/merge_classified.py` — overlays the new reads onto the base

## You need one thing from your own machine

Your export of the Companies tab (the CSV you sent me: `CSV for Claude.csv`).
It holds the contact columns, which were deliberately **not** committed to the
repo — 12,522 people's names and addresses do not belong in git.

## Run it

    cd broker-segmentation
    pip install requests beautifulsoup4 lxml openpyxl playwright
    playwright install chromium

    # 1. normalise your Companies CSV (point at wherever yours sits)
    python3 pipeline/csv_to_tsv.py ~/Downloads/"CSV for Claude.csv" companies_full.tsv

    # 2. render the 796 - about 10 minutes
    python3 pipeline/render_pass.py recrawl-worklist.csv rendered

    # 3. classify just those, then merge onto the base
    python3 pipeline/classify.py rendered
    python3 pipeline/merge_classified.py base-classified.jsonl rendered/classified.jsonl merged.jsonl

    # 4. rebuild the workbook
    python3 pipeline/build_workbook.py companies_full.tsv merged.jsonl "Farm Broker List - segmented v2.xlsx"

`render_pass.py` is resumable — if it dies, re-run the same command and it skips
what it already did.

## Knobs

- `SETTLE_MS=2800` — how long to wait after DOM load for client-side rendering.
  Raise to 4000+ if thin results persist.
- `NAV_TIMEOUT=30000` — per-navigation timeout in ms.
- It runs one browser context serially on purpose: gentler on the sites and
  easier to debug. For more speed, run it against a split worklist in two
  terminals with different output dirs, then merge both.

## Sanity check when it finishes

The merge prints how many rows the browser actually improved. Compare the
Summary tab's Coverage block before and after — `Thin / JS-only site` and
`Blocked by bot protection` should both drop sharply, and `Specialist` /
`Generic` should rise by roughly the same total. If `Unknown` barely moves,
raise `SETTLE_MS` and re-run the stragglers.
