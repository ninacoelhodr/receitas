#!/usr/bin/env python3
import io
import urllib.request
from pathlib import Path

from ddgs import DDGS
from PIL import Image

ROOT = Path(__file__).resolve().parents[1] / "imagens"
SLUGS = [
    ("pao-de-forma", "Pão de fôrma"),
    ("pao-integral", "Pão integral"),
    ("paezinhos-rapidos", "Pãezinhos rápidos"),
    ("pao-sirio", "Pão sírio"),
    ("broinhas-de-fuba", "Broinhas de fubá"),
    ("muffins", "Muffins receita"),
    ("rosca-de-natal", "Rosca de Natal"),
    ("bolo-merenda", "Bolo merenda"),
    ("bolo-de-especiarias", "Bolo de especiarias"),
    ("bolo-de-mandioca", "Bolo de mandioca"),
    ("bolo-de-chocolate", "Bolo de chocolate"),
    ("bolo-de-laranja", "Bolo de laranja"),
    ("bolo-de-abacaxi", "Bolo de abacaxi"),
    ("bolo-de-fuba-e-coco", "Bolo de fubá e coco"),
    ("bolo-gelado-de-goiaba", "Bolo gelado de goiaba"),
    ("bolo-de-sorvete-com-cerejas", "Bolo de sorvete com cerejas"),
    ("biscoitinhos-coloridos", "Biscoitinhos coloridos"),
    ("biscoitinhos-de-cerveja", "Biscoitinhos de cerveja"),
    ("biscoitinhos-de-ameixa-preta", "Biscoitinhos de ameixa"),
    ("biscoitinhos-de-chocolate-e-coco", "Biscoitinhos de chocolate e coco"),
    ("biscoitinhos-de-caramelo", "Biscoitinhos de caramelo"),
    ("esquecidos", "Biscoitos esquecidos"),
    ("casadinhos-recheados", "Casadinhos recheados"),
    ("sequilhos-de-coco", "Sequilhos de coco"),
    ("waffles-com-iogurte", "Waffles com iogurte"),
    ("cheesecake-basco-de-chocolate", "Cheesecake basco de chocolate"),
]


def save_image(data: bytes, out: Path) -> None:
    img = Image.open(io.BytesIO(data))
    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    img.save(out, "JPEG", quality=85)


def main() -> None:
    ok, fail = [], []
    for slug, query in SLUGS:
        out = ROOT / f"{slug}.jpg"
        try:
            with DDGS() as d:
                results = list(d.images(query, max_results=5))
            for r in results:
                url = r.get("image") or r.get("thumbnail")
                if not url:
                    continue
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                data = urllib.request.urlopen(req, timeout=20).read()
                if len(data) < 5000:
                    continue
                save_image(data, out)
                ok.append(slug)
                break
            else:
                fail.append(slug)
        except Exception as exc:
            fail.append(f"{slug}: {exc}")
    print(f"OK {len(ok)}")
    print(f"FAIL {len(fail)}")
    for item in fail:
        print(item)


if __name__ == "__main__":
    main()
