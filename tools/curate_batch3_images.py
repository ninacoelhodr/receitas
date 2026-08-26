#!/usr/bin/env python3
"""Download reference dish photos for batch3 recipes."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMAGENS = ROOT / "imagens"

QUERIES = {
    "cheesecake-basque-de-chocolate": "basque burnt cheesecake chocolate",
    "cheesecake-basque-de-matcha": "matcha basque cheesecake",
    "pao-de-forma": "pão de forma fatias receita",
    "pao-integral": "pão integral fatias",
    "paezinhos-rapidos": "pãezinhos sal receita",
    "pao-sirio": "pão sírio pita",
    "broinhas-de-fuba": "broinha de fubá",
    "muffins": "muffins passas receita",
    "rosca-de-natal": "rosca de natal doce",
    "bolo-merenda": "bolo merenda simples",
    "bolo-de-especiarias": "bolo de especiarias",
    "bolo-de-mandioca": "bolo de mandioca",
    "bolo-de-chocolate-com-calda": "bolo de chocolate calda",
    "bolo-de-laranja": "bolo de laranja fubá",
    "bolo-de-abacaxi": "bolo de abacaxi invertido",
    "bolo-de-fuba-e-coco": "bolo de fubá e coco",
    "bolo-gelado-de-goiaba": "bolo gelado de goiaba",
    "bolo-de-sorvete-com-cerejas": "bolo de sorvete cerejas",
    "biscoitinhos-coloridos": "biscoitos coloridos rocambole",
    "biscoitinhos-de-cerveja": "biscoitos de cerveja",
    "biscoitinhos-de-ameixa-preta": "biscoitos ameixa seca",
    "biscoitinhos-de-chocolate-e-coco": "biscoitos chocolate coco",
    "biscoitinhos-de-caramelo": "biscoitos caramelo",
    "esquecidos": "biscoitos esquecidos",
    "casadinhos-recheados": "casadinhos doce de leite",
    "sequilhos-de-coco": "sequilhos de coco",
    "waffles-com-iogurte": "waffles iogurte",
}


def get_image_url(query: str) -> str | None:
    from ddgs import DDGS

    with DDGS() as ddgs:
        for r in ddgs.images(query, max_results=5):
            url = r.get("image")
            if url and url.startswith("http"):
                return url
    return None


def download(url: str, dest: Path) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_suffix(".tmp")
    try:
        subprocess.run(
            ["curl", "-fsSL", "-A", "Mozilla/5.0", "-o", str(tmp), url],
            check=True,
            timeout=60,
        )
        if tmp.stat().st_size < 5000:
            tmp.unlink(missing_ok=True)
            return False
        tmp.rename(dest)
        return True
    except (subprocess.CalledProcessError, OSError):
        tmp.unlink(missing_ok=True)
        return False


def main() -> None:
    ok, fail = 0, 0
    for slug, query in QUERIES.items():
        dest = IMAGENS / f"{slug}.jpg"
        if dest.exists() and dest.stat().st_size > 5000:
            print(f"skip {slug}")
            ok += 1
            continue
        url = get_image_url(query)
        if not url:
            print(f"no url {slug}")
            fail += 1
            continue
        if download(url, dest):
            print(f"ok {slug}")
            ok += 1
        else:
            print(f"fail download {slug}")
            fail += 1
    print(f"done: {ok} ok, {fail} fail")


if __name__ == "__main__":
    main()
