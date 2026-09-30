#!/usr/bin/env python3
"""Assemble Systole.

src/app.html holds the whole app (styles, markup, scripts) with two placeholders:
__DATA__ for the course content and __PARTS__ for the names of the 3D parts.

Outputs:
  index.html          a complete page, ready for any static host (GitHub Pages, Vercel, ...)
  dist/artifact.html  the same app without <html>/<head>, for a Claude artifact

Run from anywhere:  python3 tools/build.py
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = ROOT / "src"


def inline(name):
    """JSON file -> compact JSON that is safe inside a <script> tag."""
    data = json.loads((SRC / name).read_text(encoding="utf-8"))
    return json.dumps(data, ensure_ascii=False).replace("</", "<\\/")


FAVICON = (
    "data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E"
    "%3Cpath d='M12 21C5 16.5 2 12.8 2 8.9 2 6 4.2 3.8 7 3.8c1.9 0 3.7 1 5 2.7 1.3-1.7 3.1-2.7 5-2.7 2.8 0 5 2.2 5 5.1 0 3.9-3 7.6-10 12.1z' fill='%23FF4760'/%3E"
    "%3Cpath d='M4.5 11h3.2l1.4-2.6 2.2 5.4 1.7-3.6 1 .8h5.5' stroke='%23fff' stroke-width='1.9' fill='none' stroke-linecap='round' stroke-linejoin='round'/%3E"
    "%3C/svg%3E"
)

# What the Claude artifact host adds around the page, reproduced for standalone hosting.
HEAD = f"""<!doctype html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="Systole : 5 minutes par jour pour arriver en études de santé avec une longueur d'avance.">
<meta name="theme-color" content="#FFFFFF" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#131722" media="(prefers-color-scheme: dark)">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Systole">
<link rel="icon" href="{FAVICON}">
<style>:root{{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}}body{{margin:0}}img{{max-width:100%}}</style>
"""


def main():
    app = (SRC / "app.html").read_text(encoding="utf-8")
    app = app.replace("__DATA__", inline("programme.json")).replace("__PARTS__", inline("parts.json"))
    assert "__DATA__" not in app and "__PARTS__" not in app

    # Everything up to the end of the stylesheet belongs in <head>; the rest is the body.
    cut = app.index("</style>") + len("</style>")
    page = HEAD + app[:cut] + "\n</head>\n<body>\n" + app[cut:].strip("\n") + "\n</body>\n</html>\n"

    (ROOT / "index.html").write_text(page, encoding="utf-8")
    (ROOT / "dist").mkdir(exist_ok=True)
    (ROOT / "dist" / "artifact.html").write_text(app, encoding="utf-8")
    print(f"index.html          {len(page.encode('utf-8')) // 1024} Ko")
    print(f"dist/artifact.html  {len(app.encode('utf-8')) // 1024} Ko")


if __name__ == "__main__":
    main()
