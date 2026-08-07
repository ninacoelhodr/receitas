#!/usr/bin/env python3
"""Generate recipe fichas from Telegram photo batch (2026-08-07 cron)."""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RECIPES: list[dict] = [
    {
        "cat": "acompanhamentos",
        "cat_label": "Acompanhamentos",
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
            "1 xícara de molho branco grosso",
            "2 colheres (sopa) de vinho Madeira ou conhaque",
            "Manteiga para untar",
        ],
        "steps": [
            "Preaqueça o forno em temperatura média (180 °C). Limpe os fígados, retirando todos os filamentos. Coloque os fígados no liquidificador com os ovos, as gemas, o sal, a pimenta-do-reino e o manjericão. Bata por 1 minuto.",
            "Adicione o molho branco e o vinho ou conhaque e bata por mais 15 segundos. Passe por uma peneira e deixe cair sobre uma terrina.",
            "Coloque a mistura numa fôrma de pão ou bolo inglês untada (7 × 12 × 25 cm, capacidade de 5 xícaras). Leve ao forno preaquecido, dentro de uma assadeira com água fervente (banho-maria), e asse por cerca de 30 minutos. Deixe esfriar e congele.",
        ],
        "notes": "Para servir quente: descongele, coloque em travessa refratária, cubra com papel-alumínio e aqueça em forno bem baixo. Decore com tiras de pimentão vermelho em conserva e sirva com torradas.",
    },
    {
        "cat": "tortas-salgadas",
        "cat_label": "Tortas salgadas",
        "slug": "torta-de-frango",
        "title": "Torta de frango",
        "meta": [("Rendimento", "6 a 8 porções")],
        "ingredients": [
            "½ kg de frango",
            "2 xícaras de mozarela ralada",
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
            "Cozinhe o frango e desfie. Ponha num prato raso e junte o queijo, o leite, a cebola e o orégano. Cubra e leve à geladeira para marinar.",
            "Descasque as batatas, corte em cubos e cozinhe em água e sal. Escorra, passe pelo espremedor e ponha numa tigela. Junte 4 colheres (sopa) de manteiga e o leite; misture até obter um purê. Tempere com sal, junte a salsa e reserve.",
            "Escorra o líquido da marinada do frango e reserve. Em outra tigela, misture o frango desfiado, a cenoura, a cebolinha e a maionese.",
            "Na frigideira, derreta a manteiga restante, polvilhe a farinha e doure ligeiramente. Retire do fogo e junte aos poucos o líquido da marinada, mexendo sempre. Leve ao fogo, junte o purê de tomate e cozinhe até engrossar.",
            "Junte o molho à mistura de frango. Despeje numa fôrma refratária (2 litros), cubra com o purê de batata e decore a superfície com sulcos de garfo.",
            "Bata a gema com 2 colheres (sopa) de água e pincele a superfície. Asse em forno alto preaquecido (200 °C) por cerca de 50 minutos, até dourar. Deixe esfriar e congele.",
        ],
        "notes": "Para congelar crua: pincele com gema batida só depois de descongelar.",
    },
    {
        "cat": "aves",
        "cat_label": "Aves · Frango",
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
            "Abra cada metade de peito de frango formando um bife largo e tempere com sal.",
            "Misture cenoura, passas, maçã ralada, vinagre e sal. Divida em oito partes e coloque sobre cada peito. Enrole e prenda com palito ou barbante.",
            "Preaqueça o forno em temperatura média (180 °C). Arrume os enrolados numa fôrma refratária.",
            "Derreta a manteiga com o leite de coco e o gengibre em fogo brando. Derrame sobre os peitos e asse por cerca de 40 minutos, até dourar e ficar macio. Deixe esfriar e congele.",
        ],
        "notes": "Ao embrulhar para congelar, proteja as pontas dos palitos com papel-alumínio.",
    },
    {
        "cat": "aves",
        "cat_label": "Aves · Frango",
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
            "Tire a pele e os ossos dos peitos e divida os filés ao meio (4 pedaços). Bata com amassador até ficar fino; tempere com sal e pimenta.",
            "Cozinhe arroz cru com água, cebolinha, cenoura, pimentão e casca de laranja até o arroz ficar macio e o líquido absorvido.",
            "Espalhe o arroz sobre os filés, enrole e prenda com palitos. Arrume na fôrma, pincele manteiga, cubra com papel-alumínio e asse em forno médio (180 °C) por cerca de 20 minutos. Deixe esfriar e congele.",
            "Para o molho: misture suco de laranja, maisena e pitada de sal. Cozinhe mexendo até formar creme grosso. Deixe esfriar e congele.",
        ],
        "notes": "Antes de embrulhar os rolinhos, embeba-os no molho para não ressecar ao congelar.",
    },
    {
        "cat": "aves",
        "cat_label": "Aves · Frango",
        "slug": "files-de-frango-recheados",
        "title": "Filés de frango recheados",
        "meta": [("Rendimento", "4 a 6 porções")],
        "ingredients": [
            "3 peitos de frango sem osso cortados ao meio",
            "6 fatias de bacon",
            "Sal e pimenta-do-reino a gosto",
            "4 colheres (sopa) de azeite de dendê",
            "1 colher (sopa) de orégano",
            "½ xícara de leite",
            "2 colheres (sopa) de requeijão cremoso",
            "2 colheres (sopa) de salsa picadinha",
        ],
        "steps": [
            "Preaqueça o forno em temperatura média (180 °C). Faça um corte em cada metade de peito, como uma bolsa, sem separar as metades.",
            "Coloque uma fatia de bacon em cada bolsa; tempere com sal e pimenta. Prenda com palitos ou barbante.",
            "Arrume os filés numa assadeira, regue com azeite de dendê e polvilhe orégano. Asse por cerca de 40 minutos até dourar.",
            "Retire do forno. Transfira o frango a embalagem de alumínio e tampe; mantenha aquecido no forno desligado.",
            "Na assadeira ao fogo brando, junte leite e requeijão aos resíduos do frango até formar molho uniforme. Cubra o frango com o molho, deixe esfriar e congele.",
        ],
        "notes": "Para rechear: abra ao meio com faca, recheie e enrole uma metade sobre a outra.",
    },
    {
        "cat": "aves",
        "cat_label": "Aves · Frango",
        "slug": "frango-assado-com-cerveja",
        "title": "Frango assado com cerveja",
        "meta": [("Rendimento", "4 porções")],
        "ingredients": [
            "1 frango (cerca de 1,5 kg) cortado em pedaços pelas juntas",
            "Sal e pimenta-do-reino a gosto",
            "5 dentes de alho descascados e picados",
            "1 cebola grande cortada em pedaços",
            "4 folhas de louro",
            "1 lata de cerveja",
        ],
        "steps": [
            "Preaqueça o forno em temperatura alta (200 °C).",
            "Tempere o frango com sal, pimenta e alho. Coloque na assadeira com cebola e louro; despeje a cerveja por cima.",
            "Asse até dourar e ficar macio (cerca de 1 h 40), regando de vez em quando com o líquido da assadeira. Deixe esfriar e congele.",
        ],
        "notes": "Pode dividir o frango em porções separadas para congelar.",
    },
    {
        "cat": "aves",
        "cat_label": "Aves · Frango",
        "slug": "frango-na-pucara",
        "title": "Frango na púcara",
        "meta": [("Rendimento", "4 porções")],
        "ingredients": [
            "100 g de presunto cru",
            "4 tomates maduros",
            "2 dentes de alho descascados",
            "1 frango (cerca de 1,5 kg) cortado em pedaços pelas juntas",
            "Sal e pimenta-do-reino a gosto",
            "10 cebolas pequenas inteiras",
            "50 g de manteiga gelada cortada em cubinhos",
            "⅓ xícara de vinho do Porto",
            "⅓ xícara de conhaque ou vinho branco",
            "2 colheres (sopa) de mostarda",
        ],
        "steps": [
            "Escalde os tomates para soltar a pele. Descasque os alhos em água fria.",
            "Preaqueça o forno em temperatura alta (200 °C). Amasse os alhos.",
            "Tempere o frango e distribua numa panela de barro refratária com tampa.",
            "Acrescente presunto escorrido, tomate em cubinhos, alho amassado e cebolas inteiras. Distribua a manteiga.",
            "Regue com vinho do Porto, conhaque e vinho branco. Junte a mostarda, tampe e leve ao forno até o frango ficar macio (cerca de 1 hora).",
        ],
        "notes": "Clássico regional português; o nome vem do tacho (púcara) onde é preparado. Sirva com batatas fritas, palitos e arroz.",
    },
    {
        "cat": "aves",
        "cat_label": "Aves · Frango",
        "slug": "frango-ao-caril",
        "title": "Frango ao caril",
        "meta": [("Rendimento", "4 a 6 porções")],
        "ingredients": [
            "1 kg de coxa e sobrecoxa ou peitos de frango",
            "5 colheres (chá) de sal",
            "½ xícara de óleo",
            "2 cebolas picadas",
            "4 dentes de alho picados",
            "1½ colher (chá) de gengibre ralado",
            "3 colheres (sopa) de pó de caril (curry)",
            "1½ xícara de água",
            "4 a 5 tomates sem pele e sem sementes",
            "2 colheres (sopa) de folhas de coentro picadas",
            "1 potinho de iogurte natural",
            "1 colher (sopa) de suco de limão",
        ],
        "steps": [
            "Lave e seque o frango; polvilhe com 3 colheres (chá) de sal.",
            "Aqueça o óleo e frite o frango por 3–4 minutos sem dourar. Reserve.",
            "Na mesma panela, refogue cebola, alho e gengibre até a cebola ficar meio dourada.",
            "Baixe o fogo; acrescente 1 colher (sopa) de caril e 1 colher (sopa) de água. Cozinhe 2 minutos. Junte tomate picado, 1 colher (sopa) de coentro, o restante do sal e da água.",
            "Aumente o fogo, acrescente o frango com o caldo do prato e o restante da água. Deixe ferver, tampe e cozinhe cerca de 25 minutos até o frango ficar macio.",
            "Desligue o fogo, junte iogurte e suco de limão. Sirva ou deixe esfriar e congele.",
        ],
        "notes": "O caril pode ser tempero comercial ou mistura de canela, cravo, coentro, cominho e cardamomo.",
    },
    {
        "cat": "aves",
        "cat_label": "Aves · Frango",
        "slug": "frango-estufado-com-tomates",
        "title": "Frango estufado com tomates",
        "meta": [("Rendimento", "2 porções")],
        "ingredients": [
            "1 colher (sopa) de óleo",
            "1 cebola picada",
            "1 dente de alho",
            "3 tiras de bacon",
            "1 pimentão verde",
            "2 sobrecoxas de frango sem pele",
            "1 lata de tomates sem pele ou 6 tomates sem pele e sem sementes",
            "2 colheres (sopa) de purê de tomate",
            "1 colher (sopa) de páprica",
            "1 pitada de açúcar",
            "Sal e pimenta-do-reino a gosto",
            "⅓ xícara de azeitonas pretas",
            "4 colheres (sopa) de salsa picada",
        ],
        "steps": [
            "Refogue cebola, alho e pimentão no óleo até dourar. Junte o bacon.",
            "Acrescente o frango, tomates, purê de tomate, páprica, açúcar, sal e pimenta. Tampe e cozinhe.",
            "Junte azeitonas e 2 colheres (sopa) de salsa; cozinhe destampado um pouco mais. Deixe esfriar e congele.",
        ],
        "notes": "A páprica existe em versões doce e picante.",
    },
    {
        "cat": "aves",
        "cat_label": "Aves · Outras aves",
        "slug": "peru-recheado-com-risoto",
        "title": "Peru recheado com risoto",
        "meta": [("Rendimento", "12 porções")],
        "ingredients": [
            "½ xícara de uvas-passas pretas",
            "1 xícara de champanha",
            "2 colheres (sopa) de manteiga",
            "1 cebola picada",
            "4 xícaras de caldo de galinha",
            "2 xícaras de arroz",
            "2 xícaras de castanhas de caju picadas",
            "1 xícara de manteiga",
            "2 cebolas picadas",
            "1 lata de purê de tomate",
            "1 colher (sopa) de sal",
            "2 colheres (chá) de pimenta-do-reino",
            "2 xícaras de champanha",
            "1 peru de 4 a 5 kg",
        ],
        "steps": [
            "Hidrate as passas na champanha (1 xícara) e reserve.",
            "Para o risoto: refogue 1 cebola na manteiga (2 colheres). Junte o arroz e frite. Adicione caldo aos poucos até o arroz ficar macio mas ainda al dente.",
            "Retire do fogo; misture passas escorridas e castanhas. Regue com a champanha das passas até obter risoto úmido. Congele o risoto.",
            "Derreta 1 xícara de manteiga; junte 2 cebolas picadas, purê de tomate, sal, pimenta e 2 xícaras de champanha.",
            "Tempere o peru com essa mistura, levantando a pele do peito para espalhar também ali.",
            "Recheie o peru com o risoto. Asse em forno preaquecido (200 °C) cerca de 1 hora por quilo, coberto com papel-alumínio; retire o papel nos últimos 30 minutos para dourar.",
        ],
        "notes": "Congelamento: embale o peru assado em filme e saco plástico. Descongele na geladeira; aqueça coberto com papel-alumínio.",
    },
    {
        "cat": "doces",
        "cat_label": "Doces · Biscoitos",
        "slug": "bolacha-de-nescau",
        "title": "Bolacha de Nescau",
        "meta": None,
        "ingredients": [
            "1 copo de farinha de trigo",
            "1 copo de Nescau",
            "1 ovo",
            "3 colheres de margarina",
        ],
        "steps": [
            "Misture todos os ingredientes até formar uma massa homogênea.",
            "Modele bolachas e disponha em assadeira.",
            "Leve ao forno preaquecido por cerca de 15 minutos, até o ponto da massa.",
        ],
        "notes": "Receita de rede social (4 ingredientes). Temperatura do forno não indicada na fonte — use forno médio (~180 °C).",
    },
]


