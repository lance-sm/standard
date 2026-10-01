# -*- coding: utf-8 -*-
"""Build the segmented broker workbook: Summary, Companies, Security Deal Hits."""
import json, os, sys, collections, datetime

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

SRC_TSV = sys.argv[1]          # his Companies tab, tab-separated, with header
CLASSIFIED = sys.argv[2]       # classified.jsonl
DEST = sys.argv[3]             # output .xlsx

INK = "1F2933"
HDR_FILL = PatternFill("solid", fgColor="1F2933")
HDR_FONT = Font(bold=True, color="FFFFFF", size=10)
TITLE_FONT = Font(bold=True, size=14, color=INK)
SUB_FONT = Font(size=9, color="6B7280", italic=True)
SEC_FONT = Font(bold=True, size=11, color=INK)
BODY = Font(size=10)
THIN = Side(style="thin", color="D8DEE4")
GRID = Border(bottom=THIN)

FOCUS_ORDER = ["Generic", "Generic - unstated", "Multi-sector", "Specialist", "Unknown"]
SEC_ORDER = ["Yes - deal evidence", "Likely - on deal page", "Sector listed, no deal shown",
             "No", "Unknown - site not reachable", "Unknown - site not readable"]
SITE_ORDER = ["OK", "Thin / JS-only site", "Blocked by bot protection", "Site down / parked",
              "Not reachable"]


def load():
    rows = []
    with open(SRC_TSV, encoding="utf-8") as fh:
        header = fh.readline().rstrip("\n").split("\t")
        col = {n.strip(): i for i, n in enumerate(header)}
        for line in fh:
            p = line.rstrip("\n").split("\t")
            if len(p) < len(header):
                p += [""] * (len(header) - len(p))
            rows.append(p)
    cls = {}
    with open(CLASSIFIED, encoding="utf-8") as fh:
        for line in fh:
            r = json.loads(line)
            cls[r["domain"]] = r
    return col, rows, cls


def n_contacts(v):
    try:
        return int(float(str(v).replace(",", "") or 0))
    except ValueError:
        return 0


