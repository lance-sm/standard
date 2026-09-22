import sys, csv, re
sys.path.insert(0,'.')
from lib import *
FOOT={'ME','NH','VT','MA','RI','CT','NY','NJ','PA','DE','MD','DC','VA'}
from screen import S
from resolved import R
from zi_nyc import Z

# ---------- load ----------
hs      = read(D+"hubspot_companies.csv")
send    = read(D+"univ__bdo_send_list.csv")
adj     = read(D+"univ__review_adjacent.csv")
nq      = read(D+"nyc__qualified.csv")
nu      = read(D+"nyc__unclassified.csv")
unscr   = read(D+"unscreened_infootprint.csv")
deals   = list(csv.DictReader(open(D+"hubspot_deal_companies.tsv",encoding="utf-8"), delimiter="\t"))

hs_by_id   = {r["hs_object_id"]: r for r in hs}
hs_by_dom  = {}
hs_by_name = {}      # loose - used only for the In-HubSpot flag
hs_by_strict = {}    # strict - used when carrying a domain/headcount onto a row
for r in hs:
    d=norm_domain(r["domain"]); n=norm_name(r["name"]); sN=norm_name_strict(r["name"])
    if d: hs_by_dom.setdefault(d,r)
    if n: hs_by_name.setdefault(n,r)
    if sN: hs_by_strict.setdefault(sN,r)
hs_groups={}
for r in hs:
    sN=norm_name_strict(r["name"])
    if sN: hs_groups.setdefault(sN,[]).append(r)

def lookup_hs(name, city, state):
    """Find the HubSpot record for a source row.

    HubSpot holds several distinct companies that share a name - three different
    "American Alarm" records, for example. Taking the first match hands one company
    another's domain and headcount, so when a name is ambiguous this disambiguates
    on state, then city, and gives up rather than guess.
    """
    g=hs_groups.get(norm_name_strict(name))
    if not g: return None, ""
    if len(g)==1: return g[0], ""
    doms={norm_domain(x["domain"]) for x in g if norm_domain(x["domain"])}
    if len(doms)<=1: return g[0], ""            # same company, duplicated in HubSpot
    st=norm_state(state)
    byst=[x for x in g if norm_state(x["state"])==st]
    if len(byst)==1: return byst[0], ""
    pool=byst or g
    bycity=[x for x in pool if city and city.lower() in (x["city"] or "").lower()]
    if len(bycity)==1: return bycity[0], ""
    return None, "Several different HubSpot companies share this name - domain left blank rather than guessed"

# ---------- blocklist ----------
block={}
def addblock(key,reason,src):
    if key and key not in block: block[key]=(reason,src)
for f,reason in [("univ__peowned_and_subsidiaries.csv","PE-owned / subsidiary"),
                 ("univ__above_buybox.csv","Above buy-box"),
                 ("univ__excluded.csv","Excluded (universe screen)")]:
    for r in read(D+f):
        addblock(("n",norm_name(r.get("Company",""))),reason,r.get("Company",""))
        addblock(("d",norm_domain(r.get("Website",""))),reason,r.get("Company",""))
for r in read(D+"nyc__excluded.csv"):
    addblock(("n",norm_name(r.get("Company Name",""))),"Excluded (NYC screen): "+(r.get("Exclusion Reason","") or ""),r.get("Company Name",""))

# ---------- verified corrections (web-checked 2026-09-21) ----------
# Each of these was checked individually because it sat in the top two size tiers,
# where a wrong row is most visible to BDO.
_CORR_RAW = {
 "Winfield Security Corporation":"Guard / security-officer services; joined Tarian (PE platform already on the PE-Owned tab)",
 "Building Security Services":"Guard / security-officer services (unarmed guards, concierge, mobile patrol)",
 "AccessIT Group":"Cybersecurity VAR, not physical security",
 "DTiQ":"PE-owned: Digital Alpha holds the majority; Bain Capital Credit invested 2024",
}
# Keys are derived with the same normalizer used for matching - never hardcoded.
CORRECTIONS = {norm_name(k):("REMOVE",v) for k,v in _CORR_RAW.items()}
FIX_DOMAIN = {norm_name("Mac Security Systems"):""}        # macsecurity.com.ec is an Ecuador TLD, not this company
FIX_TIER   = {norm_name("Security 101 - Rochester"):"Unknown"}  # 620 emp is the national franchise network

