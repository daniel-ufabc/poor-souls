#!/usr/bin/env bash
# build_content.sh — Convert all source markdown files to LaTeX.
# Run from the repository root. Safe to re-run after any markdown edit.

set -euo pipefail

SCRIPT="scripts/convert.py"
OUT="book/src/content"

echo "=== Converting includes ==="
python3 "$SCRIPT" _includes/initial-prayer.md  "$OUT/prayers/initial-prayer.tex"
# python3 "$SCRIPT" _includes/end-prayers.md     "$OUT/prayers/end-prayers.tex"

# echo "=== Converting prayers ==="
# python3 "$SCRIPT" _prayers/ladainha.md            "$OUT/prayers/ladainha.tex"           --wrapper section
# python3 "$SCRIPT" _prayers/credo.md               "$OUT/prayers/credo.tex"              --wrapper section
# python3 "$SCRIPT" _prayers/salve_rainha.md        "$OUT/prayers/salve-rainha.tex"        --wrapper section
# python3 "$SCRIPT" _prayers/oracao_pelas_almas.md  "$OUT/prayers/oracao-pelas-almas.tex" --wrapper section
# python3 "$SCRIPT" _prayers/de_profundis.md        "$OUT/prayers/de-profundis.tex"        --wrapper section

echo "=== Converting chapters ==="
for f in _book/dia{00..31}.md; do
    base=$(basename "$f" .md)
    python3 "$SCRIPT" "$f" "$OUT/chapters/${base}.tex"
done

pushd book/src/content/
pdflatex main.tex
gs -q -dBATCH -dNOPAUSE -dFastWebView=true -sDEVICE=pdfwrite -sOutputFile=main_web.pdf main.pdf \
  && mv main_web.pdf main.pdf
pdfjam --nup 2x1 --landscape --paper a4paper main.pdf '{},-' -o compact.pdf
popd

echo "=== Done ==="
