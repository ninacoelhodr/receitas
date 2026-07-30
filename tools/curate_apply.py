#!/usr/bin/env python3
"""Apply curated dish-photo decision for a slug."""
from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def find_html(slug: str) -> Path | None:
    matches = list((ROOT / "receitas").rglob(f"{slug}.html"))
    return matches[0] if matches else None


def ensure_dish_photo(html_path: Path, slug: str, alt_name: str) -> bool:
    html = html_path.read_text(encoding="utf-8")
    block = (
        f'<figure class="dish-photo no-print">\n'
        f'  <img src="../../imagens/{slug}.jpg" alt="Referência: {alt_name}" />\n'
        f'  <figcaption>Referência visual (não é a foto da receita da família).</figcaption>\n'
        f"</figure>\n"
    )
    if "dish-photo" in html:
        html2 = re.sub(
            r'<figure class="dish-photo no-print">.*?</figure>\s*',
            block,
            html,
            count=1,
            flags=re.S,
        )
        if html2 != html:
            html_path.write_text(html2, encoding="utf-8")
            return True
        return False
    m = re.search(r"(</h1>\s*)", html)
    if m:
        html = html[: m.end()] + "\n" + block + html[m.end() :]
    else:
        m2 = re.search(r"(<article class=\"recipe-card\">\s*)", html)
        if not m2:
            print("could not insert dish-photo", html_path, file=sys.stderr)
            return False
        # after h1 is preferred; try insert before ingredients
        m3 = re.search(r"(<h2>Ingredientes</h2>)", html)
        if m3:
            html = html[: m3.start()] + block + "\n" + html[m3.start() :]
        else:
            html = html[: m2.end()] + block + html[m2.end() :]
    html_path.write_text(html, encoding="utf-8")
    return True


def remove_dish_photo(html_path: Path) -> bool:
    html = html_path.read_text(encoding="utf-8")
    html2 = re.sub(
        r'<figure class="dish-photo no-print">.*?</figure>\s*',
        "",
        html,
        count=1,
        flags=re.S,
    )
    if html2 == html:
        return False
    html_path.write_text(html2, encoding="utf-8")
    return True


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--slug", required=True)
    ap.add_argument("--pick", type=int, help="candidate number 1-5")
    ap.add_argument("--remove", action="store_true")
    ap.add_argument("--title", default="")
    args = ap.parse_args()

    slug = args.slug
    html_path = find_html(slug)
    if not html_path:
        print(f"HTML not found for {slug}", file=sys.stderr)
        sys.exit(1)

    img_path = ROOT / "imagens" / f"{slug}.jpg"
    title = args.title
    if not title:
        html = html_path.read_text(encoding="utf-8")
        m = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
        title = re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else slug

    if args.remove:
        changed = remove_dish_photo(html_path)
        if img_path.exists():
            img_path.unlink()
            print(f"deleted {img_path.name}")
        print(f"removed dish-photo for {slug}" if changed else f"no dish-photo block in {slug}")
        return

    if not args.pick:
        print("need --pick N or --remove", file=sys.stderr)
        sys.exit(1)

    cand = ROOT / "imagens" / "_cands" / slug / f"{args.pick}.jpg"
    if not cand.exists():
        print(f"missing candidate {cand}", file=sys.stderr)
        sys.exit(1)
    shutil.copyfile(cand, img_path)
    ensure_dish_photo(html_path, slug, title)
    print(f"kept/replaced {slug} with candidate {args.pick}")


if __name__ == "__main__":
    main()
