#!/usr/bin/env python3
"""Generate recipe HTML from Telegram pending batch (2026-08-16)."""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CATEGORIES = {
    "doces": "Doces",
    "tortas-salgadas": "Tortas salgadas",
    "aves": "Aves",
    "acompanhamentos": "Acompanhamentos",
}

RECIPES: list[dict] = [
    {
        "cat": "acompanhamentos",
        "slug": "pate-de-figado-de-galinha",
        "title": "Patê de fígado de galinha",
        "category_label": "Acompanhamentos",
        "meta": [("Rendimento", "10 porções")],
        "ingredients": [
            "1,5 kg de fígados de galinha",
            "2 ovos grandes",
            "2 gemas",
            "2 colheres (chá) de sal",
            "1 colher (chá) de pimenta-do-reino",
            "1 colher (sopa) de manjericão bem picado",
            "1 xícara de molho branco grosso",
            "2 colheres (sopa) de vinho Madeira ou conhaque",
            "Manteiga para untar",
        ],
        "steps": [
            "Preaqueça o forno em temperatura média (180 °C). Limpe os fígados, retirando todos os filamentos. Coloque-os no liquidificador com os ovos, as gemas, o sal, a pimenta e o manjericão. Bata por 1 minuto.",
            "Adicione o molho branco e o vinho ou conhaque; bata por mais 15 segundos. Passe por uma peneira sobre uma terrina.",
            "Despeje numa forma de pão inglês untada (7 × 12 × 25 cm, ~5 xícaras). Asse em banho-maria por cerca de 30 minutos. Deixe esfriar e congele.",
        ],
        "notes": "Para servir quente: descongele, cubra com papel-alumínio e aqueça em forno bem baixo. Congele na forma, depois embale em filme. Decore com tiras de pimentão vermelho em conserva e sirva com torradas.",
    },
    {
        "cat": "tortas-salgadas",
        "slug": "torta-de-frango",
        "title": "Torta de frango",
        "category_label": "Tortas salgadas",
        "meta": [("Rendimento", "6 a 8 porções")],
        "ingredients": [
            "½ kg de frango",
            "2 xícaras de mussarela ralada",
            "1¾ xícaras de leite",
            "1 cebola picada",
            "2 colheres (chá) de orégano",
            "1 kg de batatas",
            "6 colheres (sopa) de manteiga",
            "⅓ xícara de leite",
            "5 colheres (sopa) de salsa picada",
            "2 cenouras raladas grosso e cozidas",
            "2 colheres (sopa) de cebolinha verde picada",
            "2 colheres (sopa) de maionese",
            "3 colheres (sopa) de farinha de trigo",
            "1 colher (sopa) de purê de tomate",
            "1 gema",
        ],
        "steps": [
            "Cozinhe e desfie o frango. Misture com o queijo, o leite, a cebola e o orégano; tampe e leve à geladeira para marinar.",
            "Cozinhe as batatas em cubos; escorra, passe no espremedor e misture 4 colheres de manteiga, ⅓ xícara de leite, sal, salsa — purê reservado.",
            "Escorra o líquido do frango (reserve). Misture o frango com cenoura, cebolinha e maionese.",
            "Derreta o restante da manteiga, junte a farinha e doure levemente. Fora do fogo, acrescente o líquido reservado mexendo; volte ao fogo com o purê de tomate até engrossar. Junte ao frango.",
            "Coloque o recheio num refratário de 2 litros, cubra com o purê e faça sulcos com o garfo.",
            "Pincele com gema batida com 2 colheres de água. Asse em forno alto (200 °C) por ~50 min até dourar. Deixe esfriar e congele.",
        ],
        "notes": "Para congelar crua, pincele com gema só após descongelar. Descongele na geladeira e reaqueça coberta com alumínio.",
    },
    {
        "cat": "aves",
        "slug": "enroladinhos-meireles",
        "title": "Enroladinhos Meireles",
        "category_label": "Aves · Frango",
        "meta": [("Rendimento", "6 a 8 porções")],
        "ingredients": [
            "4 peitos de frango sem osso cortados ao meio",
            "Sal a gosto",
            "1 cenoura ralada grosso",
            "⅓ xícara de uvas-passas pretas sem semente",
            "1 maçã verde com casca ralada grosso",
            "2 colheres (sopa) de vinho branco ou vinagre de maçã",
            "4 colheres (sopa) de manteiga ou margarina",
            "1 garrafinha de leite de coco",
            "1 colher (chá) de gengibre ralado",
        ],
        "steps": [
            "Abra cada metade de peito formando um bife largo; tempere com sal.",
            "Misture cenoura, passas, maçã, vinagre e sal. Divida em 8 porções e coloque sobre cada peito; enrole e prenda com palito ou barbante.",
            "Pré-aqueça o forno a 180 °C. Arrume os enroladinhos num refratário.",
            "Derreta a manteiga com o leite de coco e o gengibre; regue os enroladinhos.",
            "Asse por ~40 min até dourar e ficar macio. Deixe esfriar e congele.",
        ],
        "notes": "Proteja as pontas dos palitos com papel-alumínio ao embalar para congelar.",
    },
    {
        "cat": "aves",
        "slug": "enrolados-de-frango",
        "title": "Enrolados de frango",
        "category_label": "Aves · Frango",
        "meta": [("Rendimento", "4 porções")],
        "ingredients": [
            "2 peitos de frango (~1 kg)",
            "Sal e pimenta-do-reino a gosto",
            "1¼ xícaras de água",
            "¼ xícara de arroz cru",
            "1 colher (sopa) de cebolinha verde picada",
            "1 cenoura ralada",
            "1 pimentão verde em cubinhos",
            "1 colher (chá) de raspas de laranja",
            "Manteiga para pincelar",
            "1 xícara de suco de laranja",
            "1 colher (sopa) de maisena",
            "1 pitada de sal",
        ],
        "steps": [
            "Retire pele e osso dos peitos; divida cada um ao meio (4 filés). Bata com martelo até ficarem finos; tempere.",
            "Cozinhe o arroz com água, cebolinha, cenoura, pimentão, raspas, sal e pimenta até o arroz ficar macio e secar.",
            "Espalhe o arroz sobre os filés, enrole e prenda com palitos. Arrume numa assadeira, pincele manteiga, tampe com alumínio e asse a 180 °C por ~20 min.",
            "Para o molho: misture suco de laranja, maisena e sal; cozinhe até engrossar. Deixe esfriar e congele separadamente.",
        ],
        "notes": "Antes de embalar, mergulhe os enrolados no molho para não secar. Congele rolos e molho à parte.",
    },
    {
        "cat": "aves",
        "slug": "files-de-frango-recheados",
        "title": "Filés de frango recheados",
        "category_label": "Aves · Frango",
        "meta": [("Rendimento", "4 a 6 porções")],
        "ingredients": [
            "3 peitos de frango sem osso cortados ao meio",
            "6 fatias de bacon",
            "Sal e pimenta-do-reino a gosto",
            "4 colheres (sopa) de azeite de oliva",
            "1 colher (sopa) de orégano",
            "½ xícara de leite",
            "1 copo de requeijão cremoso",
            "2 colheres (sopa) de salsa picada",
        ],
        "steps": [
            "Pré-aqueça o forno a 180 °C. Faça um bolso em cada metade de peito; recheie com bacon, tempere e prenda com palito ou barbante.",
            "Arrume numa assadeira, regue com azeite, polvilhe orégano e asse ~40 min até dourar.",
            "Retire do forno; transfira o frango para embalagem de alumínio e mantenha aquecido no forno desligado.",
            "Leve a assadeira ao fogo brando, junte leite e requeijão e misture os sucos até formar molho uniforme.",
            "Cubra o frango com o molho, deixe esfriar e congele.",
        ],
        "notes": "Descongele na geladeira; aqueça tampado em forno baixo. Sirva polvilhado com salsa.",
    },
    {
        "cat": "aves",
        "slug": "frango-assado-com-cerveja",
        "title": "Frango assado com cerveja",
        "category_label": "Aves · Frango",
        "meta": [("Rendimento", "4 porções")],
        "ingredients": [
            "1 frango (~1,8 kg) limpo e cortado em pedaços",
            "Sal e pimenta-do-reino a gosto",
            "5 dentes de alho amassados",
            "1 cebola grande picada",
            "4 folhas de louro",
            "2 latas de cerveja",
        ],
        "steps": [
            "Pré-aqueça o forno em temperatura alta (200 °C).",
            "Tempere os pedaços com sal, pimenta e alho; coloque numa assadeira com cebola e louro.",
            "Despeje a cerveja por cima e asse até dourar e ficar macio (~1 h 40), regando de vez em quando.",
            "Deixe esfriar e congele (pode dividir em porções).",
        ],
    },
    {
        "cat": "aves",
        "slug": "frango-na-pucara",
        "title": "Frango na púcara",
        "category_label": "Aves · Frango",
        "meta": [("Rendimento", "4 porções")],
        "ingredients": [
            "100 g de presunto cru",
            "4 tomates maduros",
            "2 dentes de alho",
            "1 frango (~1,8 kg) limpo e cortado em pedaços",
            "Sal e pimenta-do-reino a gosto",
            "10 cebolinhas pequenas inteiras",
            "4 colheres (sopa) de manteiga fria em cubos",
            "⅓ xícara de vinho do Porto",
            "½ xícara de conhaque",
            "1 xícara de vinho branco seco",
            "2 colheres (sopa) de mostarda",
        ],
        "steps": [
            "Corte o presunto em cubinhos de 0,5 cm e dessalgue em água fria. Descasque os tomates, retire sementes e corte em cubos de 1 cm.",
            "Pré-aqueça o forno a 200 °C. Amasse o alho. Tempere o frango e distribua numa panela de barro com tampa.",
            "Acrescente presunto, tomate, alho e cebolinhas; distribua a manteiga. Regue com Porto, conhaque, vinho branco e mostarda.",
            "Tampe e leve ao forno até o frango ficar macio (~1 h). Destampe e volte ao forno para dourar (~30 min). Deixe esfriar e congele.",
        ],
        "notes": "Prato clássico da cozinha regional portuguesa, preparado na panela de barro (*púcara*). Sirva com batatas fritas e arroz.",
    },
    {
        "cat": "aves",
        "slug": "frango-ao-caril",
        "title": "Frango ao caril",
        "category_label": "Aves · Frango",
        "meta": [("Rendimento", "4 a 6 porções")],
        "ingredients": [
            "1 kg de coxas, sobrecoxas e peitos de frango",
            "3 colheres (chá) de sal",
            "½ xícara de óleo",
            "2 cebolas picadas",
            "4 dentes de alho picados",
            "1½ colher (chá) de gengibre ralado",
            "3 colheres (sopa) de pó de caril",
            "1½ xícaras de água",
            "4 a 5 tomates",
            "2 colheres (sopa) de coentro picado",
            "1 potinho de iogurte natural",
            "1 colher (sopa) de suco de limão",
        ],
        "steps": [
            "Lave e seque o frango; polvilhe com 2 colheres (chá) de sal.",
            "Frite os pedaços no óleo 3–4 min sem dourar demais; reserve.",
            "Na mesma panela, refogue cebola, alho e gengibre ~4 min. Abaixe o fogo, junte 1 colher de caril e 1 de água; cozinhe 2 min mexendo.",
            "Acrescente tomates picados, 1 colher de coentro, iogurte e sal restante. Volte o frango com os sucos, junte a água restante e cozinhe em fogo baixo, tampado, ~25 min.",
            "Retire do fogo, misture o limão, arrume numa bandeja e despeje o molho. Deixe esfriar e congele.",
        ],
        "notes": "Ao servir, polvilhe com caril e coentro restantes; acompanhe arroz branco.",
    },
    {
        "cat": "aves",
        "slug": "frango-estufado-com-tomates",
        "title": "Frango estufado com tomates",
        "category_label": "Aves · Frango",
        "meta": [("Rendimento", "2 porções")],
        "ingredients": [
            "1 colher (sopa) de óleo",
            "1 cebola picada",
            "1 dente de alho",
            "3 tiras de bacon",
            "1 pimentão verde",
            "2 coxas e 2 sobrecoxas de frango sem pele",
            "1 lata de tomates sem pele ou 6 tomates sem pele e sem sementes",
            "2 colheres (sopa) de purê de tomate",
            "1 colher (sopa) de páprica",
            "1 pitada de açúcar",
            "Sal e pimenta-do-reino a gosto",
            "⅓ xícara de azeitonas pretas",
            "4 colheres (sopa) de salsa picada",
        ],
        "steps": [
            "Refogue óleo, cebola, alho, bacon e pimentão até o bacon fritar.",
            "Junte o frango, tomates, purê, páprica, açúcar, sal e pimenta; tampe e cozinhe.",
            "Acrescente azeitonas e 2 colheres de salsa; cozinhe destampado. Deixe esfriar e congele.",
        ],
        "notes": "Páprica doce ou picante, a gosto. Descongele em banho-maria ou micro-ondas; polvilhe salsa ao servir.",
    },
    {
        "cat": "aves",
        "slug": "peru-recheado-com-risoto",
        "title": "Peru recheado com risoto",
        "category_label": "Aves · Outras aves",
        "meta": [("Rendimento", "12 porções")],
        "ingredients": [
            "½ xícara de uvas-passas pretas",
            "1 xícara de champanha",
            "4 colheres (sopa) de manteiga",
            "1 cebola picada",
            "2 xícaras de arroz",
            "4 xícaras de caldo de galinha",
            "2 xícaras de castanhas de caju",
            "1 xícara de manteiga (para temperar o peru)",
            "2 cebolas picadas",
            "1 lata de purê de tomate",
            "1 colher (sopa) de sal",
            "2 colheres (chá) de pimenta-branca",
            "2 xícaras de champanha (para o peru)",
            "1 peru de 4 a 5 kg",
        ],
        "steps": [
            "Deixe as passas de molho na champanha. Faça o risoto: refogue cebola na manteiga, junte o arroz, cubra com caldo e cozinhe até macio mas al dente.",
            "Misture passas escorridas e castanhas picadas; regue com a champanha das passas. Congele o risoto.",
            "Derreta 1 xícara de manteiga; misture cebolas, purê, sal, pimenta e champanha. Tempere o peru, levantando a pele do peito.",
            "Descongele peru e risoto na geladeira. Recheie o peru, cubra com alumínio e asse a 200 °C por 4–5 h, regando com caldo. Retire o alumínio nos últimos 40 min para dourar.",
        ],
        "notes": "Calcule ~1 h de forno por quilo de peru. Sirva com gomos de laranja.",
    },
    {
        "cat": "doces",
        "slug": "bolacha-de-nescau",
        "title": "Bolacha de Nescau",
        "category_label": "Doces · Biscoitos",
        "meta": None,
        "ingredients": [
            "1 copo de farinha de trigo",
            "1 copo de Nescau",
            "1 ovo",
            "3 colheres de margarina",
        ],
        "steps": [
            "Misture todos os ingredientes até formar uma massa homogênea.",
            "Faça bolinhas, achate com um garfo e disponha em assadeira.",
            "Leve ao forno por cerca de 15 minutos.",
        ],
        "notes": "Receita de 4 ingredientes (Pinterest).",
    },
    {
        "cat": "doces",
        "slug": "cheesecake-basco-de-chocolate",
        "title": "Cheesecake basco de chocolate",
        "category_label": "Doces · Tortas e bolos",
        "meta": [("Rendimento", "8 porções")],
        "ingredients": [
            "500 g de cream cheese em temperatura ambiente",
            "150 g de açúcar",
            "4 ovos",
            "150 g de chocolate meio amargo (70%)",
            "200 ml de creme de leite",
            "1 colher (chá) de essência de baunilha",
        ],
        "steps": [
            "Pré-aqueça o forno a 200 °C. Forre uma forma de aro removível com papel-manteiga.",
            "Derreta o chocolate e reserve.",
            "Bata o cream cheese com o açúcar até ficar liso. Acrescente os ovos, um a um.",
            "Incorpore o chocolate derretido, o creme de leite e a baunilha.",
            "Despeje na forma e asse até a superfície dourar e o centro ficar levemente bamboleante (~50–60 min).",
            "Deixe esfriar completamente e leve à geladeira por pelo menos 4 horas antes de servir.",
        ],
        "notes": "Adaptado de infográfico (cheesecake basco / burnt cheesecake).",
    },
    {
        "cat": "doces",
        "slug": "bolo-de-chocolate-com-3-ingredientes",
        "title": "Bolo de chocolate com 3 ingredientes",
        "category_label": "Doces · Tortas e bolos",
        "meta": [("Rendimento", "8 porções")],
        "ingredients": [
            "450 g de chocolate ao leite ou meio amargo",
            "230 g de manteiga sem sal",
            "8 ovos",
            "Açúcar de confeiteiro para untar e decorar",
        ],
        "steps": [
            "Derreta o chocolate com a manteiga no micro-ondas (1 min, mexa, mais 1 min) até homogêneo. Deixe esfriar.",
            "Bata os ovos na batedeira por 5–8 min até dobrar de volume.",
            "Incorpore o chocolate em três etapas, mexendo de baixo para cima.",
            "Despeje numa forma desmontável untada com manteiga e açúcar. Asse em banho-maria a 200 °C por 40 min.",
            "Decore com açúcar de confeiteiro.",
        ],
        "notes": "Receita da chef Heaven Delhaye (link do X/Twitter). Sem farinha.",
    },
]


