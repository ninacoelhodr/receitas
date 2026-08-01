#!/usr/bin/env python3
"""Generate recipe HTML from Telegram photo batch (2026-07-31)."""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

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
            "1 xícara de molho branco, grosso",
            "2 colheres (sopa) de vinho Madeira ou conhaque",
            "Manteiga para untar",
        ],
        "steps": [
            "Preaqueça o forno em temperatura média (180 °C). Limpe os fígados, retirando todos os filamentos.",
            "Coloque os fígados no liquidificador com os ovos, as gemas, o sal, a pimenta-do-reino e o manjericão. Bata por 1 minuto.",
            "Adicione o molho branco e o vinho ou conhaque, e bata por mais 15 segundos.",
            "Passe por uma peneira e deixe cair sobre uma terrina.",
            "Coloque a mistura numa fôrma de pão ou bolo inglês untada (7 × 12 × 25 cm, capacidade de 5 xícaras).",
            "Leve ao forno preaquecido, dentro de uma assadeira com água fervente, e asse por cerca de 30 minutos.",
            "Deixe esfriar. Para servir quente, cubra com papel-alumínio e aqueça em forno bem baixo após descongelar.",
        ],
        "notes": "Decore com tiras de pimentão vermelho em conserva e sirva com torradas.",
    },
    {
        "cat": "tortas-salgadas",
        "slug": "torta-de-frango",
        "title": "Torta de frango",
        "category_label": "Tortas salgadas",
        "meta": [("Rendimento", "6 a 8 porções"), ("Tempo", "cerca de 50 min")],
        "ingredients": [
            "½ kg de frango",
            "2 xícaras de mussarela ralada",
            "1¾ xícara de leite",
            "1 cebola picada",
            "2 colheres (chá) de orégano",
            "1 kg de batatas",
            "6 colheres (sopa) de manteiga",
            "⅓ xícara de leite",
            "5 colheres (sopa) de salsa picada",
            "2 cenouras grandes raladas grosso e cozidas",
            "2 colheres (sopa) de cebolinha verde picada",
            "2 colheres (sopa) de maionese",
            "3 colheres (sopa) de farinha de trigo",
            "1 colher (sopa) de purê de tomate",
            "1 gema",
        ],
        "steps": [
            "Cozinhe e desfie o frango. Coloque em um refratário raso e acrescente o queijo, o leite, a cebola e o orégano. Cubra e leve à geladeira para marinar.",
            "Descasque as batatas, corte em cubos e cozinhe em água com sal. Escorra, passe no espremedor e misture com 4 colheres de manteiga e o leite até virar purê. Tempere com sal, acrescente a salsa e reserve.",
            "Escorra o líquido do frango marinado e reserve. Em outra tigela, misture o frango desfiado, a cenoura, a cebolinha e a maionese. Ajuste o tempero.",
            "Em uma frigideira, derreta o restante da manteiga, polvilhe a farinha e doure levemente.",
            "Retire do fogo, acrescente aos poucos o líquido reservado, mexendo sempre. Volte ao fogo, junte o purê de tomate e cozinhe até engrossar.",
            "Misture o molho ao frango.",
            "Coloque o recheio em um refratário de 2 litros, cubra com o purê de batata e faça sulcos com um garfo.",
            "Bata a gema com 2 colheres de água e pincele a superfície.",
            "Asse em forno alto preaquecido (200 °C) por cerca de 50 minutos, até dourar.",
        ],
        "notes": "Para congelar crua, pincele com a gema só após descongelar.",
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
            "1 cenoura raspada no ralador grosso",
            "⅓ xícara de uvas-passas pretas sem sementes",
            "1 maçã verde com casca ralada no ralador grosso",
            "2 colheres (sopa) de vinagre de vinho branco ou de maçã",
            "4 colheres (sopa) de manteiga ou margarina",
            "1 garrafinha de leite de coco",
            "1 colher (chá) de gengibre ralado",
        ],
        "steps": [
            "Abra cada metade de peito de frango formando um bife largo. Tempere com sal.",
            "Misture cenoura, passas, maçã ralada, vinagre e sal. Divida em oito porções e coloque sobre cada peito. Enrole e prenda com palito ou barbante.",
            "Preaqueça o forno em temperatura média (180 °C). Arrume os rolinhos numa fôrma refratária.",
            "Em uma panela pequena, aqueça a manteiga, o leite de coco e o gengibre em fogo brando até a manteiga derreter.",
            "Despeje sobre os peitos e asse por cerca de 40 minutos, até dourar e ficar macio.",
        ],
        "notes": "Proteja as pontas dos palitos com papel-alumínio ao congelar.",
    },
    {
        "cat": "aves",
        "slug": "enrolados-de-frango",
        "title": "Enrolados de frango",
        "category_label": "Aves · Frango",
        "meta": [("Rendimento", "4 porções")],
        "ingredients": [
            "2 peitos de frango (cerca de 1 kg no total)",
            "Sal e pimenta-do-reino a gosto",
            "1¼ xícara de água",
            "¼ xícara de arroz cru",
            "1 colher (sopa) de cebolinha verde picada",
            "1 cenoura descascada e ralada",
            "1 pimentão verde cortado em quadradinhos",
            "1 colher (chá) de casca ralada de laranja",
            "Manteiga para pincelar",
            "1 xícara de suco de laranja",
            "1 colher (sopa) de maisena",
            "1 pitada de sal",
        ],
        "steps": [
            "Retire a pele e os ossos dos peitos e divida cada filé ao meio (4 pedaços).",
            "Bata os filés finos com um martelo de carne. Tempere com sal e pimenta.",
            "Misture água, arroz, cebolinha, cenoura, pimentão e casca de laranja. Tempere, tampe e cozinhe em fogo baixo por cerca de 20 minutos, até o arroz ficar macio e a água secar.",
            "Espalhe o recheio de arroz sobre os filés, enrole e prenda com palitos.",
            "Arrume numa assadeira, pincele com manteiga, cubra com papel-alumínio e asse a 180 °C por cerca de 20 minutos, até ficar macio.",
            "Para o molho: misture suco de laranja, maisena e uma pitada de sal. Cozinhe mexendo até formar um creme espesso.",
            "Sirva os enrolados com o molho de laranja por cima.",
        ],
        "notes": "Antes de congelar, embeba os rolinhos no molho para não ressecarem.",
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
            "2 colheres (sopa) de salsa picadinha",
        ],
        "steps": [
            "Preaqueça o forno a 180 °C. Faça um corte em cada metade de peito, como uma bolsa.",
            "Coloque uma fatia de bacon dentro de cada bolsa e tempere com sal e pimenta. Prenda com palitos ou amarre com barbante.",
            "Arrume os filés numa assadeira, regue com azeite e polvilhe orégano. Asse por cerca de 40 minutos, até dourar e ficar macio.",
            "Retire do forno, transfira os pedaços para um recipiente de alumínio e tampe. Mantenha aquecido no forno desligado.",
            "Coloque a assadeira no fogo brando, acrescente o leite e o requeijão e misture com os resíduos do frango até formar um molho uniforme.",
            "Cubra o frango com o molho e sirva salpicado com salsa.",
        ],
    },
    {
        "cat": "aves",
        "slug": "frango-assado-com-cerveja",
        "title": "Frango assado com cerveja",
        "category_label": "Aves · Frango",
        "meta": [("Rendimento", "4 porções"), ("Tempo", "cerca de 1 h 40 min")],
        "ingredients": [
            "1 frango (cerca de 1,8 kg) limpo e cortado em pedaços pelas juntas",
            "Sal e pimenta-do-reino a gosto",
            "5 dentes de alho descascados e amassados",
            "1 cebola grande picada",
            "4 folhas de louro",
            "2 latas de cerveja",
        ],
        "steps": [
            "Preaqueça o forno em temperatura alta (200 °C).",
            "Tempere os pedaços de frango com sal, pimenta e alho. Coloque numa assadeira.",
            "Acrescente a cebola e as folhas de louro. Despeje a cerveja por cima.",
            "Leve ao forno e asse até o frango dourar e ficar macio (cerca de 1 h 40 min), regando de vez em quando com o caldo da assadeira.",
        ],
        "notes": "Pode dividir o frango em porções separadas para congelar.",
    },
    {
        "cat": "aves",
        "slug": "frango-na-pucara",
        "title": "Frango na púcara",
        "category_label": "Aves · Frango",
        "meta": [("Rendimento", "4 porções"), ("Tempo", "cerca de 1 h 30 min")],
        "ingredients": [
            "100 g de presunto cru",
            "4 tomates maduros",
            "2 dentes de alho descascados",
            "1 frango (cerca de 1,8 kg) limpo e cortado em pedaços pelas juntas",
            "Sal e pimenta-do-reino a gosto",
            "10 cebolas bem pequenas inteiras",
            "4 colheres (sopa) de manteiga gelada cortada em cubinhos",
            "⅓ xícara de vinho do Porto",
            "½ xícara de conhaque",
            "1 xícara de vinho branco seco",
            "2 colheres (sopa) de mostarda",
        ],
        "steps": [
            "Corte o presunto em cubinhos de 0,5 cm e deixe de molho em água fria até perder o sal.",
            "Descasque os tomates, retire as sementes e corte em cubinhos de 1 cm.",
            "Preaqueça o forno a 200 °C. Esmague os dentes de alho.",
            "Tempere os pedaços de frango com sal e pimenta e distribua numa panela de barro refratária com tampa.",
            "Acrescente o presunto escorrido, o tomate, o alho e as cebolinhas inteiras.",
            "Distribua a manteiga sobre o frango. Regue com o vinho do Porto, o conhaque e o vinho branco.",
            "Junte a mostarda, tampe bem e leve ao forno até o frango ficar cozido e macio (cerca de 1 hora).",
            "Destampe e volte ao forno até a superfície dourar (cerca de 30 minutos).",
        ],
        "notes": "Clássico da cozinha regional portuguesa. Sirva na panela de barro com batatas fritas e arroz.",
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
            "3 colheres (sopa) de pó de caril (curry)",
            "1½ xícara de água",
            "4 a 5 tomates",
            "2 colheres (sopa) de folhas de coentro picadas",
            "1 potinho de iogurte natural",
            "1 colher (sopa) de suco de limão",
        ],
        "steps": [
            "Lave e seque os pedaços de frango. Polvilhe com 2 colheres (chá) de sal.",
            "Em uma panela grande, aqueça o óleo e frite o frango por 3 a 4 minutos, virando com um garfo sem deixar dourar. Transfira para um prato.",
            "Na mesma panela, refogue cebola, alho e gengibre por 4 minutos, até a cebola ficar macia e dourada.",
            "Abaixe o fogo, acrescente 1 colher de caril e 1 colher de água. Cozinhe 2 minutos mexendo. Junte os tomates descascados e sem sementes picados, 1 colher de coentro, o iogurte e o sal restante.",
            "Aumente um pouco o fogo, devolva o frango com os sucos do prato e deixe ferver, virando os pedaços para cozinhar uniformemente.",
            "Abaixe ao mínimo, tampe bem e cozinhe por 25 minutos, até o frango ficar macio.",
            "Retire do fogo, acrescente o suco de limão e misture bem.",
        ],
        "notes": "Sirva com arroz branco, polvilhado com caril e coentro.",
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
            "Em uma panela grande, coloque o óleo, a cebola, o alho amassado, o bacon e o pimentão picado. Leve ao fogo para fritar o bacon e refogar os legumes.",
            "Acrescente o frango, os tomates picados, o purê de tomate, a páprica, o açúcar, sal e pimenta. Tampe e deixe cozinhar.",
            "Junte as azeitonas e 2 colheres de salsa. Cozinhe um pouco mais com a panela destampada.",
            "Sirva salpicado com o restante da salsa.",
        ],
        "notes": "A páprica existe em versão doce ou picante.",
    },
    {
        "cat": "aves",
        "slug": "peru-recheado-com-risoto",
        "title": "Peru recheado com risoto",
        "category_label": "Aves · Outras aves",
        "meta": [("Rendimento", "12 porções"), ("Tempo", "4 a 5 h no forno")],
        "ingredients": [
            "½ xícara de uvas-passas pretas",
            "1 xícara de champanha",
            "4 colheres (sopa) de manteiga",
            "1 cebola picada",
            "2 xícaras de arroz",
            "4 xícaras de caldo de galinha",
            "2 xícaras de castanhas de caju",
            "1 xícara de manteiga",
            "2 cebolas picadas",
            "1 lata de purê de tomate",
            "1 colher (sopa) de sal",
            "2 colheres (chá) de pimenta-do-reino branca",
            "2 xícaras de champanha",
            "1 peru de 4 a 5 kg",
        ],
        "steps": [
            "Coloque as passas numa tigela, cubra com 1 xícara de champanha e deixe de molho.",
            "Para o risoto: derreta 4 colheres de manteiga em fogo baixo, doure a cebola, acrescente o arroz e refogue até soltar. Cubra com o caldo e cozinhe até o arroz ficar macio mas firme (al dente).",
            "Retire do fogo, acrescente as passas escorridas e as castanhas picadas. Regue com a champanha do molho das passas e misture com cuidado.",
            "Derreta 1 xícara de manteiga em fogo baixo. Retire do fogo e misture as cebolas, o purê de tomate, o sal, a pimenta e as 2 xícaras de champanha.",
            "Tempere o peru inteiro com essa mistura, levantando a pele do peito para espalhar por baixo.",
            "Recheie o peru com o risoto. Cubra com papel-alumínio e asse em forno alto preaquecido (200 °C) por 4 a 5 horas, regando com caldo de galinha. Retire o papel 40 minutos antes para dourar.",
        ],
        "notes": "Calcule cerca de 1 hora de forno para cada quilo de peru. Sirva com gomos de laranja.",
    },
    {
        "cat": "doces",
        "slug": "bolacha-de-nescau",
        "title": "Bolacha de Nescau",
        "category_label": "Doces · Biscoitos",
        "meta": [("Rendimento", "cerca de 20 bolachas"), ("Tempo", "15 min no forno")],
        "ingredients": [
            "1 copo de farinha de trigo",
            "1 copo de Nescau (achocolatado em pó)",
            "1 ovo",
            "3 colheres de margarina",
        ],
        "steps": [
            "Misture todos os ingredientes até formar uma massa homogênea.",
            "Modele bolachas achatadas e marque com um garfo.",
            "Leve ao forno preaquecido por cerca de 15 minutos, até firmar.",
        ],
        "notes": "Receita de 4 ingredientes (Instagram).",
    },
]


