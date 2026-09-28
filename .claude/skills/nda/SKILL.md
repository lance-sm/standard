---
name: nda
description: Draft a Badlands NDA for a seller conversation and open it in Word. Use for any ask that involves an NDA, a mutual non-disclosure, a confidentiality agreement, "send X an NDA", "NDA <company>", or a seller asking for one before sharing financials. Covers looking the counterparty up in HubSpot, filling the standing form, and the mandatory auto-open in Word.
---

# NDA (seller confidentiality agreement)

Produces a signature-ready mutual NDA for an acquisition conversation, filled from HubSpot,
opened in Word for review. Invoked as `/nda <company>` or by any NDA ask.

This is not legal advice. Every draft is a starting point for counsel before it goes out on a
live deal — say so when handing one over, once, without belabouring it.

## The run

### 1. Identify the counterparty in HubSpot

Search COMPANY for the name given. Then pull, in one pass:

- the company record — legal name, city, state, domain, description, `lifecyclestage`
- its associated CONTACT — the owner or president, their title and email; that is the signatory
- the most recent MEETING and CALL — the deal context, and whether an NDA was actually promised

Take the **legal** entity name, not the CRM display name. A meeting booking form ("Company name:
Ameritech Systems corp") or the company website footer usually carries it. If the two disagree,
or the suffix is unclear (Corp. vs Inc. vs LLC), make it an open item rather than guessing —
a misnamed party is the one defect that makes the signature worthless.

### 2. Fill the parameters

Copy the nearest existing file in `legal/nda/` to `legal/nda/<slug>.json` and edit it.
Anything not established from HubSpot, the repo or Lance's own words goes in as
`[[CONFIRM: what is missing]]`. Never invent a legal entity name, a state of formation, or a
street address. Badlands' own entity details are not in this repo — until Lance supplies them
they stay as open items on every draft.

### 3. Build, and open in Word

```
python3 legal/scripts/build_nda.py legal/nda/<slug>.json
```

**The .docx opens in Word automatically, on every run. That is the default and it stays that
way** — it is how Lance reviews these. Do not pass `--no-open` unless he asks for it in that
moment. In a cloud session there is no desktop to open on; the script says so and skips, and
in that case deliver the .docx to him directly so it is one click from Word on his end.

### 4. Report the open items

The script lists every unresolved `[[CONFIRM: ...]]` and highlights it yellow in the .docx.
Repeat that list back as the headline of the reply, not a footnote. **A document with a
highlight still in it never goes to a counterparty.** Once Lance supplies the missing values,
edit the JSON and re-run — one command, same output paths.

## Standing terms

Set in `legal/templates/mutual-nda.md`. Change them there, not per deal, unless a specific
seller asks for something different:

| Term | Setting |
|---|---|
| Shape | Mutual — Badlands shares its thesis, financing and structure as freely as the seller shares financials |
| Confidentiality term | 2 years; trade secrets for as long as they remain trade secrets |
| Employee non-solicit | 24 months, mutual, carved out for general advertising, unsolicited applicants, anyone gone 6+ months |
| No-contact | Badlands goes through the seller's designated contact only — no employees, customers, suppliers, lenders, landlords or insurers |
| Existence of discussions | Confidential both ways — sellers are usually talking to other buyers and cannot be seen to be in market |
| Governing law | New York, New York County, jury waived. Change per deal for an out-of-state seller |
| Standstill | None — not applicable to private targets |

The no-contact and non-solicit clauses are the ones owners actually read. When Lance sends the
draft on, those are what to point him at.

## Invariants

- **Never send an NDA to a counterparty.** Draft it, open it, hand it to Lance. Emailing a deal
  document to a seller is his call every time, even when the ask sounds like "send Steven an NDA".
- **A cover email is outreach copy.** If one is wanted, read `.claude/skills/outreach-writing/SKILL.md`
  and `outreach/SAGARIS-RULES.md` in full before drafting a line of it.
- Commit the `.json`, the `.md` and the `.docx` together. The `.md` is what makes a redraft
  reviewable in a diff.

## Where things live

| Path | What it is |
|---|---|
| `legal/templates/mutual-nda.md` | The standing form, with `{{TOKENS}}` |
| `legal/scripts/build_nda.py` | Renderer — fills the form, writes `.md` + `.docx`, opens Word |
| `legal/nda/<slug>.json` | Per-deal parameters |
| `legal/nda/<slug>.md` / `.docx` | Generated. Rebuild rather than hand-edit |
| `legal/README.md` | The same ground, for someone reading the repo without this skill loaded |
