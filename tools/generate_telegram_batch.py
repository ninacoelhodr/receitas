#!/usr/bin/env python3
"""Generate recipe fichas from the 2026-07-31 Telegram pending batch."""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CAT_LABELS = {
    "doces": "Doces",
    "salgados": "Salgados",
    "tortas-salgadas": "Tortas salgadas",
    "aves": "Aves",
}

RECIPES: list[dict] = [
    {
        "cat": "salgados",
        "sub": "Petiscos",
        "slug": "pate-de-figado-de-galinha",
        "title": "Patê de fígado de galinha",
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
            "Preaqueça o forno em temperatura média (180 °C). Limpe os fígados, retirando todos os filamentos. Coloque os fígados no liquidificador com os ovos, as gemas, o sal, a pimenta-do-reino e o manjericão. Bata por 1 minuto.",
            "Adicione o molho branco e o vinho ou conhaque, e bata por mais 15 segundos. Passe por uma peneira e deixe cair sobre uma terrina.",
            "Coloque a mistura numa fôrma de pão ou bolo inglês untada (7 × 12 × 25 cm, capacidade de 5 xícaras). Leve ao forno preaquecido, dentro de uma assadeira com água fervente, e asse por cerca de 30 minutos. Deixe esfriar e congele.",
        ],
        "notes": "Congelamento: coloque a fôrma com o patê dentro de um saco plástico e leve ao freezer para endurecer; retire da fôrma, embale em filme plástico, etiquete e congele. Descongelamento: descongele de um dia para o outro na geladeira. Decore com tiras de pimentão vermelho em conserva e sirva com torradas. Para servir quente, cubra com papel-alumínio e aqueça em forno bem baixo.",
    },
    {
        "cat": "tortas-salgadas",
        "sub": None,
        "slug": "torta-de-frango",
        "title": "Torta de frango",
        "meta": [("Rendimento", "6 a 8 porções")],
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
            "Cozinhe e desfie o frango. Coloque num refratário raso e acrescente o queijo, o leite, a cebola e o orégano. Tampe e leve à geladeira para marinar.",
            "Descasque as batatas, corte em cubos e cozinhe em água e sal. Escorra, passe no espremedor e misture 4 colheres de manteiga, o leite, sal a gosto e a salsa até formar purê. Reserve.",
            "Escorra o líquido da marinada do frango e reserve. Misture o frango desfiado com cenoura, cebolinha e maionese. Prove o sal.",
            "Derreta a manteiga restante numa frigideira, polvilhe a farinha e doure levemente. Retire do fogo, acrescente aos poucos o líquido da marinada, mexendo sempre. Volte ao fogo, junte o purê de tomate e cozinhe até engrossar.",
            "Misture o molho ao frango. Coloque o recheio num refratário de 2 litros, cubra com o purê e decore a superfície com o garfo.",
            "Bata a gema com 2 colheres de água e pincele a superfície. Asse em forno alto preaquecido (200 °C) por cerca de 50 minutos até dourar. Deixe esfriar e congele.",
        ],
        "notes": "Para congelar crua, pincele com gema só após descongelar. Congelamento: embrulhe o refratário em filme plástico ou saco hermético, etiquete e congele. Descongelamento: de um dia para o outro na geladeira; aqueça no forno coberto com papel-alumínio.",
    },
    {
        "cat": "aves",
        "sub": "Frango",
        "slug": "enroladinhos-meireles",
        "title": "Enroladinhos Meireles",
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
            "Corte os peitos em bifes finos e tempere com sal.",
            "Misture cenoura, passas, maçã, vinagre e sal. Divida em oito porções e coloque uma em cada pedaço de frango; enrole e prenda com palito ou barbante.",
            "Preaqueça o forno em temperatura média (180 °C). Arrume os rolinhos lado a lado num refratário.",
            "Derreta a manteiga com o leite de coco e o gengibre em fogo brando, mexendo sempre. Despeje sobre os rolinhos e asse por cerca de 40 minutos até dourar e ficar macio. Deixe esfriar e congele.",
        ],
        "notes": "Congelamento: congele em bandeja forrada; depois transfira para saco plástico, retire o ar e etiquete. Descongelamento: de um dia para o outro na geladeira; aqueça em forno baixo. Proteja as pontas dos palitos com papel-alumínio ao embalar.",
    },
    {
        "cat": "aves",
        "sub": "Frango",
        "slug": "enrolados-de-frango",
        "title": "Enrolados de frango",
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
            "Retire a pele e os ossos dos peitos e divida os filés ao meio (4 pedaços). Bata os filés com o batedor de carne até ficarem bem finos. Tempere com sal e pimenta.",
            "Misture água, arroz cru, cebolinha, cenoura, pimentão e casca de laranja. Tempere e cozinhe em fogo brando, tampado, por cerca de 20 minutos até o arroz ficar macio.",
            "Espalhe o arroz sobre os filés, enrole formando rolinhos e prenda com palitos. Arrume numa fôrma, pincele manteiga, cubra com papel-alumínio e asse a 180 °C por cerca de 20 minutos. Deixe esfriar e congele.",
            "Misture suco de laranja, maisena e pitada de sal. Leve ao fogo mexendo até formar um creme espesso. Deixe esfriar e congele separadamente.",
        ],
        "notes": "Antes de embrulhar para congelar, embeba os rolinhos no molho para não ressecar. Congelamento: congele os rolinhos na fôrma sem tampa; depois embale em saco plástico. O molho vai em recipiente rígido e depois em saco. Descongelamento: descongele na geladeira; aqueça o molho em fogo brando e os rolinhos no forno cobertos com papel-alumínio; sirva com o molho por cima.",
    },
    {
        "cat": "aves",
        "sub": "Frango",
        "slug": "files-de-frango-recheados",
        "title": "Filés de frango recheados",
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
            "Preaqueça o forno a 180 °C. Faça um corte em cada metade de peito, como uma bolsa, sem separar as duas metades.",
            "Coloque uma fatia de bacon em cada bolsa, tempere com sal e pimenta e prenda com palitos ou barbante.",
            "Arrume os filés numa assadeira, regue com azeite e polvilhe orégano. Asse por cerca de 40 minutos até dourar e ficar macio.",
            "Retire do forno. Coloque o frango numa embalagem de alumínio e tampe; mantenha aquecido no forno desligado.",
            "Leve a assadeira ao fogo brando, junte leite e requeijão e misture com os resíduos até obter um molho uniforme.",
            "Cubra o frango com o molho, deixe esfriar e congele.",
        ],
        "notes": "Congelamento: coloque a embalagem de alumínio com o frango num saco plástico, vede bem e congele. Descongelamento: descongele na geladeira de um dia para o outro; aqueça no forno, ainda tampado, em temperatura baixa. Sirva polvilhado com salsa.",
    },
    {
        "cat": "aves",
        "sub": "Frango",
        "slug": "frango-assado-com-cerveja",
        "title": "Frango assado com cerveja",
        "meta": [("Rendimento", "4 porções")],
        "ingredients": [
            "1 frango (cerca de 1,8 kg) limpo e cortado em pedaços pelas juntas",
            "Sal e pimenta-do-reino a gosto",
            "5 dentes de alho amassados",
            "1 cebola grande picada",
            "4 folhas de louro",
            "2 latas de cerveja",
        ],
        "steps": [
            "Preaqueça o forno em temperatura alta (200 °C).",
            "Tempere os pedaços de frango com sal, pimenta e alho. Coloque numa assadeira.",
            "Acrescente cebola e louro. Despeje a cerveja por cima.",
            "Asse no forno preaquecido até o frango dourar e ficar macio (cerca de 1 h 40), regando de vez em quando com o líquido da assadeira. Deixe esfriar e congele.",
        ],
        "notes": "Congelamento: coloque o frango com o molho em embalagem de alumínio, depois em saco plástico hermético, etiquete e congele. Descongelamento: descongele na geladeira de um dia para o outro; cubra com papel-alumínio e aqueça no forno. Pode dividir em porções separadas para congelar.",
    },
    {
        "cat": "aves",
        "sub": "Frango",
        "slug": "frango-na-pucara",
        "title": "Frango na púcara",
        "meta": [("Rendimento", "4 porções")],
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
            "Corte o presunto em cubos de cerca de 0,5 cm e deixe de molho em água fria até perder o sal.",
            "Descasque os tomates, retire as sementes e corte em cubos de cerca de 1 cm.",
            "Preaqueça o forno em temperatura alta (200 °C). Amasse os dentes de alho.",
            "Tempere o frango com sal e pimenta e arrume numa púcara (panela de barro com tampa).",
            "Acrescente presunto escorrido, tomate, alho amassado e cebolinhas inteiras. Distribua a manteiga por cima.",
            "Regue com vinho do Porto, conhaque e vinho branco. Junte a mostarda, tampe bem e leve ao forno até o frango cozinhar e ficar macio (cerca de 1 hora).",
            "Destampe e volte ao forno até a superfície dourar (cerca de 30 minutos). Deixe esfriar e congele.",
        ],
        "notes": "Clássico da cozinha regional portuguesa, preparado na púcara (tacho de barro com tampa). Congelamento: coloque num recipiente rígido, tampe com filme e congele; depois embale em filme plástico. Descongelamento: descongele na geladeira e aqueça na púcara tampada. Sirva com batatas palito e arroz.",
    },
    {
        "cat": "aves",
        "sub": "Frango",
        "slug": "frango-ao-caril",
        "title": "Frango ao caril",
        "meta": [("Rendimento", "4 a 6 porções")],
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
            "Lave e seque os pedaços de frango. Polvilhe com 2 colheres (chá) de sal.",
            "Aqueça bem o óleo numa panela grande e frite o frango por 3 a 4 minutos, virando com um garfo, sem deixar dourar. Transfira para um prato.",
            "Na mesma panela, refogue cebola, alho e gengibre por cerca de 4 minutos até a cebola ficar macia e dourada.",
            "Baixe o fogo, acrescente 1 colher (sopa) de caril e 1 colher (sopa) de água. Cozinhe por cerca de 2 minutos, mexendo sempre. Junte tomate sem pele nem sementes picado, 1 colher (sopa) de coentro, o iogurte e o sal restante.",
            "Aumente um pouco o fogo, devolva o frango com o caldo do prato e o restante da água. Deixe ferver, virando os pedaços para cozinhar por igual.",
            "Reduza o fogo ao mínimo, tampe bem e cozinhe por 25 minutos ou até o frango ficar macio.",
            "Retire do fogo, acrescente o suco de limão e mexa bem. Disponha numa travessa forrada com plástico, despeje o molho por cima, deixe esfriar e congele.",
        ],
        "notes": "O pó de caril é tempero indiano à base de canela, cravo, coentro, cominho, cardamomo e pimenta-do-reino. Congelamento: tampe a travessa com filme e congele; depois embale em filme plástico. Descongelamento: descongele na panela em fogo brando; polvilhe com o caril e coentro restantes e sirva com arroz branco.",
    },
    {
        "cat": "aves",
        "sub": "Frango",
        "slug": "frango-estufado-com-tomates",
        "title": "Frango estufado com tomates",
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
            "Numa panela grande, coloque óleo, cebola, alho amassado, bacon e pimentão picado. Leve ao fogo para fritar o bacon e refogar os legumes.",
            "Acrescente o frango, tomates picados, purê de tomate, páprica, açúcar, sal e pimenta. Tampe e deixe cozinhar.",
            "Junte as azeitonas e 2 colheres de salsa; cozinhe um pouco mais com a panela destampada. Deixe esfriar e congele.",
        ],
        "notes": "A páprica é tempero em pó vermelho, semelhante ao colorífico (doce ou picante). Congelamento: transfira para recipiente rígido, tampe com filme e congele; depois embale em saco plástico. Descongelamento: aqueça em banho-maria ou no micro-ondas; polvilhe com a salsa restante.",
    },
    {
        "cat": "aves",
        "sub": "Outras aves",
        "slug": "peru-recheado-com-risoto",
        "title": "Peru recheado com risoto",
        "meta": [("Rendimento", "12 porções")],
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
            "Prepare o risoto: deixe as passas de molho na champanha. Derreta 4 colheres de manteiga, doure a cebola, junte o arroz e frite até soltar. Cubra com caldo e cozinhe até o arroz ficar macio mas ainda resistente ao mordisco.",
            "Retire do fogo, acrescente passas escorridas e castanhas de caju picadas. Regue com a champanha das passas e misture até um risoto úmido. Congele separadamente.",
            "Derreta 1 xícara de manteiga, junte as 2 cebolas, purê de tomate, sal, pimenta e 2 xícaras de champanha. Tempere todo o peru com essa mistura, levantando a pele do peito para espalhar por baixo.",
            "Descongele peru e risoto na geladeira de um dia para o outro. Coloque o peru numa assadeira, recheie com o risoto, tampe com papel-alumínio e asse em forno alto preaquecido (200 °C) por 4 a 5 horas, regando com caldo de galinha. Cerca de 40 minutos antes do fim, retire o papel para dourar. Calcule cerca de 1 hora de forno por quilo de peru.",
        ],
        "notes": "Congelamento: risoto em recipiente rígido e depois em saco plástico; peru embrulhado em papel-alumínio e saco hermético. Sirva com gomos de laranja.",
    },
    {
        "cat": "doces",
        "sub": "Biscoitos",
        "slug": "bolacha-de-nescau",
        "title": "Bolacha de Nescau",
        "meta": [("Rendimento", "cerca de 15 bolachas")],
        "ingredients": [
            "1 copo de farinha de trigo",
            "1 copo de Nescau",
            "1 ovo",
            "3 colheres de margarina",
        ],
        "steps": [
            "Misture farinha, Nescau, ovo e margarina até formar uma massa homogênea.",
            "Modele bolachas, achate com um garfo e disponha numa assadeira.",
            "Leve ao forno preaquecido por cerca de 15 minutos até firmar.",
        ],
        "notes": "Receita de 4 ingredientes (fonte: Pinterest / Cozinha em Pins).",
    },
]


