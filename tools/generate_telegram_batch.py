#!/usr/bin/env python3
"""Generate recipe fichas from Telegram pending batch (Aug 2026)."""
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
        "category": "Acompanhamentos",
        "meta": [("Rendimento", "10 porções"), ("Tempo", "~30 min + esfriar")],
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
            "Preaqueça o forno em temperatura média (180 °C). Limpe os fígados, retirando todos os filamentos.",
            "No liquidificador, bata os fígados com ovos, gemas, sal, pimenta e manjericão por 1 minuto.",
            "Acrescente o molho branco e o vinho ou conhaque; bata mais 15 segundos. Passe por peneira sobre uma terrina.",
            "Despeje numa fôrma de pão inglês untada (7 × 12 × 25 cm, ~5 xícaras). Asse em banho-maria no forno preaquecido por cerca de 30 minutos.",
            "Deixe esfriar. Para servir quente, descongele, cubra com papel alumínio e aqueça em forno bem baixo.",
        ],
        "notes": "Congele na fôrma ou desenforme, embale em filme e congele. Decore com tiras de pimentão vermelho em conserva e sirva com torradas.",
    },
    {
        "cat": "tortas-salgadas",
        "slug": "torta-de-frango",
        "title": "Torta de frango",
        "category": "Tortas salgadas",
        "meta": [("Rendimento", "6 a 8 porções"), ("Tempo", "~1 h 30")],
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
            "2 cenouras raladas grosso e cozidas",
            "2 colheres (sopa) de cebolinha verde picada",
            "2 colheres (sopa) de maionese",
            "3 colheres (sopa) de farinha de trigo",
            "1 colher (sopa) de purê de tomate",
            "1 gema",
        ],
        "steps": [
            "Cozinhe o frango e desfie. Misture com queijo, leite, cebola e orégano; cubra e leve à geladeira para marinar.",
            "Descasque as batatas, cozinhe em cubos, escorra e passe pelo espremedor. Junte 4 colheres de manteiga, ⅓ xícara de leite, sal, salsa e reserve o purê.",
            "Escorra o líquido da marinada e reserve. Misture o frango com cenoura, cebolinha e maionese; tempere.",
            "Derreta a manteiga restante, polvilhe a farinha e doure. Retire do fogo, junte o líquido da marinada mexendo, volte ao fogo com o purê de tomate e cozinhe até engrossar.",
            "Junte o molho ao frango. Coloque numa fôrma refratária de 2 litros, cubra com o purê e faça sulcos com um garfo.",
            "Bata a gema com 2 colheres de água e pincele a superfície. Asse em forno alto (200 °C) por cerca de 50 minutos até dourar.",
        ],
        "notes": "Para congelar crua, pincele com gema só depois de descongelar.",
    },
    {
        "cat": "aves",
        "slug": "enroladinhos-meireles",
        "title": "Enroladinhos Meireles",
        "category": "Aves · Frango",
        "meta": [("Rendimento", "6 a 8 porções"), ("Tempo", "~50 min")],
        "ingredients": [
            "4 peitos de frango sem osso cortados ao meio",
            "Sal a gosto",
            "1 cenoura ralada grosso",
            "⅓ xícara de uvas-passas pretas sem sementes",
            "1 maçã verde com casca ralada grosso",
            "2 colheres (sopa) de vinho branco ou vinagre de maçã",
            "4 colheres (sopa) de manteiga ou margarina",
            "1 garrafinha de leite de coco",
            "1 colher (chá) de gengibre ralado",
        ],
        "steps": [
            "Abra cada metade de peito formando um bife largo e tempere com sal.",
            "Misture cenoura, passas, maçã, vinagre e sal. Divida em 8 porções e recheie cada peito; enrole e prenda com palito ou barbante.",
            "Preaqueça o forno a 180 °C. Arrume os enrolados num refratário.",
            "Derreta manteiga, leite de coco e gengibre em fogo baixo; despeje sobre o frango.",
            "Asse por cerca de 40 minutos até dourar e ficar macio. Deixe esfriar e congele.",
        ],
        "notes": "Proteja as pontas dos palitos com papel alumínio ao embalar para congelar.",
    },
    {
        "cat": "aves",
        "slug": "enrolados-de-frango",
        "title": "Enrolados de frango",
        "category": "Aves · Frango",
        "meta": [("Rendimento", "4 porções"), ("Tempo", "~1 h")],
        "ingredients": [
            "2 peitos de frango (cerca de 1 kg)",
            "Sal e pimenta-do-reino a gosto",
            "1¼ xícara de água",
            "¼ xícara de arroz cru",
            "1 colher (sopa) de cebolinha verde picada",
            "1 cenoura descascada e ralada",
            "1 pimentão verde em cubinhos",
            "1 colher (chá) de casca ralada de laranja",
            "Manteiga para pincelar",
            "Molho: 1 xícara de suco de laranja, 1 colher (sopa) de maisena, pitada de sal",
        ],
        "steps": [
            "Retire pele e osso dos peitos e divida em 4 filés. Bata com martelo até ficarem finos; tempere.",
            "Cozinhe arroz com água, cebolinha, cenoura, pimentão e casca de laranja tampado em fogo baixo (~20 min) até o arroz absorver o líquido.",
            "Espalhe o recheio nos filés, enrole e prenda com palitos. Arrume num refratário, pincele manteiga, cubra com papel alumínio e asse a 180 °C por ~20 minutos.",
            "Para o molho: misture suco de laranja, maisena e sal; cozinhe mexendo até engrossar. Deixe esfriar.",
        ],
        "notes": "Antes de congelar os enrolados, embeba-os no molho para não ressecar. Congele molho à parte.",
    },
    {
        "cat": "aves",
        "slug": "files-de-frango-recheados",
        "title": "Filés de frango recheados",
        "category": "Aves · Frango",
        "meta": [("Rendimento", "4 a 6 porções"), ("Tempo", "~50 min")],
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
            "Preaqueça o forno a 180 °C. Faça um corte em cada metade de peito formando uma bolsa.",
            "Recheie cada bolsa com uma fatia de bacon; tempere e prenda com palitos ou barbante.",
            "Arrume numa assadeira, regue com azeite, polvilhe orégano e asse ~40 minutos até dourar.",
            "Retire o frango, embrulhe em alumínio e mantenha aquecido no forno desligado.",
            "Na assadeira ao fogo brando, junte leite e requeijão aos sucos; misture até formar molho uniforme.",
            "Cubra o frango com o molho, deixe esfriar e congele. Na hora de servir, polvilhe salsa.",
        ],
    },
    {
        "cat": "aves",
        "slug": "frango-assado-com-cerveja",
        "title": "Frango assado com cerveja",
        "category": "Aves · Frango",
        "meta": [("Rendimento", "4 porções"), ("Tempo", "~1 h 40")],
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
            "Tempere os pedaços com sal, pimenta e alho; coloque numa assadeira.",
            "Junte cebola e louro; despeje a cerveja por cima.",
            "Asse até dourar e ficar macio (cerca de 1 h 40), regando de vez em quando com o caldo. Deixe esfriar e congele.",
        ],
        "notes": "Pode dividir em porções separadas para congelar.",
    },
    {
        "cat": "aves",
        "slug": "frango-na-pucara",
        "title": "Frango na púcara",
        "category": "Aves · Frango",
        "meta": [("Rendimento", "4 porções"), ("Tempo", "~1 h 30")],
        "ingredients": [
            "100 g de presunto cru",
            "4 tomates maduros",
            "2 dentes de alho descascados",
            "1 frango (cerca de 1,8 kg) limpo e cortado em pedaços pelas juntas",
            "Sal e pimenta-do-reino a gosto",
            "10 cebolas bem pequenas inteiras",
            "4 colheres (sopa) de manteiga gelada em cubinhos",
            "⅓ xícara de vinho do Porto",
            "½ xícara de conhaque",
            "1 xícara de vinho branco seco",
            "2 colheres (sopa) de mostarda",
        ],
        "steps": [
            "Corte o presunto em cubos de 0,5 cm e deixe de molho em água fria para tirar o sal.",
            "Descasque os tomates, retire as sementes e corte em cubos de 1 cm.",
            "Preaqueça o forno a 200 °C. Amasse o alho.",
            "Tempere o frango e distribua numa púcara refratária com tampa.",
            "Acrescente presunto escorrido, tomate, alho e cebolinhas; distribua a manteiga.",
            "Regue com Porto, conhaque e vinho branco; junte a mostarda, tampe e leve ao forno por ~1 h.",
            "Destampe e volte ao forno até dourar a superfície (~30 min). Deixe esfriar e congele.",
        ],
        "notes": "Prato clássico da cozinha regional portuguesa. Sirva com batatas fritas palito e arroz.",
    },
    {
        "cat": "aves",
        "slug": "frango-ao-caril",
        "title": "Frango ao caril",
        "category": "Aves · Frango",
        "meta": [("Rendimento", "4 a 6 porções"), ("Tempo", "~45 min")],
        "ingredients": [
            "1 kg de coxas, sobrecoxas e peitos de frango",
            "3 colheres (chá) de sal",
            "½ xícara de óleo",
            "2 cebolas picadas",
            "4 dentes de alho picados",
            "1½ colher (chá) de gengibre ralado",
            "3 colheres (sopa) de pó de caril",
            "1½ xícara de água",
            "4 a 5 tomates",
            "2 colheres (sopa) de folhas de coentro picadas",
            "1 potinho de iogurte natural",
            "1 colher (sopa) de suco de limão",
        ],
        "steps": [
            "Lave e seque o frango; polvilhe com 2 colheres (chá) de sal.",
            "Aqueça bem o óleo e frite o frango 3–4 minutos sem dourar; reserve.",
            "Na mesma panela, refogue cebola, alho e gengibre por ~4 minutos.",
            "Em fogo baixo, junte 1 colher de caril e 1 colher de água; cozinhe 2 minutos mexendo. Acrescente tomate sem pele e semente, 1 colher de coentro, iogurte e o sal restante.",
            "Volte o frango com os sucos, junte o restante da água e deixe ferver; vire os pedaços para cozinhar uniformemente.",
            "Tampe em fogo mínimo por ~25 minutos até macio. Retire do fogo, misture o limão, arrume numa travessa e despeje o molho. Deixe esfriar e congele.",
        ],
        "notes": "Ao servir, polvilhe caril e coentro restantes. Acompanhe arroz branco.",
    },
    {
        "cat": "aves",
        "slug": "frango-estufado-com-tomates",
        "title": "Frango estufado com tomates",
        "category": "Aves · Frango",
        "meta": [("Rendimento", "2 porções"), ("Tempo", "~40 min")],
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
            "Numa panela grande, frite bacon com óleo, cebola, alho e pimentão picado.",
            "Junte o frango, tomates picados, purê, páprica, açúcar, sal e pimenta; tampe e cozinhe.",
            "Acrescente azeitonas e 2 colheres de salsa; cozinhe um pouco mais destampado. Deixe esfriar e congele.",
        ],
        "notes": "Páprica existe em versão doce ou picante.",
    },
    {
        "cat": "aves",
        "slug": "peru-recheado-com-risoto",
        "title": "Peru recheado com risoto",
        "category": "Aves · Outras aves",
        "meta": [("Rendimento", "12 porções"), ("Tempo", "4 a 5 h no forno")],
        "ingredients": [
            "Risoto: ½ xícara de uvas-passas pretas, 1 xícara de champanha, 4 colheres (sopa) de manteiga, 1 cebola picada, 2 xícaras de arroz, 4 xícaras de caldo de galinha, 2 xícaras de castanhas de caju",
            "Peru: 1 xícara de manteiga, 2 cebolas picadas, 1 lata de purê de tomate, 1 colher (sopa) de sal, 2 colheres (chá) de pimenta-branca, 2 xícaras de champanha, 1 peru de 4 a 5 kg",
        ],
        "steps": [
            "Deixe as passas de molho na champanha. Derreta 4 colheres de manteiga, doure a cebola, junte o arroz e frite. Cubra com caldo e cozinhe até ficar al dente.",
            "Retire do fogo, misture passas escorridas e castanhas picadas; regue com a champanha das passas. Congele o risoto à parte.",
            "Derreta 1 xícara de manteiga, junte cebolas, purê, sal, pimenta e champanha; tempere todo o peru, levantando a pele do peito.",
            "Na hora de assar, recheie o peru com o risoto. Cubra com papel alumínio e asse em forno alto (200 °C) por 4 a 5 horas, regando com caldo.",
            "Retire o papel 40 minutos antes para dourar. Sirva com gomos de laranja.",
        ],
        "notes": "Calcule cerca de 1 hora de forno para cada quilo de peru.",
    },
    {
        "cat": "doces",
        "slug": "bolacha-de-nescau",
        "title": "Bolacha de Nescau",
        "category": "Doces · Biscoitos",
        "meta": [("Rendimento", "~20 unidades"), ("Tempo", "15 min no forno")],
        "ingredients": [
            "1 copo de farinha de trigo",
            "1 copo de Nescau",
            "1 ovo",
            "3 colheres de margarina",
        ],
        "steps": [
            "Misture todos os ingredientes até formar uma massa homogênea.",
            "Faça bolinhas, achate levemente com um garfo e disponha numa assadeira.",
            "Leve ao forno preaquecido por cerca de 15 minutos até firmar.",
        ],
        "notes": "Receita de Pinterest (4 ingredientes).",
    },
    {
        "cat": "doces",
        "slug": "cheesecake-basque-de-chocolate",
        "title": "Cheesecake basque de chocolate",
        "category": "Doces · Tortas e bolos",
        "meta": [("Rendimento", "8 a 10 fatias"), ("Tempo", "~1 h no forno")],
        "ingredients": [
            "500 g de cream cheese em temperatura ambiente",
            "150 g de açúcar",
            "4 ovos",
            "150 g de chocolate meio amargo (70%) derretido",
            "200 ml de creme de leite",
            "1 colher (chá) de essência de baunilha",
        ],
        "steps": [
            "Preaqueça o forno a 200 °C. Forre uma forma redonda de fundo removível com papel manteiga.",
            "Bata o cream cheese com o açúcar até ficar liso.",
            "Acrescente os ovos um a um, batendo após cada adição.",
            "Incorpore o chocolate derretido e o creme de leite; misture até homogêneo.",
            "Despeje na forma e asse até a superfície queimar e o centro ficar levemente bamboleante (~50–60 min).",
            "Deixe esfriar completamente e leve à geladeira por pelo menos 4 horas antes de servir.",
        ],
        "notes": "Cheesecake basco — superfície caramelizada, interior cremoso.",
    },
    {
        "cat": "doces",
        "slug": "cheesecake-basque-de-matcha",
        "title": "Cheesecake basque de matcha",
        "category": "Doces · Tortas e bolos",
        "meta": [("Rendimento", "8 a 10 fatias"), ("Tempo", "~1 h no forno")],
        "ingredients": [
            "500 g de cream cheese",
            "200 g de açúcar",
            "250 ml de creme de leite",
            "4 ovos",
            "1 colher e meia (sopa) de farinha de trigo",
            "1 colher e meia (sopa) de matcha em pó",
        ],
        "steps": [
            "Preaqueça o forno a 200 °C. Forre uma forma redonda de fundo removível com papel manteiga.",
            "Bata o cream cheese com o açúcar até liso.",
            "Misture o creme de leite e a farinha peneirada.",
            "Acrescente os ovos um a um.",
            "Incorpore o matcha peneirado delicadamente.",
            "Despeje na forma e asse até dourar por cima e o centro ficar levemente bamboleante.",
            "Esfrie e leve à geladeira por pelo menos 4 horas.",
        ],
        "notes": "Cheesecake basco com matcha.",
    },
]

