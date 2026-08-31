#!/usr/bin/env python3
"""
Badlands state market map builder - dark landscape edition.

Validated JSON in, house-style PDF out. Page 1 is the argument (headline, KPI
strip, who is buying, and a dot map of where the companies actually are). Page 2+
are the two rosters: the ones that went, and the ones still standing.

Usage:
    python3 build_map.py data/connecticut.json
    python3 build_map.py data/connecticut.json --audience internal
    python3 build_map.py data/connecticut.json --html-only

See references/data_schema.md for the JSON contract.
"""

import argparse
import base64
import csv
import html as _html
import json
import math
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "..", "assets")

# ------------------------------------------------------------------- palette
BG = "#08191c"
PANEL = "#0d2226"
LINE = "#1b3b41"
MINT = "#3ddfc4"
TXT = "#e8f2f2"
MUTED = "#8aa2a6"
DIM = "#5f7a7e"
LAND = "#132c31"
LANDLINE = "#1e444b"
RING = "#8aa2a6"

# ------------------------------------------------------------------ geometry
PAGE_W, PAGE_H = 1056, 816          # US Letter landscape @96dpi
M = 44                              # page margin
RAIL_W = 300                        # right rail on page 1
RAIL_X = PAGE_W - M - RAIL_W
BODY_TOP = 112                      # below the header rule
BODY_BOT = PAGE_H - 62              # above the footer rule
GUTTER = 26


def esc(s):
    return _html.escape(str(s if s is not None else ""))


def yr_int(v):
    m = re.search(r"(1[6-9]\d\d|20\d\d)", str(v or ""))
    return int(m.group(1)) if m else None


# --------------------------------------------------------------------- fonts
def font_css():
    faces = [
        ("BdSans", "Inter-Light.woff2", 300),
        ("BdSans", "Inter-Regular.woff2", 400),
        ("BdSans", "Inter-Medium.woff2", 500),
        ("BdSans", "Inter-SemiBold.woff2", 600),
        ("BdMono", "JBMono-Light.woff2", 300),
        ("BdMono", "JBMono-Regular.woff2", 400),
    ]
    out = []
    for fam, fn, wt in faces:
        p = os.path.join(ASSETS, "fonts", fn)
        if not os.path.exists(p):
            continue
        b64 = base64.b64encode(open(p, "rb").read()).decode()
        out.append(
            f"@font-face{{font-family:'{fam}';font-weight:{wt};font-style:normal;"
            f"src:url(data:font/woff2;base64,{b64}) format('woff2')}}"
        )
    return "".join(out)


