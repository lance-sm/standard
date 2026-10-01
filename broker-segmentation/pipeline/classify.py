# -*- coding: utf-8 -*-
"""Turn crawled site text into a verified read: generic vs specialist, which
verticals, and whether the firm shows evidence of security-sector deals."""
import gzip, json, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from taxonomy import (VERTICAL_RE, GENERALIST_RE, SPECIALIST_RE, TRANSACTION_RE,
                      TRANSACTION_WEAK_RE, WEAK_ALONE, WEAK_ALONE_MIN, DEAL_PAGE_HINTS,
                      PHYSICAL_HARD_RE, PHYSICAL_STRONG_RE, PHYSICAL_WEAK_RE, CYBER_RE,
                      ALARM_RE, ALARM_NONSECURITY_RE)


def is_physical_security(line):
    """Physical security / life safety only. Never a cyber deal, and never a
    sleep app's 'smart alarm' or a 'sounded the alarm' metaphor."""
    alarm = bool(ALARM_RE.search(line)) and not ALARM_NONSECURITY_RE.search(line)
    if CYBER_RE.search(line):
        return bool(PHYSICAL_HARD_RE.search(line)) or alarm
    return bool(PHYSICAL_STRONG_RE.search(line)) or alarm


def is_ambiguous_security(line):
    """'security company' with no other clue - a human has to look."""
    return bool(PHYSICAL_WEAK_RE.search(line)) and not CYBER_RE.search(line)


OUT = sys.argv[1] if len(sys.argv) > 1 else "out"
DATA = os.path.join(OUT, "sitetext")


def safe_name(d):
    return re.sub(r"[^a-z0-9.-]", "_", d.lower())


def load_blocks(domain):
    p = os.path.join(DATA, safe_name(domain) + ".txt.gz")
    if not os.path.exists(p):
        return []
    txt = gzip.open(p, "rt", encoding="utf-8").read()
    blocks, cur_url, cur = [], "", []
    for ln in txt.split("\n"):
        if ln.startswith("### "):
            if cur:
                blocks.append((cur_url, cur))
            cur_url, cur = ln[4:].strip(), []
        else:
            cur.append(ln)
    if cur:
        blocks.append((cur_url, cur))
    return blocks


BANK_RE = re.compile(r"\b(?:member fdic|fdic[- ]insured|equal housing lender|checking account|savings account|nmls #)", re.I)
LAW_RE = re.compile(r"\b(?:attorneys? at law|law offices of|attorney advertising|\besq\.|bar association)", re.I)
CPA_RE = re.compile(r"\b(?:certified public accountant|\bcpa firm|tax preparation services|audit and assurance)", re.I)

# "Main street" business brokerage
BIZBROKER_RE = re.compile(
    r"\bbusiness brokerage?\b|\bbusiness brokers?\b|\bmain street\b|\bbusinesses for sale\b"
    r"|\bbusiness for sale\b|\bsell your business\b|\bbuy a business\b|\bbusiness intermediar"
    r"|\bbusiness sales\b|\blistings?\b|\bbuyers? and sellers?\b|\bbroker of record\b", re.I)
# Advisory / investment banking
IB_RE = re.compile(
    r"\binvestment bank|\bm&a advisor|mergers (?:&|and) acquisitions advisor|sell[- ]side|buy[- ]side"
    r"|middle[- ]market|\bcapital advisor|corporate finance|\bfinancial advisory\b"
    r"|\bm&a\b|mergers (?:&|and) acquisitions|\bdivestiture|\brecapitaliz|\bfairness opinion", re.I)
# Principal buyer rather than intermediary
BUYER_RE = re.compile(
    r"\bprivate equity\b|\bwe acquire\b|\bportfolio companies\b|\bsearch fund\b|\bfamily office\b"
    r"|\bholding company\b|\bour investments\b|\bwe invest in\b|\bacquisition criteria\b"
    r"|\bwe buy businesses\b|\bour portfolio\b|\bwe partner with founders\b", re.I)
CRE_RE = re.compile(r"\bcommercial real estate\b|\brealty\b|\breal estate brokerage\b|\blisting agent\b|\bmls\b|\bsquare (?:feet|foot)\b", re.I)

NAME_BB = re.compile(r"biz ?broker|business ?broker|sunbelt|transworld|murphy business|first choice|vr business", re.I)
NAME_IB = re.compile(r"partners|advisor|capital|securities|m&a|mergers|investment|corporate", re.I)


def broker_category(text, name=""):
    """What the firm actually is, read off its own site; name only breaks ties."""
    if BANK_RE.search(text):
        return "Not a broker - bank"
    if LAW_RE.search(text):
        return "Not a broker - law firm"
    if CPA_RE.search(text):
        return "Not a broker - accounting firm"
    bb, ib = len(BIZBROKER_RE.findall(text)), len(IB_RE.findall(text))
    buyer, cre = len(BUYER_RE.findall(text)), len(CRE_RE.findall(text))
    if buyer >= 3 and buyer > bb and buyer > ib:
        return "Buyer (PE / holdco)"
    if cre >= 4 and cre > bb and cre > ib:
        return "Real estate brokerage"
    if bb >= 2 and bb >= ib:
        return "Business broker"
    if ib >= 2:
        return "M&A advisory / investment bank"
    if bb or ib:
        return "Business broker" if bb > ib else "M&A advisory / investment bank"
    if buyer:
        return "Buyer (PE / holdco)"
    if NAME_BB.search(name):
        return "Business broker (from name only)"
    if NAME_IB.search(name):
        return "M&A advisory / investment bank (from name only)"
    return "Unclear from site"


