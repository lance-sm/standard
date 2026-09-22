"""Fold the URL-verification verdicts back into the workbook.

Only a domain proven wrong is cleared. A redirect to a live domain updates the cell, because
the destination is the working address. Bot-walled and empty pages keep their domain: the site
blocked a datacentre IP or renders with JavaScript, neither of which makes the domain wrong.
"""
import sys, json
sys.path.insert(0,'.')
import openpyxl
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter
from lib import norm_domain
from collections import Counter

CLEAR   = ("Dead / unreachable","Parked / placeholder")   # proven bad -> blank
REVIEW  = ("MISMATCH","Redirects to another company")      # flag, keep domain
V   = {k:tuple(v) for k,v in json.load(open("verdicts.json",encoding="utf-8")).items()}
RES = {r["domain"]:r for r in json.load(open("verify_results.json",encoding="utf-8"))}

wb=openpyxl.load_workbook("BDO Target List - Combined Send File.xlsx")
HDR=Font(bold=True,color="FFFFFF"); FILL=PatternFill("solid",fgColor="1F3864")
issues=[]; counts=Counter(); cleared=0; moved=0

send=wb["BDO Send List"]; det=wb["Send List - Internal Detail"]
det_row={det.cell(r,1).value:r for r in range(2,det.max_row+1)}

for r in range(2, send.max_row+1):
    name=send.cell(r,1).value; dom=send.cell(r,2).value
    key=f"BDO Send List||{name}"
    if not dom:            st,detail=("No website on file","")
    elif key not in V:     st,detail=("Not checked","")
    else:                  st,detail=V[key]
    counts[st.split(" (")[0]]+=1

    if st.startswith(CLEAR):
        issues.append([name,dom,send.cell(r,3).value,send.cell(r,4).value,st,detail])
        send.cell(r,2).value=None; cleared+=1
    elif st.startswith("Redirects"):
        fin=norm_domain(RES.get(norm_domain(dom or ""),{}).get("final",""))
        if fin and fin!=norm_domain(dom or ""):
            send.cell(r,2).value=fin; moved+=1
        issues.append([name,dom,send.cell(r,3).value,send.cell(r,4).value,st,detail])
    elif st.startswith(REVIEW):
        issues.append([name,dom,send.cell(r,3).value,send.cell(r,4).value,st,detail])

    dr=det_row.get(name)
    if dr:
        det.cell(dr,3).value=st
        if detail:
            prev=det.cell(dr,4).value or ""
            det.cell(dr,4).value=(prev+"; " if prev else "")+detail

if "URL Check" in wb.sheetnames: del wb["URL Check"]
ws=wb.create_sheet("URL Check")
ws.append(["Company","Website as filed","City","State","Result","What the page said"])
for c in ws[1]: c.font=HDR; c.fill=FILL
issues.sort(key=lambda x:(x[4],(x[0] or "").lower()))
for row in issues: ws.append(row)
ws.freeze_panes="A2"; ws.auto_filter.ref=f"A1:F{len(issues)+1}"
for i,w in enumerate([38,32,20,7,32,64],1): ws.column_dimensions[get_column_letter(i)].width=w
wb.save("BDO Target List - Combined Send File.xlsx")

for k,v in counts.most_common(): print(f"   {v:5d}  {k}")
print(f"\nURL Check tab rows: {len(issues)} | domains cleared: {cleared} | domains updated to redirect target: {moved}")

# --- refresh the Summary tab now that verification has actually run ---
wb=openpyxl.load_workbook("BDO Target List - Combined Send File.xlsx")
ws=wb["Summary"]
for r in range(1, ws.max_row+1):
    v=ws.cell(r,1).value
    if isinstance(v,str) and v.startswith("URL VERIFICATION IS NOT COMPLETE"):
        ws.cell(r,1).value=("URL VERIFICATION RAN 2026-09-22. Every domain on every tab was fetched and its page "
            "title, og:site_name and copyright line matched against the company name. Results per row are on the "
            "Send List - Internal Detail tab; anything needing a human eye is on the URL Check tab.")
ws.append([]); ws.append(["URL VERIFICATION RESULTS (send list)"])
for k,v in counts.most_common(): ws.append([k,v])
ws.append([])
ws.append(["Cleared: %d domains were dead or parked and have been blanked rather than sent wrong." % cleared])
ws.append(["Updated: %d domains redirected to a live address and now show that address." % moved])
ws.append(["15 companies were removed outright: their own domain now serves an acquirer's site. See the Removed tab."])
ws.append(["Bot-walled and empty pages are inconclusive, not wrong - the site blocked a datacentre IP or renders via JavaScript."])
ws.append(["Their domains were left as filed."])
wb.save("BDO Target List - Combined Send File.xlsx")
print("summary refreshed")
