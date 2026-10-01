# -*- coding: utf-8 -*-
"""Fetch each broker's own website and keep only the text that could answer:
   (a) which industries do they say they serve, (b) have they closed security deals.

Writes one gzipped condensed-text file per domain plus a JSONL index.
Resumable: re-running skips domains already recorded.
"""
import gzip, hashlib, json, os, re, sys, threading, time
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from taxonomy import ALL_KEYWORD_RE, DEAL_PAGE_HINTS, VERTICAL_PAGE_HINTS

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
HEADERS = {"User-Agent": UA, "Accept": "text/html,application/xhtml+xml,*/*;q=0.8",
           "Accept-Language": "en-US,en;q=0.9"}
MAX_BYTES = 2_000_000
MAX_PAGES = 6
CONDENSE_CAP = 30_000
TIMEOUT = (8, 18)

OUT_DIR = sys.argv[2] if len(sys.argv) > 2 else "out"
DATA_DIR = os.path.join(OUT_DIR, "sitetext")
INDEX = os.path.join(OUT_DIR, "index.jsonl")
os.makedirs(DATA_DIR, exist_ok=True)

_lock = threading.Lock()
_done = 0
_t0 = time.time()


def safe_name(d):
    return re.sub(r"[^a-z0-9.-]", "_", d.lower())


def get(session, url):
    try:
        r = session.get(url, headers=HEADERS, timeout=TIMEOUT, allow_redirects=True, stream=True)
        ct = (r.headers.get("content-type") or "").lower()
        if "html" not in ct and "text" not in ct and ct:
            r.close()
            return None, r.status_code, "non-html"
        buf = b""
        for chunk in r.iter_content(65536):
            buf += chunk
            if len(buf) > MAX_BYTES:
                break
        r.close()
        enc = r.encoding or "utf-8"
        try:
            html = buf.decode(enc, errors="replace")
        except (LookupError, TypeError):
            html = buf.decode("utf-8", errors="replace")
        return html, r.status_code, r.url
    except Exception as e:
        return None, None, type(e).__name__


JSON_STR = re.compile(r'"([^"\\\\]{18,400})"')


def _payload_text(soup):
    """Squarespace/Wix/Next/Framer sites render client-side but still ship their
    copy in meta tags, JSON-LD and inline JSON. Read that rather than give up."""
    bits = []
    for m in soup.find_all("meta"):
        if (m.get("name") or m.get("property") or "").lower() in (
                "description", "og:description", "og:title", "twitter:description",
                "keywords", "og:site_name"):
            if m.get("content"):
                bits.append(m["content"])
    for s in soup.find_all("script"):
        typ = (s.get("type") or "").lower()
        raw = s.string or s.get_text() or ""
        if not raw:
            continue
        if "ld+json" in typ or "application/json" in typ or "__NEXT_DATA__" in (s.get("id") or ""):
            bits.extend(JSON_STR.findall(raw)[:400])
        elif len(raw) > 200 and ("window." in raw or "__" in raw):
            bits.extend(JSON_STR.findall(raw)[:200])
    seen, out = set(), []
    for b in bits:
        b = re.sub(r"\\[unt][0-9a-fA-F]*", " ", b)
        b = re.sub(r"\s+", " ", b).strip()
        if len(b) > 12 and b.lower() not in seen and not b.startswith(("http", "/", "#", "data:")):
            seen.add(b.lower())
            out.append(b)
    return "\n".join(out)[:40000]


def text_of(soup):
    payload = _payload_text(soup)
    for t in soup(["script", "style", "svg"]):
        t.decompose()
    txt = soup.get_text("\n", strip=True)
    txt = re.sub(r"\n{2,}", "\n", txt)
    if len(txt) < 1500 and payload:
        txt = txt + "\n" + payload
    return txt


def pick_links(soup, base, host):
    vert, deal = [], []
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if href.startswith(("mailto:", "tel:", "javascript:", "#")):
            continue
        url = urljoin(base, href)
        p = urlparse(url)
        if p.scheme not in ("http", "https"):
            continue
        if host not in p.netloc.lower():
            continue
        if re.search(r"\.(pdf|jpe?g|png|gif|zip|docx?|xlsx?|pptx?|mp4|mp3)$", p.path, re.I):
            continue
        blob = (p.path + " " + (a.get_text(" ", strip=True) or "")).lower()
        if any(h in blob for h in VERTICAL_PAGE_HINTS):
            vert.append(url.split("#")[0])
        if any(h in blob for h in DEAL_PAGE_HINTS):
            deal.append(url.split("#")[0])
    def dedupe(seq):
        seen, out = set(), []
        for u in seq:
            k = u.rstrip("/").lower()
            if k not in seen:
                seen.add(k)
                out.append(u)
        return out
    return dedupe(vert)[:3], dedupe(deal)[:3]