# ---------- deals: hold-back / broker ----------
ACTIVE={"Initial Meeting","Management Meeting","IOI","Due Diligence","On Hold"}
holdback={}; brokers={}; owned={}
for d in deals:
    cid=d["company_id"]; st=d["stage"]
    h=hs_by_id.get(cid)
    if not h: continue
    key_d=norm_domain(h["domain"]); key_n=norm_name(h["name"])
    rec=(h["name"],h["domain"],h["city"],norm_state(h["state"]),st)
    if st=="BROKER":   brokers[cid]=rec
    elif st=="Closed": owned[cid]=rec
    elif st in ACTIVE: holdback[cid]=rec
for cid,rec in list(brokers.items())+list(owned.items()):
    addblock(("n",norm_name(rec[0])),"Broker/advisor tied to a deal" if cid in brokers else "Badlands-owned (Closed)",rec[0])
    addblock(("d",norm_domain(rec[1])),"Broker/advisor tied to a deal" if cid in brokers else "Badlands-owned (Closed)",rec[0])
hb_keys=set()
for cid,rec in holdback.items():
    if norm_domain(rec[1]): hb_keys.add(("d",norm_domain(rec[1])))
    hb_keys.add(("n",norm_name(rec[0])))

def tier(emp):
    if emp is None or emp=="" : return "Unknown"
    try: e=int(float(emp))
    except: return "Unknown"
    if e>=250: return "1: 250+"
    if e>=100: return "2: 100-249"
    if e>=50:  return "3: 50-99"
    if e>=20:  return "4: 20-49"
    return "5: <20"

def in_hubspot(dom,name):
    return "Yes" if (norm_domain(dom) in hs_by_dom or norm_name(name) in hs_by_name) else "No"

# ---------- assemble ----------
rows=[]; removed=[]; held=[]; adjacent_hs=[]
seen={}
def add(company,website,city,state,vertical,emp,source,urlcheck,note=""):
    d=norm_domain(website); n=norm_name(company)
    # A domain match always means the same company. A loose-name match only means the
    # same company when the state agrees too - "American Alarm" is three different
    # companies in MA, CT and NY, and the loose normalizer cannot tell them apart.
    kd=("d",d) if d else None; kn=("n",n,norm_state(state))
    # verified corrections take precedence
    if n in CORRECTIONS:
        removed.append([company,website,city,state,vertical,CORRECTIONS[n][1],source]); return
    if n in FIX_DOMAIN:
        website=FIX_DOMAIN[n]; d=""; kd=None; note=(note+"; " if note else "")+"ZoomInfo domain was wrong - cleared"
    # blocklist
    for k in (kd,("n",n)):
        if k and k in block:
            removed.append([company,website,city,state,vertical,block[k][0],source]); return
    # hold-back
    for k in (kd,("n",n)):
        if k and k in hb_keys:
            stg=next((r[4] for r in holdback.values() if norm_name(r[0])==n or (d and norm_domain(r[1])==d)),"Active")
            held.append([company,website,city,state,vertical,stg,source]); return
    # dedupe (check domain key AND name key)
    prev=None
    for k in (kd,kn):
        if k and k in seen: prev=seen[k]; break
    if prev is not None:
        if not prev["Website"] and website: prev["Website"]=website
        # Only a domain match is strong enough to carry a headcount across. A loose name
        # match (which strips systems/services/group) can join two different companies.
        if kd and kd in seen and prev["Size Tier"]=="Unknown" and tier(emp)!="Unknown":
            prev["Size Tier"]=tier(emp); prev["_emp"]=emp
        if kd and kd not in seen: seen[kd]=prev
        if kn not in seen: seen[kn]=prev
        return
    key = kd or kn
    rec={"Company":company,"Website":website,"City":city,"State":state,"Vertical":vertical,
         "Size Tier":tier(emp),"In HubSpot":in_hubspot(website,company),
         "URL Check":urlcheck,"Source":source,"Notes":note,"_emp":emp if emp not in ("",None) else 0}
    if n in FIX_TIER:
        rec["Size Tier"]=FIX_TIER[n]; rec["_emp"]=0
        rec["Notes"]=(rec["Notes"]+"; " if rec["Notes"] else "")+"Headcount in HubSpot is the national franchise network, not this location"
    seen[key]=rec; rows.append(rec)
    if kd and kn not in seen: seen[kn]=rec

