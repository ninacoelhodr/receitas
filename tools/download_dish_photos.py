#!/usr/bin/env python3
"""Download Wikimedia Commons reference images for new recipe slugs missing imagens/<slug>.jpg."""
from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IMG = ROOT / "imagens"
UA = "ReceitasFamiliaBot/1.0 (personal recipe book; contact: local)"

# Search terms for Commons (slug -> query). Unlisted slugs use title-ish fallback from slug.
SEARCH: dict[str, str] = {
    "biscoitos-de-chocolate": "chocolate cookies",
    "biscoitos-de-maracuja": "passion fruit cookies",
    "biscoitos-amanteigados-de-laranja": "orange butter cookies",
    "biscoitos-de-nata": "cream cookies biscuits",
    "biscoitos-de-limao": "lemon cookies",
    "biscoitos-amanteigados": "butter cookies",
    "musse-de-guarana": "mousse dessert glass",
    "musse-requintada": "berry mousse dessert",
    "musse-napolitana": "neapolitan mousse",
    "musse-de-coco-com-calda-de-pessego": "coconut mousse peach",
    "musse-de-baunilha-e-compota-de-uva": "vanilla mousse grapes",
    "musse-espuma-de-pessego": "peach mousse dessert",
    "musse-delicia": "chocolate mousse layered",
    "musse-de-festa": "fruit mousse dessert",
    "musse-caramelada-de-banana-e-gengibre": "banana caramel mousse",
    "musse-paixao": "passion fruit chocolate mousse",
    "musse-de-morango": "strawberry mousse dessert",
    "musse-chic": "pear chocolate mousse",
    "musse-de-tangerina-e-chocolate-branco": "white chocolate tangerine dessert",
    "musse-de-manga-com-leite-de-coco": "mango coconut mousse",
    "musse-de-maracuja": "passion fruit mousse",
    "musse-de-abobora-com-amendoim": "pumpkin mousse dessert",
    "musse-torta-de-limao": "lemon mousse dessert",
    "musse-de-castanha": "cashew dessert cream",
    "musse-de-biscoito-com-mel": "honey biscuit dessert",
    "musse-especial": "peanut caramel mousse",
    "musse-caramelo": "caramel mousse",
    "musse-bis": "chocolate orange mousse",
    "musse-de-amora": "blackberry mousse",
    "musse-brigadeiro-branco": "white chocolate mousse",
    "musse-de-amendoim": "peanut butter mousse",
    "musse-limonada": "lemon mousse dessert",
    "musse-bombom-de-chocolate": "chocolate mousse bonbon",
    "tortinhas-de-banana": "banana tart",
    "flan-de-chocolate-e-creme": "chocolate flan cream",
    "mousse-de-chocolate": "chocolate mousse",
    "sufle-de-damasco": "apricot souffle",
    "bolinho-de-chuva": "bolinho de chuva",
    "hang-yang-peang": "almond cookies chinese",
    "calda-de-maracuja-para-torta": "passion fruit sauce dessert",
    "morango-ao-creme": "strawberries and cream",
    "torta-de-maracuja-com-ganache": "passion fruit tart chocolate",
    "terrine-de-pistache": "pistachio terrine dessert",
    "compota-de-tomate": "tomato compote dessert",
    "sorvete-de-especiarias": "spiced ice cream",
    "molho-branco-sem-fogo": "white sauce cream",
    "waffle-salgado": "savory waffle",
    "pao-de-queijo": "pão de queijo",
    "espaguete-a-carbonara": "spaghetti carbonara",
    "macarrao-a-moda-do-sul": "baked pasta cheese ham",
    "macarrao-tentador": "chicken pasta casserole",
    "ravioli-a-camaresca": "ravioli shrimp cream",
    "lasanha-aos-quatro-queijos": "four cheese lasagna",
    "fiesta-com-batatas-e-creme-azedo": "roast chicken potatoes",
    "peru-com-peras-e-arroz-de-nozes": "roast turkey pears rice",
    "tender-picante": "glazed ham mustard",
    "pernil-recheado-com-canjiquinha": "roast pork stuffed",
    "talharim-com-vongole": "tagliatelle vongole",
    "macarrao-ao-creme": "pasta cream ham peas",
    "peixe-a-thermidor": "fish thermidor",
    "espaguete-aos-quatro-queijos": "four cheese spaghetti",
    "bucatini-com-atum-iogurte-e-pimenta": "pasta tuna yogurt",
    "gratinado-de-frango": "chicken gratin",
    "ju-har-kow": "fried shrimp batter chinese",
    "goo-low-yuke": "sweet and sour pork",
    "tempura-de-camarao": "shrimp tempura",
    "escalope-de-foie-gras-com-maca-verde": "foie gras apple",
    "hadoque-defumado-com-maca": "smoked haddock apple",
    "pera-com-truta-defumada": "smoked trout pear",
    "terrine-de-camarao-e-palmito": "shrimp terrine",
    "vol-au-vent-de-vieiras": "vol-au-vent scallops",
    "atum-fresco-grelhado-ao-curry": "grilled tuna curry coconut",
    "ossobuco-de-vitela-com-risotto-de-rucula": "ossobuco risotto",
    "picanha-de-porco-ao-molho-de-tamarindo": "pork steak tamarind",
    "camaraoes-com-vodca-ao-molho-de-salsa": "shrimp vodka cream",
    "truta-grande-hotel-ao-molho-de-pinhao": "trout pine nuts sauce",
    "avestruz-a-la-bourguignonne": "bourguignon stew",
    "costeletas-de-cordeiro-com-menta": "lamb chops mint",
    "torta-de-bacon-e-minicebola": "bacon onion tart",
    "torta-de-catalonia": "chicory pie savory",
    "folhado-de-linguica-e-ricota": "sausage puff pastry",
    "torta-de-cebola": "onion tart",
    "torta-maravilha-de-frango-e-presunto": "chicken ham pie",
    "torta-de-escarola-com-requeijao": "escarole pie",
    "quiche-de-tomate-seco-e-peito-de-peru": "quiche sun dried tomato",
    "torta-folhada-de-queijo": "puff pastry cheese tart",
    "tortinhas-de-mussarela-de-bufala": "caprese tartlet",
    "torta-pizza": "savory tomato olive pie",
    "torta-de-atum-e-batata": "tuna potato pie",
    "torta-de-queijo-e-milho": "corn cheese pie",
    "torta-de-frango-com-catupiry": "chicken cream cheese pie",
    "torta-de-atum": "tuna pie sesame",
}


