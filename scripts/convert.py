#!/usr/bin/env python3
"""
convert.py — Convert a Jekyll/Markdown file to a LaTeX fragment.

Usage:
    python3 convert.py INPUT OUTPUT [--wrapper {chapter,section}] [--title TITLE]

The --wrapper flag controls how the title from the YAML frontmatter is wrapped:
    chapter  (default)  →  \\chapter{title}
    section              →  \\section*{title}

Use --title to override the title extracted from frontmatter (useful for files
that have no frontmatter, like _includes/initial-prayer.md).

Examples:
    python3 convert.py _includes/initial-prayer.md  prayers/initial-prayer.tex
    python3 convert.py _prayers/ladainha.md          prayers/ladainha.tex  --wrapper section
    python3 convert.py _book/dia00.md               chapters/dia00.tex
"""

import argparse
import re
import sys
from pathlib import Path


# Current file being processed — used for warnings
_current_file = ""


# ---------------------------------------------------------------------------
# Frontmatter
# ---------------------------------------------------------------------------

def strip_frontmatter(text):
    """Remove YAML frontmatter block; return (title, display, short, body)."""
    title = ""
    display = ""
    short = ""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            for line in text[3:end].splitlines():
                m = re.match(r'^title:\s*(.+)$', line)
                if m:
                    title = m.group(1).strip().strip("\"'")
                m = re.match(r'^display:\s*(.+)$', line)
                if m:
                    display = m.group(1).strip().strip("\"'")
                m = re.match(r'^short:\s*(.+)$', line)
                if m:
                    short = m.group(1).strip().strip("\"'")
            text = text[end + 4:]
    return title, display, short, text.lstrip("\n")


# ---------------------------------------------------------------------------
# Liquid / Jekyll
# ---------------------------------------------------------------------------

# Matches the two-line pattern:
#   {% capture NAME %}{% include FILE %}{% endcapture %}
#   {{ NAME | markdownify }}
_LIQUID_INCLUDE = re.compile(
    r'\{%\s*capture\s+\w+\s*%\}\s*\{%\s*include\s+(?P<file>[^\s%]+)\s*%\}\s*\{%\s*endcapture\s*%\}\s*\n\s*\{\{[^}]*\}\}'
)

_INCLUDE_MAP = {
    # The initial prayer is its own frontmatter chapter; drop the per-chapter inclusion.
    "initial-prayer.md": "",
    # Replace the closing prayer list with a short forward reference.
    "end-prayers.md":    """
\\begin{center}
\\textit{Requiescant in pace!}
\\end{center}

Rezai agora uma dezena do terço e as orações no final deste livro.""",
}

def replace_liquid_includes(text):
    def _sub(m):
        fname = m.group("file")
        return _INCLUDE_MAP.get(fname, "")
    text = _LIQUID_INCLUDE.sub(_sub, text)
    # Strip any remaining Liquid tags
    text = re.sub(r'\{%[^%]*%\}', '', text)
    text = re.sub(r'\{\{[^}]*\}\}', '', text)
    return text


# ---------------------------------------------------------------------------
# HTML
# ---------------------------------------------------------------------------

