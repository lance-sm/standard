# Data schema

One JSON file per state, saved as `data/<state>.json` and kept forever. The build script
validates it before rendering and exits non-zero on a structural error.

Everything on page 1 - the headline, the deck paragraph, the KPI numbers, the acquirer
panel, the dot map - is computed from the two lists below. You write facts; the script
writes the sentences.

```jsonc
{
  "state": "Connecticut",        // required
  "state_abbrev": "CT",          // required for the map (picks assets/geo/CT.json)
  "as_of": "July 2026",          // required, appears in the header and filename
  "audience": "external",        // "external" | "internal" (CLI --audience overrides)
  "brand": "Badlands",
  "tagline": "Security Company",
  "hq": "New York, NY",
  "show_founded": true,          // false = drop every founding year from the page
  "map_labels": 9,               // how many towns get a name on the map
  "roster_cols": 4,              // columns on the roster pages

  "acquisitions": [
    {
      "company": "Integrated Security Group",  // required
      "city": "Middletown",                    // required - also places the map ring
      "year": 2022,                            // int 2015-2030, or null if unverified
      "acquirer": "Pye-Barker Fire & Safety",  // operating brand, not the fund
      "sponsor": "Altas Partners",             // internal cut only
      "verb": "part of",                       // optional, replaces "acquired by"
      "note": "HQ moved to North Carolina",    // optional
      "source": "trade press"                  // required in practice - your audit trail
    }
  ],

  "sections": [
    {
      "name": "Locksmiths & Safe Specialists", // count appended automatically
      "items": [
        {
          "company": "Karpilow Safe & Lock",   // required
          "city": "Bridgeport",                // required - places the map dot
          "founded": 1870,                     // int, or "~1955", or omit
          "succession": true,                  // internal only - mint diamond
          "revenue_band": "$1-5M"              // internal only, optional
        }
      ]
    }
  ],

  "footer_note": "Compiled July 2026 from ZoomInfo, state records, industry press ...",
  "notes": ["Borderline calls and source caveats - never rendered on the page"]
}
```

## Optional overrides

Use these only when the generated line is wrong or flat. The defaults are usually better
than a hand-written one because they cannot contradict the data.

| Field | Overrides |
|---|---|
| `headline` | The page-1 headline. HTML allowed: `<br>` for the line break, `<em>` for the mint phrase. |
| `deck` | The paragraph under the headline. |
| `acq_title` / `ind_title` | "The thirteen that went" / "The eighty still standing". |
| `map_title` | "Where they are". |
| `extra_kpis` | `[{"value": 45, "label": "Trucks at the largest"}]` - fills any unused KPI slot. |

## Behavior you get for free

- **Sentences from data.** Headline, deck, KPI labels and the "absorbed since YYYY" window
  all derive from the rows. Add an acquisition and every number on page 1 updates.
- **KPI slot four** shows the oldest verified founding year, or - when `show_founded` is
  false or no years are verified - the number of towns holding an independent.
- **The acquirer panel** is tallied from `acquirer`, sorted by deal count, top buyer in mint.
- **The map** places a mint dot per town (size = number of independents) and a slate ring
  for absorbed companies, from `assets/places_ne.csv`. A town with no coordinate match is
  reported on stderr rather than silently dropped - fix the spelling or add the place.
- **Sorting.** Acquisitions by year ascending, undated last. Firms by founding year, unknown
  last (alphabetical within that group). With `show_founded: false`, firms sort alphabetically.
- **Pagination.** Lay out, measure the real rendered document, lay out again until the
  numbers stop moving, then assert nothing crosses the footer rule. Big states just add pages.

## Validation errors that stop the build

- missing `state` or `as_of`
- an acquisition or firm row with no company name
- an acquisition year outside 2015-2030
- the same company listed twice across sections
- the same company listed as both acquired and independent