def condense(chunks):
    """Keep only keyword-bearing lines, plus a little front matter for context."""
    out, total = [], 0
    for url, txt in chunks:
        keep = [ln for ln in txt.split("\n") if len(ln) > 3 and ALL_KEYWORD_RE.search(ln)]
        head = txt[:1500]
        block = "### %s\n%s\n%s\n" % (url, head, "\n".join(keep))
        out.append(block)
        total += len(block)
        if total > CONDENSE_CAP:
            break
    return ("\n".join(out))[:CONDENSE_CAP]


def crawl(row):
    company, domain = row
    rec = {"company": company, "domain": domain, "pages": [], "status": "", "final_url": ""}
    d = domain.strip().lower().lstrip("*.").strip("/")
    if not d or "." not in d:
        rec["status"] = "no-domain"
        return rec, ""
    session = requests.Session()
    html = code = None
    final = ""
    for cand in ("https://%s/" % d, "https://www.%s/" % d, "http://%s/" % d):
        html, code, final = get(session, cand)
        if html:
            break
    if not html:
        rec["status"] = "unreachable:%s" % (final or code)
        session.close()
        return rec, ""
    rec["final_url"] = final if isinstance(final, str) else ""
    host = urlparse(rec["final_url"] or "https://%s/" % d).netloc.lower()
    host = re.sub(r"^www\.", "", host)
    soup = BeautifulSoup(html, "lxml")
    title = (soup.title.get_text(strip=True) if soup.title else "")[:200]
    rec["title"] = title
    def sig(t):
        return hashlib.md5(re.sub(r"\s+", " ", t[:4000]).strip().lower().encode()).hexdigest()

    home_text = text_of(soup)
    chunks = [(rec["final_url"], home_text)]
    seen_sig = {sig(home_text)}
    rec["pages"].append({"url": rec["final_url"], "kind": "home"})

    vert, deal = pick_links(soup, rec["final_url"], host)
    targets = [(u, "vertical") for u in vert] + [(u, "deal") for u in deal]
    deep = os.environ.get("DEEP") == "1"
    if not vert:
        guesses = ["/industries"]
        if deep:
            guesses += ["/industries-served", "/who-we-serve", "/expertise"]
        targets += [(urljoin(rec["final_url"], g), "vertical-guess") for g in guesses]
    if not deal:
        guesses = ["/transactions"]
        if deep:
            guesses += ["/completed-transactions", "/recent-transactions", "/case-studies"]
        targets += [(urljoin(rec["final_url"], g), "deal-guess") for g in guesses]

    cap = int(os.environ.get("MAX_PAGES", MAX_PAGES))
    for url, kind in targets[:cap - 1]:
        h, c, f = get(session, url)
        if not h:
            continue
        s2 = BeautifulSoup(h, "lxml")
        t2 = text_of(s2)
        s = sig(t2)
        if s in seen_sig:
            rec["pages"].append({"url": url, "kind": kind, "dup": True})
            continue
        seen_sig.add(s)
        chunks.append((url, t2))
        rec["pages"].append({"url": url, "kind": kind})
    session.close()
    rec["status"] = "ok"
    rec["raw_chars"] = sum(len(t) for _, t in chunks)
    rec["head"] = re.sub(r"\s+", " ", chunks[0][1])[:300]
    return rec, condense(chunks)


def worker(row):
    global _done
    try:
        rec, text = crawl(row)
    except Exception as e:
        rec, text = {"company": row[0], "domain": row[1], "status": "error:%s" % type(e).__name__,
                     "pages": [], "final_url": ""}, ""
    if text:
        with gzip.open(os.path.join(DATA_DIR, safe_name(row[1]) + ".txt.gz"), "wt",
                       encoding="utf-8") as fh:
            fh.write(text)
    with _lock:
        _done += 1
        with open(INDEX, "a", encoding="utf-8") as fh:
            fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
        if _done % 25 == 0:
            el = time.time() - _t0
            print("  %d done  %.1f/s  elapsed %.0fs" % (_done, _done / el, el), flush=True)
    return None


def main():
    src = sys.argv[1]
    rows = []
    with open(src, encoding="utf-8") as fh:
        for line in fh:
            parts = line.rstrip("\n").split("\t")
            if len(parts) >= 2 and parts[1].strip():
                rows.append((parts[0], parts[1]))
    seen = set()
    if os.path.exists(INDEX):
        with open(INDEX, encoding="utf-8") as fh:
            for line in fh:
                try:
                    seen.add(json.loads(line)["domain"])
                except Exception:
                    pass
    todo = [r for r in rows if r[1] not in seen]
    print("total %d, already done %d, to crawl %d" % (len(rows), len(seen), len(todo)), flush=True)
    with ThreadPoolExecutor(max_workers=int(os.environ.get("WORKERS", "32"))) as ex:
        list(ex.map(worker, todo))
    print("finished %d in %.0fs" % (_done, time.time() - _t0), flush=True)


if __name__ == "__main__":
    main()