def category_line(r: dict) -> str:
    label = CAT_LABELS[r["cat"]]
    if r.get("sub"):
        return f"{label} · {r['sub']}"
    return label


def render_recipe(r: dict) -> str:
    cat = r["cat"]
    cat_label = CAT_LABELS[cat]
    title = r["title"]
    slug = r["slug"]
    cat_line = category_line(r)
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
        <p class="category">{html.escape(cat_line)}</p>
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


def index_link(r: dict) -> str:
    return (
        f'          <li>\n'
        f'            <a href="./receitas/{r["cat"]}/{r["slug"]}.html">{html.escape(r["title"])}</a>\n'
        f"          </li>\n"
    )


def insert_into_subcategory(text: str, cat_id: str, sub: str, link: str, title: str) -> str:
    slug = re.search(r"/([^/]+)\.html", link).group(1)
    pattern = (
        rf'(<section class="category-block" id="{re.escape(cat_id)}">.*?'
        rf'<h3 class="subcategory">{re.escape(sub)}</h3>\s*'
        rf'<ul class="recipe-list" data-subcategory="{re.escape(sub)}">\s*)'
        rf"(.*?)(\s*</ul>)"
    )
    m = re.search(pattern, text, flags=re.S)
    if not m:
        raise SystemExit(f"subcategory {cat_id}/{sub} not found")
    items = m.group(2)
    if f"{slug}.html" in items:
        return text
    entries = re.findall(r"<li>.*?</li>", items, flags=re.S)
    titles = []
    for e in entries:
        tm = re.search(r">([^<]+)</a>", e)
        titles.append((tm.group(1).strip() if tm else "", e))
    titles.append((title, link.rstrip("\n")))
    titles.sort(key=lambda x: x[0].lower())
    new_items = "".join(t[1] if t[1].startswith("          <li>") else t[1] for t in titles)
    return text[: m.start(2)] + new_items + text[m.end(2) :]


