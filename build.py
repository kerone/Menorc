#!/usr/bin/env python3
"""Genera index.html inyectando las galerías de images.json en template.html.

Uso: python3 build.py
Placeholders en template.html: <!--GALLERY:slug--> o <!--GALLERY:slug1+slug2-->
"""
import json
import re

with open("images.json") as f:
    IMAGES = json.load(f)

# fotos que no corresponden al sitio (revisadas a mano)
EXCLUDE = {"Sanitja tower.JPG"}

def gallery(slugs):
    items = []
    for slug in slugs.split("+"):
        for img in IMAGES.get(slug, []):
            if img["title"] in EXCLUDE:
                continue
            items.append(
                f'<a class="ph" href="{img["page"]}" target="_blank" rel="noopener">'
                f'<img src="{img["thumb"]}" alt="{img["title"]}" loading="lazy"></a>'
            )
    if not items:
        return ""
    return '<div class="gallery">' + "\n".join(items) + "</div>"

with open("template.html") as f:
    html = f.read()

html = re.sub(r"<!--GALLERY:([\w+-]+)-->", lambda m: gallery(m.group(1)), html)

with open("index.html", "w") as f:
    f.write(html)

n = html.count('class="ph"')
print(f"index.html generado con {n} fotos")
