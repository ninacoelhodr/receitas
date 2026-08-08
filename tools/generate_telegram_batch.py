#!/usr/bin/env python3
"""Generate recipe fichas from Telegram pending batch (Aug 2026)."""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CAT_LABEL = {
    "acompanhamentos": "Acompanhamentos",
    "tortas-salgadas": "Tortas salgadas",
    "aves": "Aves",
    "doces": "Doces",
}

RECIPES: list[dict] = [
    {
        "cat": "acompanhamentos",
        "slug": "pate-de-figado-de-galinha",
        "title": "Patê de fígado de galinha",
        "category_line": "Acompanhamentos",
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
            "Preaqueça o forno em temperatura média (180 °C). Limpe os fígados, retirando todos os filamentos. Coloque os fígados no copo do liquidificador com os ovos, as gemas, o sal, a pimenta-do-reino e o manjericão. Bata por 1 minuto.",
            "Adicione o molho branco e o vinho ou conhaque, e bata por mais 15 segundos. Passe por uma peneira e deixe cair sobre uma terrina.",
            "Coloque a mistura numa fôrma de pão ou bolo inglês untada, de 7 × 12 × 25 cm, com capacidade de 5 xícaras. Leve ao forno preaquecido, dentro de uma assadeira com água fervendo (banho-maria), e asse por cerca de 30 minutos. Deixe esfriar e congele.",
        ],
        "notes": (
            "Para servir quente: coloque em travessa refratária, cubra com papel-alumínio e, "
            "após descongelar, aqueça em forno bem baixo. "
            "<strong>Congelamento:</strong> coloque a fôrma com o patê dentro de um saco plástico "
            "e leve ao freezer para endurecer; retire da fôrma, embale em filme plástico, etiquete e congele. "
            "<strong>Descongelamento:</strong> descongele de um dia para o outro na geladeira; "
            "decore com tiras de pimentão vermelho em conserva e sirva com torradas."
        ),
    },
    {
        "cat": "tortas-salgadas",
        "slug": "torta-de-frango",
        "title": "Torta de frango",
        "category_line": "Tortas salgadas",
        "meta": [("Rendimento", "6 a 8 porções"), ("Tempo", "50 min")],
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
            "Descasque, corte em cubos e cozinhe as batatas em água e sal.",
            "Escorra as batatas, amasse e coloque numa tigela. Junte 4 colheres de manteiga e o leite, misturando até virar purê. Tempere com sal, acrescente a salsa e misture bem. Reserve.",
            "Escorra o líquido do marinado do frango e reserve. Numa tigela, misture o frango desfiado, a cenoura, a cebolinha e a maionese. Ajuste o tempero.",
            "Numa frigideira, derreta o restante da manteiga. Polvilhe a farinha e deixe dourar levemente.",
            "Retire do fogo e acrescente aos poucos o líquido reservado do marinado, mexendo sempre. Volte ao fogo, junte o purê de tomate e cozinhe até o molho engrossar.",
            "Junte o molho à mistura de frango.",
            "Coloque o recheio num refratário de 2 litros, cubra com o purê de batata e decore a superfície com marcas de garfo.",
            "Numa tigela pequena, bata a gema com 2 colheres de água. Pincele a superfície da torta.",
            "Leve ao forno preaquecido em temperatura alta (200 °C) por cerca de 50 minutos, até dourar. Deixe esfriar e congele.",
        ],
        "notes": (
            "Para congelar crua, deixe para pincelar com a gema batida depois de descongelar. "
            "<strong>Congelamento:</strong> embrulhe o refratário em filme plástico ou saco hermético; "
            "etiquete e congele. "
            "<strong>Descongelamento:</strong> descongele na geladeira de um dia para o outro; "
            "retire o plástico e aqueça no forno coberta com papel-alumínio."
        ),
    },
    {
        "cat": "aves",
        "slug": "enroladinhos-meireles",
        "title": "Enroladinhos Meireles",
        "category_line": "Aves · Frango",
        "meta": [("Rendimento", "6 a 8 porções")],
        "ingredients": [
            "4 peitos de frango sem osso cortados ao meio",
            "Sal a gosto",
            "1 cenoura raspada e passada no ralador grosso",
            "⅓ xícara de uvas-passas pretas sem sementes",
            "1 maçã verde com casca passada no ralador grosso",
            "2 colheres (sopa) de vinagre de vinho branco ou de maçã",
            "4 colheres (sopa) de manteiga ou margarina",
            "1 garrafinha de leite de coco",
            "1 colher (chá) de gengibre ralado",
        ],
        "steps": [
            "Com uma faca afiada, abra cada metade de peito de frango, formando um bife largo. Tempere cada um com sal a gosto.",
            "Numa tigela, coloque a cenoura, as uvas-passas, a maçã ralada, o vinagre e sal a gosto; misture bem.",
            "Divida o recheio em oito partes e coloque uma em cada metade de peito. Enrole e prenda com palito de dente ou amarre com barbante.",
            "Preaqueça o forno em temperatura média (180 °C).",
            "Arrume os enrolados lado a lado numa assadeira.",
            "Numa panela pequena, coloque a manteiga, o leite de coco e o gengibre; cozinhe em fogo baixo, mexendo sempre, até a manteiga derreter.",
            "Retire do fogo e despeje sobre os peitos na assadeira. Asse no forno preaquecido por cerca de 40 minutos ou até a carne dourar e ficar macia. Deixe esfriar e congele.",
        ],
        "notes": (
            "Proteja as pontas dos palitos com papel-alumínio ao embrulhar para não furar a embalagem. "
            "<strong>Congelamento:</strong> coloque os enrolados num tabuleiro forrado com plástico, "
            "tampe e leve ao freezer; transfira para saco plástico, retire o ar e feche. Etiquete e congele. "
            "<strong>Descongelamento:</strong> descongele na geladeira de um dia para o outro; "
            "transfira para assadeira e aqueça em forno em temperatura baixa."
        ),
    },
    {
        "cat": "aves",
        "slug": "enrolados-de-frango",
        "title": "Enrolados de frango",
        "category_line": "Aves · Frango",
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
            "Retire a pele e os ossos dos peitos de frango e divida os filés ao meio para obter 4 pedaços.",
            "Sobre uma tábua, bata os filés com um martelo de carne até ficarem bem finos. Tempere com sal e pimenta e reserve.",
            "Numa panela, misture a água com o arroz cru, a cebolinha, a cenoura, o pimentão e a casca de laranja. Tempere com sal e pimenta. Tampe e cozinhe em fogo baixo por cerca de 20 minutos, até o arroz ficar macio e absorver todo o líquido.",
            "Espalhe o arroz sobre os filés, enrole cada um em cilindro e prenda com palitos.",
            "Arrume os enrolados lado a lado numa assadeira. Pincele um pouco de manteiga, tampe com papel-alumínio e asse em forno médio (180 °C) por cerca de 20 minutos, até ficarem macios. Deixe esfriar e congele.",
            "Numa panela, misture o suco de laranja com a maisena e uma pitada de sal. Cozinha mexendo sempre até formar um creme grosso. Deixe esfriar e congele à parte.",
        ],
        "notes": (
            "Antes de embrulhar, embeba os pedaços no molho para não ressecarem. "
            "<strong>Congelamento:</strong> congele os enrolados no tabuleiro descoberto; "
            "transfira para saco plástico. O molho de laranja vai em recipiente rígido, depois em saco plástico. "
            "<strong>Descongelamento:</strong> descongele os enrolados na geladeira; "
            "aqueça o molho em fogo baixo; aqueça os enrolados no forno cobertos com papel-alumínio, "
            "despeje o molho e sirva."
        ),
    },
    {
        "cat": "aves",
        "slug": "files-de-frango-recheados",
        "title": "Filés de frango recheados",
        "category_line": "Aves · Frango",
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
            "Preaqueça o forno em temperatura média (180 °C). Faça um corte em cada metade de peito, como se fosse uma bolsa.",
            "Coloque uma fatia de bacon dentro de cada bolsa e tempere com sal e pimenta. Prenda com palitos ou amarre com barbante.",
            "Arrume os filés numa assadeira, regue com o azeite e polvilhe com orégano. Asse por cerca de 40 minutos ou até dourar e ficar macio.",
            "Retire do forno. Coloque os pedaços de frango numa embalagem de alumínio e tampe. Mantenha aquecido no forno desligado.",
            "Leve a assadeira ao fogo brando, junte o leite e o requeijão e misture bem com os resíduos do frango até obter um molho uniforme.",
            "Cubra o frango com o molho, deixe esfriar e congele.",
        ],
        "notes": (
            "Alternativa: abra os peitos ao meio sem separar as metades, recheie, enrole uma metade sobre a outra "
            "e prenda com palitos ou barbante. "
            "<strong>Congelamento:</strong> coloque a embalagem de alumínio com o frango num saco plástico, "
            "vede, etiquete e congele. "
            "<strong>Descongelamento:</strong> descongele na geladeira de um dia para o outro; "
            "aqueça no forno ainda tampado em temperatura baixa; passe para travessa, "
            "polvilhe com salsa e sirva."
        ),
    },
    {
        "cat": "aves",
        "slug": "frango-assado-com-cerveja",
        "title": "Frango assado com cerveja",
        "category_line": "Aves · Frango",
        "meta": [("Rendimento", "4 porções"), ("Tempo", "1 h 40 min")],
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
            "Leve ao forno preaquecido e asse até o frango dourar e ficar macio (cerca de 1 hora e 40 minutos), "
            "banhando de vez em quando com o caldo da assadeira. Retire do forno, deixe esfriar e congele.",
        ],
        "notes": (
            "Pode dividir o frango em porções separadas para congelar. "
            "<strong>Congelamento:</strong> coloque o frango com o molho em embalagem de papel-alumínio, "
            "ponha num saco plástico, retire o ar e feche hermeticamente; etiquete e congele. "
            "<strong>Descongelamento:</strong> descongele na geladeira de um dia para o outro; "
            "cubra com papel-alumínio e leve ao forno para aquecer."
        ),
    },
    {
        "cat": "aves",
        "slug": "frango-na-pucara",
        "title": "Frango na púcara",
        "category_line": "Aves · Frango",
        "meta": [("Rendimento", "4 porções"), ("Tempo", "1 h 30 min")],
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
            "Descasque os tomates, retire as sementes e corte em cubinhos de cerca de 1 cm.",
            "Preaqueça o forno em temperatura alta (200 °C). Esmague os dentes de alho.",
            "Tempere os pedaços de frango com sal e pimenta e distribua numa panela de barro refratária com tampa.",
            "Acrescente o presunto escorrido, o tomate, o alho e as cebolas inteiras.",
            "Distribua a manteiga sobre os pedaços de frango.",
            "Regue com o vinho do Porto, o conhaque e o vinho branco. Junte a mostarda.",
            "Tampe bem a panela e leve ao forno preaquecido até o frango ficar cozido e macio (cerca de 1 hora).",
            "Destampe e volte ao forno até a superfície dourar (cerca de 30 minutos). Retire, deixe esfriar e congele.",
        ],
        "notes": (
            "Clássico da cozinha regional portuguesa; o nome vem do tacho de barro com tampa (púcara). "
            "<strong>Congelamento:</strong> coloque o frango num recipiente rígido, cubra com filme plástico "
            "e congele; retire do recipiente, embale em filme, vede e etiquete. "
            "<strong>Descongelamento:</strong> descongele na geladeira de um dia para o outro e aqueça "
            "na panela de barro tampada. Sirva na mesma panela, com batatas fritas em palitos e arroz."
        ),
    },
    {
        "cat": "aves",
        "slug": "frango-ao-caril",
        "title": "Frango ao caril",
        "category_line": "Aves · Frango",
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
            "Numa panela grande de ferro ou alumínio, aqueça bem o óleo e frite os pedaços de frango por 3 a 4 minutos, "
            "virando com um garfo, sem deixar dourar. Transfira para um prato.",
            "Na mesma panela, coloque a cebola, o alho e o gengibre e refogue mexendo sempre por 4 minutos "
            "ou até a cebola ficar macia e dourada.",
            "Abaixe o fogo, acrescente 1 colher de caril e 1 colher de água. Cozinhe cerca de 2 minutos mexendo sempre. "
            "Junte os tomates descascados, sem sementes e picados, 1 colher de coentro, o iogurte e o sal restante.",
            "Aumente um pouco o fogo, acrescente o frango com o caldo do prato e o restante da água. "
            "Deixe ferver e vá virando os pedaços para cozinhar uniformemente.",
            "Reduza o fogo ao mínimo, tampe bem e cozinhe por 25 minutos ou até o frango ficar macio.",
            "Retire do fogo, acrescente o suco de limão e misture bem. Arrume os pedaços num refratário forrado com plástico, "
            "despeje o molho por cima, deixe esfriar e congele.",
        ],
        "notes": (
            "O pó de caril é tempero indiano (canela, cravo, coentro, cominho, cardamomo e pimenta-do-reino). "
            "<strong>Congelamento:</strong> tampe o refratário com plástico e congele; "
            "retire do refratário, embrulhe em filme, etiquete e congele. "
            "<strong>Descongelamento:</strong> desembrulhe e coloque numa panela; "
            "aqueça em fogo baixo. Polvilhe o caril e coentro restantes e sirva com arroz branco."
        ),
    },
    {
        "cat": "aves",
        "slug": "frango-estufado-com-tomates",
        "title": "Frango estufado com tomates",
        "category_line": "Aves · Frango",
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
            "Numa panela grande, coloque o óleo, a cebola, o alho amassado, o bacon e o pimentão picados. "
            "Leve ao fogo para fritar o bacon e refogar os legumes.",
            "Junte os pedaços de frango, os tomates picados, o purê de tomate, a páprica, o açúcar, sal e pimenta. "
            "Tampe e deixe cozinhar o frango.",
            "Acrescente as azeitonas e 2 colheres de salsa; cozinhe mais um pouco com a panela destampada. "
            "Deixe esfriar e congele.",
        ],
        "notes": (
            "A páprica é tempero em pó vermelho (doce ou picante), semelhante ao colorífico. "
            "<strong>Congelamento:</strong> passe para recipiente rígido, cubra com filme e congele; "
            "retire, transfira para saco plástico, retire o ar e feche. "
            "<strong>Descongelamento:</strong> coloque numa panela em banho-maria em fogo brando "
            "ou no micro-ondas (descongelar depois aquecer). Polvilhe a salsa restante e sirva."
        ),
    },
    {
        "cat": "aves",
        "slug": "peru-recheado-com-risoto",
        "title": "Peru recheado com risoto",
        "category_line": "Aves · Outras aves",
        "meta": [("Rendimento", "12 porções")],
        "ingredients": [
            "½ xícara de uvas-passas pretas",
            "1 xícara de champanhe",
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
            "2 xícaras de champanhe",
            "1 peru de 4 a 5 kg",
        ],
        "steps": [
            "Coloque as uvas-passas numa tigela, cubra com champanhe e deixe de molho.",
            "Numa panela, derreta 4 colheres de manteiga em fogo baixo. Junte a cebola e deixe dourar. "
            "Acrescente o arroz e frite até soltar. Cubra com o caldo de galinha e cozinhe até o arroz ficar macio mas al dente.",
            "Retire do fogo, acrescente as uvas-passas escorridas e as castanhas picadas. Misture.",
            "Regue o arroz com o champanhe do molho das uvas e misture com cuidado até obter um risoto úmido. Congele.",
            "Numa outra panela, derreta 1 xícara de manteiga em fogo baixo. Retire do fogo e acrescente as cebolas, "
            "o purê de tomate, o sal, a pimenta branca e o champanhe. Misture.",
            "Tempere o peru inteiro com essa mistura, levantando a pele do peito para espalhar por baixo também.",
        ],
        "notes": (
            "Ao assar, calcule cerca de 1 hora de forno para cada quilo de peru. "
            "<strong>Congelamento:</strong> risoto em recipiente rígido, depois em saco plástico; "
            "peru embrulhado em alumínio e saco plástico hermético. "
            "<strong>Descongelamento:</strong> descongele peru e risoto na geladeira de um dia para o outro; "
            "recheie o peru com o risoto, cubra com alumínio e asse a 200 °C por 4 a 5 horas, "
            "regando com caldo de galinha; retire o alumínio 40 min antes para dourar. Sirva com gomos de laranja."
        ),
    },
    {
        "cat": "doces",
        "slug": "bolacha-de-nescau",
        "title": "Bolacha de Nescau",
        "category_line": "Doces · Biscoitos",
        "meta": [("Rendimento", "cerca de 20 bolachas"), ("Tempo", "15 min")],
        "ingredients": [
            "1 copo de farinha de trigo",
            "1 copo de Nescau",
            "1 ovo",
            "3 colheres de margarina",
        ],
        "steps": [
            "Misture a farinha, o Nescau, o ovo e a margarina até formar uma massa homogênea.",
            "Modele bolinhas, achate com um garfo e disponha numa assadeira.",
            "Leve ao forno por cerca de 15 minutos até firmar.",
        ],
        "notes": "Receita de 4 ingredientes (Pinterest). Use o mesmo copo para medir farinha e Nescau.",
    },
]

