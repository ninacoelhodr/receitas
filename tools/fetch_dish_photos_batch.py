#!/usr/bin/env python3
"""Download dish reference photos via DuckDuckGo Images for new slugs."""
from __future__ import annotations

import sys
import time
import urllib.request
from pathlib import Path

from ddgs import DDGS

ROOT = Path(__file__).resolve().parents[1]
IMG = ROOT / "imagens"
UA = "ReceitasNinaBot/1.0"

SLUGS = [
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
]

QUERIES = {
    "pate-de-figado-de-galinha": "patê de fígado de galinha",
    "torta-de-frango": "torta de frango purê batata",
    "enroladinhos-meireles": "enroladinho de frango assado",
    "enrolados-de-frango": "enrolado de frango arroz",
    "files-de-frango-recheados": "filé de frango recheado bacon",
    "frango-assado-com-cerveja": "frango assado cerveja",
    "frango-na-pucara": "frango na púcara português",
    "frango-ao-caril": "frango ao caril",
    "frango-estufado-com-tomates": "frango estufado tomate",
    "peru-recheado-com-risoto": "peru recheado risoto",
    "bolacha-de-nescau": "bolacha de nescau",
    "cheesecake-basco-de-chocolate": "basque burnt cheesecake chocolate",
    "bolo-de-chocolate-com-3-ingredientes": "bolo de chocolate sem farinha",
}


def download(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read()
    dest.write_bytes(data)


def main() -> None:
    IMG.mkdir(exist_ok=True)
    ok = 0
    with DDGS() as ddgs:
        for slug in SLUGS:
            dest = IMG / f"{slug}.jpg"
            if dest.exists() and dest.stat().st_size > 5000:
                print(f"skip {slug}")
                ok += 1
                continue
            q = QUERIES.get(slug, slug.replace("-", " "))
            try:
                results = list(ddgs.images(q, max_results=5))
                if not results:
                    print(f"no results {slug}")
                    continue
                for i, r in enumerate(results):
                    url = r.get("image", "")
                    if not url:
                        continue
                    try:
                        download(url, dest)
                        if dest.stat().st_size > 3000:
                            print(f"ok {slug} (#{i+1})")
                            ok += 1
                            break
                    except Exception as e:
                        print(f"  fail {slug} #{i+1}: {e}")
                else:
                    print(f"failed all {slug}")
            except Exception as e:
                print(f"err {slug}: {e}")
            time.sleep(0.5)
    print(f"done {ok}/{len(SLUGS)}")


if __name__ == "__main__":
    main()
