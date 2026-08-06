#!/usr/bin/env python3
"""Baixa 5 candidatas por receita para curadoria."""

import urllib.request
from pathlib import Path

from ddgs import DDGS

RECIPES = [
    ("pate-de-figado-de-galinha", "patê de fígado de galinha"),
    ("torta-de-frango", "torta de frango purê batata"),
    ("enroladinhos-meireles", "enroladinhos de frango assado"),
    ("enrolados-de-frango", "enrolados de frango arroz"),
    ("files-de-frango-recheados", "filé de frango recheado bacon"),
    ("frango-assado-com-cerveja", "frango assado com cerveja"),
    ("frango-na-pucara", "frango na púcara português"),
    ("frango-ao-caril", "frango ao caril"),
    ("frango-estufado-com-tomates", "frango estufado tomate"),
    ("peru-recheado-com-risoto", "peru recheado risoto natal"),
    ("bolacha-de-nescau", "bolacha de nescau"),
]

OUT = Path("/tmp/curate")


def download(url: str, dest: Path) -> bool:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = resp.read()
        if len(data) < 5000:
            return False
        dest.write_bytes(data)
        return True
    except Exception as e:
        print("  fail", dest.name, e)
        return False


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with DDGS() as ddg:
        for slug, query in RECIPES:
            print(f"\n=== {slug} ({query}) ===")
            seen = set()
            idx = 0
            for r in ddg.images(query, max_results=12):
                url = r.get("image", "")
                if not url or url in seen:
                    continue
                seen.add(url)
                dest = OUT / f"{slug}-{idx}.jpg"
                if download(url, dest):
                    print(f"  {idx}: {url[:80]}...")
                    idx += 1
                if idx >= 5:
                    break


if __name__ == "__main__":
    main()
