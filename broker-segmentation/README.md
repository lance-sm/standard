# Broker farm segmentation

Reads every website on the Farm Broker List and records what each firm's own site
says, rather than guessing from its name: whether it is generic or specialised,
which verticals it actually works in, and whether it has closed security, fire or
life-safety deals.

Built 2026-10-01 for the Farm Broker List (`1 Pipeline/Target Lists & Universes/
Farm Broker List - Clean.xlsx` in Lance's OneDrive): 6,450 rows, 5,424 of them
brokers.

## Why this exists

The source file already had a `Broker Type` column, but it was a keyword read of
the company name and domain — its own Summary tab called it "a rough guide, not
verified - check websites before relying on it." This replaces that guess with a
read of each site.

## Run it

    ./run_all.sh <companies.tsv> <outdir> <dest.xlsx>

`companies.tsv` is tab-separated with a header containing at least `Company` and
`Domain`. To get there from an Excel export:

    python3 pipeline/csv_to_tsv.py exported.csv companies.tsv

Five passes: crawl, retry what failed, classify, dig deeper where no sector was
read, build the workbook. The crawl is resumable — re-running skips domains
already in `<outdir>/index.jsonl`, so an interrupted run picks up where it left
off. Budget ~1.5-2 hours for 6,450 sites.

## Output

Three tabs. **Summary**: coverage, generic vs specialist, verticals ranked by
firm count, security-deal evidence, firm type. **Companies**: a row per company
with `Focus`, `Verticals`, `Security Deals`, `Security Evidence`, `Firm Type
(verified)`, `Site` and `Page Checked`. **Security Deal Hits**: just the firms
showing security/fire/life-safety deal evidence, with the quote and the page it
came from.

## Things that were wrong before they were fixed

Worth knowing, because each one silently corrupted results:

- **"The M&A landscape"** was being counted as a landscaping specialist.
- **"SPA"** (share purchase agreement) was being counted as a day spa.
- **"Financial advisor"** is how these firms describe *themselves*, so it was
  tagging almost everyone as a wealth-management specialist.
- **Cyber security deals were counting as physical security.** This was the worst
  one — a network-security deal read as a Badlands-type hit. `taxonomy.py` now
  splits unmistakably physical language (`alarm`, `locksmith`, `CCTV`, `central
  station`, `fire alarm`) from wording that could be either (`security company`,
  `systems integrator`), and the ambiguous set only counts when no cyber wording
  sits in the same sentence. See `classify.is_physical_security`.
- **Soft 404s.** Many sites answer any path with their homepage at HTTP 200, so
  probing `/industries` returned the homepage again and double-counted every
  keyword on it. The crawler now fingerprints page text and drops echoes.

## Known limits

- **~14% of rows come back `Unknown`**: dead domains, parked sites, and JS-only
  sites that need a rendering browser. Headless Chromium would recover most of
  the JS-only ones but needs a TLS permission this sandbox denies, so these are
  labelled by exact reason instead of guessed at.
- Verticals are what a site *claims*, not deal history. `Security Deals` is the
  column backed by evidence.
- A firm naming several sectors is counted under each, so the vertical counts on
  the Summary tab do not sum to the company total.
