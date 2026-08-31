# QC checklist - run before every ship

The external cut goes to owners and brokers. One wrong fact costs a relationship.

## Build output

- [ ] Script exited clean. No `VALIDATION FAILED`.
- [ ] No `[OVERFLOW]` on stderr. If one appears, the layout engine has a bug worth fixing -
      say so, do not paper over it by cutting rows.
- [ ] No `[warn] no coordinates for:` towns. Each one is a company missing from the map,
      almost always a misspelled or non-postal city name. Fix the spelling in the JSON.

## Data integrity

- [ ] No company appears in both the acquisition list and the independent roster.
- [ ] Every acquisition row has a `source`. Spot-check three at random against the live web.
- [ ] Every acquisition target was actually HQ'd in this state, not a branch the acquirer's
      press release happened to mention.
- [ ] No guessed years anywhere. Undated deals show no year and that is correct.
- [ ] Founding years spot-checked on the five oldest names - those drive the KPI and are the
      ones people notice. If they cannot be sourced, set `show_founded: false` for the state.
- [ ] Dissolved or absorbed companies removed from the roster.

## The page

- [ ] Open the PDF and look at every page. Nothing clipped, no orphan sub-header, columns
      reasonably balanced.
- [ ] Headline and deck read as true sentences and agree with the KPI numbers.
- [ ] Map: dot density looks right against the roster, no label collisions or labels running
      off the frame, the biggest dots are where you would expect them.
- [ ] Acquirer panel totals equal the number of dated and undated deals in the roster.
- [ ] Hyphens throughout, zero em dashes.

## Audience

- [ ] External cut has no PE sponsors, no succession diamonds, no revenue bands, no INTERNAL
      mark. Confirm by looking, not by trusting the flag.
- [ ] Internal cut is named `_INTERNAL` and is never the file attached to an owner email.

## Delivery

- [ ] Both PDFs surfaced in chat.
- [ ] `data/<state>.json` saved alongside the prior version, not over it.
- [ ] Summary states independents remaining, absorbed since the window start, most active
      acquirer, and what changed since the last version.
