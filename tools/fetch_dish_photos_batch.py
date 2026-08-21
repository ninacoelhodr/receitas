#!/usr/bin/env python3
"""Download reference dish photos for recipe slugs via DuckDuckGo Images."""
from __future__ import annotations

import json
import time
import urllib.request
from pathlib import Path

from ddgs import DDGS

ROOT = Path(__file__).resolve().parents[1]
IMG = ROOT / "imagens"
UA = "ReceitasNinaBot/1.0 (personal cookbook)"

SLUGS: dict[str, str] = {
    "pao-de-forma": "pão de forma fatias",
    "pao-integral": "pão integral fatias",
    "paezinhos-rapidos": "pãezinhos assados",
    "pao-sirio": "pão sírio pita",
    "broinhas-de-fuba": "broinha de fubá",
    "muffins": "muffins passas",
    "rosca-de-natal": "rosca de natal doce",
    "bolo-merenda": "bolo simples fatia",
    "bolo-de-especiarias": "bolo de especiarias",
    "bolo-de-mandioca": "bolo de mandioca",
    "bolo-de-chocolate": "bolo de chocolate calda",
    "bolo-de-laranja": "bolo de laranja fubá",
    "bolo-de-abacaxi": "bolo de abacaxi invertido",
    "bolo-de-fuba-e-coco": "bolo de fubá coco",
    "bolo-gelado-de-goiaba": "bolo gelado de goiaba",
    "bolo-de-sorvete-com-cerejas": "bolo de sorvete cerejas",
    "cheesecake-basco-de-chocolate": "cheesecake basco chocolate",
    "biscoitinhos-coloridos": "biscoitos coloridos enrolados",
    "biscoitinhos-de-cerveja": "biscoitos de cerveja",
    "biscoitinhos-de-ameixa-preta": "biscoitos ameixa seca",
    "biscoitinhos-de-chocolate-e-coco": "biscoitos chocolate coco",
    "biscoitinhos-de-caramelo": "biscoitos caramelo",
    "esquecidos": "biscoitos esquecidos",
    "casadinhos-recheados": "casadinhos doce de leite",
    "sequilhos-de-coco": "sequilhos de coco",
    "waffles-com-iogurte": "waffles iogurte",
}


def download(url: str, dest: Path) -> bool:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = r.read()
        if len(data) < 3000:
            return False
        dest.write_bytes(data)
        return True
    except Exception as e:
        print(f"  fail: {e}")
        return False


def fetch_one(slug: str, query: str) -> bool:
    dest = IMG / f"{slug}.jpg"
    if dest.exists():
        print(f"skip {slug} (exists)")
        return True
    print(f"=== {slug} :: {query}")
    with DDGS() as d:
        hits = list(d.images(query, max_results=8))
    for i, hit in enumerate(hits):
        url = hit.get("image") or hit.get("thumbnail")
        if not url:
            continue
        if download(url, dest):
            print(f"  saved from hit {i + 1}")
            return True
    print(f"  NO IMAGE for {slug}")
    return False


def main() -> None:
    ok = 0
    for slug, query in SLUGS.items():
        if fetch_one(slug, query):
            ok += 1
        time.sleep(0.5)
    print(f"Done: {ok}/{len(SLUGS)}")


if __name__ == "__main__":
    main()