INDEX_INSERTS: dict[str, list[tuple[str, str, str]]] = {
    "acompanhamentos": [
        ("pate-de-figado-de-galinha", "Patê de fígado de galinha", ""),
    ],
    "tortas-salgadas": [
        ("torta-de-frango", "Torta de frango", ""),
    ],
    "aves": [
        ("enroladinhos-meireles", "Enroladinhos Meireles", "Frango"),
        ("enrolados-de-frango", "Enrolados de frango", "Frango"),
        ("files-de-frango-recheados", "Filés de frango recheados", "Frango"),
        ("frango-assado-com-cerveja", "Frango assado com cerveja", "Frango"),
        ("frango-ao-caril", "Frango ao caril", "Frango"),
        ("frango-estufado-com-tomates", "Frango estufado com tomates", "Frango"),
        ("frango-na-pucara", "Frango na púcara", "Frango"),
        ("peru-recheado-com-risoto", "Peru recheado com risoto", "Outras aves"),
    ],
    "doces": [
        ("bolacha-de-nescau", "Bolacha de Nescau", "Biscoitos"),
        ("cheesecake-basque-de-chocolate", "Cheesecake basque de chocolate", "Tortas e bolos"),
        ("cheesecake-basque-de-matcha", "Cheesecake basque de matcha", "Tortas e bolos"),
    ],
}


