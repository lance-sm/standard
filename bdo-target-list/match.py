import sys, re, json
sys.path.insert(0,'.')
from lib import norm_domain, norm_name_strict

GENERIC = {"inc","llc","corp","co","company","the","and","of","ltd","group","services","service",
           "systems","system","solutions","solution","home","welcome","official","site","website",
           "security","fire","alarm","lock","locksmith","protection","safety","technologies",
           "technology","tech","contact","us"}

def toks(s):
    s=(s or "").lower()
    s=re.sub(r"[^a-z0-9]+"," ",s)
    return [t for t in s.split() if len(t)>1]

def distinctive(name):
    """Tokens from the company name that actually identify it."""
    t=toks(name)
    d=[x for x in t if x not in GENERIC]
    return d or t

def dom_core(dom):
    d=norm_domain(dom)
    d=re.sub(r"\.(com|net|org|us|biz|info|co|io|ai|nyc|tech|services|solutions|company|systems|security)(\.[a-z]{2})?$","",d)
    return re.sub(r"[^a-z0-9]","",d)

def verdict(company, dom, r):
    """Return (status, detail)."""
    if not r: return "Not checked",""
    flag=r.get("flag") or ""
    blob=" ".join([r.get("title",""), r.get("site",""), r.get("desc",""), r.get("copyright","")])
    btok=set(toks(blob)); bjoin=re.sub(r"[^a-z0-9]","",blob.lower())
    dcore=dom_core(dom)
    dist=distinctive(company)
    hit=[w for w in dist if w in btok or (len(w)>4 and w in bjoin)]
    # Acronyms: "Communications Electronics Systems" trades as "CES Integrated",
    # "SecureWatch24" as "SW24". Count an initialism of the name as a match.
    if not hit:
        ini="".join(w[0] for w in toks(company) if w)
        for n in (len(ini), 4, 3, 2):
            cand=ini[:n]
            if len(cand)>=2 and (cand in btok or cand in dcore):
                hit=[cand]; break
    # Name squashed into one token: "Security 2000" -> "Security2000", "SW24"
    if not hit:
        sq=re.sub(r"[^a-z0-9]","",company.lower())
        if len(sq)>4 and sq in bjoin: hit=[sq]
    # domain itself echoes the company name -> supporting evidence
    dom_echo = any(w in dcore for w in dist if len(w)>3) or norm_name_strict(company)[:12] in dcore

    if flag=="dead":   return "Dead / unreachable", r.get("err","")
    if flag=="parked": return "Parked / placeholder", (r.get("title") or "")[:60]
    if flag=="empty":  return "Empty page", (r.get("title") or "")[:60]
    if flag=="botwall":
        return ("Bot-walled (domain matches name)" if dom_echo else "Bot-walled (inconclusive)"), (r.get("title") or "")[:60]

    # redirect to a different registrable domain?
    fin=norm_domain(r.get("final",""))
    moved = fin and dom_core(fin)!=dcore
    # A redirect off the filed domain always gets flagged. When the destination still
    # carries the company name it usually means the company was acquired and its domain
    # now serves the buyer's site - which is exactly what this list must not miss.
    if moved:
        lbl = "Redirects - likely acquired" if hit else "Redirects to another company"
        return lbl, f"-> {fin} | {(r.get('title') or '')[:60]}"
    if hit:
        return "Verified", (r.get("site") or r.get("title") or "")[:70]
    if dom_echo:
        return "Likely OK (domain matches name)", (r.get("title") or "")[:70]
    return "MISMATCH - review", (r.get("title") or r.get("desc") or "")[:70]

if __name__=="__main__":
    import openpyxl
    res={r["domain"]:r for r in json.load(open("verify_results.json",encoding="utf-8"))}
    wb=openpyxl.load_workbook("BDO Target List - Combined Send File.xlsx")
    out={}
    for tab,ci,di in [("BDO Send List",0,1),("Hold Back - Live Deals",0,1),
                      ("Adjacent - Review",0,1),("NYC Unclassified - Review",0,1)]:
        for row in wb[tab].iter_rows(min_row=2,values_only=True):
            d=norm_domain(row[di] or "")
            if not d: continue
            out[(tab,row[ci])]=verdict(row[ci], d, res.get(d))
    json.dump({f"{k[0]}||{k[1]}":v for k,v in out.items()}, open("verdicts.json","w"), indent=0)
    from collections import Counter
    print(Counter(v[0].split(" (")[0] for v in out.values()).most_common())
