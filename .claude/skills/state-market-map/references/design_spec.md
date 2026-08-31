# Design spec

The look is locked in `scripts/build_map.py`. This file documents it so nobody has to
re-derive it. Change the constants at the top of the script; never restyle one state by
hand or the set stops looking like a set.

## Format

US Letter landscape, 1056 x 816px at 96dpi, 44px margins. Dark ground, mint accent, one
typographic voice per job: Inter for reading, JetBrains Mono for labels. Both are subset
and embedded in the file, so the PDF renders identically on any machine and nothing depends
on fonts being installed.

| Token | Value | Used for |
|---|---|---|
| Ground | `#08191c` | page background |
| Panel | `#0d2226` | legend and acquirer boxes |
| Rule | `#1b3b41` | hairlines, KPI dividers, borders |
| Mint | `#3ddfc4` | logo mark, "still independent" dots, top acquirer, accent phrase |
| Text | `#e8f2f2` | company names, headline |
| Muted | `#8aa2a6` | deck copy, absorbed rings, map labels |
| Dim | `#5f7a7e` | city metadata, footer |
| Land | `#132c31` / `#1e444b` | map fill / county lines |

Type: headline 37px Light with -0.9px tracking, KPI numbers 33px Light, company names 9.4px
Medium, city metadata 7.4px mono, section kickers 6.6-6.8px mono uppercase at ~1.7px
tracking. Mono uppercase with wide tracking is the label voice - it does the work that a
heavier weight would otherwise do, without shouting.

## Page 1 - the argument

1. **Header** - mint mark, wordmark, and the file's own identity on the right (market map,
   month, state, page N of M). Repeats on every page.
2. **Headline** - one sentence with the last phrase in mint. Generated from the data, so it
   cannot contradict the numbers below it.
3. **Deck** - three lines that say what happened, to how many, and how many are left.
4. **KPI strip** - four numbers behind hairline dividers: standing, absorbed, to a single
   buyer, and either the oldest verified founding year or the town count.
5. **Right rail** - the legend, then "Who is doing the buying" tallied from the deal rows
   with the most active buyer in mint. This is the panel people photograph.
6. **The map** - counties in near-black, a mint dot per town sized by how many independents
   sit there, a slate ring for every absorbed company. Towns holding both show a mint core
   inside a ring, which is the whole argument in one mark.

## Page 2+ - the rosters

"The thirteen that went" in two columns: ring bullet, company, city and year in mono, then
the acquirer on the line below with an arrow. "The eighty still standing" in four columns,
mint dot, company, city, founding year where verified, grouped by vertical with a mono
sub-header carrying the count.

## Internal cut

`--audience internal` adds PE sponsors after the acquirer, mint diamonds on succession
candidates, revenue bands where present, and a mint INTERNAL - NOT FOR DISTRIBUTION mark in
the footer. Everything else is identical, from the same data.

## What is allowed to change per state

Headline, deck, section names, the number of map labels, roster column count, and whether
founding years show. That is it. Color, type, geometry and page structure are global.

## Why the layout is code

Two reasons, both learned the expensive way.

A design pass re-narrates numbers it does not understand. Ask a model to make a roster
prettier and it will helpfully round a founding year, drop a city, or invent a tidy total.
Here the numbers only ever come from the JSON.

And overflow is silent. The first hand-designed draft of this document ran off the bottom of
page 2 mid-list, and the only way to catch that is to look at every page of every state,
every quarter, forever. Instead the builder lays out, measures the real rendered document,
lays out again until the numbers stop moving, and then asserts that nothing crosses the
footer rule. A state that needs four pages gets four pages without anyone noticing.