# A) universe send list
for r in send:
    add(r["Company"], r["Website"], r["HQ City"], r["State"], r["Vertical"],
        r["Employees"], "Universe build", "ZoomInfo-sourced", r.get("Ownership","") if r.get("Ownership")=="Unverified" else "")
# B) HubSpot screened targets
for i,r in enumerate(unscr):
    dec,val = S[i]
    emp=r["emp"]; uc="Not verified"; note=""
    if dec=="U":
        dec2,val2,zemp,flag = R[i]
        dec,val = dec2,val2
        if zemp: emp=zemp; uc="ZI verified"
        if flag: note=flag
    if dec=="A":
        adjacent_hs.append([r["name"], r["domain"], r["city"], r["state"], val, emp or "", "HubSpot screen"]); continue
    if dec!="T":
        lbl={"N":"Not a buy-box business","D":"Duplicate record"}[dec]
        removed.append([r["name"], r["domain"], r["city"], r["state"], "", lbl+": "+val, "HubSpot screen"]); continue
    add(r["name"], r["domain"], r["city"], r["state"], val, emp, "HubSpot screen", uc, note)
# B2) Records the name-collision above had hidden from the screen.
# A HubSpot record was treated as "already on a prior list" whenever ANY company shared
# its name, so genuinely different companies were dropped. Recovered and classified here.
for _nm,_dom,_city,_st,_vert,_emp,_note in [
    ("American Alarm","americanalarmltd.com","Norwalk","CT","Alarm & Monitoring","",
     "Distinct from American Alarm & Communications (MA) and American Alarm (Newburgh, NY)"),
    ("Approved Fire Protection","approvedfps.com","Somerset","NJ","Fire & Life Safety","",
     "Second NJ record under this name (other is afpnj.com) - confirm it is not a duplicate"),
]:
    add(_nm,_dom,_city,_st,_vert,_emp,"HubSpot screen","Not verified",_note)

# C) NYC qualified
for r in nq:
    h,amb = lookup_hs(r["Company Name"], r["City"], r["State"])
    dom=h["domain"] if h else ""
    emp=h["numberofemployees"] if h else ""
    add(r["Company Name"], dom, r["City"], r["State"], r["Vertical"], emp, "NYC metro list", "Not verified", amb)

TIERORD={"1: 250+":0,"2: 100-249":1,"3: 50-99":2,"4: 20-49":3,"5: <20":4,"Unknown":5}
def empnum(r):
    try: return int(float(r["_emp"] or 0))
    except: return 0
rows.sort(key=lambda r:(TIERORD[r["Size Tier"]], -empnum(r), r["Company"].lower()))
print("SEND:",len(rows)," REMOVED:",len(removed)," HELD:",len(held))
from collections import Counter
print("tiers:",Counter(r["Size Tier"] for r in rows))
print("inhs:",Counter(r["In HubSpot"] for r in rows))
print("src:",Counter(r["Source"] for r in rows))

# ---------- adjacent + NYC unclassified ----------
adjacent=[]
for r in adj:
    adjacent.append([r["Company"],r["Website"],r["HQ City"],r["State"],r["Vertical"],
                     r["Employees"],"Universe build",r.get("Why It's Borderline","")])
for a in adjacent_hs:
    adjacent.append(a[:6]+["HubSpot screen",""])

unclass=[]
for r in nu:
    h,_amb = lookup_hs(r["Company Name"], r["City"], r["State"])
    dom=norm_domain(h["domain"]) if h else ""
    z=Z.get(dom)
    if z:
        zi_name,zi_ind,zemp,zrev,zcity,zstate,par,defunct = z
        flag = "Defunct (ZI)" if defunct else ("Owned by "+par if par else "")
    else:
        zi_name=zi_ind=""; zemp=zrev=None; par=None; flag="No ZoomInfo match" if dom else "No domain in HubSpot"
        zi_ind = "NO_MATCH" if dom else ""
    unclass.append([r["Company Name"], h["domain"] if h else "", r["City"], r["State"],
                    zi_ind or "", zemp or "", (zrev or ""), tier(zemp), flag])