def render_recipe(r: dict) -> str:
    cat = r["cat"]
    cat_label = CATEGORIES[cat]
    title = r["title"]
    slug = r["slug"]
    category_display = r.get("category_label", cat_label)
    desc = html.escape(f"{title} — ficha A5 para imprimir.")
    meta_html = ""
    if r.get("meta"):
        spans = "".join(
            f"\n          <span><strong>{html.escape(k)}:</strong> {html.escape(v)}</span>"
            for k, v in r["meta"]
        )
        meta_html = f'\n        <div class="meta">{spans}\n        </div>'
    ingredients = "\n".join(
        f"          <li>{html.escape(i)}</li>" for i in r["ingredients"]
    )
    steps = "\n".join(f"          <li>{html.escape(s)}</li>" for s in r["steps"])
    notes = ""
    if r.get("notes"):
        notes = f"""
        <h2>Observação</h2>
        <p class="notes">{html.escape(r["notes"])}</p>"""
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{html.escape(title)} — Livro de Receitas</title>
    <meta name="description" content="{desc}" />
    <link rel="stylesheet" href="../../css/site.css" />
    <link rel="stylesheet" href="../../css/print.css" />
  </head>
  <body>
    <header class="site-header no-print">
      <a class="brand" href="../../index.html">Livro de Receitas</a>
      <nav class="site-nav" aria-label="Principal">
        <a href="../../index.html#{cat}">{html.escape(cat_label)}</a>
        <a href="../../na-cozinha/">Na cozinha</a>
      </nav>
    </header>

    <main class="recipe-page">
      <div class="recipe-actions no-print">
        <a class="btn btn-ghost" href="../../index.html">← Voltar</a>
        <button class="btn" type="button" onclick="window.print()">
          Imprimir
        </button>
      </div>

      <article class="recipe-card">
        <p class="category">{html.escape(category_display)}</p>
        <h1>{html.escape(title)}</h1>{meta_html}
        <figure class="dish-photo no-print">
          <img src="../../imagens/{slug}.jpg" alt="Referência: {html.escape(title)}" />
          <figcaption>Referência visual (não é a foto da receita da família).</figcaption>
        </figure>

        <h2>Ingredientes</h2>
        <ul class="ingredients">
{ingredients}
        </ul>

        <h2>Modo de preparo</h2>
        <ol class="steps">
{steps}
        </ol>{notes}
      </article>
    </main>
  </body>
