#!/usr/bin/env python3
"""Generate recipe HTML files from Telegram batch Aug 2026."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RECIPES = [
    {
        "slug": "pate-de-figado-de-galinha",
        "folder": "acompanhamentos",
        "title": "Patê de fígado de galinha",
        "category": "Acompanhamentos",
        "nav_hash": "acompanhamentos",
        "meta": ["<span><strong>Rendimento:</strong> 10 porções</span>"],
        "ingredients": [
            "1,5 kg de fígados de galinha",
            "2 ovos grandes",
            "2 gemas",
            "2 colheres (chá) de sal",
            "1 colher (chá) de pimenta-do-reino",
            "1 colher (sopa) de manjericão picado",
            "1 xícara de molho branco grosso",
            "2 colheres (sopa) de vinho da Madeira ou conhaque",
            "Manteiga para untar",
        ],
        "steps": [
            "Preaqueça o forno em temperatura média (180°C). Limpe os fígados, retirando todos os filamentos. Coloque os fígados no liquidificador com os ovos, as gemas, o sal, a pimenta-do-reino e o manjericão. Bata por 1 minuto.",
            "Acrescente o molho branco e o vinho ou conhaque e bata por mais 15 segundos. Passe por uma peneira em uma terrina.",
            "Coloque a mistura em uma forma de pão untada (7 × 12 × 25 cm, capacidade de 5 xícaras). Coloque a forma dentro de uma assadeira com água fervente (banho-maria) e leve ao forno preaquecido por cerca de 30 minutos. Deixe esfriar e congele.",
        ],
        "notes": "Para servir quente: coloque em travessa refratária, cubra com papel alumínio e, após descongelar, aqueça em forno bem brando.",
    },
    {
        "slug": "torta-de-frango",
        "folder": "tortas-salgadas",
        "title": "Torta de frango",
        "category": "Tortas salgadas",
        "nav_hash": "tortas-salgadas",
        "meta": ["<span><strong>Rendimento:</strong> 6 a 8 porções</span>"],
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
            "2 cenouras raladas grossas e cozidas",
            "2 colheres (sopa) de cebolinha verde picada",
            "2 colheres (sopa) de maionese",
            "3 colheres (sopa) de farinha de trigo",
            "1 colher (sopa) de purê de tomate",
            "1 gema",
        ],
        "steps": [
            "Cozinhe e desfie o frango. Coloque em travessa rasa e acrescente o queijo, o leite, a cebola e o orégano. Tampe e leve à geladeira para marinar.",
            "Descasque as batatas, corte em cubos e cozinhe em água com sal. Escorra, passe no espremedor e coloque em tigela. Acrescente 4 colheres de manteiga e o leite (⅓ xícara), misture até formar purê. Tempere com sal, junte a salsa e misture. Reserve.",
            "Escorra o líquido onde o frango marinou e reserve. Em outra tigela, coloque o frango desfiado, as cenouras, a cebolinha e a maionese. Prove o tempero e misture.",
            "Na frigideira, derreta o restante da manteiga. Polvilhe a farinha e doure levemente.",
            "Retire do fogo e acrescente gradualmente o líquido reservado, mexendo sempre. Volte ao fogo, junte o purê de tomate e cozinhe até o molho engrossar.",
            "Acrescente o molho à mistura de frango.",
            "Coloque a mistura de frango em travessa refratária de 2 litros, cubra com o purê de batata e decore a superfície fazendo sulcos com os dentes de um garfo.",
            "Em tigela pequena, bata a gema com 2 colheres de água. Pincele a superfície da torta.",
            "Leve ao forno quente preaquecido (200°C) por cerca de 50 minutos, até dourar. Deixe esfriar e congele.",
        ],
        "notes": "Para congelar crua, pincele com a gema batida só após descongelar.",
    },
    {
        "slug": "enroladinhos-meireles",
        "folder": "aves",
        "title": "Enroladinhos Meireles",
        "category": "Aves · Frango",
        "nav_hash": "aves",
        "meta": ["<span><strong>Rendimento:</strong> 6 a 8 porções</span>"],
        "ingredients": [
            "4 peitos de frango sem osso cortados ao meio",
            "Sal a gosto",
            "1 cenoura ralada grossa",
            "⅓ xícara de uvas-passas pretas sem sementes",
            "1 maçã verde com casca ralada grossa",
            "2 colheres (sopa) de vinagre de vinho branco ou de maçã",
            "4 colheres (sopa) de manteiga ou margarina",
            "1 garrafinha de leite de coco",
            "1 colher (chá) de gengibre ralado",
        ],
        "steps": [
            "Com faca afiada, abra cada metade de peito em filé largo. Tempere com sal.",
            "Em tigela, misture a cenoura, as passas, a maçã ralada, o vinagre e sal.",
            "Divida a mistura em oito partes e coloque em cada metade de peito. Enrole e prenda com palito ou amarre com barbante.",
            "Preaqueça o forno em temperatura média (180°C).",
            "Coloque os enrolados lado a lado em assadeira.",
            "Em panela pequena, junte a manteiga, o leite de coco e o gengibre. Mexa em fogo baixo até a manteiga derreter.",
            "Retire do fogo e despeje sobre os enrolados. Leve ao forno preaquecido por cerca de 40 minutos ou até dourar e ficar macio. Deixe esfriar e congele.",
        ],
        "notes": "Ao embrulhar para congelar, proteja as pontas dos palitos com papel alumínio.",
    },
    {
        "slug": "enrolados-de-frango",
        "folder": "aves",
        "title": "Enrolados de frango",
        "category": "Aves · Frango",
        "nav_hash": "aves",
        "meta": ["<span><strong>Rendimento:</strong> 4 porções</span>"],
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
            "Retire a pele e os ossos dos peitos e divida os filés ao meio, obtendo 4 pedaços.",
            "Sobre uma tábua, bata os filés com martelo de bife até ficar bem fino. Tempere com sal e pimenta e reserve.",
            "Na panela, misture a água com o arroz cru, a cebolinha, a cenoura, o pimentão e a casca de laranja. Tempere com sal e pimenta. Tampe e cozinhe em fogo baixo por cerca de 20 minutos, até o arroz ficar macio e o líquido ser absorvido.",
            "Espalhe a mistura de arroz sobre os filés, enrole cada um e prenda com palitos.",
            "Coloque os enrolados lado a lado em assadeira. Pincele com manteiga. Cubra com papel alumínio e leve ao forno médio (180°C) por cerca de 20 minutos, até ficar macio. Deixe esfriar e congele.",
            "Na panela, junte o suco de laranja com a maisena e uma pitada de sal. Misture bem. Cozinhe em fogo, mexendo sempre, até obter um creme grosso. Deixe esfriar e congele.",
        ],
        "notes": "Antes de embrulhar para congelar, embeba os pedaços no molho para não ressecar.",
    },
    {
        "slug": "files-de-frango-recheados",
        "folder": "aves",
        "title": "Filés de frango recheados",
        "category": "Aves · Frango",
        "nav_hash": "aves",
        "meta": ["<span><strong>Rendimento:</strong> 4 a 6 porções</span>"],
        "ingredients": [
            "3 peitos de frango sem osso cortados ao meio",
            "6 fatias de bacon",
            "Sal e pimenta-do-reino a gosto",
            "4 colheres (sopa) de azeite de oliva",
            "1 colher (sopa) de orégano",
            "½ xícara de leite",
            "1 pote de requeijão cremoso",
            "2 colheres (sopa) de salsa picada",
        ],
        "steps": [
            "Preaqueça o forno em temperatura média (180°C). Faça um corte em cada metade de peito para formar um saquinho.",
            "Coloque uma fatia de bacon dentro de cada saquinho e tempere com sal e pimenta. Prenda com palitos ou amarre com barbante.",
            "Coloque os filés em assadeira lado a lado, regue com azeite e polvilhe com orégano. Leve ao forno preaquecido por cerca de 40 minutos ou até dourar e ficar macio.",
            "Retire do forno. Coloque os pedaços de frango em recipiente de alumínio e tampe. Mantenha aquecido dentro do forno desligado.",
            "Coloque a assadeira usada para o frango em fogo baixo. Acrescente o leite e o requeijão, misturando bem com o resíduo do frango até formar molho uniforme.",
            "Cubra o frango com o molho, deixe esfriar e congele.",
        ],
        "notes": "Para rechear: abra os peitos ao meio com faca sem separar as duas metades. Recheie e enrole uma metade sobre a outra.",
    },
    {
        "slug": "frango-assado-com-cerveja",
        "folder": "aves",
        "title": "Frango assado com cerveja",
        "category": "Aves · Frango",
        "nav_hash": "aves",
        "meta": ["<span><strong>Rendimento:</strong> 4 porções</span>"],
        "ingredients": [
            "1 frango (cerca de 1,8 kg) limpo e cortado em pedaços pelas juntas",
            "Sal e pimenta-do-reino a gosto",
            "5 dentes de alho descascados e amassados",
            "1 cebola grande picada",
            "4 folhas de louro",
            "2 latas de cerveja",
        ],
        "steps": [
            "Preaqueça o forno em temperatura alta (200°C).",
            "Tempere os pedaços de frango com sal, pimenta-do-reino e o alho. Coloque em assadeira.",
            "Junte a cebola e as folhas de louro. Despeje a cerveja por cima do frango.",
            "Leve ao forno preaquecido e deixe assar até o frango dourar e ficar macio (cerca de 1 hora e 40 minutos), banhando de vez em quando com o caldo da assadeira. Retire do forno, deixe esfriar e congele.",
        ],
        "notes": "Se quiser, divida o frango em porções separadas para congelar.",
    },
    {
        "slug": "frango-na-pucara",
        "folder": "aves",
        "title": "Frango na púcara",
        "category": "Aves · Frango",
        "nav_hash": "aves",
        "meta": ["<span><strong>Rendimento:</strong> 4 porções</span>"],
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
            "Corte o presunto em cubinhos de cerca de 0,5 cm e ponha de molho em tigela com água fria até perder o sal.",
            "Descasque os tomates, retire as sementes e corte em cubinhos de cerca de 1 cm.",
            "Preaqueça o forno em temperatura alta (200°C).",
            "Esmague os dentes de alho com socador ou aparelho próprio.",
            "Tempere os pedaços de frango com sal e pimenta e distribua em panela de barro refratária com tampa.",
            "Acrescente o presunto escorrido, o tomate, o alho amassado e as cebolas inteiras.",
            "Distribua a manteiga sobre os pedaços de frango.",
            "Regue com o vinho do Porto, o conhaque e o vinho branco.",
            "Junte a mostarda, tampe bem e leve ao forno preaquecido até o frango ficar cozido e macio (cerca de 1 hora).",
            "Destampe e leve novamente ao forno até a superfície dourar (cerca de 30 minutos). Retire do forno, deixe esfriar e congele.",
        ],
        "notes": "Clássico da cozinha regional portuguesa; o nome vem da panela de barro com tampa (púcara). Sirva com batatas fritas em palito e arroz.",
    },
    {
        "slug": "frango-ao-caril",
        "folder": "aves",
        "title": "Frango ao caril",
        "category": "Aves · Frango",
        "nav_hash": "aves",
        "meta": ["<span><strong>Rendimento:</strong> 4 a 6 porções</span>"],
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
            "Em panela grande de ferro ou alumínio, aqueça bem o óleo e frite os pedaços de frango por 3 a 4 minutos, virando com garfo, sem deixar dourar. Transfira para um prato.",
            "Na mesma panela, coloque a cebola, o alho e o gengibre e, mexendo sempre, frite por 4 minutos ou até a cebola ficar macia e dourada.",
            "Baixe o fogo, acrescente 1 colher (sopa) de caril e 1 colher (sopa) de água. Cozinhe por cerca de 2 minutos, mexendo sempre. Acrescente o tomate sem pele nem sementes picado, 1 colher (sopa) de coentro, o iogurte e o restante do sal.",
            "Aumente um pouco o fogo e adicione o frango com o caldo do prato. Junte o restante da água, deixe ferver e vire os pedaços para cozinhar por igual.",
            "Reduza o fogo ao mínimo, tampe bem e cozinhe por 25 minutos ou até o frango ficar macio.",
            "Retire do fogo, acrescente o suco de limão e mexa bem. Disponha os pedaços em travessa forrada com plástico e despeje o molho por cima. Deixe esfriar e congele.",
        ],
        "notes": "O pó de caril é tempero indiano (canela, cravo, coentro, cominho, cardamomo e pimenta-do-reino). Sirva com arroz branco.",
    },
    {
        "slug": "frango-estufado-com-tomates",
        "folder": "aves",
        "title": "Frango estufado com tomates",
        "category": "Aves · Frango",
        "nav_hash": "aves",
        "meta": ["<span><strong>Rendimento:</strong> 2 porções</span>"],
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
            "Em panela grande, coloque o óleo, a cebola, o alho amassado, o bacon e o pimentão picados. Leve ao fogo para fritar o bacon e refogar os legumes.",
            "Junte os pedaços de frango, os tomates picados, o purê de tomate, a páprica, o açúcar, sal e pimenta. Tampe e cozinhe o frango.",
            "Junte as azeitonas e 2 colheres de salsa; cozinhe mais um pouco com a panela destampada. Deixe esfriar e congele.",
        ],
        "notes": "A páprica é tempero em pó vermelho, semelhante ao colorífico (doce ou picante).",
    },
    {
        "slug": "peru-recheado-com-risoto",
        "folder": "aves",
        "title": "Peru recheado com risoto",
        "category": "Aves · Outras aves",
        "nav_hash": "aves",
        "meta": ["<span><strong>Rendimento:</strong> 12 porções</span>"],
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
            "Prepare o risoto: coloque as passas em tigela pequena, cubra com a champanha e deixe de molho.",
            "Em panela, coloque a manteiga e leve ao fogo brando para derreter. Acrescente a cebola e deixe dourar. Junte o arroz e frite até ficar soltinho. Cubra com o caldo de galinha e cozinhe até o arroz ficar macio mas ainda resistente ao mordisco.",
            "Retire do fogo, acrescente as passas escorridas e as castanhas de caju picadas. Misture.",
            "Regue o arroz com a champanha em que as passas estavam e misture com cuidado até obter risoto úmido. Congele.",
            "Coloque a manteiga em panela e leve ao fogo brando para derreter. Retire e acrescente as cebolas, o purê de tomate, o sal, a pimenta e a champanha. Misture.",
            "Tempere todo o peru com essa mistura, levantando a pele do peito e espalhando também ali.",
        ],
        "notes": "Ao assar, calcule cerca de 1 hora de forno para cada quilo de peru. Descongele peru e risoto na geladeira, recheie, cubra com papel alumínio e asse em forno alto (200°C) por 4 a 5 horas, regando com caldo. Retire o alumínio 40 minutos antes para dourar. Sirva com gomos de laranja.",
    },
    {
        "slug": "bolacha-de-nescau",
        "folder": "doces",
        "title": "Bolacha de Nescau",
        "category": "Doces · Biscoitos",
        "nav_hash": "doces",
        "meta": ["<span><strong>Tempo:</strong> 15 min no forno</span>"],
        "ingredients": [
            "1 copo de farinha de trigo",
            "1 copo de Nescau",
            "1 ovo",
            "3 colheres de margarina",
        ],
        "steps": [
            "Misture a farinha, o Nescau, o ovo e a margarina até formar massa homogênea.",
            "Modele bolachas, coloque em assadeira e achate levemente com garfo.",
            "Leve ao forno por 15 minutos.",
        ],
        "notes": "Receita com 4 ingredientes (fonte: Pinterest).",
    },
]


def render(recipe: dict) -> str:
    slug = recipe["slug"]
    title = recipe["title"]
    category = recipe["category"]
    nav_hash = recipe["nav_hash"]
    meta_html = "\n          ".join(recipe.get("meta", []))
    ingredients = "\n          ".join(f"<li>{i}</li>" for i in recipe["ingredients"])
    steps = "\n          ".join(f"<li>{s}</li>" for s in recipe["steps"])
    notes = recipe.get("notes")
    notes_html = (
        f"\n        <p class=\"notes\"><strong>Observação:</strong> {notes}</p>"
        if notes
        else ""
    )
    photo = f"""
        <figure class="dish-photo no-print">
          <img src="../../imagens/{slug}.jpg" alt="Referência: {title}" />
          <figcaption>Referência visual (não é a foto da receita da família).</figcaption>
        </figure>"""

    meta_block = f"\n        <div class=\"meta\">\n          {meta_html}\n        </div>" if meta_html else ""

    return f"""<!DOCTYPE html>
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
        <a href="../../index.html#{nav_hash}">{category.split(" · ")[0]}</a>
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
        <h1>{title}</h1>{photo}{meta_block}
        <h2>Ingredientes</h2>
        <ul class="ingredients">
          {ingredients}
        </ul>

        <h2>Modo de preparo</h2>
        <ol class="steps">
          {steps}
        </ol>{notes_html}
      </article>
    </main>
  </body>
</html>
"""


def main():
    for recipe in RECIPES:
        folder = ROOT / "receitas" / recipe["folder"]
        folder.mkdir(parents=True, exist_ok=True)
        path = folder / f"{recipe['slug']}.html"
        path.write_text(render(recipe), encoding="utf-8")
        print(f"Wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