INDEX_INSERTS: list[tuple[str, str, str]] = [
    # (section marker regex or unique anchor, title, href slug path)
    ("pate-de-miudos-de-frango", "Patê de fígado de galinha", "./receitas/acompanhamentos/pate-de-figado-de-galinha.html"),
    ("torta-de-frango-com-catupiry", "Torta de frango", "./receitas/tortas-salgadas/torta-de-frango.html"),
    ("files-de-frango-gelados", "Filés de frango recheados", "./receitas/aves/files-de-frango-recheados.html"),
    ("frango-ao-forno", "Enroladinhos Meireles", "./receitas/aves/enroladinhos-meireles.html"),
    ("frango-ao-forno", "Enrolados de frango", "./receitas/aves/enrolados-de-frango.html"),
    ("frango-ao-forno", "Frango ao caril", "./receitas/aves/frango-ao-caril.html"),
    ("frango-ao-forno", "Frango assado com cerveja", "./receitas/aves/frango-assado-com-cerveja.html"),
    ("frango-ao-forno", "Frango estufado com tomates", "./receitas/aves/frango-estufado-com-tomates.html"),
    ("frango-ao-forno", "Frango na púcara", "./receitas/aves/frango-na-pucara.html"),
    ("peru-com-peras-e-arroz-de-nozes", "Peru recheado com risoto", "./receitas/aves/peru-recheado-com-risoto.html"),
    ("bolachinha-croc-de-chocolate", "Bolacha de Nescau", "./receitas/doces/bolacha-de-nescau.html"),
]


