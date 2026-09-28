#!/usr/bin/env python3
"""Render a Badlands NDA from a template plus a JSON parameter file.

Writes a filled Markdown copy and a signature-ready .docx next to the
parameter file, then opens the .docx in Word. Anything still wrapped in
[[double brackets]] is an open item: it is highlighted yellow in the .docx
and listed on stdout.

    python3 legal/scripts/build_nda.py legal/nda/ameritech-systems-corp.json
    python3 legal/scripts/build_nda.py <params.json> --no-open

Opening is the default so the draft lands in front of you for review. It is
skipped automatically when there is no desktop to open it on — a cloud
Claude Code session, CI, an ssh shell — and the script says so rather than
failing.
"""

import json
import os
import platform
import re
import subprocess
import sys
from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_COLOR_INDEX

REPO = Path(__file__).resolve().parents[2]
TEMPLATE = REPO / "legal" / "templates" / "mutual-nda.md"
OPEN_ITEM = re.compile(r"\[\[(.+?)\]\]")
BOLD = re.compile(r"\*\*(.+?)\*\*")


def fill(template_text, params):
    out = template_text
    for key, value in params.items():
        out = out.replace("{{%s}}" % key, str(value))
    left = re.findall(r"\{\{(\w+)\}\}", out)
    if left:
        sys.exit("Unfilled tokens in template: %s" % ", ".join(sorted(set(left))))
    return out


def add_runs(paragraph, text, base_size=10.5):
    """Write text into a paragraph, honouring **bold** and [[open items]]."""
    for chunk in re.split(r"(\*\*.+?\*\*|\[\[.+?\]\])", text):
        if not chunk:
            continue
        if chunk.startswith("**") and chunk.endswith("**"):
            run = paragraph.add_run(chunk[2:-2])
            run.bold = True
        elif chunk.startswith("[[") and chunk.endswith("]]"):
            run = paragraph.add_run(chunk[2:-2])
            run.bold = True
            run.font.highlight_color = WD_COLOR_INDEX.YELLOW
            run.font.color.rgb = RGBColor(0x00, 0x00, 0x00)
        else:
            run = paragraph.add_run(chunk)
        run.font.size = Pt(base_size)
    return paragraph


def signature_block(doc, params):
    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    blocks = [
        (
            "BADLANDS",
            params["BADLANDS_ENTITY"],
            params["BADLANDS_SIGNATORY"],
            params["BADLANDS_SIGNATORY_TITLE"],
        ),
        (
            "COMPANY",
            params["COMPANY_ENTITY"],
            params["COMPANY_SIGNATORY"],
            params["COMPANY_SIGNATORY_TITLE"],
        ),
    ]
    for cell, (label, entity, name, title) in zip(table.rows[0].cells, blocks):
        cell.width = Inches(3.2)
        first = cell.paragraphs[0]
        add_runs(first, entity, base_size=10.5)
        for run in first.runs:
            run.bold = True
        for line in ("", "By: ______________________________", "", "Name: %s" % name,
                     "Title: %s" % title, "Date: ______________________________"):
            add_runs(cell.add_paragraph(), line, base_size=10.5)
    for row in table.rows:
        for cell in row.cells:
            for para in cell.paragraphs:
                para.paragraph_format.space_after = Pt(2)
    return table


def notices_block(doc, params):
    para = doc.add_paragraph()
    add_runs(para, "**Notice addresses.**", base_size=10.5)
    for label, entity, addr, email in (
        ("Badlands", params["BADLANDS_ENTITY"], params["BADLANDS_ADDRESS"], params["BADLANDS_EMAIL"]),
        ("Company", params["COMPANY_ENTITY"], params["COMPANY_ADDRESS"], params["COMPANY_EMAIL"]),
    ):
        block = doc.add_paragraph()
        block.paragraph_format.space_after = Pt(6)
        add_runs(block, "%s: %s, %s. Email: %s" % (label, entity, addr, email), base_size=10.5)


def build_docx(text, params, out_path):
    doc = Document()
    style = doc.styles["Normal"]
    style.font.name = "Calibri"
    style.font.size = Pt(10.5)
    for section in doc.sections:
        section.top_margin = section.bottom_margin = Inches(0.9)
        section.left_margin = section.right_margin = Inches(1.0)

    for raw in text.split("\n\n"):
        line = raw.strip()
        if not line:
            continue
        if line == "---SIGNATURES---":
            signature_block(doc, params)
            doc.add_paragraph()
            notices_block(doc, params)
            continue
        if line.startswith("# "):
            para = doc.add_paragraph()
            para.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = para.add_run(line[2:].strip())
            run.bold = True
            run.font.size = Pt(13)
            para.paragraph_format.space_after = Pt(12)
            continue
        if line.startswith("## "):
            para = doc.add_paragraph()
            para.paragraph_format.space_before = Pt(10)
            para.paragraph_format.space_after = Pt(4)
            run = para.add_run(line[3:].strip())
            run.bold = True
            run.font.size = Pt(11)
            continue
        para = doc.add_paragraph()
        para.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        para.paragraph_format.space_after = Pt(6)
        add_runs(para, line)

    doc.save(out_path)


def open_in_word(path):
    """Open the .docx in Word. Returns a note describing what happened."""
    system = platform.system()

    if system == "Darwin":
        for argv in (["open", "-a", "Microsoft Word", str(path)], ["open", str(path)]):
            if subprocess.run(argv, capture_output=True).returncode == 0:
                return "opened in %s" % ("Word" if "Microsoft Word" in argv else "the default handler")
        return "could not open it — do it by hand"

    if system == "Windows":
        try:
            os.startfile(str(path))  # noqa: S606 - Windows-only, opens the default handler
            return "opened in Word"
        except OSError as exc:
            return "could not open it (%s) — do it by hand" % exc

    if not (os.environ.get("DISPLAY") or os.environ.get("WAYLAND_DISPLAY")):
        return "no desktop session here, so nothing was opened — the file is listed above"
    if subprocess.run(["xdg-open", str(path)], capture_output=True).returncode == 0:
        return "handed to the desktop's default handler"
    return "could not open it — do it by hand"


def main():
    argv = [a for a in sys.argv[1:] if a != "--no-open"]
    auto_open = "--no-open" not in sys.argv
    if len(argv) != 1:
        sys.exit(__doc__)
    params_path = Path(argv[0]).resolve()
    params = json.loads(params_path.read_text())
    slug = params.get("slug") or params_path.stem

    text = fill(TEMPLATE.read_text(), params)
    md_path = params_path.with_name("%s.md" % slug)
    docx_path = params_path.with_name("%s.docx" % slug)
    md_path.write_text(text)
    build_docx(text, params, docx_path)

    print("wrote %s" % md_path.relative_to(REPO))
    print("wrote %s" % docx_path.relative_to(REPO))
    scanned = list(OPEN_ITEM.findall(text))
    for value in params.values():
        scanned.extend(OPEN_ITEM.findall(str(value)))
    open_items = sorted(set(scanned))
    if open_items:
        print("\n%d open item(s) highlighted in the .docx:" % len(open_items))
        for item in open_items:
            print("  - %s" % item)

    if auto_open:
        print("\nWord: %s" % open_in_word(docx_path))


if __name__ == "__main__":
    main()
