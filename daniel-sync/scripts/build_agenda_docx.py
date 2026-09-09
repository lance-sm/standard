#!/usr/bin/env python3
"""Build the weekly Daniel-sync agenda .docx.

Copies the template package byte-for-byte and swaps only the body paragraphs,
so Aptos font, the ListParagraph numbering and the sectPr survive exactly.

Usage:
    python3 build_agenda_docx.py <items.json> <output.docx> [template.docx]

items.json is a list of [level, text] pairs; level 0 = top-level, 1 = sub-item.
    [[0, "CF, Webster, Hiring, other BL updates"], [1, "Colin onboarding"]]

Verified against "August 26 Agenda.docx": reproduces the template's own
paragraphs exactly when fed the template's own text.
"""
import json
import os
import shutil
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TPL = os.path.join(HERE, os.pardir, "templates", "agenda-template.docx")

# Run properties lifted verbatim from the template.
RF = (
    '<w:rFonts w:ascii="Aptos" w:eastAsia="Aptos" w:hAnsi="Aptos" w:cs="Aptos"/>'
    '<w:color w:val="000000" w:themeColor="text1"/>'
)

PARA = (
    "<w:p><w:pPr><w:pStyle w:val=\"ListParagraph\"/>"
    '<w:numPr><w:ilvl w:val="{level}"/><w:numId w:val="1"/></w:numPr>'
    '<w:shd w:val="clear" w:color="auto" w:fill="FFFFFF" w:themeFill="background1"/>'
    '<w:spacing w:after="0" w:line="279" w:lineRule="auto"/>'
    "<w:rPr>{rf}</w:rPr></w:pPr>"
    "<w:r><w:rPr>{rf}</w:rPr>"
    '<w:t xml:space="preserve">{text}</w:t></w:r></w:p>'
)

# The template's trailing empty paragraph; everything from here on (it plus the
# sectPr) is kept so page setup is untouched.
TAIL_ANCHOR = '<w:p w14:paraId="45034E33"'


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def build(items, out_path, tpl_path):
    work = out_path + ".work"
    if os.path.exists(work):
        shutil.rmtree(work)
    os.makedirs(work)

    with zipfile.ZipFile(tpl_path) as z:
        names = z.namelist()          # preserve entry order on rezip
        z.extractall(work)

    doc = os.path.join(work, "word", "document.xml")
    with open(doc, encoding="utf-8") as fh:
        xml = fh.read()

    head, body = xml.split("<w:body>")
    idx = body.find(TAIL_ANCHOR)
    if idx < 0:
        raise SystemExit(
            "FATAL: anchor paragraph %s not found in template %s - the template "
            "changed. Stop and report rather than emitting a mis-styled file."
            % (TAIL_ANCHOR, tpl_path)
        )
    tail = body[idx:]

    paras = "".join(
        PARA.format(level=int(lvl), rf=RF, text=esc(text)) for lvl, text in items
    )

    with open(doc, "w", encoding="utf-8") as fh:
        fh.write(head + "<w:body>" + paras + tail)

    if os.path.exists(out_path):
        os.remove(out_path)
    with zipfile.ZipFile(out_path, "w", zipfile.ZIP_DEFLATED) as z:
        for name in names:
            z.write(os.path.join(work, name), name)

    shutil.rmtree(work)
    return out_path


def main():
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    items = json.load(open(sys.argv[1], encoding="utf-8"))
    out_path = sys.argv[2]
    tpl_path = sys.argv[3] if len(sys.argv) > 3 else DEFAULT_TPL
    if not os.path.exists(tpl_path):
        raise SystemExit(
            "FATAL: agenda template missing at %s. Do NOT fabricate a substitute "
            "document - report that the template is absent." % tpl_path
        )
    build(items, out_path, tpl_path)
    print("wrote %s (%d paragraphs)" % (out_path, len(items)))


if __name__ == "__main__":
    main()