def commons_file_url(query: str) -> str | None:
    api = "https://commons.wikimedia.org/w/api.php"
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": f"filetype:bitmap {query}",
        "gsrnamespace": "6",
        "gsrlimit": "5",
        "prop": "imageinfo",
        "iiprop": "url|mime|size",
        "iiurlwidth": "800",
    }
    url = api + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.load(resp)
    pages = data.get("query", {}).get("pages", {})
    for page in pages.values():
        infos = page.get("imageinfo") or []
        if not infos:
            continue
        info = infos[0]
        mime = info.get("mime", "")
        if "jpeg" not in mime and "jpg" not in mime and "png" not in mime:
            continue
        return info.get("thumburl") or info.get("url")
    return None


def download(url: str, dest: Path) -> None:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as resp:
        dest.write_bytes(resp.read())


def make_placeholder(dest: Path, fallback: Path) -> None:
    # Copy an existing dish photo as placeholder so figure loads.
    dest.write_bytes(fallback.read_bytes())


def main() -> None:
    fallback = next(IMG.glob("*.jpg"))
    missing = []
    for html_path in (ROOT / "receitas").rglob("*.html"):
        slug = html_path.stem
        dest = IMG / f"{slug}.jpg"
        if dest.exists():
            continue
        missing.append(slug)

    print(f"Missing images: {len(missing)}")
    ok = 0
    for i, slug in enumerate(missing, 1):
        query = SEARCH.get(slug) or slug.replace("-", " ")
        dest = IMG / f"{slug}.jpg"
        try:
            url = commons_file_url(query)
            if not url:
                # try simpler food term
                url = commons_file_url("food dish plate")
            if url:
                download(url, dest)
                print(f"[{i}/{len(missing)}] OK {slug}")
                ok += 1
            else:
                make_placeholder(dest, fallback)
                print(f"[{i}/{len(missing)}] PLACEHOLDER {slug}")
        except Exception as e:
            make_placeholder(dest, fallback)
            print(f"[{i}/{len(missing)}] ERR {slug}: {e} -> placeholder")
        time.sleep(0.35)
    print(f"Done. Downloaded/ok-ish: {ok}/{len(missing)}")


if __name__ == "__main__":
    main()