def render_recipe(r: dict) -> str:
    cat = r["cat"]
    title = r["title"]
    slug = r["slug"]
    cat_label = r["category_label"]
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
    nav_cat = cat
    if cat == "tortas-salgadas":
        nav_cat = "tortas-salgadas"
    nav_label = cat_label.split(" · ")[0]
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
        <a href="../../index.html#{nav_cat}">{html.escape(nav_label)}</a>
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
        <p class="category">{html.escape(cat_label)}</p>
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


def write_recipes() -> list[dict]:
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
    return written


def insert_sorted_li(ul_content: str, href: str, title: str) -> str:
    new_li = (
        f'          <li>\n'
        f'            <a href="{href}">{html.escape(title)}</a>\n'
        f"          </li>\n"
    )
    items = re.findall(r"          <li>.*?</li>\n", ul_content, re.S)
    if not items:
        return ul_content + new_li
    titles = []
    for item in items:
        m = re.search(r">([^<]+)</a>", item)
        titles.append((m.group(1).lower() if m else "", item))
    titles.append((title.lower(), new_li))
    titles.sort(key=lambda x: x[0])
    return "".join(t for _, t in titles)


def update_index(new_recipes: list[dict]) -> None:
    index_path = ROOT / "index.html"
    text = index_path.read_text(encoding="utf-8")

    for r in new_recipes:
        cat = r["cat"]
        slug = r["slug"]
        title = r["title"]
        href = f"./receitas/{cat}/{slug}.html"
        cat_label = r["category_label"]

        if cat == "aves":
            if "Outras aves" in cat_label:
                pattern = (
                    r'(<h3 class="subcategory">Outras aves</h3>\s*'
                    r'<ul class="recipe-list" data-subcategory="Outras aves">\n)(.*?)(        </ul>)'
                )
            else:
                pattern = (
                    r'(<h3 class="subcategory">Frango</h3>\s*'
                    r'<ul class="recipe-list" data-subcategory="Frango">\n)(.*?)(        </ul>)'
                )
        elif cat == "doces" and "Biscoitos" in cat_label:
            pattern = (
                r'(<h3 class="subcategory">Biscoitos</h3>\s*'
                r'<ul class="recipe-list" data-subcategory="Biscoitos">\n)(.*?)(        </ul>)'
            )
        elif cat == "tortas-salgadas":
            pattern = (
                r'(<section class="category-block" id="tortas-salgadas">\s*'
                r'<h2>Tortas salgadas</h2>\s*<ul class="recipe-list">\n)(.*?)(        </ul>)'
            )
        elif cat == "acompanhamentos":
            pattern = (
                r'(<section class="category-block" id="acompanhamentos">\s*'
                r'<h2>Acompanhamentos</h2>\s*<ul class="recipe-list">\n)(.*?)(        </ul>)'
            )
        else:
            print(f"skip index update for {slug} (unknown section)")
            continue

        m = re.search(pattern, text, re.S)
        if not m:
            raise SystemExit(f"Could not find index section for {slug}")
        if href in m.group(2):
            continue
        new_ul = insert_sorted_li(m.group(2), href, title)
        text = text[: m.start(2)] + new_ul + text[m.end(2) :]
        print(f"index + {title}")

    index_path.write_text(text, encoding="utf-8")


def main() -> None:
    written = write_recipes()
    if written:
        update_index(written)
    print(f"Created {len(written)} recipes")


if __name__ == "__main__":
    main()
