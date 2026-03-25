#!/usr/bin/env bash
# spellcheck.sh — Run aspell (pt_BR) over all source markdown files.
# Strips Jekyll frontmatter, Liquid tags, HTML, and markdown syntax before
# checking so only real prose words are tested.
#
# Usage:
#   bash scripts/spellcheck.sh            # check all _book/dia*.md
#   bash scripts/spellcheck.sh _book/dia03.md   # check a single file
#
# Output: one line per misspelling — "file:word"
# Requires: aspell, aspell-pt-br

set -euo pipefail

DICT="pt_BR"
FILES="${@:-_book/dia*.md _includes/*.md _prayers/*.md}"

if ! aspell dump dicts | grep -q "$DICT"; then
    echo "ERROR: aspell dictionary '$DICT' not found." >&2
    echo "Install it with: sudo apt-get install aspell-pt-br" >&2
    exit 1
fi

for f in $FILES; do
    # Strip in order:
    #   1. YAML frontmatter (between --- markers)
    #   2. Liquid tags  {% ... %} and {{ ... }}
    #   3. HTML tags and entities
    #   4. Markdown links, bold, italic markers, headings, list markers
    #   5. Footnote definitions and references
    clean=$(sed \
        -e '/^---$/,/^---$/d' \
        -e 's/{% [^%]*%}//g' \
        -e 's/{{ [^}]*}}//g' \
        -e 's/<[^>]*>//g' \
        -e 's/&[a-z]*;//g' \
        -e 's/\[^\([^]]*\)\]: \(.*\)//g' \
        -e 's/\[^\([^]]*\)\]//g' \
        -e 's/\[\([^]]*\)\]([^)]*)//g' \
        -e 's/^##* //g' \
        -e 's/\*\*//g' \
        -e 's/\*//g' \
        -e 's/^- //g' \
        "$f")

    misspellings=$(echo "$clean" \
        | aspell --lang="$DICT" --encoding=utf-8 list \
        | sort -u)

    if [ -n "$misspellings" ]; then
        while IFS= read -r word; do
            echo "$f: $word"
        done <<< "$misspellings"
    fi
done
