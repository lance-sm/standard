# -*- coding: utf-8 -*-
"""Render the sites plain HTTP could not read, using a real browser.

For the rows the cloud run marked "Thin / JS-only site" or "Blocked by bot
protection". Renders with Playwright Chromium, then hands the rendered HTML to
the SAME parsing and condensing code the static crawler uses, so the
classification behaves identically - only the fetch differs.

    python3 pipeline/render_pass.py recrawl-worklist.csv rendered

Resumable: re-running skips domains already in <outdir>/index.jsonl.
"""
import csv, gzip, json, os, re, sys, time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bs4 import BeautifulSoup
from crawl import text_of, pick_links, condense, safe_name, MAX_PAGES
from playwright.sync_api import sync_playwright

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
WORKLIST = sys.argv[1] if len(sys.argv) > 1 else "recrawl-worklist.csv"
OUT = sys.argv[2] if len(sys.argv) > 2 else "rendered"
DATA = os.path.join(OUT, "sitetext")
INDEX = os.path.join(OUT, "index.jsonl")
SETTLE_MS = int(os.environ.get("SETTLE_MS", "2800"))
NAV_TIMEOUT = int(os.environ.get("NAV_TIMEOUT", "30000"))
os.makedirs(DATA, exist_ok=True)


def load_worklist():
    rows = []
    with open(WORKLIST, newline="", encoding="utf-8-sig") as fh:
        for r in csv.DictReader(fh):
            d = (r.get("Domain") or "").strip().lower()
            if d:
                rows.append((r.get("Company", ""), d))
    done = set()
    if os.path.exists(INDEX):
        with open(INDEX, encoding="utf-8") as fh:
            for line in fh:
                try:
                    done.add(json.loads(line)["domain"])
                except Exception:
                    pass
    return [r for r in rows if r[1] not in done], len(done)


def render(page, url):
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=NAV_TIMEOUT)
        page.wait_for_timeout(SETTLE_MS)       # let client-side rendering settle
        return page.content()
    except Exception:
        return None


def do_domain(ctx, company, domain):
    rec = {"company": company, "domain": domain, "pages": [], "status": "",
           "final_url": "", "title": "", "rendered": True}
    page = ctx.new_page()
    html = None
    for cand in ("https://%s/" % domain, "https://www.%s/" % domain, "http://%s/" % domain):
        html = render(page, cand)
        if html and len(html) > 500:
            break
    if not html:
        rec["status"] = "unreachable:render-failed"
        page.close()
        return rec, ""
    rec["final_url"] = page.url
    soup = BeautifulSoup(html, "lxml")
    rec["title"] = (soup.title.get_text(strip=True) if soup.title else "")[:200]
    home = text_of(soup)
    chunks = [(rec["final_url"], home)]
    rec["pages"].append({"url": rec["final_url"], "kind": "home"})

    host = re.sub(r"^www\.", "", page.url.split("/")[2].lower()) if "//" in page.url else domain
    vert, deal = pick_links(soup, rec["final_url"], host)
    import hashlib
    sig = lambda t: hashlib.md5(re.sub(r"\s+", " ", t[:4000]).strip().lower().encode()).hexdigest()
    seen = {sig(home)}
    for url, kind in ([(u, "vertical") for u in vert] + [(u, "deal") for u in deal])[:MAX_PAGES - 1]:
        h = render(page, url)
        if not h:
            continue
        t = text_of(BeautifulSoup(h, "lxml"))
        s = sig(t)
        if s in seen:                       # soft-404 echo of a page already held
            rec["pages"].append({"url": url, "kind": kind, "dup": True})
            continue
        seen.add(s)
        chunks.append((url, t))
        rec["pages"].append({"url": url, "kind": kind})
    page.close()
    rec["status"] = "ok"
    rec["raw_chars"] = sum(len(t) for _, t in chunks)
    rec["head"] = re.sub(r"\s+", " ", home)[:300]
    return rec, condense(chunks)


def main():
    todo, already = load_worklist()
    print("worklist %d to render (%d already done)" % (len(todo), already), flush=True)
    if not todo:
        return
    t0 = time.time()
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        ctx = browser.new_context(user_agent=UA, viewport={"width": 1366, "height": 900},
                                  locale="en-US")
        ctx.set_default_timeout(NAV_TIMEOUT)
        for i, (company, domain) in enumerate(todo, 1):
            try:
                rec, text = do_domain(ctx, company, domain)
            except Exception as e:
                rec, text = {"company": company, "domain": domain, "pages": [],
                             "status": "error:%s" % type(e).__name__, "final_url": "",
                             "rendered": True}, ""
            if text:
                with gzip.open(os.path.join(DATA, safe_name(domain) + ".txt.gz"),
                               "wt", encoding="utf-8") as fh:
                    fh.write(text)
            with open(INDEX, "a", encoding="utf-8") as fh:
                fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
            if i % 20 == 0:
                el = time.time() - t0
                print("  %d/%d  %.2f/s  eta %.0f min" %
                      (i, len(todo), i / el, (len(todo) - i) / max(i / el, .01) / 60), flush=True)
        browser.close()
    print("rendered %d in %.0f min" % (len(todo), (time.time() - t0) / 60), flush=True)


if __name__ == "__main__":
    main()