def render_recipe(r: dict) -> str:
    cat = r["cat"]
    cat_label = r["category"]
    title = r["title"]
    slug = r["slug"]
    nav_cat = cat if cat != "tortas-salgadas" else "tortas-salgadas"
    nav_label = {
        "acompanhamentos": "Acompanhamentos",
        "tortas-salgadas": "Tortas salgadas",
        "aves": "Aves",
        "doces": "Doces",
    }[cat]
    desc = html.escape(f"{title} — ficha A5 para imprimir.")
    meta_html = ""
    if r.get("meta"):
        spans = "".join(
            f"\n          <span><strong>{html.escape(k)}:</strong> {html.escape(v)}</span>"
            for k, v in r["meta"]
        )
        meta_html = f"\n        <div class=\"meta\">{spans}\n        </div>"
    ingredients = "\n".join(
        f"          <li>{html.escape(i)}</li>" for i in r["ingredients"]
    )
    steps = "\n".join(f"          <li>{html.escape(s)}</li>" for s in r["steps"])
    notes = ""
    if r.get("notes"):
        notes = f"""
        <p class="notes">{html.escape(r['notes'])}</p>"""
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


def insert_index_entries() -> None:
    index_path = ROOT / "index.html"
    text = index_path.read_text(encoding="utf-8")

    for section_id, entries in INDEX_INSERTS.items():
        for slug, title, sub in entries:
            if section_id == "aves":
                cat_path = "aves"
                href = f"./receitas/{cat_path}/{slug}.html"
                li = f"""          <li>
            <a href="{href}">{html.escape(title)}</a>
          </li>\n"""
                marker = f'data-subcategory="{sub}"'
                pos = text.find(marker)
                if pos == -1:
                    raise SystemExit(f"subcategory {sub} not found")
                ul_end = text.find("</ul>", pos)
                text = text[:ul_end] + li + text[ul_end:]
            elif section_id == "doces":
                href = f"./receitas/doces/{slug}.html"
                li = f"""          <li>
            <a href="{href}">{html.escape(title)}</a>
          </li>\n"""
                marker = f'data-subcategory="{sub}"'
                pos = text.find(marker)
                if pos == -1:
                    raise SystemExit(f"subcategory {sub} not found")
                ul_end = text.find("</ul>", pos)
                text = text[:ul_end] + li + text[ul_end:]
            else:
                href = f"./receitas/{section_id}/{slug}.html"
                li = f"""          <li>
            <a href="{href}">{html.escape(title)}</a>
          </li>\n"""
                sec = f'id="{section_id}"'
                pos = text.find(sec)
                if pos == -1:
                    raise SystemExit(f"section {section_id} not found")
                ul_start = text.find('<ul class="recipe-list">', pos)
                ul_end = text.find("</ul>", ul_start)
                block = text[ul_start:ul_end]
                if slug in block:
                    continue
                text = text[:ul_end] + li + text[ul_end:]

    index_path.write_text(text, encoding="utf-8")
    print("Updated index.html")


def write_recipes() -> None:
    for r in RECIPES:
        out = ROOT / "receitas" / r["cat"] / f"{r['slug']}.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_recipe(r), encoding="utf-8")
        print(f"wrote {out.relative_to(ROOT)}")


def main() -> None:
    write_recipes()
    insert_index_entries()
    print(f"Done: {len(RECIPES)} recipes")


if __name__ == "__main__":
    main()