def convert_html(text):
    # <p style="...center...italic...">content</p>  →  \begin{center}\textit{content}\end{center}
    def _styled_p(m):
        style, content = m.group(1), m.group(2).strip()
        if "text-align: center" in style and "font-style: italic" in style:
            return f"\\begin{{center}}\\textit{{{content}}}\\end{{center}}"
        if "text-align: center" in style:
            return f"\\begin{{center}}{content}\\end{{center}}"
        return content

    text = re.sub(r'<p\s+style="([^"]*)">(.*?)</p>', _styled_p, text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', '', text)  # strip remaining tags
    return text


# ---------------------------------------------------------------------------
# Inline conversion (applied to a string, possibly multi-line for blockquotes)
# ---------------------------------------------------------------------------

def convert_inline(s):
    # HTML entities
    s = s.replace("&mdash;", "---")
    s = s.replace("&ndash;", "--")
    s = s.replace("&amp;", r"\&")

    # Markdown links [text](...) → text
    s = re.sub(r'\[([^\]]+)\]\([^)]*\)', r'\1', s)

    # Bold (**text**) before italic to avoid conflicts
    s = re.sub(r'\*\*(.+?)\*\*', r'\\textbf{\1}', s, flags=re.DOTALL)

    # Italic (_text_) — word-boundary aware so it doesn't fire on lone underscores
    s = re.sub(r'(?<!\w)_(.+?)_(?!\w)', r'\\textit{\1}', s, flags=re.DOTALL)

    # Escape any remaining bare _ (unmatched italic markers in the source)
    def _warn_and_escape(m):
        start = max(0, m.start() - 30)
        snippet = s[start:m.start() + 31].replace('\n', ' ')
        print(f"WARNING: {_current_file}: unclosed _ near: ...{snippet}...", file=sys.stderr)
        return r"\_"
    s = re.sub(r'(?<!\\)_', _warn_and_escape, s)

    return s


def convert_inline_line(line):
    """Inline conversion for a single line, also handling trailing line-break."""
    line = convert_inline(line)
    # Trailing double space → LaTeX forced line break
    if line.endswith("  "):
        line = line.rstrip() + r" \\"
    return line


# ---------------------------------------------------------------------------
# Block-level processing
# ---------------------------------------------------------------------------

def convert_footnotes(text):
    """Collect [^N]: definition lines, inline them as \\footnote{} at each [^N] reference."""
    # Collect definitions: [^label]: body text
    defs = {}
    def _collect(m):
        defs[m.group(1)] = m.group(2).strip()
        return ""
    text = re.sub(r'^\[\^([^\]]+)\]:\s*(.+)$', _collect, text, flags=re.MULTILINE)

    # Replace inline references [^label] with \footnote{body}
    def _inline(m):
        label = m.group(1)
        body = convert_inline(defs.get(label, ""))
        return f"\\footnote{{{body}}}"
    text = re.sub(r'\[\^([^\]]+)\]', _inline, text)

    return text


def process_body(text):
    text = replace_liquid_includes(text)
    text = convert_footnotes(text)
    text = convert_html(text)

    lines = text.splitlines()
    out = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # -- Section heading (## ...) ----------------------------------------
        m = re.match(r'^##\s+(.+)$', line)
        if m:
            out.append(f"\\section*{{{convert_inline(m.group(1))}}}")
            i += 1
            continue

        # -- Blockquote ---------------------------------------------------------
        # First line starts with '> '; continuation lines are non-empty lines
        # that follow immediately (lazy blockquote, common in kramdown/Jekyll).
        # All quotes are rendered italic. If the source lacks the outer _..._
        # wrapping, a warning is emitted.
        if line.startswith('> '):
            block_lines = [line[2:]]
            i += 1
            while i < len(lines) and lines[i].strip() != '':
                if lines[i].startswith('> '):
                    block_lines.append(lines[i][2:])
                else:
                    block_lines.append(lines[i])
                i += 1
            # Strip each line before joining to remove trailing whitespace
            # that would otherwise break italic detection.
            block_text = ' '.join(b.strip() for b in block_lines).strip()

            # Warn if the source has no italic markers at all.
            if '_' not in block_text:
                print(f"WARNING: {_current_file}: blockquote not in italic: "
                      f"...{block_text[:60]}...", file=sys.stderr)

            # Let convert_inline handle all _..._ markers (single span, multiple
            # spans, etc.), then wrap the whole block in \textit{} for consistency.
            out.append('\\begin{quote}')
            out.append(f'\\textit{{{convert_inline(block_text)}}}')
            out.append('\\end{quote}')
            continue

        # -- Itemize block ------------------------------------------------------
        if line.startswith('- '):
            out.append('\\begin{itemize}')
            while i < len(lines) and lines[i].startswith('- '):
                out.append(f"  \\item {convert_inline_line(lines[i][2:])}")
                i += 1
            out.append('\\end{itemize}')
            continue

        # -- Horizontal rule (--- / *** / ___) — discard ----------------------
        if re.match(r'^(\-{3,}|\*{3,}|_{3,})\s*$', line):
            i += 1
            continue

        # -- "Oremos." paragraph — vertical space + no indent ------------------
        if line.strip().startswith('**Oremos.**'):
            out.append(r'\vspace{\baselineskip}\noindent ' + convert_inline_line(line.strip()))
            i += 1
            continue

        # -- Normal line --------------------------------------------------------
        out.append(convert_inline_line(line))
        i += 1

    return '\n'.join(out)


# ---------------------------------------------------------------------------
# Title helpers
# ---------------------------------------------------------------------------

def sanitise_title(title):
    """Apply inline conversions to a frontmatter title (HTML entities, etc.)."""
    title = title.replace("&mdash;", "---")
    title = title.replace("&ndash;", "--")
    title = title.replace("&amp;", r"\&")
    return title


def make_heading(title, display, short, wrapper):
    if not title:
        return ""
    if wrapper == "chapter":
        if "---" in title:
            # Split "Display --- Subtitle" into separate identifier and title.
            # display field   → \thechapterdisplay (replaces "Capítulo N")
            # part after ---  → \chapter argument and running header
            # full title      → TOC entry
            parts = title.split("---", 1)
            subtitle = parts[1].strip()
            label = display if display else parts[0].strip()
            runner = short if short else subtitle
            return (
                f"\\renewcommand{{\\thechapterdisplay}}{{{label}}}\n"
                f"\\renewcommand{{\\thechapterrunner}}{{{runner}}}\n"
                f"\\chapter[{title}]{{{subtitle}}}\n"
            )
        else:
            runner = short if short else title
            return (
                f"\\renewcommand{{\\thechapterdisplay}}{{}}\n"
                f"\\renewcommand{{\\thechapterrunner}}{{{runner}}}\n"
                f"\\chapter{{{title}}}\n"
            )
    return f"\\section*{{{title}}}\n"


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def convert(input_path, output_path, wrapper, title_override):
    global _current_file
    _current_file = input_path
    text = Path(input_path).read_text(encoding="utf-8")
    fm_title, fm_display, fm_short, body = strip_frontmatter(text)

    title = sanitise_title(title_override if title_override else fm_title)
    display = sanitise_title(fm_display)
    short = sanitise_title(fm_short)
    body = process_body(body)

    output = make_heading(title, display, short, wrapper) + body.strip() + "\n"

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(output, encoding="utf-8")
    print(f"  {input_path}  →  {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Convert a Jekyll/Markdown file to a LaTeX fragment."
    )
    parser.add_argument("input",  help="Input .md file")
    parser.add_argument("output", help="Output .tex file")
    parser.add_argument(
        "--wrapper",
        choices=["chapter", "section"],
        default="chapter",
        help="LaTeX heading wrapper for the title (default: chapter)",
    )
    parser.add_argument(
        "--title",
        default="",
        help="Override the title from frontmatter",
    )
    args = parser.parse_args()
    convert(args.input, args.output, args.wrapper, args.title)


if __name__ == "__main__":
    main()