# ----------------------------------------------------------------------- map
def load_places():
    p = os.path.join(ASSETS, "places_ne.csv")
    out = {}
    if not os.path.exists(p):
        return out
    with open(p, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            out[(r["state"].upper(), r["city"].strip().lower())] = (
                float(r["lat"]),
                float(r["lon"]),
            )
    return out


def geo_path(coords, proj):
    """MultiPolygon/Polygon coordinate list -> SVG path data."""
    d = []
    def ring(r):
        pts = [proj(x, y) for x, y in r]
        d.append("M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + "Z")
    def walk(c, depth):
        if depth == 1:
            ring(c)
        else:
            for sub in c:
                walk(sub, depth - 1)
    walk(coords, 3 if isinstance(coords[0][0][0], (list, tuple)) else 2)
    return "".join(d)


def build_map_svg(d, box_w, box_h, internal):
    """Dot map: filled mint = still independent, slate ring = absorbed."""
    ab = (d.get("state_abbrev") or d["state"][:2]).upper()
    gp = os.path.join(ASSETS, "geo", f"{ab}.json")
    if not os.path.exists(gp):
        return "", []
    gj = json.load(open(gp, encoding="utf-8"))

    xs, ys = [], []
    def scan(c, depth):
        if depth == 1:
            for x, y in c:
                xs.append(x)
                ys.append(y)
        else:
            for s in c:
                scan(s, depth - 1)
    for f in gj["features"]:
        c = f["geometry"]["coordinates"]
        scan(c, 3 if isinstance(c[0][0][0], (list, tuple)) else 2)
    lon0, lon1, lat0, lat1 = min(xs), max(xs), min(ys), max(ys)
    k = math.cos(math.radians((lat0 + lat1) / 2))
    w_deg, h_deg = (lon1 - lon0) * k, (lat1 - lat0)
    scale = min(box_w / w_deg, box_h / h_deg) * 0.98
    ox = (box_w - w_deg * scale) / 2
    oy = (box_h - h_deg * scale) / 2

    def proj(lon, lat):
        return (ox + (lon - lon0) * k * scale, oy + (lat1 - lat) * scale)

    parts = [
        f"<svg width='{box_w}' height='{box_h}' viewBox='0 0 {box_w} {box_h}' "
        "xmlns='http://www.w3.org/2000/svg'>"
    ]
    for f in gj["features"]:
        parts.append(
            f"<path d='{geo_path(f['geometry']['coordinates'], proj)}' "
            f"fill='{LAND}' stroke='{LANDLINE}' stroke-width='0.7'/>"
        )

    places = load_places()
    towns = {}
    missing = []
    def bump(city, key):
        if not city:
            return
        c = city.strip()
        ll = places.get((ab, c.lower()))
        if not ll:
            missing.append(c)
            return
        t = towns.setdefault(c, {"ll": ll, "ind": 0, "abs": 0})
        t[key] += 1
    for s in d.get("sections", []):
        for it in s.get("items", []):
            bump(it.get("city"), "ind")
    for a in d.get("acquisitions", []):
        bump(a.get("city"), "abs")

    labeled = sorted(
        towns.items(), key=lambda kv: -(kv[1]["ind"] + kv[1]["abs"] * 0.9)
    )[: d.get("map_labels", 9)]
    label_names = {n for n, _ in labeled}

    for name, t in sorted(towns.items(), key=lambda kv: kv[1]["ind"] + kv[1]["abs"]):
        x, y = proj(t["ll"][1], t["ll"][0])
        if t["abs"]:
            r = 5.0 + 2.0 * math.sqrt(max(0, t["abs"] - 1))
            parts.append(
                f"<circle cx='{x:.1f}' cy='{y:.1f}' r='{r:.1f}' fill='none' "
                f"stroke='{RING}' stroke-width='1.1' opacity='.85'/>"
            )
        if t["ind"]:
            r = 3.0 + 2.3 * math.sqrt(max(0, t["ind"] - 1))
            parts.append(
                f"<circle cx='{x:.1f}' cy='{y:.1f}' r='{r:.1f}' fill='{MINT}' opacity='.92'/>"
            )
    drawn = []
    for name, t in labeled:
        x, y = proj(t["ll"][1], t["ll"][0])
        r = 3.0 + 2.3 * math.sqrt(max(0, t["ind"] - 1)) if t["ind"] else 6
        ly = y + r + 10
        if any(abs(x - px) < 62 and abs(ly - py) < 13 for px, py in drawn):
            continue  # skip labels that would collide
        half = 3.2 * len(name)  # keep the label inside the frame
        x = min(max(x, half + 2), box_w - half - 2)
        ly = min(ly, box_h - 3)
        drawn.append((x, ly))
        parts.append(
            f"<text x='{x:.1f}' y='{ly:.1f}' text-anchor='middle' "
            f"font-family='BdMono' font-size='6.6' letter-spacing='1.1' "
            f"fill='{MUTED}'>{esc(name.upper())}</text>"
        )
    parts.append("</svg>")
    return "".join(parts), sorted(set(missing))


# ------------------------------------------------------------------ stats
def compute(d):
    inds = [it for s in d.get("sections", []) for it in s.get("items", [])]
    acqs = d.get("acquisitions", [])
    years = [yr_int(a.get("year")) for a in acqs]
    years = [y for y in years if y]
    tally = {}
    for a in acqs:
        if a.get("acquirer"):
            tally[a["acquirer"]] = tally.get(a["acquirer"], 0) + 1
    top = max(tally.items(), key=lambda kv: kv[1]) if tally else ("", 0)
    founded = [yr_int(i.get("founded")) for i in inds]
    founded = [y for y in founded if y]
    towns = {i.get("city", "").strip().lower() for i in inds if i.get("city")}
    return {
        "n_ind": len(inds),
        "n_abs": len(acqs),
        "top_acq": top[0],
        "top_n": top[1],
        "yr_lo": min(years) if years else None,
        "yr_hi": max(years) if years else None,
        "oldest": min(founded) if founded else None,
        "n_towns": len(towns),
        "tally": sorted(tally.items(), key=lambda kv: (-kv[1], kv[0])),
    }


# ------------------------------------------------------------------- pieces
def header(d, page_no, n_pages):
    return (
        "<div class='hd'>"
        "<div class='bl'><div class='mark'>b</div><div>"
        f"<div class='wm'>{esc(d.get('brand','BADLANDS'))}</div>"
        f"<div class='kick'>{esc(d.get('tagline','Security Company'))} &middot; {esc(d.get('hq','New York, NY'))}</div>"
        "</div></div>"
        "<div class='br'>"
        f"<div class='kick'>Market Map &middot; {esc(d['as_of'])}</div>"
        f"<div class='kick'>{esc(d['state'])} Independents &middot; {page_no} of {n_pages}</div>"
        "</div></div>"
    )


def footer(d, internal):
    note = d.get(
        "footer_note",
        "Compiled from ZoomInfo, state records, industry press and company materials. "
        "Founding years shown where verified. Corrections and additions welcome.",
    )
    warn = "<span class='conf'>Internal - not for distribution</span> &nbsp; " if internal else ""
    return f"<div class='ft'>{warn}{esc(note)}</div>"


def kpi_cells(d, st, internal):
    show_f = d.get("show_founded", True)
    cells = [
        (st["n_ind"], "Independent and standing"),
        (st["n_abs"], f"Absorbed since {st['yr_lo']}" if st["yr_lo"] else "Absorbed"),
    ]
    if st["top_n"] > 1:
        cells.append((st["top_n"], "To a single acquirer"))
    if show_f and st["oldest"]:
        cells.append((st["oldest"], "Oldest shop still owner-run"))
    else:
        cells.append((st["n_towns"], "Towns with an independent"))
    for extra in d.get("extra_kpis", [])[: max(0, 4 - len(cells))]:
        cells.append((extra["value"], extra["label"]))
    return "".join(
        f"<div class='kpi'><div class='kn'>{esc(v)}</div><div class='kl'>{esc(l)}</div></div>"
        for v, l in cells[:4]
    )


def rail(d, st):
    legend = (
        "<div class='box'><div class='bt'>Legend</div>"
        f"<div class='lg'><span class='dot'></span>Still independent</div>"
        f"<div class='lg'><span class='ring'></span>Absorbed"
        + (f" {st['yr_lo']}-{st['yr_hi']}" if st["yr_lo"] else "")
        + "</div>"
        "<div class='ln'>Towns holding both show a mint core inside a slate ring.</div>"
        "</div>"
    )
    rows = "".join(
        f"<div class='ar'><span class='an'>{esc(a)}</span>"
        f"<span class='ac{' hot' if n == st['top_n'] and n > 1 else ''}'>{n}</span></div>"
        for a, n in st["tally"]
    )
    buy = f"<div class='box'><div class='bt'>Who is doing the buying</div>{rows}</div>"
    return legend + buy


# ------------------------------------------------------------------- rosters
def acq_item_html(a, internal):
    yr = yr_int(a.get("year"))
    meta = esc(a.get("city", ""))
    if yr:
        meta += f" &middot; {yr}"
    right = ""
    if a.get("acquirer"):
        arrow = a.get("verb_short") or "&#8594;"
        right = f"{arrow} {esc(a['acquirer'])}"
        if internal and a.get("sponsor"):
            right += f" <span class='spn'>({esc(a['sponsor'])})</span>"
    note = f"<span class='nte'> - {esc(a['note'])}</span>" if a.get("note") else ""
    return (
        "<div class='it acq'><span class='ring'></span><div class='ib'>"
        f"<div class='l1'><span class='cn'>{esc(a['company'])}</span>"
        f"<span class='cm'>{meta}</span>{note}</div>"
        f"<div class='l2'>{right}</div></div></div>"
    )


def ind_item_html(f, show_founded, internal):
    bits = [esc(f.get("city", ""))]
    y = yr_int(f.get("founded"))
    if show_founded and y:
        bits.append(str(y))
    if internal and f.get("revenue_band"):
        bits.append(esc(f["revenue_band"]))
    flag = "<span class='sx'>&#9670;</span>" if internal and f.get("succession") else ""
    return (
        "<div class='it'><span class='dot'></span><div class='ib'>"
        f"<span class='cn'>{esc(f['company'])}</span>{flag}"
        f"<span class='cm'>{' &middot; '.join(b for b in bits if b)}</span>"
        "</div></div>"
    )


# ------------------------------------------------------------------ flow
def tag(html, key):
    """Stamp data-m onto the item's own outer element so the measured DOM is
    byte-identical to the rendered one - a wrapper div is enough to shift
    heights and silently break pagination."""
    return html.replace("<div class=", f"<div data-m='{key}' class=", 1)


def measure_doc(html):
    """Measure every tagged element inside the REAL rendered document.

    Measuring a synthetic stand-in is what silently breaks pagination: the
    numbers look plausible, the page overflows, and nobody notices until an
    owner is reading a truncated list. So we lay out, measure the actual
    document, and lay out again until the numbers stop moving.
    """
    import tempfile

    try:
        from playwright.sync_api import sync_playwright

        with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
            f.write(html)
            path = f.name
        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page()
            pg.goto("file://" + path)
            pg.evaluate("() => document.fonts.ready")
            out = pg.evaluate(
                "() => Object.fromEntries([...document.querySelectorAll('[data-m]')]"
                ".map(e => [e.dataset.m, e.getBoundingClientRect().height]))"
            )
            b.close()
        os.unlink(path)
        return {k: math.ceil(v) for k, v in out.items()}
    except Exception as e:
        sys.stderr.write(f"[warn] measure unavailable ({e}); using estimates\n")
        return {}


def verify(hpath):
    """Open the finished document and prove nothing runs past the footer rule."""
    try:
        from playwright.sync_api import sync_playwright

        with sync_playwright() as p:
            b = p.chromium.launch()
            pg = b.new_page()
            pg.goto("file://" + os.path.abspath(hpath))
            pg.evaluate("() => document.fonts.ready")
            bad = pg.evaluate(
                "(bot) => [...document.querySelectorAll('.page')].map((pg,i) => {"
                " const pt = pg.getBoundingClientRect().top;"
                " const over = [...pg.querySelectorAll('.sec')].map(s =>"
                "   Math.round(s.getBoundingClientRect().bottom - pt - bot));"
                " return {page:i+1, over:Math.max(0, ...over)}; })"
                ".filter(x => x.over > 0)",
                BODY_BOT,
            )
            b.close()
        return bad
    except Exception:
        return []


def flow(sections, heights, top_y):
    """Pour sections into column grids across as many pages as needed.

    sections: [{key, title, kicker, cols, items:[(id, html)]}]
    returns:  [[{title, kicker, cols, columns:[[html,...]], cont, h}]] per page
    """
    pages = [[]]
    y = top_y
    for s in sections:
        idx = 0
        first = True
        KICK_H = heights.get(s["key"], 60)
        while idx < len(s["items"]):
            avail = BODY_BOT - y - KICK_H
            if avail < 80:
                pages.append([])
                y = BODY_TOP
                continue
            cw = (PAGE_W - 2 * M - GUTTER * (s["cols"] - 1)) / s["cols"]
            cols = [[] for _ in range(s["cols"])]
            heights_used = [0] * s["cols"]
            ci = 0
            placed = 0
            # if everything left fits on this page, balance the columns instead
            # of stuffing column one and leaving the rest empty
            rest = sum(heights[k] for k, _ in s["items"][idx:])
            target = min(avail, math.ceil(rest / s["cols"]) + 24) if rest <= avail * s["cols"] else avail
            while idx < len(s["items"]):
                k, htm = s["items"][idx]
                h = heights[k]
                # never orphan a sub-header at the foot of a column
                need = h
                if k.startswith("h") and idx + 1 < len(s["items"]):
                    need += sum(heights[kk] for kk, _ in s["items"][idx + 1: idx + 4])
                cap = target if ci < s["cols"] - 1 else avail
                if heights_used[ci] + need <= cap or not cols[ci]:
                    cols[ci].append(htm)
                    heights_used[ci] += h
                    idx += 1
                    placed += 1
                elif ci < s["cols"] - 1:
                    ci += 1
                else:
                    break
            if not placed:
                pages.append([])
                y = BODY_TOP
                continue
            pages[-1].append(
                {
                    "key": s["key"],
                    "title": s["title"],
                    "kicker": s["kicker"],
                    "cols": s["cols"],
                    "cw": cw,
                    "columns": cols,
                    "cont": not first,
                    "h": max(heights_used),
                    "head_h": KICK_H,
                }
            )
            first = False
            y += KICK_H + max(heights_used) + 26
            if idx < len(s["items"]):
                pages.append([])
                y = BODY_TOP
    return pages


# ------------------------------------------------------------------ styling
def build_css():
    return (
        font_css()
        + f"""
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'BdSans',Inter,Helvetica,Arial,sans-serif;background:{BG};color:{TXT};
 -webkit-font-smoothing:antialiased}}
.page{{width:{PAGE_W}px;height:{PAGE_H}px;position:relative;overflow:hidden;
 background:{BG};page-break-after:always}}
.page:last-child{{page-break-after:auto}}
.hd{{position:absolute;left:{M}px;right:{M}px;top:38px;display:flex;
 justify-content:space-between;align-items:flex-start;
 border-bottom:1px solid {LINE};padding-bottom:16px}}
.bl{{display:flex;gap:11px;align-items:center}}
.mark{{width:26px;height:26px;border-radius:6px;background:{MINT};color:{BG};
 font-size:17px;font-weight:600;line-height:26px;text-align:center}}
.wm{{font-size:13px;font-weight:600;letter-spacing:3.4px;text-transform:uppercase}}
.kick{{font-family:'BdMono';font-size:7.2px;letter-spacing:1.7px;color:{MUTED};
 text-transform:uppercase;margin-top:3px}}
.br{{text-align:right}}
.br .kick{{margin-top:0;line-height:1.75}}
.ft{{position:absolute;left:{M}px;right:{M}px;bottom:26px;border-top:1px solid {LINE};
 padding-top:9px;font-family:'BdMono';font-size:6.6px;letter-spacing:.9px;
 color:{DIM};text-transform:uppercase}}
.conf{{color:{MINT}}}

/* page 1 */
.hero{{position:absolute;left:{M}px;top:{BODY_TOP + 14}px;width:{RAIL_X - M - 46}px}}
.h1{{font-size:37px;font-weight:300;line-height:1.14;letter-spacing:-.9px}}
.h1 em{{font-style:normal;color:{MINT}}}
.deck{{margin-top:16px;font-size:11.2px;line-height:1.62;color:{MUTED};max-width:520px}}
.kpis{{display:flex;margin-top:26px;border-left:1px solid {LINE}}}
.kpi{{flex:1;border-right:1px solid {LINE};padding:2px 14px 4px}}
.kn{{font-size:33px;font-weight:300;letter-spacing:-1.2px;line-height:1.1}}
.kl{{font-family:'BdMono';font-size:6.4px;letter-spacing:1.3px;color:{MUTED};
 text-transform:uppercase;margin-top:7px;line-height:1.5}}
.maplab{{position:absolute;left:{M}px;font-size:14px;font-weight:400}}
.mapsub{{font-family:'BdMono';font-size:6.5px;letter-spacing:1.5px;color:{DIM};
 text-transform:uppercase;margin-top:5px}}
.mapwrap{{position:absolute;left:{M}px}}
.rail{{position:absolute;left:{RAIL_X}px;width:{RAIL_W}px;top:{BODY_TOP + 14}px}}
.box{{background:{PANEL};border:1px solid {LINE};border-radius:3px;padding:14px 16px;
 margin-bottom:16px}}
.bt{{font-family:'BdMono';font-size:6.8px;letter-spacing:1.9px;color:{MUTED};
 text-transform:uppercase;margin-bottom:11px}}
.lg{{font-size:10px;color:{TXT};margin-bottom:7px;display:flex;align-items:center;gap:9px}}
.ln{{font-size:9px;color:{DIM};line-height:1.5;margin-top:9px}}
.ar{{display:flex;justify-content:space-between;align-items:baseline;
 padding:5px 0;border-top:1px solid {LINE};font-size:9.6px}}
.ar:first-of-type{{border-top:none}}
.an{{color:{TXT}}}
.ac{{font-family:'BdMono';font-size:9.5px;color:{MUTED}}}
.ac.hot{{color:{MINT}}}

/* rosters */
.sec{{position:absolute;left:{M}px;right:{M}px}}
.head{{overflow:hidden}}  /* stop margin-collapse so the head measures true */
.st{{font-size:15px;font-weight:400;margin-bottom:5px}}
.sk{{font-family:'BdMono';font-size:6.6px;letter-spacing:1.6px;color:{DIM};
 text-transform:uppercase;padding-bottom:11px;border-bottom:1px solid {LINE};
 margin-bottom:14px}}
.grid{{display:flex;gap:{GUTTER}px}}
.it{{display:flex;gap:8px;align-items:flex-start;padding:2.5px 0}}
.dot{{width:5px;height:5px;border-radius:50%;background:{MINT};flex:none;margin-top:4.5px}}
.ring{{width:6px;height:6px;border-radius:50%;border:1px solid {RING};flex:none;margin-top:4px}}
.ib{{flex:1;min-width:0}}
.cn{{font-size:9.4px;font-weight:500;color:{TXT}}}
.cm{{font-family:'BdMono';font-size:7.4px;color:{DIM};margin-left:6px;letter-spacing:.2px}}
.nte{{font-size:8.6px;color:{DIM}}}
.acq{{padding:5px 0;border-bottom:1px solid rgba(27,59,65,.55)}}
.acq .l1{{line-height:1.35}}
.acq .l2{{font-size:8.8px;color:{MUTED};margin-top:2px}}
.spn{{color:{DIM}}}
.sx{{color:{MINT};font-size:6px;margin-left:5px;vertical-align:2px}}
.subh{{font-family:'BdMono';font-size:6.8px;letter-spacing:1.7px;color:{MINT};
 text-transform:uppercase;padding:14px 0 7px;margin-bottom:3px;
 border-bottom:1px solid {LINE}}}
/* no first-child padding override: a sub-header's height must not depend on
   where it lands, or the measure-and-reflow loop oscillates and never settles */
"""
    )


# ------------------------------------------------------------------- render
def render(d, st, internal, css):
    """Lay out, measure the real document, lay out again until stable."""
    secs = build_sections(d, st, internal)
    heights = {}
    for s in secs:
        heights[s["key"]] = 60
        for k, h in s["items"]:
            heights[k] = 46 if "acq" in h else 26
    heights["hero"] = 250
    html = ""
    for _ in range(6):
        pages = flow(secs, heights, BODY_TOP + 6)
        html = render_html(d, st, internal, css, pages, heights)
        new = measure_doc(html)
        if not new:
            break
        # monotonic: never shrink a measured height, so the loop always converges
        # and a block can only ever be over-reserved, never clipped
        merged = dict(heights)
        for k, v in new.items():
            if k in heights:
                merged[k] = max(heights[k], v)
        if merged == heights:
            break
        heights = merged
    return html


def build_sections(d, st, internal):
    show_f = d.get("show_founded", True)
    secs = []
    if d.get("acquisitions"):
        acqs = sorted(
            d["acquisitions"],
            key=lambda a: (0, yr_int(a.get("year")), "")
            if yr_int(a.get("year"))
            else (1, 0, a.get("company", "").lower()),
        )
        rng = (
            f"Acquired {st['yr_lo']}-{st['yr_hi']} &middot; year shown where verified"
            if st["yr_lo"]
            else "Acquired &middot; year shown where verified"
        )
        secs.append(
            {
                "key": "sec_acq",
                "title": d.get("acq_title") or f"The {num_word(st['n_abs'])} that went",
                "kicker": rng,
                "cols": 2,
                "items": [
                    (f"a{i}", tag(acq_item_html(a, internal), f"a{i}"))
                    for i, a in enumerate(acqs)
                ],
            }
        )
    kick = f"{esc(d['state'])}-headquartered, independently owned"
    if show_f:
        kick += " &middot; founding year where verified"
    items = []
    for si, s in enumerate(d.get("sections", [])):
        rows = sorted(
            s.get("items", []),
            key=lambda f: (0, yr_int(f.get("founded")), "")
            if (show_f and yr_int(f.get("founded")))
            else (1, 0, f.get("company", "").lower()),
        )
        items.append(
            (
                f"h{si}",
                tag(
                    f"<div class='subh'>{esc(s['name'])} &middot; {len(rows)}</div>",
                    f"h{si}",
                ),
            )
        )
        items += [
            (f"i{si}_{j}", tag(ind_item_html(f, show_f, internal), f"i{si}_{j}"))
            for j, f in enumerate(rows)
        ]
    if items:
        secs.append(
            {
                "key": "sec_ind",
                "title": d.get("ind_title") or f"The {num_word(st['n_ind'])} still standing",
                "kicker": kick,
                "cols": d.get("roster_cols", 4),
                "items": items,
            }
        )

    return secs


def render_html(d, st, internal, css, pages, heights):
    n = len(pages) + 1

    out = [f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body>"]

    # ---- page 1
    map_w = RAIL_X - M - 46
    head = d.get("headline") or default_headline(d, st)
    deck = d.get("deck") or default_deck(d, st)
    hero_html = (
        f"<div class='h1'>{head}</div>"
        f"<div class='deck'>{esc(deck)}</div>"
        f"<div class='kpis'>{kpi_cells(d, st, internal)}</div>"
    )
    hero_h = heights.get("hero", 250)
    map_top = BODY_TOP + 14 + hero_h + 62
    map_h = BODY_BOT - map_top - 6
    svg, missing = build_map_svg(d, map_w, map_h, internal)
    out.append("<div class='page'>" + header(d, 1, n))
    out.append(f"<div class='hero' data-m='hero'>{hero_html}</div>")
    out.append(f"<div class='rail'>{rail(d, st)}</div>")
    if svg:
        out.append(
            f"<div class='maplab' style='top:{map_top - 44}px'>{esc(d.get('map_title','Where they are'))}"
            "<div class='mapsub'>Dot size = companies headquartered in that town</div></div>"
            f"<div class='mapwrap' style='top:{map_top}px'>{svg}</div>"
        )
    out.append(footer(d, internal) + "</div>")

    # ---- roster pages
    for pi, blocks in enumerate(pages):
        out.append("<div class='page'>" + header(d, pi + 2, n))
        y = BODY_TOP + 6
        for b in blocks:
            title = b["title"] + (" (continued)" if b["cont"] else "")
            cols = "".join(
                f"<div class='col' style='width:{b['cw']:.0f}px'>{''.join(c)}</div>"
                for c in b["columns"]
            )
            out.append(
                f"<div class='sec' style='top:{y}px'>"
                f"<div class='head' data-m='{b['key']}'><div class='st'>{esc(title)}</div>"
                f"<div class='sk'>{b['kicker']}</div></div>"
                f"<div class='grid'>{cols}</div></div>"
            )
            y += b["head_h"] + b["h"] + 26
        out.append(footer(d, internal) + "</div>")
    out.append("</body></html>")
    if missing:
        sys.stderr.write(
            "[warn] no coordinates for: " + ", ".join(missing[:12]) + "\n"
        )
    return "".join(out)


def num_word(n):
    words = {
        1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven",
        8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen",
        14: "fourteen", 15: "fifteen", 16: "sixteen", 17: "seventeen", 18: "eighteen",
        19: "nineteen", 20: "twenty",
    }
    tens = {2: "twenty", 3: "thirty", 4: "forty", 5: "fifty", 6: "sixty", 7: "seventy",
            8: "eighty", 9: "ninety"}
    if n in words:
        return words[n]
    if n < 100:
        t, o = divmod(n, 10)
        return tens[t] + ("-" + words[o] if o else "")
    if n < 1000:
        h, r = divmod(n, 100)
        return words[h] + " hundred" + (" " + num_word(r) if r else "")
    return str(n)


def default_headline(d, st):
    return (
        f"{esc(d['state'])}'s independents are<br>being bought <em>one at a time.</em>"
    )


def default_deck(d, st):
    lo = st["yr_lo"] or 2015
    s = (
        f"{num_word(st['n_abs']).capitalize()} owner-run security, alarm, locksmith and fire "
        f"shops have gone into national and PE-backed rollups since {lo}"
    )
    if st["top_n"] > 1:
        s += f" - {num_word(st['top_n'])} of them to the same buyer"
    s += f". {num_word(st['n_ind']).capitalize()} are still standing. This is where they are."
    return s


# ---------------------------------------------------------------- validation
def validate(d):
    errs = []
    for k in ("state", "as_of"):
        if not d.get(k):
            errs.append(f"missing required field: {k}")
    for a in d.get("acquisitions", []):
        if not a.get("company"):
            errs.append("acquisition row with no company name")
        y = yr_int(a.get("year"))
        if a.get("year") and not (2015 <= (y or 0) <= 2030):
            errs.append(f"acquisition year out of range: {a.get('company')} {a['year']}")
    seen = set()
    for s in d.get("sections", []):
        for f in s.get("items", []):
            if not f.get("company"):
                errs.append(f"firm row with no company name in {s.get('name')}")
            key = f.get("company", "").lower().strip()
            if key in seen:
                errs.append(f"duplicate firm across sections: {f.get('company')}")
            seen.add(key)
    acq = {a.get("company", "").lower().strip() for a in d.get("acquisitions", [])}
    for dup in seen & acq:
        errs.append(f"listed as BOTH acquired and independent: {dup}")
    return errs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("data")
    ap.add_argument("--out")
    ap.add_argument("--audience", choices=["external", "internal"])
    ap.add_argument("--html-only", action="store_true")
    a = ap.parse_args()

    d = json.load(open(a.data, encoding="utf-8"))
    internal = (a.audience or d.get("audience", "external")) == "internal"
    errs = validate(d)
    if errs:
        sys.stderr.write("VALIDATION FAILED:\n  " + "\n  ".join(errs) + "\n")
        sys.exit(1)

    css = build_css()
    st = compute(d)
    doc = render(d, st, internal, css)

    base = a.out or os.path.join(
        os.path.dirname(os.path.abspath(a.data)),
        f"Badlands_{(d.get('state_abbrev') or d['state'][:2]).upper()}_Market_Map_"
        f"{d['as_of'].replace(' ', '_')}{'_INTERNAL' if internal else ''}.pdf",
    )
    hpath = os.path.splitext(base)[0] + ".html"
    os.makedirs(os.path.dirname(os.path.abspath(base)) or ".", exist_ok=True)
    open(hpath, "w", encoding="utf-8").write(doc)
    for bad in verify(hpath):
        sys.stderr.write(
            f"[OVERFLOW] page {bad['page']} runs {bad['over']}px past the footer\n"
        )
    if a.html_only:
        print(hpath)
        return

    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page()
        pg.goto("file://" + os.path.abspath(hpath))
        pg.evaluate("() => document.fonts.ready")
        pg.pdf(
            path=base,
            width=f"{PAGE_W}px",
            height=f"{PAGE_H}px",
            print_background=True,
            margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
        )
        b.close()
    print(base)


if __name__ == "__main__":
    main()
