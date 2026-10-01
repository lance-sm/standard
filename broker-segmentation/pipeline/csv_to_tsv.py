# -*- coding: utf-8 -*-
"""Normalise Lance's exported Companies CSV into the TSV the pipeline expects.

Tolerant on purpose: finds the real header row wherever it sits, accepts header
spelling variants, and keeps the columns the pipeline needs.
"""
import csv, re, sys

SRC, DEST = sys.argv[1], sys.argv[2]

WANT = {
    "Company": ["company", "company name", "name", "firm", "firm name"],
    "Domain": ["domain", "website", "company domain", "url", "web site"],
    "Segment": ["segment"],
    "Description": ["description", "note", "notes"],
    "# Contacts": ["# contacts", "contacts count", "num contacts", "no. contacts", "# of contacts"],
    "Contacts": ["contacts"],
}


def norm(s):
    return re.sub(r"\s+", " ", (s or "").strip().lower()).strip()


def pick(header):
    """Map our wanted column -> index in this file's header."""
    hn = [norm(h) for h in header]
    out = {}
    for want, aliases in WANT.items():
        for a in aliases:
            if a in hn:
                idx = hn.index(a)
                if idx not in out.values() or want == "Contacts":
                    out[want] = idx
                    break
    # '# Contacts' and 'Contacts' can collide; prefer exact matches
    if out.get("# Contacts") == out.get("Contacts"):
        for i, h in enumerate(hn):
            if h == "contacts" and i != out.get("# Contacts"):
                out["Contacts"] = i
    return out


def sniff(path):
    with open(path, newline="", encoding="utf-8-sig", errors="replace") as fh:
        sample = fh.read(65536)
    try:
        return csv.Sniffer().sniff(sample, delimiters=",;\t|").delimiter
    except csv.Error:
        return ","


def main():
    delim = sniff(SRC)
    rows = []
    with open(SRC, newline="", encoding="utf-8-sig", errors="replace") as fh:
        for r in csv.reader(fh, delimiter=delim):
            rows.append(r)
    # the header is the first row that carries both a company-ish and domain-ish column
    hdr_i, colmap = None, None
    for i, r in enumerate(rows[:40]):
        m = pick(r)
        if "Company" in m and "Domain" in m:
            hdr_i, colmap = i, m
            break
    if hdr_i is None:
        sys.exit("Could not find a header row with a Company and a Domain column. "
                 "First row seen: %r" % (rows[0][:12] if rows else None))
    order = ["Company", "Domain", "Segment", "Description", "# Contacts", "Contacts"]
    kept, skipped = 0, 0
    with open(DEST, "w", encoding="utf-8") as out:
        out.write("\t".join(order) + "\n")
        for r in rows[hdr_i + 1:]:
            if not any((c or "").strip() for c in r):
                continue
            vals = []
            for k in order:
                i = colmap.get(k)
                v = r[i] if (i is not None and i < len(r)) else ""
                vals.append(re.sub(r"[\t\r\n]+", " ", (v or "").strip()))
            if not vals[0] and not vals[1]:
                skipped += 1
                continue
            out.write("\t".join(vals) + "\n")
            kept += 1
    print("header row %d | columns found: %s" % (hdr_i + 1, sorted(colmap)))
    print("wrote %s: %d rows (%d blank skipped)" % (DEST, kept, skipped))


if __name__ == "__main__":
    main()
