#!/bin/bash
# Crawl every broker site, retry what failed, dig deeper where no sector was read,
# classify, then build the workbook.
#   usage: run_all.sh <companies.tsv> <outdir> <dest.xlsx>
set -e
cd "$(dirname "$0")"
TSV="$1"; OUT="$2"; DEST="$3"
SEED="$OUT.seed.tsv"
mkdir -p "$OUT"
tail -n +2 "$TSV" | awk -F'\t' '$2!=""{print $1"\t"$2}' > "$SEED"
echo "== pass 1/5: crawl $(wc -l < "$SEED") sites =="
WORKERS=${W1:-32} python3 pipeline/crawl.py "$SEED" "$OUT"
echo "== pass 2/5: retry the unreadable ones =="
python3 pipeline/repair.py "$OUT"
WORKERS=${W2:-14} python3 pipeline/crawl.py "$SEED" "$OUT"
echo "== pass 3/5: first classify =="
python3 pipeline/classify.py "$OUT"
echo "== pass 4/5: deeper look where no sector was read =="
python3 pipeline/deepen.py "$OUT"
DEEP=1 MAX_PAGES=10 WORKERS=${W3:-20} python3 pipeline/crawl.py "$SEED" "$OUT"
python3 pipeline/classify.py "$OUT"
echo "== pass 5/5: workbook =="
python3 pipeline/build_workbook.py "$TSV" "$OUT/classified.jsonl" "$DEST"
