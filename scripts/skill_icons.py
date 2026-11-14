"""Build combined skill-icon SVGs from LelouchFR/skill-icons assets.

Usage: python3 scripts/skill_icons.py   # rerun after editing SETS
"""

import math
import urllib.request
from pathlib import Path

BASE = "https://raw.githubusercontent.com/LelouchFR/skill-icons/main/assets"
SETS = {
    "profile/skills.svg": "python,r,rust,nextflow,bash,linux,anaconda,typst,latex",
    "profile/webdev-skills.svg": "litestar,fastapi,typescript,vuejs,nuxtjs,postgresql,docker,podman",
}
PER_LINE, SCALE = 15, 48 / (300 - 44)  # same layout as the original API


def fetch(name: str) -> str:
    # themed icons ship as <name>-auto.svg, the rest as plain <name>.svg
    for file in (f"{name}-auto.svg", f"{name}.svg"):
        try:
            return urllib.request.urlopen(f"{BASE}/{file}").read().decode()
        except urllib.error.HTTPError:
            pass
    raise SystemExit(f"icon not found: {name}")


def combine(icons: list[str]) -> str:
    w = min(PER_LINE, len(icons)) * 300 - 44
    h = math.ceil(len(icons) / PER_LINE) * 300 - 44
    body = "".join(
        f'<g transform="translate({i % PER_LINE * 300}, {i // PER_LINE * 300})">{svg}</g>'
        for i, svg in enumerate(icons)
    )
    return (
        f'<svg width="{int(w * SCALE)}" height="{int(h * SCALE)}" viewBox="0 0 {w} {h}" fill="none" '
        f'xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1">'
        f"{body}</svg>\n"
    )


for out, names in SETS.items():
    Path(out).write_text(combine([fetch(n) for n in names.split(",")]))
    print("wrote", out)