def render_recipe(r: dict) -> str:
    cat = r["cat"]
    cat_label = r["cat_label"]
    title = r["title"]
    slug = r["slug"]
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
        <p class="notes">
          <strong>Observação:</strong> {html.escape(r["notes"])}
        </p>"""
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
        <a href="../../index.html#{cat}">{html.escape(cat_label.split(" · ")[0])}</a>
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


def insert_index_entry(text: str, section_id: str, subcategory: str | None, slug: str, title: str, cat: str) -> str:
    href = f"./receitas/{cat}/{slug}.html"
    entry = f"""          <li>
            <a href="{href}">{html.escape(title)}</a>
          </li>
"""
    if subcategory:
        pattern = (
            rf'(<h3 class="subcategory">{re.escape(subcategory)}</h3>\s*'
            rf'<ul class="recipe-list" data-subcategory="{re.escape(subcategory)}">\s*)'
            rf'(.*?)'
            rf'(</ul>)'
        )
        m = re.search(pattern, text, re.S)
        if not m:
            raise SystemExit(f"subcategory not found: {subcategory} in {section_id}")
        block = m.group(2)
        if slug in block:
            return text
        new_block = block + entry
        return text[: m.start(2)] + new_block + text[m.end(2) :]

    pattern = (
        rf'(<section class="category-block" id="{section_id}">\s*'
        rf'<h2>.*?</h2>\s*'
        rf'<ul class="recipe-list">\s*)'
        rf'(.*?)'
        rf'(</ul>\s*</section>)'
    )
    m = re.search(pattern, text, re.S)
    if not m:
        raise SystemExit(f"section not found: {section_id}")
    block = m.group(2)
    if f"/{slug}.html" in block:
        return text
    new_block = block + entry
    return text[: m.start(2)] + new_block + text[m.end(2) :]


def main() -> None:
    written: list[dict] = []
    for r in RECIPES:
        out = ROOT / "receitas" / r["cat"] / f"{r['slug']}.html"
        if out.exists():
            print(f"skip exists {out.relative_to(ROOT)}")
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(render_recipe(r), encoding="utf-8")
        written.append(r)
        print(f"wrote {out.relative_to(ROOT)}")

    if not written:
        print("no new recipes")
        return

    index_path = ROOT / "index.html"
    text = index_path.read_text(encoding="utf-8")
    for r in written:
        sub = None
        if " · " in r["cat_label"]:
            sub = r["cat_label"].split(" · ", 1)[1]
        text = insert_index_entry(text, r["cat"], sub, r["slug"], r["title"], r["cat"])
    index_path.write_text(text, encoding="utf-8")
    print(f"Updated index with {len(written)} entries")


if __name__ == "__main__":
    main()
