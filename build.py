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

# añade un botón Waze junto a cada enlace de Google Maps, con el mismo destino
def waze(m):
    q = m.group(2)
    return (
        f'{m.group(1)}<a class="wz" href="https://waze.com/ul?q={q}&amp;navigate=yes"'
        f' target="_blank" rel="noopener" title="Abrir en Waze">Waze</a>'
    )

html = re.sub(
    r'(<a[^>]+href="https://www\.google\.com/maps/search/\?api=1&amp;query=([^"]+)"[^>]*>[^<]*</a>)',
    waze,
    html,
)

with open("index.html", "w") as f:
    f.write(html)

n = html.count('class="ph"')
w = html.count('class="wz"')
print(f"index.html generado con {n} fotos y {w} enlaces Waze")
