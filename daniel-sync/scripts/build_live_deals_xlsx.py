#!/usr/bin/env python3
"""Build the weekly Badlands live-deals .xlsx.

Loads the template workbook itself, captures row 2's per-column styling,
clears the old data rows and rewrites them, then reapplies the captured
styles cell by cell. Never builds a fresh workbook when the template exists.

Usage:
    python3 build_live_deals_xlsx.py <deals.json> <output.xlsx> <YYYY-MM-DD> [template.xlsx]

deals.json is a list of objects:
    {"dealname":..., "stage":..., "location":..., "revenue":..., "ebitda":...,
     "description":..., "deal_source":...}
revenue/ebitda may be null. Valuation Proposed and Multiple are always left
blank - HubSpot has no such fields.

Requires openpyxl (pip install openpyxl).
"""
import json
import math
import os
import sys
import copy

try:
    import openpyxl
except ImportError:
    raise SystemExit("FATAL: openpyxl not installed. Run: pip install openpyxl")

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TPL = os.path.join(HERE, os.pardir, "templates", "live-deals-template.xlsx")

HEADERS = [
    "Deal Name", "Deal Stage", "Location", "Revenue", "EBITDA",
    "Valuation Proposed", "Multiple", "Deal Description", "Deal Source",
]

STAGE_ORDER = [
    "Initial Meeting", "NDA Sent", "NDA Signed", "Management Meeting",
    "IOI", "LOI", "Due Diligence",
]

# Verified against "Live Deals Aug 19.xlsx" - used only for the no-template fallback.
COL_WIDTHS = {
    "A": 28.33203125, "B": 19.44140625, "C": 16.88671875, "D": 14.88671875,
    "E": 13.88671875, "F": 18.21875, "G": 7.88671875, "H": 75.0, "I": 11.109375,
}
ACCOUNTING_FMT = '_("$"* #,##0.00_);_("$"* \\(#,##0.00\\);_("$"* "-"??_);_(@_)'


def row_height(description):
    """Template rule: ceil(len/88) lines at 14.4pt, floor of 28.8."""
    n = len(description) if description else 0
    return max(28.8, math.ceil(n / 88) * 14.4)


def sort_deals(deals):
    def key(d):
        stage = d.get("stage") or ""
        return (STAGE_ORDER.index(stage) if stage in STAGE_ORDER else len(STAGE_ORDER),
                (d.get("dealname") or "").lower())
    return sorted(deals, key=key)


def build(deals, out_path, tab_date, tpl_path):
    deals = sort_deals(deals)
    used_fallback = False

    if os.path.exists(tpl_path):
        wb = openpyxl.load_workbook(tpl_path)
        ws = wb[wb.sheetnames[0]]
        style = {}
        for c in range(1, 10):
            cell = ws.cell(2, c)
            style[c] = (copy.copy(cell.font), copy.copy(cell.fill),
                        cell.number_format, copy.copy(cell.alignment),
                        copy.copy(cell.border))
        if ws.max_row > 1:
            ws.delete_rows(2, ws.max_row - 1)
    else:
        used_fallback = True
        sys.stderr.write(
            "WARNING: template missing at %s - building a fresh workbook from the "
            "recorded spec. SAY SO in the report.\n" % tpl_path
        )
        wb = openpyxl.Workbook()
        ws = wb.active
        base = openpyxl.styles.Font(name="Aptos Narrow", size=11)
        for c, h in enumerate(HEADERS, start=1):
            cell = ws.cell(1, c, value=h)
            cell.font = copy.copy(base)
        style = {}
        for c in range(1, 10):
            align = openpyxl.styles.Alignment(wrap_text=True) if c == 8 else openpyxl.styles.Alignment()
            fmt = ACCOUNTING_FMT if c in (4, 5, 6) else "General"
            style[c] = (copy.copy(base), openpyxl.styles.PatternFill(), fmt, align,
                        openpyxl.styles.Border())

    for i, d in enumerate(deals):
        r = i + 2
        values = [
            d.get("dealname"),
            d.get("stage"),
            d.get("location"),
            d.get("revenue"),
            d.get("ebitda"),
            None,               # Valuation Proposed - never inferred
            None,               # Multiple - never inferred
            d.get("description"),
            d.get("deal_source"),
        ]
        for c, v in enumerate(values, start=1):
            cell = ws.cell(r, c, value=v)
            font, fill, fmt, align, border = style[c]
            cell.font = copy.copy(font)
            cell.fill = copy.copy(fill)
            cell.number_format = fmt
            cell.alignment = copy.copy(align)
            cell.border = copy.copy(border)
        ws.row_dimensions[r].height = row_height(d.get("description"))

    for col, width in COL_WIDTHS.items():
        ws.column_dimensions[col].width = width

    ws.title = "Badlands_Live_Deals_%s_" % tab_date
    wb.save(out_path)
    return out_path, used_fallback


def main():
    if len(sys.argv) < 4:
        raise SystemExit(__doc__)
    deals = json.load(open(sys.argv[1], encoding="utf-8"))
    out_path, tab_date = sys.argv[2], sys.argv[3]
    tpl_path = sys.argv[4] if len(sys.argv) > 4 else DEFAULT_TPL
    path, fallback = build(deals, out_path, tab_date, tpl_path)
    print("wrote %s (%d deals)%s" % (path, len(deals),
                                     " [FRESH-WORKBOOK FALLBACK]" if fallback else ""))


if __name__ == "__main__":
    main()
