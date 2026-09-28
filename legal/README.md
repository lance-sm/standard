# legal/

Deal documents Badlands sends to sellers. Not legal advice — every document here is a
starting draft for counsel to review before it goes out on a live deal.

## NDAs

`templates/mutual-nda.md` is the standing form: a mutual NDA sized for a lower-middle-market
acquisition conversation. Mutual rather than one-way, because Badlands shares its own thesis,
financing and structure with a seller as readily as the seller shares financials.

Terms the form takes as given (change them in the template, not per deal, unless a seller asks):

| Term | Setting | Why |
|---|---|---|
| Confidentiality term | 2 years from the Effective Date | Trade secrets run longer, for as long as they stay trade secrets. |
| Employee non-solicit | 24 months, mutual | Carve-outs for general advertising, unsolicited applicants, and anyone gone 6+ months. |
| No-contact | Badlands goes through the seller's designated contact only | The clause owners actually care about — no calls to their techs, customers or landlord. |
| Existence of discussions | Confidential on both sides | Sellers are usually talking to other buyers and cannot be seen to be in market. |
| Governing law | New York, New York County, jury waived | Most targets are NY/NJ/CT. Change per deal for an out-of-state seller. |
| Standstill | None | Not applicable to private targets. |

### Building one

Copy an existing parameter file in `nda/`, edit it, and run:

```
python3 legal/scripts/build_nda.py legal/nda/<slug>.json
```

That writes `<slug>.md` (the filled text, reviewable in a diff) and `<slug>.docx`
(signature-ready, two-column signature block and notice addresses).

Anything left as `[[CONFIRM: ...]]` in the parameter file is an open item: it renders
**bold and highlighted yellow** in the .docx and the script lists it on stdout. Never send a
document with a highlight still in it.

| File | Deal |
|---|---|
| `nda/ameritech-systems-corp.json` | Ameritech Systems Corp. (Flushing, NY) — Steven Lee, President. Drafted 2026-09-28 after the intro call. |
