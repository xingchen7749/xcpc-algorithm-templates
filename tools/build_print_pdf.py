"""Render only the existing Markdown handbook as an A4 print PDF.

Dependencies: pip install typst markdown-it-py
Usage: python tools/build_print_pdf.py
"""
from pathlib import Path
import json
import re
import unicodedata
from markdown_it import MarkdownIt
import typst

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'RBC_XCPC_算法模板' / 'RBC_XCPC_算法模板.md'
OUT = ROOT / 'output' / 'pdf'
MD = MarkdownIt('commonmark').enable('table')


def string(value):
    return json.dumps(value, ensure_ascii=False)


def inline(value, table_cell=False):
    tokens = MD.parseInline(value)[0].children
    if table_cell:
        plain = ''.join(t.content for t in tokens if t.type in ('text', 'code_inline', 'html_inline'))
        chunks, current, width = [], '', 0
        limit = 88 // table_cell
        for c in plain:
            size = 2 if unicodedata.east_asian_width(c) in 'WF' else 1
            if width + size > limit:
                chunks.append(current)
                current, width = '', 0
            current += c
            width += size
        chunks.append(current)
        return '#linebreak()'.join('#text(' + string(chunk) + ')' for chunk in chunks)
    result = []
    links = []
    for token in tokens:
        if token.type in ('text', 'html_inline'):
            result.append('#text(' + string(token.content) + ')')
        elif token.type == 'code_inline':
            result.append('#raw(' + string(token.content) + ')')
        elif token.type == 'strong_open':
            result.append('#strong[')
        elif token.type == 'em_open':
            result.append('#emph[')
        elif token.type in ('strong_close', 'em_close'):
            result.append(']')
        elif token.type == 'link_open':
            links.append(token.attrGet('href'))
        elif token.type == 'link_close':
            target = links.pop()
            if target.startswith('#'):
                result.append('（第 #ref(label(' + string(target[1:]) + '), form: "page", supplement: none) 页）')
            elif target.startswith(('http:', 'https:')):
                result.append('#footnote[' + '#text(' + string(target) + ')]')
        elif token.type in ('softbreak', 'hardbreak'):
            result.append(' ')
        else:
            raise ValueError('Unhandled inline token: ' + token.type)
    return ''.join(result)


def wrap_code(code, limit=94):
    """Visual wrapping only; the Markdown and standalone C++ remain unchanged."""
    output = []
    for line in code.splitlines():
        current = ''
        width = 0
        prefix = ' ' * min(len(line) - len(line.lstrip()), 12) + '↪ '
        for char in line.expandtabs(4):
            size = 2 if unicodedata.east_asian_width(char) in 'WF' else 1
            if width + size > limit:
                output.append(current)
                current, width = prefix, len(prefix)
            current += char
            width += size
        output.append(current)
    return '\n'.join(output)


PREAMBLE = r'''
#set document(title: "RBC_XCPC_算法模板 · 打印版")
#set text(font: ("SimSun", "Consolas"), size: 10pt, lang: "zh", fill: black)
#set par(leading: 0.5em, spacing: 0.65em, justify: false)
#set page(paper: "a4", binding: left,
  margin: (inside: 22mm, outside: 16mm, top: 20mm, bottom: 18mm),
  numbering: "1", number-align: center + bottom,
  header: context {
    set text(size: 8pt, font: "Microsoft YaHei")
    let p = here().page()
    let hs = query(heading.where(outlined: true)).filter(h => h.location().page() <= p)
    let same = hs.filter(h => h.location().page() == p)
    let prior = hs.filter(h => h.location().page() < p)
    if same.len() > 0 and same.first().location().position().y < 85pt { same.first().body }
    else if prior.len() > 0 { prior.last().body; text("（续）") }
    else if same.len() > 0 { same.first().body }
    else { text("RBC_XCPC_算法模板") }
    line(length: 100%, stroke: 0.4pt)
  })
#set heading(numbering: none)
#show heading: set text(font: "Microsoft YaHei", weight: "bold")
#show heading.where(level: 1): set text(size: 17pt)
#show heading.where(level: 2): set text(size: 13pt)
#show heading.where(level: 3): set text(size: 11pt)
#show heading.where(level: 4): set text(size: 10pt)
#show heading: set block(above: 1em, below: 0.6em)
#set raw(theme: none)
#show raw: set text(font: ("Consolas", "SimSun"), size: 9pt)
#show raw.where(block: true): set block(breakable: true, above: 7pt, below: 7pt)
#show raw.where(block: true): set par(leading: 2.4pt)
#show outline.entry: set block(above: 3pt, below: 3pt)
#set table(inset: 5pt, stroke: 0.4pt)
#let codeblock(s) = block(breakable: true, above: 7pt, below: 7pt, {
  for line in s.split("\n") {
    block(height: 12pt, above: 0pt, below: 0pt, breakable: false, raw(if line == "" { " " } else { line }))
  }
})
#align(center)[#text(font: "Microsoft YaHei", size: 23pt, weight: "bold", "RBC_XCPC_算法模板")]
#align(center)[C++17 · 黑白打印版]
#v(8pt)
#text(size: 9pt)[打印说明：A4，双面长边翻转，按实际大小（100%）打印。内侧预留装订边距。目录及依赖引用使用本册页码。代码中的 ↪ 为排版续行标记，不属于代码；续行时仍属于上一条源代码行。]
'''


