"""Re-queue the sites whose sector could not be read, so a DEEP pass retries them
against a wider set of likely industries/transactions paths."""
import json, os, sys
out = sys.argv[1]
idx = os.path.join(out, "index.jsonl")
cls = {json.loads(l)["domain"]: json.loads(l)
       for l in open(os.path.join(out, "classified.jsonl"), encoding="utf-8")}
redo = {d for d, c in cls.items()
        if c["focus"] in ("Generic - unstated", "Unknown") or c["site"] != "OK"}
recs = [json.loads(l) for l in open(idx, encoding="utf-8")]
keep = [r for r in recs if r["domain"] not in redo]
with open(idx, "w", encoding="utf-8") as fh:
    for r in keep:
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")
print("kept %d, deep-retrying %d" % (len(keep), len(recs) - len(keep)))
