"""Drop weak rows from the crawl index so the resumable crawler retries them."""
import json, os, sys
out = sys.argv[1]
idx = os.path.join(out, "index.jsonl")
recs = [json.loads(l) for l in open(idx, encoding="utf-8")]
keep, drop = [], []
for r in recs:
    (keep if (r.get("status") == "ok" and r.get("raw_chars", 0) >= 600) else drop).append(r)
with open(idx, "w", encoding="utf-8") as fh:
    for r in keep:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")
print("kept %d, will retry %d" % (len(keep), len(drop)))