_seen_rm=set(); removed_u=[]
for _r in removed:
    _k=(norm_name(_r[0]), _r[5])
    if _k in _seen_rm: continue
    _seen_rm.add(_k); removed_u.append(_r)
removed_u.sort(key=lambda x:(x[5], x[0].lower()))

# The hold-back tab is built from the deal pipeline itself, so every active deal appears
# whether or not that company happened to sit on one of the source lists.
_held_by_name={norm_name(h[0]):h for h in held}
held_all=[]
for cid,rec in holdback.items():
    nm,dom,city,st,stage = rec
    h=_held_by_name.get(norm_name(nm))
    vert = h[4] if h else ""
    src_ = h[6] if h else "HubSpot deal pipeline"
    held_all.append([nm,dom,city,st,vert,stage,src_])
_ORD={"Due Diligence":0,"IOI":1,"Management Meeting":2,"Initial Meeting":3,"On Hold":4}
held_all.sort(key=lambda x:(_ORD.get(x[5],9), x[0].lower()))

# ---------- guard: no in-footprint HubSpot record may vanish silently ----------
_on_a_tab=set()
for _r in rows: _on_a_tab.add(norm_name(_r["Company"])); _on_a_tab.add(norm_domain(_r["Website"] or ""))
for _grp in (removed_u, held_all, adjacent, unclass):
    for _r in _grp: _on_a_tab.add(norm_name(_r[0])); _on_a_tab.add(norm_domain(_r[1] or ""))
_on_a_tab.discard("")
_lost=[h for h in hs if norm_state(h["state"]) in FOOT
       and norm_name(h["name"]) not in _on_a_tab
       and (not norm_domain(h["domain"]) or norm_domain(h["domain"]) not in _on_a_tab)]
print("GUARD in-footprint HubSpot records on no tab:",len(_lost))
for _h in _lost[:10]: print("   LOST:",_h["name"],"|",_h["domain"],"|",_h["city"],_h["state"])

# ---------- write workbook ----------
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

wb=openpyxl.Workbook(); wb.remove(wb.active)
HDR=Font(bold=True,color="FFFFFF"); FILL=PatternFill("solid",fgColor="1F3864")

def sheet(title, headers, data, widths=None):
    ws=wb.create_sheet(title)
    ws.append(headers)
    for c in ws[1]: c.font=HDR; c.fill=FILL; c.alignment=Alignment(vertical="center")
    for row in data: ws.append(row)
    ws.freeze_panes="A2"
    ws.auto_filter.ref=f"A1:{get_column_letter(len(headers))}{len(data)+1}"
    for i,h in enumerate(headers,1):
        w=(widths or {}).get(h, max(12,min(42,len(h)+4)))
        ws.column_dimensions[get_column_letter(i)].width=w
    return ws

W={"Company":38,"Website":32,"City":20,"State":7,"Vertical":32,"Size Tier":13,"In HubSpot":12,
   "Deal Stage":20,"Reason Removed":46,"Why Borderline":50,"Source":16,"URL Check":16,"Notes":26,
   "ZI Industry":32,"ZI Employees":13,"ZI Revenue":14,"Flag":26,"Employees":11}

# Summary
ws=wb.create_sheet("Summary")
from collections import Counter
tc=Counter(r["Size Tier"] for r in rows); vc=Counter(r["Vertical"] for r in rows)
sc=Counter(r["State"] for r in rows); hc=Counter(r["In HubSpot"] for r in rows)
L=[["BDO Intro Target List - Combined Send File"],
   ["Built 2026-09-21 for Lance Smith, Badlands Security. Footprint: ME through VA."],
   [],
   ["TAB","WHAT IT IS","ROWS","FOR BDO?"],
   ["BDO Send List","Deduped acquisition targets, company-level columns only",len(rows),"YES - send this tab"],
   ["Send List - Internal Detail","Per-row provenance for the send list",len(rows),"No - internal"],
   ["Hold Back - Live Deals","Companies with an active deal in the M&A pipeline",len(holdback),"No - Lance decides"],
   ["Adjacent - Review","Distributors, wholesale monitoring, electrical/controls w/ security",len(adjacent),"No - Lance decides"],
   ["NYC Unclassified - Review","NYC 'Ancillary' names the 9/11 cleanup left unclassified",len(unclass),"No - Lance decides"],
   ["Removed","Everything screened out, with the reason",len(removed_u),"No - audit trail"],
   [],
   ["SEND LIST BY SIZE TIER"]]
