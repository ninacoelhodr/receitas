#!/usr/bin/env python3
"""Insert missing recipe links into index.html subcategory lists."""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

NEW_SLUGS = {
    "pate-de-figado-de-galinha",
    "torta-de-frango",
    "enroladinhos-meireles",
    "enrolados-de-frango",
    "files-de-frango-recheados",
    "frango-assado-com-cerveja",
    "frango-na-pucara",
    "frango-ao-caril",
    "frango-estufado-com-tomates",
    "peru-recheado-com-risoto",
    "bolacha-de-nescau",
    "cheesecake-basco-de-chocolate",
    "bolo-de-chocolate-com-3-ingredientes",
}


def insert_link(index_text: str, cat: str, sub: str | None, slug: str, title: str) -> str:
    href = f"./receitas/{cat}/{slug}.html"
    if href in index_text:
        return index_text
    new_li = f'          <li>\n            <a href="{href}">{html.escape(title)}</a>\n          </li>\n'
    if sub:
        pat = (
            rf'(<ul class="recipe-list" data-subcategory="{re.escape(sub)}">\s*)'
            r"((?:\s*<li>.*?</li>)*)"
            r"(\s*</ul>)"
        )
    else:
        # first ul in category section without data-subcategory or any ul in flat section
        section_m = re.search(
            rf'<section class="category-block" id="{re.escape(cat)}">(.*?)</section>',
            index_text,
            re.S,
        )
        if not section_m:
            raise SystemExit(f"section {cat} not found")
        section = section_m.group(1)
        pat = r"(<ul class=\"recipe-list\">\s*)((?:\s*<li>.*?</li>)*)(\s*</ul>)"
        m = re.search(pat, section, re.S)
        if not m:
            raise SystemExit(f"ul in {cat} not found")
        items = m.group(2) + new_li
        lis = re.findall(r"<li>.*?</li>\s*", items, re.S)
        lis.sort(key=lambda x: re.sub(r"<[^>]+>", "", x).strip().lower())
        new_section = section[: m.start()] + m.group(1) + "".join(lis) + m.group(3) + section[m.end() :]
        return index_text[: section_m.start()] + new_section + index_text[section_m.end() :]

    m = re.search(pat, index_text, re.S)
    if not m:
        raise SystemExit(f"subcategory {cat}/{sub} not found")
    items = m.group(2) + new_li
    lis = re.findall(r"<li>.*?</li>\s*", items, re.S)
    lis.sort(key=lambda x: re.sub(r"<[^>]+>", "", x).strip().lower())
    return index_text[: m.start()] + m.group(1) + "".join(lis) + m.group(3) + index_text[m.end() :]


def main() -> None:
    index_path = ROOT / "index.html"
    text = index_path.read_text(encoding="utf-8")
    count = 0
    for html_file in sorted((ROOT / "receitas").rglob("*.html")):
        if html_file.stem not in NEW_SLUGS:
            continue
        content = html_file.read_text(encoding="utf-8")
        cat = html_file.parent.name
        slug = html_file.stem
        title = re.search(r"<h1>(.*?)</h1>", content).group(1)
        label = re.search(r'<p class="category">(.*?)</p>', content).group(1)
        sub = label.split(" · ", 1)[1] if " · " in label else None
        text = insert_link(text, cat, sub, slug, title)
        count += 1
        print(f"indexed {slug}")
    index_path.write_text(text, encoding="utf-8")
    print(f"done {count}")


if __name__ == "__main__":
    main()
