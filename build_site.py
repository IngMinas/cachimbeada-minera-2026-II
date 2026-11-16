# -*- coding: utf-8 -*-
# Envuelve el fragmento index.html (pensado para el Artifact de Claude,
# que agrega su propio <!doctype>/<head> automaticamente) en un documento
# HTML5 completo y valido, para publicarlo tal cual en GitHub Pages.
import re

SRC = "fragment.html"
OUT = "dist/index.html"
PUBLISH_COPY = "index.html"  # copia servida por GitHub Pages desde la raiz del repo

with open(SRC, "r", encoding="utf-8") as f:
    fragment = f.read()

title_match = re.search(r"<title>.*?</title>", fragment, re.S)
title_tag = title_match.group(0) if title_match else "<title>Cachimbeada Minera</title>"

# Todo lo que precede al primer <header> es material de <head>
# (title, meta propio de Claude, <style>, <link> de Google Fonts).
split_idx = fragment.index("<header")
head_extra = fragment[:split_idx]
body_content = fragment[split_idx:]

# Quita el <title> original de head_extra para no duplicarlo.
head_extra = head_extra.replace(title_tag, "", 1)

html = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
{title_tag}
{head_extra}
</head>
<body>
{body_content}
</body>
</html>
"""

import os
os.makedirs("dist", exist_ok=True)
with open(OUT, "w", encoding="utf-8") as f:
    f.write(html)
with open(PUBLISH_COPY, "w", encoding="utf-8") as f:
    f.write(html)
print("Generado", OUT, "y", PUBLISH_COPY, "(", len(html), "caracteres )")