</html>
"""


def insert_into_index(index_text: str, cat: str, subcategory: str | None, slug: str, title: str) -> str:
    href = f'./receitas/{cat}/{slug}.html'
    new_li = (
        f'          <li>\n'
        f'            <a href="{href}">{html.escape(title)}</a>\n'
        f'          </li>\n'
    )
    section_pat = rf'(<section class="category-block" id="{re.escape(cat)}">.*?)(</section>)'
    m = re.search(section_pat, index_text, re.S)
    if not m:
        raise SystemExit(f"Category section not found: {cat}")
    section = m.group(1)

    if subcategory:
        ul_pat = (
            rf'(<ul class="recipe-list" data-subcategory="{re.escape(subcategory)}">\s*)'
            r'((?:\s*<li>.*?</li>)*)'
            r'(\s*</ul>)'
        )
        um = re.search(ul_pat, section, re.S)
        if not um:
            raise SystemExit(f"Subcategory not found: {cat}/{subcategory}")
        items = um.group(2)
        if href in items:
            return index_text
        items += new_li
        # sort by title inside li
        lis = re.findall(r'<li>.*?</li>\s*', items, re.S)
        lis.sort(key=lambda x: re.sub(r'<[^>]+>', '', x).strip().lower())
        new_items = ''.join(lis)
        new_section = section[: um.start()] + um.group(1) + new_items + um.group(3) + section[um.end() :]
    else:
        ul_pat = r'(<ul class="recipe-list">\s*)((?:.*?</li>\s*)*)(</ul>)'
        um = re.search(ul_pat, section, re.S)
        if not um:
            raise SystemExit(f"Recipe list not found in {cat}")
        items = um.group(2)
        if href in items:
            return index_text
        items += new_li
        lis = re.findall(r'<li>.*?</li>\s*', items, re.S)
        lis.sort(key=lambda x: re.sub(r'<[^>]+>', '', x).strip().lower())
        new_items = ''.join(lis)
        new_section = section[: um.start()] + um.group(1) + new_items + um.group(3) + section[um.end() :]

    return index_text[: m.start()] + new_section + m.group(2) + index_text[m.end() :]


def parse_subcategory(category_label: str) -> tuple[str, str | None]:
    if " · " in category_label:
        _, sub = category_label.split(" · ", 1)
        return category_label.split(" · ", 1)[0], sub
    return category_label, None


def main() -> None:
    index_path = ROOT / "index.html"
    index_text = index_path.read_text(encoding="utf-8")
    written = []

    for r in RECIPES:
        out = ROOT / "receitas" / r["cat"] / f"{r['slug']}.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        if out.exists():
            print(f"skip exists {out.relative_to(ROOT)}")
            continue
        out.write_text(render_recipe(r), encoding="utf-8")
        written.append(r)
        print(f"wrote {out.relative_to(ROOT)}")

        cat_label, sub = parse_subcategory(r.get("category_label", CATEGORIES[r["cat"]]))
        if sub:
            index_text = insert_into_index(index_text, r["cat"], sub, r["slug"], r["title"])
        else:
            index_text = insert_into_index(index_text, r["cat"], None, r["slug"], r["title"])

    if written:
        index_path.write_text(index_text, encoding="utf-8")
        print(f"Updated index.html with {len(written)} recipes")
    print(f"Created {len(written)} new recipes")


if __name__ == "__main__":
    main()