def render_recipe(r: dict) -> str:
    cat = r["cat"]
    cat_label = CAT_LABEL[cat]
    title = r["title"]
    slug = r["slug"]
    category_line = r.get("category_line", cat_label)
    desc = html.escape(f"{title} — ficha A5 para imprimir.")
    meta_html = ""
    if r.get("meta"):
        spans = "".join(
            f"\n          <span><strong>{html.escape(k)}:</strong> {html.escape(v)}</span>"
            for k, v in r["meta"]
        )
        meta_html = f"\n        <div class=\"meta\">{spans}\n        </div>"
    ingredients = "\n".join(f"          <li>{html.escape(i)}</li>" for i in r["ingredients"])
    steps = "\n".join(f"          <li>{html.escape(s)}</li>" for s in r["steps"])
    notes = ""
    if r.get("notes"):
        notes = f"""
        <h2>Observação</h2>
        <p class="notes">{r["notes"]}</p>"""
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
        <p class="category">{html.escape(category_line)}</p>
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


def insert_index_entries() -> None:
    index_path = ROOT / "index.html"
    text = index_path.read_text(encoding="utf-8")
    for anchor, title, href in INDEX_INSERTS:
        if href.split("/")[-1].replace(".html", "") in text:
            print(f"skip index {title}")
            continue
        pattern = rf'(          <li>\n            <a href="\./receitas/[^"]+/{re.escape(anchor)}\.html">[^<]+</a>\n          </li>)'
        m = re.search(pattern, text)
        if not m:
            raise SystemExit(f"anchor not found: {anchor}")
        insert = (
            f"{m.group(1)}\n"
            f"          <li>\n"
            f'            <a href="{href}">{html.escape(title)}</a>\n'
            f"          </li>"
        )
        text = text.replace(m.group(1), insert, 1)
        print(f"index + {title}")
    index_path.write_text(text, encoding="utf-8")


def main() -> None:
    written = write_recipes()
    if written:
        insert_index_entries()
    print(f"Created {len(written)} recipes")


if __name__ == "__main__":
    main()