def main():
    col, rows, cls = load()
    wb = Workbook()

    # ------------------------------------------------------------ Companies --
    ws = wb.create_sheet("Companies")
    headers = ["Company", "Domain", "Segment", "Focus", "Verticals", "Security Deals",
               "Security Evidence", "Firm Type (verified)", "# Contacts", "Contacts",
               "Site", "Page Checked"]
    ws.append(headers)
    out_rows = []
    for p in rows:
        dom = p[col["Domain"]]
        c = cls.get(dom, {})
        out_rows.append([
            p[col["Company"]], dom, p[col["Segment"]],
            c.get("focus", "Unknown"), c.get("verticals", ""),
            c.get("sec", "Unknown - site not reachable"), c.get("evidence", ""),
            c.get("category", "Unknown"),
            n_contacts(p[col["# Contacts"]]), p[col["Contacts"]],
            c.get("site", "Not reachable"), c.get("checked", ""),
        ])
    # security hits first, then specialists, then the rest - most useful at the top
    rank = {v: i for i, v in enumerate(SEC_ORDER)}
    out_rows.sort(key=lambda r: (rank.get(r[5], 9), FOCUS_ORDER.index(r[3]) if r[3] in FOCUS_ORDER else 9,
                                 -r[8], r[0].lower()))
    for r in out_rows:
        ws.append(r)

    for i, h in enumerate(headers, 1):
        c = ws.cell(row=1, column=i)
        c.fill, c.font, c.alignment = HDR_FILL, HDR_FONT, Alignment(vertical="center")
    widths = [38, 30, 11, 18, 46, 28, 62, 34, 11, 46, 24, 40]
    for i, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.freeze_panes = "C2"
    ws.auto_filter.ref = "A1:%s%d" % (get_column_letter(len(headers)), ws.max_row)
    ws.row_dimensions[1].height = 26
    for r in range(2, ws.max_row + 1):
        for cc in range(1, len(headers) + 1):
            ws.cell(row=r, column=cc).font = BODY
            ws.cell(row=r, column=cc).alignment = Alignment(vertical="top")

    # ------------------------------------------------- Security Deal Hits ----
    hits = [r for r in out_rows if r[5] in SEC_ORDER[:3]]
    wh = wb.create_sheet("Security Deal Hits")
    hh = ["Company", "Domain", "Security Deals", "Security Evidence", "Firm Type (verified)",
          "Focus", "Verticals", "# Contacts", "Page Checked"]
    wh.append(hh)
    for r in hits:
        wh.append([r[0], r[1], r[5], r[6], r[7], r[3], r[4], r[8], r[11]])
    for i, h in enumerate(hh, 1):
        c = wh.cell(row=1, column=i)
        c.fill, c.font = HDR_FILL, HDR_FONT
    for i, w in enumerate([38, 30, 28, 70, 34, 18, 40, 11, 40], 1):
        wh.column_dimensions[get_column_letter(i)].width = w
    wh.freeze_panes = "A2"
    if wh.max_row > 1:
        wh.auto_filter.ref = "A1:I%d" % wh.max_row
    for r in range(2, wh.max_row + 1):
        for cc in range(1, len(hh) + 1):
            wh.cell(row=r, column=cc).font = BODY
            wh.cell(row=r, column=cc).alignment = Alignment(vertical="top")

    # ---------------------------------------------------------- Summary -----
    wsum = wb["Sheet"]
    wsum.title = "Summary"
    A = wsum.append

    def blank():
        A([])

    def section(t):
        blank()
        A([t])
        wsum.cell(row=wsum.max_row, column=1).font = SEC_FONT

    def table(cols, data, pct_col=None, total_label=None):
        A(cols)
        hr = wsum.max_row
        for i in range(1, len(cols) + 1):
            c = wsum.cell(row=hr, column=i)
            c.fill, c.font = HDR_FILL, HDR_FONT
        for d in data:
            A(d)
            for i in range(1, len(cols) + 1):
                wsum.cell(row=wsum.max_row, column=i).font = BODY
                wsum.cell(row=wsum.max_row, column=i).border = GRID
        if total_label:
            A(total_label)
            for i in range(1, len(cols) + 1):
                wsum.cell(row=wsum.max_row, column=i).font = Font(bold=True, size=10)

    tot_co = len(out_rows)
    tot_ct = sum(r[8] for r in out_rows)
    brokers = [r for r in out_rows if r[2] == "Broker"]

    A(["Farm Broker List - verified segmentation"])
    wsum.cell(row=1, column=1).font = TITLE_FONT
    A(["Every website on the list was fetched and read on %s. Focus, Verticals, Security Deals "
       "and Firm Type are what each firm's own site says - not a guess from its name."
       % datetime.date.today().isoformat()])
    wsum.cell(row=wsum.max_row, column=1).font = SUB_FONT

    section("1  Coverage")
    site_c = collections.Counter(r[10] for r in out_rows)
    table(["Site read", "Companies", "% of list"],
          [[k, site_c[k], round(100.0 * site_c[k] / tot_co, 1)] for k in SITE_ORDER if site_c[k]],
          total_label=["Total companies", tot_co, 100.0])

    section("2  Generic vs specialist")
    fc = collections.Counter(r[3] for r in out_rows)
    fct = collections.Counter()
    for r in out_rows:
        fct[r[3]] += r[8]
    meaning = {
        "Generic": "Site says it works across all industries - farm for anything",
        "Generic - unstated": "Reads like a generalist but names no sectors",
        "Multi-sector": "Names 4-7 sectors - broad but not truly generic",
        "Specialist": "Names 1-3 sectors only - farm only if a sector fits",
        "Unknown": "Site could not be read - needs a human look",
    }
    table(["Focus", "What it means", "Companies", "Contacts", "% of companies"],
          [[k, meaning[k], fc[k], fct[k], round(100.0 * fc[k] / tot_co, 1)]
           for k in FOCUS_ORDER if fc[k]],
          total_label=["Total", "", tot_co, tot_ct, 100.0])

    section("3  Verticals the specialists actually work in")
    A(["Counts firms whose Focus is Specialist or Multi-sector. A firm naming several sectors "
       "is counted under each, so these do not sum to the total."])
    wsum.cell(row=wsum.max_row, column=1).font = SUB_FONT
    vc, vct = collections.Counter(), collections.Counter()
    for r in out_rows:
        if r[3] in ("Specialist", "Multi-sector") and r[4]:
            for v in [x.strip() for x in r[4].split(";") if x.strip()]:
                vc[v] += 1
                vct[v] += r[8]
    table(["Vertical", "Firms", "Contacts"],
          [[v, n, vct[v]] for v, n in vc.most_common()])

    section("4  Security, fire and life safety deal evidence")
    sc = collections.Counter(r[5] for r in out_rows)
    sct = collections.Counter()
    for r in out_rows:
        sct[r[5]] += r[8]
    smean = {
        "Yes - deal evidence": "A security/fire/life-safety deal named in a transaction sentence",
        "Likely - on deal page": "Security wording sits on their closed-deal page",
        "Sector listed, no deal shown": "Claims the sector but shows no deal",
        "No": "Site read clean, nothing in the sector",
        "Unknown - site not reachable": "Site did not load",
        "Unknown - site not readable": "Site loaded but gave no usable text",
    }
    table(["Security deals", "What it means", "Companies", "Contacts"],
          [[k, smean[k], sc[k], sct[k]] for k in SEC_ORDER if sc[k]],
          total_label=["Total", "", tot_co, tot_ct])
    blank()
    A(["The %d firms in the top three rows are listed on the Security Deal Hits tab."
       % sum(sc[k] for k in SEC_ORDER[:3])])
    wsum.cell(row=wsum.max_row, column=1).font = SUB_FONT

    section("5  Firm type, verified from the site")
    cc_ = collections.Counter(r[7] for r in out_rows)
    table(["Firm type", "Companies", "Contacts"],
          [[k, n, sum(r[8] for r in out_rows if r[7] == k)] for k, n in cc_.most_common()])

    for i, w in enumerate([34, 62, 13, 12, 15], 1):
        wsum.column_dimensions[get_column_letter(i)].width = w
    wsum.sheet_view.showGridLines = False

    wb.save(DEST)
    print("wrote %s: %d companies, %d security hits" % (DEST, tot_co, len(hits)))


if __name__ == "__main__":
    main()
