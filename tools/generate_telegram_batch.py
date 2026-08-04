#!/usr/bin/env python3
"""Generate recipe fichas from Telegram photo batch (Aug 2026)."""
from __future__ import annotations

import html
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RECIPES: list[dict] = [
    {
        "cat": "acompanhamentos",
        "slug": "pate-de-figado-de-galinha",
        "title": "Patê de fígado de galinha",
        "category": "Acompanhamentos",
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
        "notes": "Livro «A arte de congelar». Para servir quente: coloque em travessa refratária, cubra com papel de alumínio e aqueça em forno baixo após descongelar.",
    },
    {
        "cat": "tortas-salgadas",
        "slug": "torta-de-frango",
        "title": "Torta de frango",
        "category": "Tortas salgadas",
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
            "Cozinhe e desfie o frango. Coloque em travessa rasa e adicione o queijo, leite, cebola e orégano. Cubra e leve à geladeira para marinar.",
            "Descasque as batatas, corte em cubos e cozinhe em água e sal.",
            "Escorra as batatas, passe pelo espremedor e coloque em tigela. Adicione 4 colheres de manteiga e o leite; misture até obter purê. Tempere com sal, junte a salsa e misture. Reserve.",
            "Em tigela, escoe o líquido onde o frango estava marinando e reserve. Em outra tigela, coloque o frango desfiado, cenoura, cebolinha e maionese. Prove o tempero e misture.",
            "Em frigideira, derreta o restante da manteiga. Polvilhe a farinha e doure levemente.",
            "Retire do fogo e adicione gradualmente o líquido reservado, mexendo sempre. Volte ao fogo, junte o purê de tomate e cozinhe até o molho engrossar.",
            "Adicione o molho à mistura de frango.",
            "Coloque a mistura de frango em travessa refratária de 2 litros, cubra com o purê de batata e decore a superfície fazendo sulcos com um garfo.",
            "Em tigela pequena, bata a gema com 2 colheres de sopa de água. Pincele a superfície da torta.",
            "Leve ao forno alto preaquecido (200 °C) por cerca de 50 minutos, até dourar. Deixe esfriar e congele.",
        ],
        "notes": "Para congelar crua, pincelar com gema batida só após descongelar. Livro «A arte de congelar».",
    },
    {
        "cat": "aves",
        "slug": "enroladinhos-meireles",
        "title": "Enroladinhos Meireles",
        "category": "Aves · Frango",
        "meta": [("Rendimento", "6 a 8 porções")],
        "ingredients": [
            "4 peitos de frango sem osso cortados ao meio",
            "Sal a gosto",
            "1 cenoura raspada no ralador grosso",
            "⅓ xícara de uvas-passas pretas sem sementes",
            "1 maçã verde com casca no ralador grosso",
            "2 colheres (sopa) de vinagre de vinho branco ou de maçã",
            "4 colheres (sopa) de manteiga ou margarina",
            "1 garrafinha de leite de coco",
            "1 colher (chá) de gengibre ralado",
        ],
        "steps": [
            "Com faca afiada, abra cada metade de peito em filé largo. Tempere cada pedaço com sal.",
            "Em tigela, misture cenoura, passas, maçã ralada, vinagre e sal; misture bem.",
            "Divida a mistura em oito partes e coloque em cada peito de frango. Enrole e prenda com palito de madeira ou barbante de cozinha.",
            "Preaqueça o forno em temperatura média (180 °C).",
            "Arrume os enrolados lado a lado em travessa refratária.",
            "Em panela pequena, misture manteiga, leite de coco e gengibre. Aqueça em fogo brando, mexendo, até a manteiga derreter.",
            "Despeje sobre os peitos. Asse no forno preaquecido por cerca de 40 minutos ou até a carne dourar e ficar macia. Deixe esfriar e congele.",
        ],
        "notes": "Proteja as pontas dos palitos com papel de alumínio ao embrulhar para congelar. Livro «A arte de congelar».",
    },
    {
        "cat": "aves",
        "slug": "enrolados-de-frango",
        "title": "Enrolados de frango",
        "category": "Aves · Frango",
        "meta": [("Rendimento", "4 porções")],
        "ingredients": [
            "2 peitos de frango (cerca de 1 kg no total)",
            "Sal e pimenta-do-reino a gosto",
            "1¼ xícaras de água",
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
            "Retire a pele e os ossos dos peitos de frango e divida os filés ao meio, obtendo 4 pedaços.",
            "Em tábua, bata os filés com o pilão até ficar bem finos. Tempere com sal e pimenta-do-reino e reserve.",
            "Em panela, misture água, arroz cru, cebolinha, cenoura, pimentão e casca de laranja. Tempere com sal e pimenta. Tampe e cozinhe em fogo brando por cerca de 20 minutos, até o arroz ficar macio e o líquido secar.",
            "Espalhe o arroz sobre os filés, enrole cada um e prenda com palitos.",
            "Arrume os enrolados lado a lado em travessa. Pincele com manteiga, cubra com papel de alumínio e asse em forno médio (180 °C) por cerca de 20 minutos, até ficarem macios. Deixe esfriar e congele.",
            "Em panela, misture suco de laranja, maisena e pitada de sal. Cozinhe mexendo até formar creme grosso. Deixe esfriar e congele.",
        ],
        "notes": "Embrulhe os enrolados no molho antes de congelar para não ressecar. Congele enrolados e molho separados. Livro «A arte de congelar».",
    },
    {
        "cat": "aves",
        "slug": "files-de-frango-recheados",
        "title": "Filés de frango recheados",
        "category": "Aves · Frango",
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
            "Preaqueça o forno em temperatura média (180 °C). Faça um corte em cada metade de peito de frango, como se fosse uma bolsa.",
            "Coloque uma fatia de bacon dentro de cada bolsa e tempere com sal e pimenta-do-reino. Prenda os filés com palitos de madeira ou amarre com barbante.",
            "Arrume os filés numa assadeira, um ao lado do outro, regue com o azeite e polvilhe com orégano. Leve ao forno preaquecido e asse por cerca de 40 minutos ou até a carne dourar e ficar macia.",
            "Retire do forno. Coloque os pedaços de frango numa embalagem de alumínio e tampe. Mantenha aquecido no forno desligado.",
            "Leve a assadeira onde estava o frango ao fogo brando, junte o leite e o requeijão, e misture bem com os resíduos do frango até obter molho uniforme.",
            "Cubra o frango com esse molho, deixe esfriar e congele.",
        ],
        "notes": "Livro «A arte de congelar».",
    },
    {
        "cat": "aves",
        "slug": "frango-assado-com-cerveja",
        "title": "Frango assado com cerveja",
        "category": "Aves · Frango",
        "meta": [("Rendimento", "4 porções")],
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
            "Tempere os pedaços de frango com sal, pimenta-do-reino e alho. Coloque-os numa assadeira.",
            "Junte a cebola e as folhas de louro. Despeje a cerveja por cima do frango.",
            "Leve ao forno preaquecido e deixe assar até o frango dourar e ficar macio (cerca de 1 hora e 40 minutos), banhando de vez em quando com o caldo da assadeira. Retire do forno, deixe esfriar e congele.",
        ],
        "notes": "Pode dividir o frango em porções separadas para congelar. Livro «A arte de congelar».",
    },
    {
        "cat": "aves",
        "slug": "frango-na-pucara",
        "title": "Frango na púcara",
        "category": "Aves · Frango",
        "meta": [("Rendimento", "4 porções")],
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
            "Corte o presunto em cubinhos de cerca de 0,5 cm e deixe de molho em água fria até perder o sal.",
            "Descaspe os tomates, retire as sementes e corte em cubinhos de cerca de 1 cm.",
            "Preaqueça o forno em temperatura alta (200 °C).",
            "Esmague os dentes de alho.",
            "Tempere os pedaços de frango com sal e pimenta-do-reino e distribua-os numa panela de barro refratária com tampa.",
            "Junte presunto escorrido, tomate, alho amassado e cebolas inteiras.",
            "Distribua a manteiga sobre os pedaços de frango.",
            "Regue com vinho do Porto, conhaque e vinho branco.",
            "Junte a mostarda, tampe bem a panela e leve ao forno preaquecido até o frango cozinhar e ficar macio (cerca de 1 hora).",
            "Destampe a panela e leve novamente ao forno até a superfície do frango dourar (cerca de 30 minutos). Retire do forno, deixe esfriar e congele.",
        ],
        "notes": "Clássico da cozinha regional portuguesa; acompanhe com batatas fritas e arroz. Livro «A arte de congelar».",
    },
    {
        "cat": "aves",
        "slug": "frango-ao-caril",
        "title": "Frango ao caril",
        "category": "Aves · Frango",
        "meta": [("Rendimento", "4 a 6 porções")],
        "ingredients": [
            "1 kg de coxas, sobrecoxas e peitos de frango",
            "3 colheres (chá) de sal",
            "½ xícara de óleo",
            "2 cebolas picadas",
            "4 dentes de alho picados",
            "1½ colheres (chá) de gengibre ralado",
            "3 colheres (sopa) de pó de caril",
            "1½ xícaras de água",
            "4 a 5 tomates",
            "2 colheres (sopa) de coentro picado",
            "1 copo de iogurte natural",
            "1 colher (sopa) de suco de limão",
        ],
        "steps": [
            "Lave e seque os pedaços de frango. Polvilhe com 2 colheres de chá de sal.",
            "Em panela grande de ferro ou alumínio, aqueça bem o óleo e frite os pedaços de frango por 3 a 4 minutos, virando com garfo sem deixar dourar. Transfira para um prato.",
            "Na mesma panela, junte cebola, alho e gengibre. Mexendo sempre, frite por 4 minutos ou até a cebola ficar macia e dourada.",
            "Abaixe o fogo, adicione 1 colher de sopa de caril e 1 colher de sopa de água. Cozinhe por cerca de 2 minutos, mexendo sempre. Junte tomates picados sem pele e sem sementes, 1 colher de sopa de coentro, iogurte e sal restante.",
            "Aumente levemente o fogo, adicione o frango com os sucos do prato e o restante da água. Leve ao fervor e vire os pedaços para cozinhar uniformemente.",
            "Reduza ao mínimo, tampe bem a panela e deixe cozinhar por 25 minutos ou até o frango ficar macio.",
            "Retire a panela do fogo, adicione o suco de limão e mexa bem. Coloque os pedaços de frango numa travessa forrada com plástico e despeje o molho. Deixe esfriar e congele.",
        ],
        "notes": "Ao servir, polvilhe com o caril e coentro restantes. Sirva com arroz branco. Livro «A arte de congelar».",
    },
    {
        "cat": "aves",
        "slug": "frango-estufado-com-tomates",
        "title": "Frango estufado com tomates",
        "category": "Aves · Frango",
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
            "Em panela grande, coloque o óleo, cebola, alho amassado, bacon e pimentão picado. Leve ao fogo para fritar o bacon e refogar os legumes.",
            "Junte os pedaços de frango, tomates picados, purê de tomate, páprica, açúcar, sal e pimenta-do-reino a gosto. Tampe a panela e deixe o frango cozinhar.",
            "Acrescente as azeitonas e 2 colheres de salsa; cozinhe um pouco mais com a panela destampada. Deixe esfriar e congele.",
        ],
        "notes": "Livro «A arte de congelar».",
    },
    {
        "cat": "aves",
        "slug": "peru-recheado-com-risoto",
        "title": "Peru recheado com risoto",
        "category": "Aves · Outras aves",
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
            "Deixe as uvas-passas de molho na champanha por cerca de 30 minutos.",
            "Risoto: refogue a cebola em 4 colheres de manteiga; junte o arroz e mexa. Adicione o caldo de galinha aos poucos, mexendo, até o arroz cozinhar. Junte a champanha das passas, as passas escorridas e as castanhas de caju.",
            "Em panela, aqueça 1 xícara de manteiga com 2 cebolas, purê de tomate, sal, pimenta e 2 xícaras de champanha até formar pasta de tempero.",
            "Levante a pele do peru e espalhe parte do tempero sob a pele e no interior. Recheie com o risoto.",
            "Asse coberto com papel de alumínio a 200 °C (cerca de 1 hora por kg de peru), regando com caldo de galinha se necessário. Destampe no final para dourar. Deixe esfriar e congele.",
        ],
        "notes": "Congele o risoto e o peru temperado separados se preferir assar depois. Livro «A arte de congelar».",
    },
    {
        "cat": "doces",
        "slug": "bolacha-de-nescau",
        "title": "Bolacha de Nescau",
        "category": "Doces · Biscoitos",
        "meta": None,
        "ingredients": [
            "1 copo de farinha de trigo",
            "1 copo de Nescau",
            "1 ovo",
            "3 colheres de margarina",
        ],
        "steps": [
            "Misture todos os ingredientes até formar massa homogênea.",
            "Faça bolachas achatadas e marque com garfo.",
            "Leve ao forno por cerca de 15 minutos.",
        ],
        "notes": "Receita de rede social (4 ingredientes).",
    },
]


def render_recipe(r: dict) -> str:
    cat = r["cat"]
    category = r["category"]
    title = r["title"]
    slug = r["slug"]
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
        <a href="../../index.html#{cat}">{html.escape(category.split(" · ")[0])}</a>
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
        <p class="category">{html.escape(category)}</p>
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


def main() -> None:
    written: list[str] = []
    for r in RECIPES:
        out = ROOT / "receitas" / r["cat"] / f"{r['slug']}.html"
        out.parent.mkdir(parents=True, exist_ok=True)
        if out.exists():
            print(f"skip exists {out.relative_to(ROOT)}")
            continue
        out.write_text(render_recipe(r), encoding="utf-8")
        written.append(r["slug"])
        print(f"wrote {out.relative_to(ROOT)}")
    print(f"Created {len(written)} fichas: {', '.join(written)}")


if __name__ == "__main__":
    main()
