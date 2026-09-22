import sys, re, json, ssl, socket, threading, queue, time, html as htmlmod
sys.path.insert(0,'.')
from lib import norm_domain
import urllib.request, urllib.error

CTX = ssl.create_default_context(cafile="/root/.ccr/ca-bundle.crt")
UA  = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0 Safari/537.36"
BOT = ("one moment, please","just a moment","attention required","access denied","checking your browser",
       "enable javascript and cookies","ddos-guard","are you a human","request unsuccessful")
PARK= ("domain is for sale","buy this domain","this domain may be for sale","parked","godaddy.com/forsale",
       "hugedomains","domain for sale","sedoparking","future home of","under construction",
       "website coming soon","default web site page","index of /")

def grab(url, timeout=18):
    req=urllib.request.Request(url, headers={"User-Agent":UA,"Accept":"text/html,*/*",
        "Accept-Language":"en-US,en;q=0.9"})
    r=urllib.request.urlopen(req, context=CTX, timeout=timeout)
    raw=r.read(250000)
    enc="utf-8"
    ct=r.headers.get("Content-Type","")
    m=re.search(r"charset=([\w-]+)", ct, re.I)
    if m: enc=m.group(1)
    return r.status, r.geturl(), raw.decode(enc,"ignore")

def probe(dom):
    out={"domain":dom,"status":None,"final":"","title":"","site":"","desc":"","copyright":"","err":"","flag":""}
    last=None
    for scheme in ("https://","http://"):
        for attempt in (1,2):
            try:
                st,fin,body = grab(scheme+dom+"/")
                out["status"]=st; out["final"]=fin
                t=re.search(r"<title[^>]*>(.*?)</title>", body, re.S|re.I)
                if t: out["title"]=htmlmod.unescape(re.sub(r"\s+"," ",t.group(1))).strip()[:160]
                og=re.search(r'(?:property|name)=["\']og:site_name["\'][^>]*content=["\']([^"\']+)', body, re.I) \
                   or re.search(r'content=["\']([^"\']+)["\'][^>]*(?:property|name)=["\']og:site_name', body, re.I)
                if og: out["site"]=htmlmod.unescape(og.group(1)).strip()[:120]
                de=re.search(r'(?:name)=["\']description["\'][^>]*content=["\']([^"\']*)', body, re.I)
                if de: out["desc"]=htmlmod.unescape(de.group(1)).strip()[:200]
                cp=re.findall(r"(?:©|&copy;|copyright)\s*(?:\d{4}\s*(?:-\s*\d{4})?\s*)?([A-Za-z0-9&.,'\- ]{3,60})", body, re.I)
                if cp: out["copyright"]=htmlmod.unescape(cp[0]).strip()[:80]
                low=(out["title"]+" "+out["desc"]+" "+body[:4000]).lower()
                if any(b in low for b in BOT):  out["flag"]="botwall"
                elif any(p in low for p in PARK) and len(body)<20000: out["flag"]="parked"
                elif not out["title"] and len(body)<1500: out["flag"]="empty"
                return out
            except urllib.error.HTTPError as e:
                out["status"]=e.code; out["final"]=scheme+dom
                if e.code in (401,403,406,429): out["flag"]="botwall"; return out
                last=f"HTTP {e.code}"
                break
            except Exception as e:
                last=f"{type(e).__name__}: {str(e)[:70]}"
                if attempt==1: time.sleep(1.2); continue
    out["err"]=last or "unreachable"; out["flag"]=out["flag"] or "dead"
    return out

def main(infile, outfile, workers=14):
    doms=[l.strip() for l in open(infile,encoding="utf-8") if l.strip()]
    q=queue.Queue(); [q.put(d) for d in doms]
    res=[]; lock=threading.Lock(); done=[0]
    def work():
        while True:
            try: d=q.get_nowait()
            except queue.Empty: return
            r=probe(d)
            with lock:
                res.append(r); done[0]+=1
                if done[0]%50==0:
                    print(f"  {done[0]}/{len(doms)}", flush=True)
            q.task_done()
    ts=[threading.Thread(target=work,daemon=True) for _ in range(workers)]
    [t.start() for t in ts]; [t.join() for t in ts]
    json.dump(res, open(outfile,"w",encoding="utf-8"), indent=0)
    print("WROTE",outfile,len(res), flush=True)

if __name__=="__main__":
    socket.setdefaulttimeout(25)
    main(sys.argv[1], sys.argv[2])
