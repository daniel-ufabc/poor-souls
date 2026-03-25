# Migration plan: `_book/` → `book/src/content/`

## Source structure

- `_book/dia00.md` … `dia31.md` — 32 chapter files (Portuguese)
- `_includes/initial-prayer.md` — opening prayer block, included in every chapter
- `_includes/end-prayers.md` — closing prayer list, included in every chapter
- `_prayers/*.md` — individual prayer texts (ladainha, credo, salve rainha, de profundis, oracao_pelas_almas)

Each chapter file contains:
- Jekyll frontmatter (`title`, `display`, `order`)
- Body text in Portuguese
- `## Section headings`
- Occasional `> blockquote` passages
- `**bold**` and `_italic_` inline markup
- `{% include initial-prayer.md %}` and `{% include end-prayers.md %}` Liquid tags

---

## Target structure

```
book/src/content/
  main.tex              ← already exists; wire up all \inputs
  chapters/
    dia00.tex … dia31.tex
  prayers/
    initial-prayer.tex  ← frontmatter chapter
    ladainha.tex
    credo.tex
    salve-rainha.tex
    de-profundis.tex
    oracao-pelas-almas.tex
```

---

## Conversion rules

| Markdown / Jekyll | LaTeX |
|---|---|
| frontmatter `title:` | `\chapter{title}` |
| `## Heading` | `\section*{heading}` (unnumbered, consistent with devotional style) |
| `**text**` | `\textbf{text}` |
| `_text_` | `\textit{text}` |
| `> paragraph` | `\begin{quote}paragraph\end{quote}` |
| `- item` list | `\begin{itemize}\item …\end{itemize}` |
| `{% include initial-prayer.md %}` | `\input{prayers/initial-prayer}` |
| `{% include end-prayers.md %}` | reference to the prayers chapter at the back |
| Jekyll links `{% link _prayers/xxx.md %}` | plain text prayer name only (links meaningless in print) |
| `&mdash;` HTML entity | `---` (em-dash) |
| trailing `  ` (line break) | `\\` |
| blank line | blank line (paragraph break, same as LaTeX) |

---

## Steps

0. **Write `convert.py`**
   A single script that converts any markdown file to a `.tex` file.
   - Accepts input path, output path, and a `--wrapper` flag: `chapter` (default) or `section`
   - Strips Jekyll frontmatter; uses `title:` value as the wrapper heading
   - Applies all conversion rules in the table above
   - `--wrapper chapter` → `\chapter{title}\n<body>`
   - `--wrapper section` → `\section*{title}\n<body>`

   Run it for every source file:
   ```
   convert.py _includes/initial-prayer.md  prayers/initial-prayer.tex  --wrapper chapter
   convert.py _prayers/ladainha.md          prayers/ladainha.tex         --wrapper section
   convert.py _prayers/credo.md             prayers/credo.tex            --wrapper section
   convert.py _prayers/salve_rainha.md      prayers/salve-rainha.tex     --wrapper section
   convert.py _prayers/de_profundis.md      prayers/de-profundis.tex     --wrapper section
   convert.py _prayers/oracao_pelas_almas.md prayers/oracao-pelas-almas.tex --wrapper section
   convert.py _book/dia00.md               chapters/dia00.tex           --wrapper chapter
   …
   convert.py _book/dia31.md               chapters/dia31.tex           --wrapper chapter
   ```

1. **Run `convert.py`** for all source files as above.

2. **Update `main.tex`**
   ```latex
   \frontmatter
   % title page, TOC
   \input{prayers/initial-prayer}   % opening prayer as its own chapter

   \mainmatter
   \input{chapters/dia00}
   …
   \input{chapters/dia31}

   \backmatter
   \chapter{Orações}
   \input{prayers/ladainha}
   \input{prayers/credo}
   \input{prayers/salve-rainha}
   \input{prayers/de-profundis}
   \input{prayers/oracao-pelas-almas}
   ```

5. **Test compilation**
   Run `pdflatex` three times and fix any encoding or formatting issues.

---

## Notes

- `dia00.md` is the introduction/prologue — maps to a `\chapter{}` in `\mainmatter` as the first chapter.
- The `end-prayers.md` include contains a list of prayers with Jekyll links. In the chapter files, replace the whole Liquid block with a short sentence like: *"Em seguida, rezar as orações do final deste livro."* The full texts are in the prayers chapter at the back.
- Special characters (`ã`, `ç`, `â`, etc.) are handled correctly by `inputenc utf8` already in `main.tex`.