for t in ["1: 250+","2: 100-249","3: 50-99","4: 20-49","5: <20","Unknown"]:
    L.append([t,tc.get(t,0)])
L += [[],["SEND LIST BY STATE"]]
for s,n in sorted(sc.items(), key=lambda x:-x[1]): L.append([s or "(blank)",n])
L += [[],["SEND LIST BY VERTICAL"]]
for v,n in sorted(vc.items(), key=lambda x:-x[1]): L.append([v or "(blank)",n])
L += [[],["IN HUBSPOT"],["Yes",hc.get("Yes",0)],["No (new names)",hc.get("No",0)],
      [],["METHOD AND CAVEATS"],
      ["Sources: NYC Metro Target List (Qualified tab), NE Security Target Universe (Send List), and a fresh HubSpot company export (1,649 records, pulled 2026-09-21)."],
      ["Screening: 636 in-footprint HubSpot records not on either prior list were screened one by one. 106 ambiguous ones were resolved with ZoomInfo enrichment (industry, headcount, parent, defunct flag)."],
      ["Blocklist applied: universe PE-Owned, Above Buy-Box and Excluded tabs, plus the NYC Excluded tab, matched on normalized name and domain."],
      ["Also removed: broker/advisor companies attached to deals (Flatirons, Hedgestone, DGP, Corum, The Advisory IB, SEMM) and Cosmic Fischer (Badlands-owned)."],
      ["Dedupe: by domain and by normalized name (strips inc/llc/corp/co/company/the/and/systems/services/group and punctuation)."],
      ["SIZE TIER IS INCOMPLETE: "+str(tc.get('Unknown',0))+" of "+str(len(rows))+" rows have no headcount. The NYC metro list carried no size data and most HubSpot records have no employee count. Tiers shown come from the universe build or from ZoomInfo."],
      ["URL VERIFICATION IS NOT COMPLETE. This session's network policy blocks outbound access to company websites, so homepages could not be fetched and matched. Domains carried from the universe build are ZoomInfo-sourced; domains taken from HubSpot are unverified. See the URL Check column on the internal detail tab."],
      ["Nothing was written to HubSpot."]]
for r_ in L: ws.append(r_)
ws["A1"].font=Font(bold=True,size=14)
for i,w in [(1,46),(2,62),(3,10),(4,20)]: ws.column_dimensions[get_column_letter(i)].width=w
for rr in (4,): 
    for c in ws[rr]: c.font=Font(bold=True)
wb.move_sheet("Summary", offset=-len(wb.sheetnames))

sheet("BDO Send List", ["Company","Website","City","State","Vertical","Size Tier","In HubSpot"],
      [[r["Company"],r["Website"],r["City"],r["State"],r["Vertical"],r["Size Tier"],r["In HubSpot"]] for r in rows], W)
sheet("Send List - Internal Detail", ["Company","Source","URL Check","Notes"],
      [[r["Company"],r["Source"],r["URL Check"],r["Notes"]] for r in rows], W)
sheet("Hold Back - Live Deals", ["Company","Website","City","State","Vertical","Deal Stage","Source"], held_all, W)
sheet("Adjacent - Review", ["Company","Website","City","State","Vertical","Employees","Source","Why Borderline"], adjacent, W)
sheet("NYC Unclassified - Review", ["Company","Website","City","State","ZI Industry","ZI Employees","ZI Revenue","Size Tier","Flag"], unclass, W)
sheet("Removed", ["Company","Website","City","State","Vertical","Reason Removed","Source"], removed_u, W)

out="BDO Target List - Combined Send File.xlsx"
wb.save(out)
print("saved",out)
print("tabs:",wb.sheetnames)