BLOCK_RE = re.compile(r"sgcaptcha|just a moment|one moment, please|you are being redirected"
                      r"|checking your browser|attention required|cloudflare|enable javascript"
                      r"|access denied|403 forbidden|are you a robot|verify you are human", re.I)
DEAD_RE = re.compile(r"undergoing maintenance|wordpress\s*.\s*error|account suspended|coming soon"
                     r"|domain (?:is )?for sale|this site can.t be reached|parked|site not found"
                     r"|under construction|database error|502 bad gateway|service unavailable", re.I)


def site_reason(rec, full):
    """Name the failure precisely so Lance knows which rows a human must look at."""
    probe = " ".join([rec.get("title") or "", rec.get("head") or "", full[:1500]])
    if BLOCK_RE.search(probe):
        return "Blocked by bot protection"
    if DEAD_RE.search(probe):
        return "Site down / parked"
    return "Thin / JS-only site"


def classify(rec):
    domain = rec["domain"]
    out = {"company": rec["company"], "domain": domain,
           "site": "", "focus": "", "verticals": "", "sec": "", "evidence": "",
           "category": "", "checked": rec.get("final_url", "")}

    if rec["status"] != "ok":
        out["site"] = "Not reachable"
        out["focus"] = "Unknown"
        out["sec"] = "Unknown - site not reachable"
        out["category"] = "Unknown"
        return out

    blocks = load_blocks(domain)
    full = "\n".join("\n".join(b[1]) for b in blocks)
    raw = rec.get("raw_chars", len(full))
    if raw < 600:
        out["site"] = site_reason(rec, full)
        out["focus"] = "Unknown"
        out["sec"] = "Unknown - site not readable"
        out["category"] = broker_category(full, rec["company"])
        return out
    out["site"] = "OK"
    out["category"] = broker_category(full, rec["company"])

    # ---- verticals
    counts = {}
    for label, rx in VERTICAL_RE.items():
        n = len(rx.findall(full))
        if n:
            counts[label] = n
    named = {k: v for k, v in counts.items() if v >= 2}
    strong = {k: v for k, v in named.items() if k not in WEAK_ALONE or v >= WEAK_ALONE_MIN}

    gen_hits = len(GENERALIST_RE.findall(full))
    spec_hits = len(SPECIALIST_RE.findall(full))

    ordered = sorted(strong.items(), key=lambda kv: -kv[1])
    if gen_hits >= 1 and len(strong) <= 8 and spec_hits == 0:
        out["focus"] = "Generic"
    elif len(strong) >= 8:
        out["focus"] = "Generic"
    elif not strong:
        out["focus"] = "Generic - unstated"
    elif len(strong) <= 3:
        out["focus"] = "Specialist"
    else:
        out["focus"] = "Multi-sector"

    if out["focus"].startswith("Generic"):
        # still record any sector it leans on, but only a clear leader
        if ordered and ordered[0][1] >= 6 and len(strong) <= 4:
            out["verticals"] = ordered[0][0]
    else:
        out["verticals"] = "; ".join(k for k, _ in ordered[:6])

    # ---- security-deal evidence
    best, best_rank = "", 0
    for url, lines in blocks:
        deal_page = any(h in url.lower() for h in DEAL_PAGE_HINTS)
        for i, ln in enumerate(lines):
            if not is_physical_security(ln):
                continue
            ctx = " ".join(lines[max(0, i - 1):i + 2])
            if TRANSACTION_RE.search(ln):
                rank = 4
            elif TRANSACTION_RE.search(ctx):
                rank = 3
            elif deal_page:
                rank = 2
            else:
                rank = 1
            if rank > best_rank:
                best_rank, best = rank, re.sub(r"\s+", " ", ln).strip()[:220] + "  [" + url + "]"
    sec_total = sum(1 for ln in full.split("\n") if is_physical_security(ln))
    if best_rank >= 3:
        out["sec"] = "Yes - deal evidence"
    elif best_rank == 2:
        out["sec"] = "Likely - on deal page"
    elif sec_total >= 3:
        out["sec"] = "Sector listed, no deal shown"
    else:
        out["sec"] = "No"
    out["evidence"] = best if best_rank >= 2 else ""
    return out


def main():
    recs = [json.loads(l) for l in open(os.path.join(OUT, "index.jsonl"), encoding="utf-8")]
    res = [classify(r) for r in recs]
    with open(os.path.join(OUT, "classified.jsonl"), "w", encoding="utf-8") as fh:
        for r in res:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    print("classified %d" % len(res))


if __name__ == "__main__":
    main()