def build():
    source = SOURCE.read_text(encoding='utf-8')
    # Remove the electronic TOC; Typst derives its replacement from all headings.
    source = re.sub(r'## 目录\n.*?(?=<a id="chapter-1")', 'PRINT_TOC\n\n', source, flags=re.S)
    lines = source.splitlines()
    output = [PREAMBLE]
    index = 0
    anchor = None
    code_count = 0
    headings = []
    while index < len(lines):
        line = lines[index]
        index += 1
        if not line.strip():
            continue
        if line == '# RBC_XCPC_算法模板' or line.startswith('> C++17'):
            continue
        if line.startswith('[完整代码：') or '返回目录' in line:
            continue
        if line == 'PRINT_TOC':
            output.append('#pagebreak()\n#outline(title: [目录], depth: 3, indent: 1em)')
            continue
        match = re.fullmatch(r'<a id="([^"]+)"></a>', line)
        if match:
            anchor = match[1]
            continue
        match = re.match(r'^(#{1,6}) (.*)$', line)
        if match:
            level, title = len(match[1]), match[2]
            outlined = bool(re.match(r'^\d+\.', title))
            if level == 1:
                output.append('#pagebreak()')
            output.append(f'#heading(level: {level}, outlined: {str(outlined).lower()})[' + inline(title) + ']' + (f' <{anchor}>' if anchor else ''))
            if outlined:
                headings.append(title)
            anchor = None
            continue
        if line.startswith('```'):
            code = []
            while index < len(lines) and not lines[index].startswith('```'):
                code.append(lines[index])
                index += 1
            assert index < len(lines), 'Unclosed code fence'
            index += 1
            output.append('#codeblock(' + string(wrap_code('\n'.join(code))) + ')')
            code_count += 1
            continue
        if line.startswith('|'):
            rows = [line]
            while index < len(lines) and lines[index].startswith('|'):
                rows.append(lines[index])
                index += 1
            cells = []
            for token in MD.parse('\n'.join(rows)):
                if token.type == 'tr_open':
                    cells.append([])
                elif token.type == 'inline':
                    cells[-1].append(token.content)
            ncols = len(cells[0])
            assert all(len(row) == ncols for row in cells)
            output.append('#table(columns: (' + ', '.join(['1fr'] * ncols) + '),\ntable.header(' + ','.join('[' + inline(c, ncols) + ']' for c in cells[0]) + '),\n' + ',\n'.join('[' + inline(c, ncols) + ']' for row in cells[1:] for c in row) + ')')
            continue
        if line.startswith('- '):
            output.append('#block(inset: (left: 10pt))[' + '• ' + inline(line[2:]) + ']')
        else:
            output.append(inline(line.removeprefix('> ')))
    OUT.mkdir(parents=True, exist_ok=True)
    typ_path = OUT / 'RBC_XCPC_算法模板_打印版.typ'
    pdf_path = OUT / 'RBC_XCPC_算法模板_打印版.pdf'
    typ_path.write_text('\n\n'.join(output), encoding='utf-8')
    typst.compile(str(typ_path), output=str(pdf_path), font_paths=['C:/Windows/Fonts'])
    assert code_count == len(re.findall(r'^```[^\n]+$', source, re.M))
    print(json.dumps({'pdf': str(pdf_path), 'code_blocks': code_count, 'headings': len(headings)}, ensure_ascii=False))


if __name__ == '__main__':
    build()