def insert_into_flat_list(text: str, cat_id: str, link: str, title: str) -> str:
    pattern = (
        rf'(<section class="category-block" id="{re.escape(cat_id)}">\s*'
        rf"<h2>[^<]+</h2>\s*"
        rf'<ul class="recipe-list">\s*)'
        rf"(.*?)(\s*</ul>)"
    )
    m = re.search(pattern, text, flags=re.S)
    if not m:
        raise SystemExit(f"flat list {cat_id} not found")
    items = m.group(2)
    slug = re.search(r"/([^/]+)\.html", link).group(1)
    if f"{slug}.html" in items:
        return text
    entries = re.findall(r"<li>.*?</li>", items, flags=re.S)
    titles = []
    for e in entries:
        tm = re.search(r">([^<]+)</a>", e)
        titles.append((tm.group(1).strip() if tm else "", e))
    titles.append((title, link.rstrip("\n")))
    titles.sort(key=lambda x: x[0].lower())
    new_items = "".join(t[1] if t[1].startswith("          <li>") else t[1] for t in titles)
    return text[: m.start(2)] + new_items + text[m.end(2) :]


def update_index(new_recipes: list[dict]) -> None:
    index_path = ROOT / "index.html"
    text = index_path.read_text(encoding="utf-8")
    for r in new_recipes:
        link = index_link(r)
        if r.get("sub"):
            text = insert_into_subcategory(text, r["cat"], r["sub"], link, r["title"])
        else:
            text = insert_into_flat_list(text, r["cat"], link, r["title"])
    index_path.write_text(text, encoding="utf-8")
    print(f"Updated index.html (+{len(new_recipes)} recipes)")


def main() -> None:
    written = write_recipes()
    if written:
        update_index(written)
    print(f"Created {len(written)} new recipes")


if __name__ == "__main__":
    main()
