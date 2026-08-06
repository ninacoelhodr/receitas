#!/usr/bin/env python3
"""Gera fichas HTML do lote Telegram 2026-07-31."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TEMPLATE = """<!DOCTYPE html>
<html lang="pt-BR">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{title} — Livro de Receitas</title>
    <meta name="description" content="{title} — ficha A5 para imprimir." />
    <link rel="stylesheet" href="../../css/site.css" />
    <link rel="stylesheet" href="../../css/print.css" />
  </head>
  <body>
    <header class="site-header no-print">
      <a class="brand" href="../../index.html">Livro de Receitas</a>
      <nav class="site-nav" aria-label="Principal">
        <a href="../../index.html#{nav_cat}">{nav_label}</a>
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
        <p class="category">{category}</p>
        <h1>{title}</h1>
        {meta}
        <figure class="dish-photo no-print">
          <img src="../../imagens/{slug}.jpg" alt="Referência: {title}" />
          <figcaption>Referência visual (não é a foto da receita da família).</figcaption>
        </figure>
        <h2>Ingredientes</h2>
        <ul class="ingredients">
{ingredients}
        </ul>

        <h2>Modo de preparo</h2>
        <ol class="steps">
{steps}
        </ol>
{notes}
      </article>
    </main>
  </body>
</html>
"""

RECIPES = [
    {
        "slug": "pate-de-figado-de-galinha",
        "folder": "salgados",
        "nav_cat": "salgados",
        "nav_label": "Salgados",
        "category": "Salgados · Petiscos",
        "title": "Patê de fígado de galinha",
        "meta": '<div class="meta"><span><strong>Rendimento:</strong> 10 porções</span></div>',
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
            "Preaqueça o forno em temperatura média (180 °C). Limpe os fígados, retirando todos os filamentos. Bata no liquidificador com os ovos, gemas, sal, pimenta e manjericão por 1 minuto.",
            "Acrescente o molho branco e o vinho ou conhaque; bata mais 15 segundos. Passe por peneira e deixe cair numa terrina.",
            "Despeje numa forma de bolo untada (7 × 12 × 25 cm, capacidade de 5 xícaras). Asse em banho-maria no forno preaquecido por cerca de 30 minutos. Deixe esfriar e congele.",
        ],
        "notes": '<p class="notes">Para servir quente: coloque num refratário, cubra com papel-alumínio e, após descongelar, aqueça em forno bem brando. <strong>Congelamento:</strong> coloque a forma com o patê num saco plástico e leve ao freezer para endurecer; retire da forma, embrulhe em filme, etiquete e congele. <strong>Descongelamento:</strong> descongele na geladeira de um dia para o outro; decore com tiras de pimentão vermelho em conserva e sirva com torradas.</p>',
    },
    {
        "slug": "torta-de-frango",
        "folder": "tortas-salgadas",
        "nav_cat": "tortas-salgadas",
        "nav_label": "Tortas salgadas",
        "category": "Tortas salgadas",
        "title": "Torta de frango",
        "meta": '<div class="meta"><span><strong>Rendimento:</strong> 6 a 8 porções</span></div>',
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
            "Cozinhe e desfie o frango. Coloque num refratário raso com o queijo, leite, cebola e orégano. Tampe e leve à geladeira para marinar.",
            "Descasque as batatas, corte em cubos e cozinhe em água com sal. Escorra, passe no espremedor e misture com 4 colheres de manteiga e o leite até virar purê. Tempere com sal, acrescente a salsa e reserve.",
            "Escorra o líquido do marinado e reserve. Misture o frango com cenoura, cebolinha e maionese; ajuste o sal.",
            "Derreta o restante da manteiga numa frigideira, polvilhe a farinha e doure levemente. Fora do fogo, acrescente o líquido reservado aos poucos, mexendo. Volte ao fogo, junte o purê de tomate e cozinhe até engrossar. Misture ao frango.",
            "Coloque o recheio num refratário de 2 litros, cubra com o purê de batata e faça sulcos com um garfo.",
            "Bata a gema com 2 colheres (sopa) de água e pincele a superfície. Asse em forno alto (200 °C) por cerca de 50 minutos, até dourar. Deixe esfriar e congele.",
        ],
        "notes": '<p class="notes">Para congelar crua, deixe para pincelar com a gema batida depois de descongelar. <strong>Congelamento:</strong> embrulhe o refratário com filme plástico ou saco hermético; etiquete e congele. <strong>Descongelamento:</strong> descongele na geladeira de um dia para o outro; retire o plástico e aqueça no forno coberto com papel-alumínio.</p>',
    },
    {
        "slug": "enroladinhos-meireles",
        "folder": "aves",
        "nav_cat": "aves",
        "nav_label": "Aves",
        "category": "Aves · Frango",
        "title": "Enroladinhos Meireles",
        "meta": '<div class="meta"><span><strong>Rendimento:</strong> 6 a 8 porções</span></div>',
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
            "Abra cada metade de peito com uma faca afiada, formando um bife largo. Tempere com sal.",
            "Misture cenoura, passas, maçã, vinagre e sal. Divida em oito partes e coloque sobre cada peito. Enrole e prenda com palito ou barbante.",
            "Preaqueça o forno em temperatura média (180 °C). Arrume os rolinhos num refratário.",
            "Derreta a manteiga com o leite de coco e o gengibre em fogo brando, mexendo sempre. Despeje sobre os peitos e asse por cerca de 40 minutos, até dourar e ficar macio. Deixe esfriar e congele.",
        ],
        "notes": '<p class="notes">Proteja as pontas dos palitos com papel-alumínio para não furarem a embalagem. <strong>Congelamento:</strong> coloque os rolinhos numa travessa forrada com plástico, cubra com filme e congele; passe para saco plástico, retire o ar, vede, etiquete e congele. <strong>Descongelamento:</strong> descongele na geladeira de um dia para o outro; transfira para refratário e aqueça em forno brando.</p>',
    },
    {
        "slug": "enrolados-de-frango",
        "folder": "aves",
        "nav_cat": "aves",
        "nav_label": "Aves",
        "category": "Aves · Frango",
        "title": "Enrolados de frango",
        "meta": '<div class="meta"><span><strong>Rendimento:</strong> 4 porções</span></div>',
        "ingredients": [
            "2 peitos de frango (cerca de 1 kg no total)",
            "Sal e pimenta-do-reino a gosto",
            "1¼ xícara de água",
            "¼ xícara de arroz cru",
            "1 colher (sopa) de cebolinha verde picada",
            "1 cenoura descascada e ralada",
            "1 pimentão verde em quadradinhos",
            "1 colher (chá) de casca ralada de laranja",
            "Manteiga para pincelar",
            "1 xícara de suco de laranja",
            "1 colher (sopa) de maisena",
            "1 pitada de sal",
        ],
        "steps": [
            "Retire a pele e os ossos dos peitos e divida cada filé ao meio (4 pedaços). Bata com martelo até ficar bem fino. Tempere com sal e pimenta.",
            "Misture água, arroz, cebolinha, cenoura, pimentão e casca de laranja. Tempere, tampe e cozinhe em fogo baixo por cerca de 20 minutos, até o arroz ficar macio e a água secar.",
            "Espalhe o arroz sobre os filés, enrole em cilindros e prenda com palitos. Arrume no refratário, pincele com manteiga, cubra com alumínio e asse a 180 °C por cerca de 20 minutos, até ficarem macios. Deixe esfriar e congele.",
            "Misture suco de laranja, maisena e pitada de sal. Cozinhe mexendo até formar um creme espesso. Deixe esfriar e congele separadamente.",
        ],
        "notes": '<p class="notes">Antes de embrulhar para congelar, embeba os pedaços no molho para não ressecarem. <strong>Congelamento:</strong> congele os rolinhos na travessa, desenforme e passe para saco plástico; molho em recipiente rígido, depois saco. <strong>Descongelamento:</strong> descongele os rolinhos na geladeira; aqueça o molho em fogo brando; aqueça os rolinhos cobertos com alumínio no forno, regue com o molho e sirva.</p>',
    },
    {
        "slug": "files-de-frango-recheados",
        "folder": "aves",
        "nav_cat": "aves",
        "nav_label": "Aves",
        "category": "Aves · Frango",
        "title": "Filés de frango recheados",
        "meta": '<div class="meta"><span><strong>Rendimento:</strong> 4 a 6 porções</span></div>',
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
            "Preaqueça o forno em temperatura média (180 °C). Faça um corte em cada metade de peito, como uma bolsa. Recheie com uma fatia de bacon, tempere com sal e pimenta e prenda com palitos ou barbante.",
            "Arrume numa assadeira, regue com azeite e polvilhe orégano. Asse por cerca de 40 minutos, até dourar e ficar macio.",
            "Retire do forno. Coloque os pedaços numa embalagem de alumínio e tampe; mantenha aquecido no forno desligado.",
            "Leve a assadeira ao fogo brando, junte leite e requeijão e misture com os resíduos até formar um molho uniforme. Cubra o frango, deixe esfriar e congele.",
        ],
        "notes": '<p class="notes">Para rechear, abra o peito ao meio sem separar as metades; recheie, enrole uma metade sobre a outra e prenda. <strong>Congelamento:</strong> coloque a embalagem de alumínio num saco plástico, vede, etiquete e congele. <strong>Descongelamento:</strong> descongele na geladeira; aqueça no forno ainda tampado em temperatura baixa; transfira para travessa, polvilhe salsa e sirva.</p>',
    },
    {
        "slug": "frango-assado-com-cerveja",
        "folder": "aves",
        "nav_cat": "aves",
        "nav_label": "Aves",
        "category": "Aves · Frango",
        "title": "Frango assado com cerveja",
        "meta": '<div class="meta"><span><strong>Rendimento:</strong> 4 porções</span></div>',
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
            "Tempere os pedaços com sal, pimenta e alho. Coloque numa assadeira com cebola e louro. Despeje a cerveja por cima.",
            "Asse no forno preaquecido até dourar e ficar macio (cerca de 1 h 40 min), regando de vez em quando com o caldo. Deixe esfriar e congele.",
        ],
        "notes": '<p class="notes">Pode dividir o frango em porções separadas para congelar. <strong>Congelamento:</strong> coloque frango e molho em embalagem de alumínio, ponha num saco plástico, retire o ar e feche hermeticamente; etiquete e congele. <strong>Descongelamento:</strong> descongele na geladeira de um dia para o outro; cubra com alumínio e aqueça no forno.</p>',
    },
    {
        "slug": "frango-na-pucara",
        "folder": "aves",
        "nav_cat": "aves",
        "nav_label": "Aves",
        "category": "Aves · Frango",
        "title": "Frango na púcara",
        "meta": '<div class="meta"><span><strong>Rendimento:</strong> 4 porções</span></div>',
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
            "Corte o presunto em cubinhos de 0,5 cm e deixe de molho em água fria até perder o sal.",
            "Descasque os tomates, retire as sementes e corte em cubos de cerca de 1 cm.",
            "Preaqueça o forno em temperatura alta (200 °C). Esmague o alho.",
            "Tempere o frango com sal e pimenta e distribua numa panela de barro refratária com tampa.",
            "Acrescente presunto escorrido, tomate, alho e cebolas inteiras. Distribua a manteiga sobre o frango.",
            "Regue com vinho do Porto, conhaque e vinho branco. Junte a mostarda, tampe e leve ao forno até o frango ficar macio (cerca de 1 hora).",
            "Destampe e volte ao forno até dourar a superfície (cerca de 30 minutos). Deixe esfriar e congele.",
        ],
        "notes": '<p class="notes">Clássico da cozinha regional portuguesa, preparado na púcara (tacho de barro com tampa). <strong>Congelamento:</strong> coloque num recipiente rígido, cubra com filme e congele; retire do recipiente, embrulhe em filme, vede, etiquete e congele. <strong>Descongelamento:</strong> descongele na geladeira; aqueça na panela de barro tampada e sirva na mesma panela, com batatas fritas em palito e arroz.</p>',
    },
    {
        "slug": "frango-ao-caril",
        "folder": "aves",
        "nav_cat": "aves",
        "nav_label": "Aves",
        "category": "Aves · Frango",
        "title": "Frango ao caril",
        "meta": '<div class="meta"><span><strong>Rendimento:</strong> 4 a 6 porções</span></div>',
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
            "Lave e seque os pedaços de frango; polvilhe com 2 colheres (chá) de sal.",
            "Frite o frango em panela grande com óleo por 3–4 minutos, sem dourar. Retire para um prato.",
            "Refogue cebola, alho e gengibre na mesma panela por 4 minutos, até amolecer e dourar.",
            "Abaixe o fogo, junte 1 colher (sopa) de caril e 1 colher (sopa) de água; cozinhe 2 minutos. Acrescente tomates descascados e sem sementes, 1 colher (sopa) de coentro, iogurte e o sal restante.",
            "Aumente o fogo, devolva o frango com os sucos e o restante da água; ferva e vire os pedaços para cozinhar uniformemente.",
            "Reduza ao mínimo, tampe bem e cozinhe por 25 minutos ou até ficar macio. Retire do fogo, junte o suco de limão, misture, coloque num refratário forrado com plástico, regue com o molho, deixe esfriar e congele.",
        ],
        "notes": '<p class="notes">O pó de caril é mistura de especiarias indianas (canela, cravo, coentro, cominho, cardamomo e pimenta-preta). <strong>Congelamento:</strong> cubra com filme, congele, retire do refratário, embrulhe, etiquete e congele. <strong>Descongelamento:</strong> desembrulhe e aqueça em fogo brando; polvilhe com o caril e coentro reservados e sirva com arroz branco.</p>',
    },
    {
        "slug": "frango-estufado-com-tomates",
        "folder": "aves",
        "nav_cat": "aves",
        "nav_label": "Aves",
        "category": "Aves · Frango",
        "title": "Frango estufado com tomates",
        "meta": '<div class="meta"><span><strong>Rendimento:</strong> 2 porções</span></div>',
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
            "Numa panela grande, refogue cebola, alho amassado, bacon e pimentão picados no óleo até fritar o bacon e refogar os legumes.",
            "Junte o frango, tomates picados, purê de tomate, páprica, açúcar, sal e pimenta. Tampe e cozinhe o frango.",
            "Acrescente as azeitonas e 2 colheres (sopa) de salsa; cozinhe mais um pouco com a panela destampada. Deixe esfriar e congele.",
        ],
        "notes": '<p class="notes">A páprica é tempero em pó vermelho, semelhante ao colorífico (doce ou picante). <strong>Congelamento:</strong> transfira para recipiente rígido, cubra com filme, congele; passe para saco plástico, retire o ar, vede, etiquete e congele. <strong>Descongelamento:</strong> aqueça em banho-maria em fogo brando ou no micro-ondas (descongelar 5 min em potência 3, depois 5 min em potência 7); polvilhe com a salsa restante e sirva.</p>',
    },
    {
        "slug": "peru-recheado-com-risoto",
        "folder": "aves",
        "nav_cat": "aves",
        "nav_label": "Aves",
        "category": "Aves · Outras aves",
        "title": "Peru recheado com risoto",
        "meta": '<div class="meta"><span><strong>Rendimento:</strong> 12 porções</span></div>',
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
            "Para o risoto: deixe as passas de molho na champanha.",
            "Derreta 4 colheres de manteiga, doure a cebola, junte o arroz e frite até soltar. Cubra com caldo e cozinhe até o arroz ficar macio mas al dente.",
            "Retire do fogo, acrescente passas escorridas e castanhas picadas. Regue com a champanha das passas e misture até risoto úmido. Congele.",
            "Derreta 1 xícara de manteiga, junte cebolas, purê de tomate, sal, pimenta e champanha; misture.",
            "Tempere todo o peru com essa mistura, levantando a pele do peito para espalhar por baixo.",
            "Ao assar, calcule cerca de 1 hora de forno para cada quilo de peru.",
        ],
        "notes": '<p class="notes"><strong>Congelamento:</strong> risoto em recipiente rígido, depois saco plástico; peru embrulhado em alumínio e saco plástico sem ar. <strong>Descongelamento:</strong> descongele peru e risoto na geladeira; coloque o peru numa assadeira, recheie com o risoto, cubra com alumínio e asse a 200 °C por 4–5 horas, regando com caldo; retire o alumínio 40 minutos antes para dourar. Sirva com gomos de laranja.</p>',
    },
    {
        "slug": "bolacha-de-nescau",
        "folder": "doces",
        "nav_cat": "doces",
        "nav_label": "Doces",
        "category": "Doces · Biscoitos",
        "title": "Bolacha de Nescau",
        "meta": "",
        "ingredients": [
            "1 copo de farinha de trigo",
            "1 copo de Nescau",
            "1 ovo",
            "3 colheres de margarina",
        ],
        "steps": [
            "Misture todos os ingredientes até formar uma massa homogênea.",
            "Modele bolachas, achate com um garfo e leve ao forno por cerca de 15 minutos.",
        ],
        "notes": '<p class="notes">Receita de 4 ingredientes (fonte: rede social).</p>',
    },
]


def li(items):
    return "\n".join(f"          <li>{x}</li>" for x in items)


def main():
    for r in RECIPES:
        html = TEMPLATE.format(
            title=r["title"],
            slug=r["slug"],
            nav_cat=r["nav_cat"],
            nav_label=r["nav_label"],
            category=r["category"],
            meta=r["meta"],
            ingredients=li(r["ingredients"]),
            steps=li(r["steps"]),
            notes=("\n        " + r["notes"]) if r["notes"] else "",
        )
        path = ROOT / "receitas" / r["folder"] / f"{r['slug']}.html"
        path.write_text(html, encoding="utf-8")
        print("wrote", path.relative_to(ROOT))


if __name__ == "__main__":
    main()
