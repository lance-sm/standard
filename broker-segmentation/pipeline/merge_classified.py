"""Overlay freshly rendered classifications onto the base state, by domain.

    python3 pipeline/merge_classified.py base-classified.jsonl rendered/classified.jsonl merged.jsonl
"""
import json, sys

base, overlay, dest = sys.argv[1], sys.argv[2], sys.argv[3]
rows = {}
for l in open(base, encoding="utf-8"):
    r = json.loads(l)
    rows[r["domain"]] = r
replaced = added = kept_base = 0
for l in open(overlay, encoding="utf-8"):
    r = json.loads(l)
    # only take the rendered read when it actually read something
    if r.get("site") == "OK" or r.get("focus") not in ("Unknown", None):
        if r["domain"] in rows:
            replaced += 1
        else:
            added += 1
        rows[r["domain"]] = r
    else:
        kept_base += 1
with open(dest, "w", encoding="utf-8") as fh:
    for r in rows.values():
        fh.write(json.dumps(r, ensure_ascii=False) + "\n")
print("merged %d rows: %d improved by the browser, %d new, %d still unreadable (base kept)"
      % (len(rows), replaced, added, kept_base))
