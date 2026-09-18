#!/usr/bin/env python3
"""Generate recipe HTML from Telegram batch (2026-08-20) — A arte de congelar."""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PENDING = ROOT / "entradas" / "pending"

CATEGORIES = {
    "doces": "Doces",
    "salgados": "Salgados",
}

RECIPES: list[dict] = [
    # --- SALGADOS / Massas fritas/assadas ---
    {
        "cat": "salgados",
        "subcat": "Massas fritas/assadas",
        "slug": "pao-de-forma",
        "title": "Pão de fôrma",
        "meta": [("Rendimento", "1 pão")],
        "ingredients": [
            "5 1/2 a 6 1/2 xícaras de farinha de trigo",
            "2 colheres (chá) de sal",
            "2 colheres (sopa) de manteiga",
            "1 tablete (15 g) de fermento para pão",
            "1 3/4 xícaras de água morna",
            "Farinha de trigo para polvilhar",
            "Manteiga para untar",
        ],
        "steps": [
            "Numa tigela, peneire a farinha com o sal. Acrescente a manteiga e esfarele na farinha. Faça uma cova no centro. Dissolva o fermento na água morna.",
            "Despeje o fermento dissolvido de uma vez e misture com colher de pau, acrescentando farinha se necessário, até obter massa consistente.",
            "Vire a massa sobre superfície enfarinhada e sove cerca de 10 minutos até ficar lisa, elástica e não grudar.",
            "Forme uma bola, coloque numa tigela grande untada, cubra com saco plástico untado e deixe crescer até dobrar de volume.",
            "Despeje sobre superfície enfarinhada, sove para eliminar bolhas de ar e modele um rolo do comprimento da forma. Enrolar, dobrar as pontas por baixo e colocar numa forma de pão de 900 g untada.",
            "Cubra novamente e deixe crescer até dobrar. Preaqueça o forno em temperatura alta (230 °C) e asse por 30 a 40 minutos até dourar.",
            "O pão está pronto quando soa oco ao bater na base. Deixe esfriar sobre uma grade e congele.",
        ],
        "notes": "Congelamento: embrulhe em papel-alumínio ou filme plástico, coloque num saco plástico, retire o ar, vede bem, etiquete e congele. Descongelamento: deixe em temperatura ambiente por cerca de 2 horas.",
    },
    {
        "cat": "salgados",
        "subcat": "Massas fritas/assadas",
        "slug": "pao-integral",
        "title": "Pão integral",
        "meta": [("Rendimento", "2 pães")],
        "ingredients": [
            "3 colheres (sopa) de açúcar",
            "2 tabletes (30 g) de fermento para pão",
            "4 colheres (chá) de sal",
            "4 xícaras de farinha integral",
            "3 a 3 1/2 xícaras de farinha de trigo",
            "2 1/2 xícaras de leite",
            "1/3 xícara de manteiga ou margarina",
            "1/3 xícara de melado",
            "Farinha de trigo para polvilhar",
            "Manteiga ou margarina para untar",
        ],
        "steps": [
            "Numa tigela grande, misture o açúcar, o fermento, o sal, 2 xícaras de farinha integral e 1 xícara de farinha de trigo.",
            "Em outra tigela, aqueça o leite, a manteiga e o melado em fogo baixo até ficar bem quente.",
            "Na batedeira em velocidade baixa, vá acrescentando os líquidos aos secos. Bata em velocidade média por 2 minutos. Junte mais 1/2 xícara de farinha de trigo e bata por mais 2 minutos.",
            "Acrescente mais 1 1/2 xícaras de farinha integral e cerca de 1 1/2 xícaras de farinha de trigo, misturando com colher de pau.",
            "Sove sobre superfície enfarinhada até ficar elástica. Forme uma bola, coloque numa tigela untada, vire a massa e deixe crescer em local morno até dobrar de volume.",
            "Despeje sobre superfície enfarinhada, divida em duas partes e deixe descansar 15 minutos cobertas. Unte duas formas de pão de 13 × 23 cm.",
            "Abra cada porção em retângulo de 20 × 30,5 cm, enrole como rocambole, sele as pontas, dobre por baixo e coloque nas formas. Deixe crescer até dobrar.",
            "Asse em forno preaquecido em temperatura média (200 °C) por 30 a 35 minutos. Desenforme, deixe esfriar e congele.",
        ],
        "notes": "Para saber se a massa cresceu, coloque uma bolinha de massa num copo d'água logo após prepará-la: quando subir à superfície, a massa está pronta. Congelamento: embrulhe em filme ou alumínio, coloque num saco plástico sem ar, etiquete e congele. Descongelamento: temperatura ambiente por cerca de 2 horas.",
    },
    {
        "cat": "salgados",
        "subcat": "Massas fritas/assadas",
        "slug": "paezinhos-rapidos",
        "title": "Pãezinhos rápidos",
        "meta": [("Rendimento", "28 pãezinhos")],
        "ingredients": [
            "2 xícaras de farinha de trigo",
            "2 1/2 colheres (chá) de fermento em pó",
            "1 colher (chá) de sal",
            "1/3 xícara de manteiga ou margarina gelada",
            "Farinha de trigo para polvilhar",
        ],
        "steps": [
            "Preaqueça o forno em temperatura alta (250 °C). Numa tigela, peneire a farinha, o fermento e o sal. Acrescente a manteiga e, com duas facas, corte em pedacinhos até formar farofa.",
            "Amasse até incorporar bem. Polvilhe a mesa com farinha, abra a massa com as mãos até 1 cm de espessura.",
            "Corte com cortador redondo de 5 cm de diâmetro.",
            "Disponha numa assadeira sem untar e asse no forno preaquecido até levemente dourados (12 a 15 minutos). Deixe esfriar e congele.",
        ],
        "notes": "Congelamento: leve ao freezer cobertos com plástico até firmarem; passe para saco plástico, retire o ar, vede e congele. Descongelamento: temperatura ambiente por cerca de 1 hora. Pode variar o sabor com alcaravia, erva-doce ou linguiça antes de assar.",
    },
    {
        "cat": "salgados",
        "subcat": "Massas fritas/assadas",
        "slug": "pao-sirio",
        "title": "Pão sírio",
        "meta": [("Rendimento", "10 pães")],
        "ingredients": [
            "6 xícaras de farinha de trigo",
            "1 tablete (15 g) de fermento para pão",
            "2 xícaras de água morna",
            "1 1/2 colher (chá) de sal",
            "1 colher (chá) de açúcar",
            "2 colheres (sopa) de óleo",
            "Farinha de trigo para polvilhar",
            "Óleo para untar",
        ],
        "steps": [
            "Preaqueça o forno em temperatura baixa (100 °C). Peneire a farinha numa tigela grande e aqueça no forno.",
            "Dissolva o fermento em 1/4 xícara de água morna. Acrescente o restante da água, o sal e o açúcar; misture bem.",
            "Retire a farinha do forno, separe 2 xícaras. Faça uma cova na farinha restante, despeje a mistura de fermento e mexa até formar uma pasta. Cubra e deixe descansar protegida do frio até espumar.",
            "Junte a farinha reservada e o óleo aos poucos; bata bem por 10 minutos.",
            "Sove sobre superfície enfarinhada por 10 minutos até ficar lisa por dentro e levemente enrugada por fora. Forme uma bola, unte com óleo, cubra com plástico e deixe crescer por 1 hora.",
            "Despeje, sove 1 minuto e forme 10 bolas iguais. Abra cada uma com 20 cm de diâmetro e coloque sobre pano enfarinhado. Cubra e descanse 20 minutos. Preaqueça o forno em temperatura média (200 °C).",
            "Unte uma assadeira com óleo e coloque na parte mais alta do forno até ficar bem quente. Asse um pão de cada vez por 4 a 5 minutos, até incharem. Envolva em pano limpo para manter macios.",
        ],
        "notes": "Congelamento: embrulhe em filme plástico, congele até firmar e passe para saco plástico sem ar. Descongelamento: temperatura ambiente por 1 hora. Fermento biológico fresco pode ser congelado em papel-alumínio (dura 3 meses).",
    },
    # --- DOCES / Outros doces ---
    {
        "cat": "doces",
        "subcat": "Outros doces",
        "slug": "broinhas-de-fuba",
        "title": "Broinhas de fubá",
        "meta": [("Rendimento", "40 broinhas")],
        "ingredients": [
            "2 xícaras de açúcar",
            "1 xícara de manteiga",
            "5 gemas",
            "1 garrafa pequena (200 ml) de leite de coco",
            "1 xícara de leite",
            "2 xícaras de fubá",
            "1 xícara de farinha de trigo",
            "1 colher (sopa) de fermento em pó",
            "5 claras batidas em neve firme",
        ],
        "steps": [
            "Forre 40 forminhas de 7 cm de diâmetro com 2 camadas de forminha de papel.",
            "Preaqueça o forno em temperatura média (180 °C). Bata o açúcar com a manteiga até formar creme esbranquiçado.",
            "Acrescente as gemas uma a uma, alternando com o leite de coco e o leite, sem parar a batedeira. Desligue.",
            "Junte o fubá, a farinha e o fermento; misture com colher de pau. Incorpore as claras em neve delicadamente.",
            "Distribua nas forminhas e asse até dourar (cerca de 35 minutos). Desenforme, deixe esfriar e congele.",
        ],
        "notes": "Congelamento: coloque num recipiente rígido, próximas umas das outras, preenchendo os espaços vazios e intercalando camadas com toalhas de papel; vede bem e congele. Descongelamento: temperatura ambiente por 1 hora e aqueça no forno.",
    },
    {
        "cat": "doces",
        "subcat": "Outros doces",
        "slug": "muffins",
        "title": "Muffins",
        "meta": [("Rendimento", "12 muffins")],
        "ingredients": [
            "Manteiga para untar",
            "1 xícara de farinha de trigo",
            "1 xícara de farinha de trigo integral",
            "1 colher (sopa) de açúcar",
            "1/2 colher (chá) de sal",
            "3 colheres (chá) de fermento em pó",
            "1 ovo",
            "1/4 xícara de óleo",
            "1 xícara de leite",
            "1/2 xícara de passas brancas de molho em água morna e escorridas",
        ],
        "steps": [
            "Preaqueça o forno em temperatura média (180 °C). Unte 12 forminhas para muffins.",
            "Peneire juntas as farinhas, o açúcar, o sal e o fermento numa tigela média.",
            "Numa jarra, misture o ovo batido, o óleo e o leite. Despeje sobre a farinha com as passas e misture rapidamente com colher de pau — a massa deve ficar empelotada.",
            "Distribua nas forminhas até 2/3 da capacidade e asse até dourar e crescer (cerca de 25 minutos). Desenforme, deixe esfriar e congele.",
        ],
        "notes": "Congelamento: recipiente rígido com toalhas de papel entre camadas e nos espaços vazios; vede e congele. Descongelamento: temperatura ambiente por 1 hora e aqueça no forno. Sirva com manteiga e geleia. Sem forminhas de muffin, use forminhas de empada de 7 cm untadas.",
    },
    # --- DOCES / Tortas e bolos ---
    {
        "cat": "doces",
        "subcat": "Tortas e bolos",
        "slug": "rosca-de-natal",
        "title": "Rosca de Natal",
        "meta": [("Rendimento", "10 porções")],
        "ingredients": [
            "1 caixa (400 g) de mistura para salgados",
            "1/3 xícara de leite",
            "3 ovos (2 para a massa, 1 para o recheio)",
            "1/4 xícara de manteiga",
            "1/2 xícara de açúcar cristal",
            "1/4 xícara de leite (recheio)",
            "1/4 xícara de mel",
            "1 colher (chá) de canela em pó",
            "1 1/2 xícara de nozes picadas",
            "2 colheres (chá) de suco de limão",
            "2 xícaras de passas brancas inteiras e frutas cristalizadas picadas de molho em 2/3 xícara de licor Cointreau",
            "1 gema batida",
        ],
        "steps": [
            "Numa tigela, misture a mistura para salgados, 1/3 xícara de leite e 2 ovos com as mãos; reserve.",
            "Para o recheio: derreta a manteiga com o açúcar cristal, 1/4 xícara de leite, o mel e a canela; leve a ferver. Junte as nozes, retire do fogo e deixe amornar. Acrescente o terceiro ovo batido e o suco de limão.",
            "Abra a massa em retângulo de 37 × 54 cm. Espalhe o recheio, escorra passas e frutas cristalizadas e distribua por cima.",
            "Enrole pelo lado comprido como rocambole e pincele com a gema. Coloque numa assadeira untada, umedeça e grude as pontas. Corte fatias iguais até dois dedos abaixo do centro e incline cada fatia.",
            "Cubra com papel-alumínio untado e deixe crescer 20 minutos. Preaqueça o forno em temperatura média (200 °C).",
            "Retire o alumínio e asse 15 minutos. Reduza para 180 °C e asse mais 10 minutos ou até dourar. Deixe esfriar sobre grade e congele.",
        ],
        "notes": "Massas de pão cruas não devem ser recongeladas — asse antes de congelar de novo. Congelamento: cubra com plástico, congele, passe para saco plástico sem ar. Descongelamento: temperatura ambiente por 2 horas; decore com glacê de açúcar de confeiteiro e limão.",
    },
    {
        "cat": "doces",
        "subcat": "Tortas e bolos",
        "slug": "bolo-merenda",
        "title": "Bolo merenda",
        "meta": [("Rendimento", "8 porções")],
        "ingredients": [
            "3/4 xícara de manteiga",
            "3/4 xícara de açúcar",
            "3 gemas",
            "1 1/2 xícara de farinha de trigo",
            "1 colher (chá) de fermento em pó",
            "2 colheres (sopa) de leite",
            "3 claras",
            "Manteiga para untar",
        ],
        "steps": [
            "Preaqueça o forno em temperatura média (200 °C). Bata a manteiga até ficar cremosa. Acrescente o açúcar aos poucos, depois as gemas uma a uma, até formar creme claro.",
            "Desligue a batedeira. Incorpore a farinha peneirada com o fermento, alternando com o leite, até homogeneizar.",
            "Bata as claras em neve e misture delicadamente à massa.",
            "Despeje numa forma de abrir de 21 cm untada e asse até dourar (cerca de 30 minutos). Desenforme, deixe esfriar e congele.",
        ],
        "notes": "Congelamento: cubra com plástico, congele, embrulhe em filme ou alumínio e coloque num saco plástico sem ar. Descongelamento: temperatura ambiente por 2 horas. Variações: goiabada (1/2 xícara de cubos) ou chocolate chips (1/2 xícara).",
    },
    {
        "cat": "doces",
        "subcat": "Tortas e bolos",
        "slug": "bolo-de-especiarias",
        "title": "Bolo de especiarias",
        "meta": [("Rendimento", "6 a 8 porções")],
        "ingredients": [
            "2 xícaras de farinha de trigo",
            "1 xícara de açúcar",
            "1 colher (sopa) de fermento em pó",
            "1 colher (chá) de sal",
            "1/2 colher (chá) de bicarbonato de sódio",
            "1/2 colher (sopa) de cravo-da-índia em pó",
            "1 colher (sopa) de canela em pó",
            "1/2 xícara de margarina",
            "3/4 xícara de açúcar mascavo",
            "1 xícara de creme de leite azedado com 1 colher (sopa) de suco de limão",
            "3 ovos",
            "1/2 xícara de nozes picadas",
        ],
        "steps": [
            "Preaqueça o forno em temperatura média (180 °C). Misture a farinha, o açúcar, o fermento, o sal, o bicarbonato, o cravo e a canela.",
            "Acrescente a margarina, o açúcar mascavo e o creme azedado; misture até a farinha umedecer.",
            "Bata na batedeira 2 minutos em velocidade média. Junte os ovos e bata mais 2 minutos. Incorpore as nozes.",
            "Despeje numa forma de bolo inglês (7,5 × 12 × 25 cm) untada e enfarinhada. Asse 30 a 35 minutos. Desenforme após 10 minutos, deixe esfriar e congele.",
        ],
        "notes": "Congelamento: cubra com plástico, congele, embrulhe em alumínio ou filme e coloque num saco plástico sem ar. Descongelamento: temperatura ambiente por 2 horas, forno por 10 minutos ou micro-ondas em descongelar por 3 minutos.",
    },
    {
        "cat": "doces",
        "subcat": "Tortas e bolos",
        "slug": "bolo-de-mandioca",
        "title": "Bolo de mandioca",
        "meta": [("Rendimento", "12 porções")],
        "ingredients": [
            "2 1/4 xícaras de mandioca ralada fina",
            "2 1/4 xícaras de queijo-de-minas meia cura ralado fino",
            "2 1/4 xícaras de açúcar",
            "1 1/4 xícaras de leite",
            "1 colher (café) de canela em pó",
            "1 colher (café) de cravo em pó",
            "8 ovos levemente batidos",
            "Manteiga para untar",
            "Canela em pó e açúcar para polvilhar",
        ],
        "steps": [
            "Preaqueça o forno em temperatura média (180 °C). Misture mandioca, queijo, açúcar, leite, canela e cravo.",
            "Acrescente os ovos e misture até incorporar.",
            "Despeje numa assadeira untada de 24 × 34 cm e asse até dourar (cerca de 45 minutos).",
            "Polvilhe generosamente com mistura de canela e açúcar. Deixe esfriar, corte em quadrados e congele.",
        ],
        "notes": "Congelamento: disponha os quadrados numa assadeira coberta com plástico, congele, passe para saco plástico sem ar. Descongelamento: temperatura ambiente por cerca de 1 hora.",
    },
    {
        "cat": "doces",
        "subcat": "Tortas e bolos",
        "slug": "bolo-de-chocolate",
        "title": "Bolo de chocolate",
        "meta": [("Rendimento", "10 porções")],
        "ingredients": [
            "Massa: 50 g de chocolate amargo picado, 3/4 xícara de manteiga, 1 1/2 xícara de açúcar, 3 ovos, 1 colher (chá) de essência de baunilha, 2 xícaras de farinha de trigo, 2 colheres (chá) de fermento em pó, 1/2 colher (chá) de sal, 3/4 xícara de leite",
            "Calda: 1 colher (sopa) de manteiga, 1 xícara de açúcar, 1/2 xícara de chocolate em pó, 1/4 xícara de leite",
            "120 g de chocolate branco picado para decorar",
        ],
        "steps": [
            "Derreta o chocolate amargo em banho-maria; bata até ficar liso e reserve.",
            "Misture vigorosamente a manteiga com o açúcar até cremoso. Junte os ovos um a um, a baunilha e o chocolate derretido.",
            "Peneire a farinha com fermento e sal; incorpore alternando com o leite até massa homogênea.",
            "Preaqueça o forno em temperatura média (180 °C). Despeje numa forma de buraco de 26 cm untada e asse até firmar. Desenforme após 10 minutos e deixe esfriar.",
            "Para a calda: derreta a manteiga, junte açúcar, chocolate em pó e leite; cozinhe em fogo brando mexendo. Espalhe sobre o bolo frio.",
            "Derreta o chocolate branco em banho-maria, bata até liso e despeje sobre o bolo. Deixe esfriar e congele.",
        ],
        "notes": "Congelamento: cubra com plástico, congele, retire do prato e passe para saco plástico. Descongelamento: temperatura ambiente por 2 horas.",
    },
    {
        "cat": "doces",
        "subcat": "Tortas e bolos",
        "slug": "bolo-de-laranja",
        "title": "Bolo de laranja",
        "meta": [("Rendimento", "8 porções")],
        "ingredients": [
            "1/2 xícara de óleo",
            "2 xícaras de açúcar",
            "4 gemas",
            "2 xícaras de fubá",
            "1 xícara de farinha de trigo",
            "1 colher (sopa) de fermento em pó",
            "1 xícara de suco de laranja",
            "4 claras batidas em neve",
            "Manteiga para untar",
            "Farinha de trigo para polvilhar",
        ],
        "steps": [
            "Preaqueça o forno em temperatura média (180 °C). Bata o óleo, o açúcar e as gemas até formar creme.",
            "Peneire o fubá, a farinha e o fermento; incorpore ao creme alternando com o suco de laranja.",
            "Misture as claras em neve por último. Despeje numa forma redonda grande com buraco, untada e enfarinhada.",
            "Asse por 45 minutos. Desenforme, deixe esfriar e congele.",
        ],
        "notes": "Congelamento: cubra com plástico, congele, embrulhe em filme e congele. Descongelamento: temperatura ambiente por cerca de 2 horas. Em formas com buraco, preencha o vazio com plástico antes de congelar.",
    },
    {
        "cat": "doces",
        "subcat": "Tortas e bolos",
        "slug": "bolo-de-abacaxi",
        "title": "Bolo de abacaxi",
        "meta": [("Rendimento", "8 porções")],
        "ingredients": [
            "1 colher (sopa) de manteiga",
            "1/4 xícara de açúcar demerara",
            "5 rodelas de abacaxi em conserva escorridas",
            "5 cerejas ao marasquino escorridas e cortadas ao meio",
            "1 xícara de farinha de trigo",
            "3/4 xícara de açúcar",
            "1 pitada de sal",
            "1 ovo",
            "2 colheres (sopa) de margarina cremosa",
            "1/2 xícara da calda do abacaxi",
            "1 colher (chá) de essência de baunilha",
            "1 colher (chá) de fermento em pó",
        ],
        "steps": [
            "Preaqueça o forno em temperatura média (180 °C). Derreta a manteiga numa forma refratária de vidro de 25 cm e espalhe nas paredes.",
            "Polvilhe o açúcar demerara. Forre com rodelas de abacaxi e complete com cerejas.",
            "No liquidificador, bata farinha, açúcar, sal, ovo, margarina, calda do abacaxi e baunilha por 3 minutos. Acrescente o fermento e bata mais um pouco.",
            "Despeje sobre o abacaxi e asse até o palito sair limpo perto do centro. Desenforme sobre prato, deixe esfriar e congele.",
        ],
        "notes": "Congelamento: cubra com plástico, congele, retire do prato e embrulhe em filme. Descongelamento: temperatura ambiente por 2 horas.",
    },
    {
        "cat": "doces",
        "subcat": "Tortas e bolos",
        "slug": "bolo-de-fuba-e-coco",
        "title": "Bolo de fubá e coco",
        "meta": [("Rendimento", "24 porções")],
        "ingredients": [
            "1 xícara de açúcar",
            "1/2 xícara de manteiga ou margarina",
            "3 gemas",
            "1 vidro pequeno (200 ml) de leite de coco",
            "1 xícara de leite",
            "1 xícara de fubá",
            "1 pacote pequeno (50 g) de coco ralado",
            "1/2 xícara de farinha de trigo",
            "1 colher (sopa) de fermento em pó",
            "3 claras batidas em neve firme",
            "Manteiga para untar",
            "2 colheres (sopa) de açúcar",
        ],
        "steps": [
            "Preaqueça o forno em temperatura média (200 °C). Bata açúcar e manteiga até creme esbranquiçado.",
            "Junte as gemas uma a uma, metade do leite de coco e todo o leite; continue batendo.",
            "Desligue e incorpore fubá, coco, farinha e fermento. Misture as claras em neve delicadamente.",
            "Despeje numa assadeira de 20 × 30 cm untada. Asse 20 minutos, reduza para 150 °C e asse mais 5 minutos.",
            "Misture o restante do leite de coco com 2 colheres de açúcar e despeje sobre o bolo quente. Deixe esfriar, corte em quadrados e congele.",
        ],
        "notes": "Congelamento: quadrados numa assadeira coberta com plástico, congele, passe para saco plástico sem ar. Descongelamento: temperatura ambiente por cerca de 1 hora.",
    },
    {
        "cat": "doces",
        "subcat": "Tortas e bolos",
        "slug": "bolo-gelado-de-goiaba",
        "title": "Bolo gelado de goiaba",
        "meta": [("Rendimento", "10 a 12 porções")],
        "ingredients": [
            "Sorvete: 3 gemas, 1 xícara de açúcar, 1 xícara de leite morno, 1 garrafa (500 ml) de suco de goiaba industrializado, 1/2 xícara de creme de leite fresco batido em chantilly",
            "Rocambole: 4 gemas, 1/2 xícara de açúcar, 4 claras em neve, 2/3 xícara de farinha de trigo, 1 pitada de sal, manteiga e farinha para untar, 400 g de doce de goiaba em pasta",
        ],
        "steps": [
            "Bata as gemas do sorvete com açúcar até claro. Acrescente o leite morno aos poucos até esfriar. Junte o suco de goiaba e incorpore o chantilly. Cubra e congele 1 hora.",
            "Retire, bata para cremoso e volte ao freezer. Preaqueça o forno em temperatura média (200 °C).",
            "Para o rocambole: bata gemas com açúcar; misture 4 colheres de claras. Peneire farinha e sal por cima, incorpore o restante das claras.",
            "Divida em duas partes e asse em assadeiras de 21 × 31 cm forradas com papel untado e enfarinhado por cerca de 10 minutos.",
            "Desenforme sobre pano úmido, espalhe metade do doce de goiaba, enrole com o pano e deixe esfriar. Repita com o outro bolo.",
            "Corte os rocamboles em fatias finas, disponha num prato, cubra com plástico e refrigere 1 hora.",
            "Forre uma forma semiesférica com plástico, forre com fatias de rocambole, recheie com sorvete de goiaba pressionando bem, cubra com mais fatias e congele.",
        ],
        "notes": "Congelamento: cubra com plástico e congele. Descongelamento: descongele na geladeira, desenforme sobre prato redondo e decore a borda com chantilly.",
    },
    {
        "cat": "doces",
        "subcat": "Tortas e bolos",
        "slug": "bolo-de-sorvete-com-cerejas",
        "title": "Bolo de sorvete com cerejas",
        "meta": [("Rendimento", "8 porções")],
        "ingredients": [
            "2 xícaras de sorvete crocante comprado pronto",
            "Cerca de 200 g de biscoitos champanhe",
            "Licor Cointreau",
            "2 xícaras de sorvete de baunilha ou creme comprado pronto",
            "1/3 xícara de chocolate cobertura ralado",
            "2 xícaras de creme de leite fresco",
            "Cerca de 1 1/2 xícara de cerejas em calda escorridas ou cristalizadas",
        ],
        "steps": [
            "Forre o fundo de uma forma quadrada (~1 1/2 litro) com papel-manteiga esticado.",
            "Espalhe uma camada de sorvete crocante e cubra com biscoitos champanhe molhados no licor.",
            "Coloque o sorvete de baunilha por cima. Leve à geladeira para firmar e congele.",
            "Derreta o chocolate ralado em fogo brando; deixe esfriar perto do fogo para não endurecer.",
            "Bata o creme de leite até firmar, incorpore o chocolate frio e congele o creme separadamente.",
        ],
        "notes": "Congelamento: cubra o bolo com plástico, congele e passe para saco plástico; congele o creme de chocolate num recipiente rígido vedado. Descongelamento: descongele bolo e creme na geladeira, decore a borda com o creme em saco de confeitar e polvilhe cerejas por cima.",
    },
    {
        "cat": "doces",
        "subcat": "Tortas e bolos",
        "slug": "cheesecake-basco-de-chocolate",
        "title": "Cheesecake basco de chocolate",
        "meta": [("Rendimento", "8 porções")],
        "ingredients": [
            "500 g de cream cheese em temperatura ambiente",
            "150 g de açúcar",
            "4 ovos",
            "150 g de chocolate meio amargo (70%)",
            "200 ml de creme de leite",
            "1 colher (chá) de sal",
        ],
        "steps": [
            "Preaqueça o forno em temperatura alta (200 °C). Forre uma forma de aro removível com papel-manteiga.",
            "Derreta o chocolate e reserve.",
            "Bata o cream cheese com o açúcar até ficar liso. Acrescente os ovos, um a um.",
            "Incorpore o chocolate derretido, o creme de leite e o sal.",
            "Despeje na forma e asse cerca de 25 minutos, até a superfície dourar e o centro ficar levemente bamboleante.",
            "Deixe esfriar completamente e leve à geladeira por pelo menos 4 horas antes de servir.",
        ],
        "notes": "Fonte Pinterest / @fernandocruz37. Congelamento: fatias embrulhadas em filme num saco plástico sem ar; descongele na geladeira.",
    },
    # --- DOCES / Biscoitos ---
    {
        "cat": "doces",
        "subcat": "Biscoitos",
        "slug": "biscoitinhos-coloridos",
        "title": "Biscoitinhos coloridos",
        "meta": [("Rendimento", "18 biscoitos")],
        "ingredients": [
            "3/4 xícara de margarina",
            "1/2 xícara de açúcar",
            "1 1/2 xícaras de farinha de trigo",
            "1 pacote pequeno (50 g) de coco ralado",
            "1 colher (sopa) de água",
            "1 colher (sopa) de chocolate em pó",
            "Margarina para untar",
        ],
        "steps": [
            "Aqueça uma tigela em banho-maria. Bata margarina e açúcar com colher de pau até obter creme com mais volume.",
            "Acrescente farinha e coco; misture até massa compacta (use água se necessário). Divida ao meio e misture o chocolate em pó a uma metade.",
            "Abra cada metade em retângulo de 17 × 22 cm sobre papel-manteiga. Sobreponha e enrole como rocambole. Envolva em papel-manteiga e refrigere 30 minutos.",
            "Preaqueça o forno em temperatura média (180 °C). Corte rodelas de 1 cm, disponha em assadeira untada e asse 25 minutos ou até dourar. Deixe esfriar e congele.",
        ],
        "notes": "Congelamento: saco plástico sem ar, etiquetado. Descongelamento: temperatura ambiente por cerca de 1 hora.",
    },
    {
        "cat": "doces",
        "subcat": "Biscoitos",
        "slug": "biscoitinhos-de-cerveja",
        "title": "Biscoitinhos de cerveja",
        "meta": [("Rendimento", "45 biscoitinhos")],
        "ingredients": [
            "2 3/4 xícaras de farinha de trigo",
            "1 xícara de manteiga sem sal em temperatura ambiente",
            "2 colheres (sopa) de cerveja",
            "1 xícara de açúcar cristal",
        ],
        "steps": [
            "Preaqueça o forno em temperatura média (180 °C). Misture farinha e manteiga, amassando com as mãos.",
            "Acrescente a cerveja e continue amassando até a massa ligar e poder ser enrolada.",
            "Faça bolinhas de 1,5 cm de diâmetro e passe no açúcar cristal.",
            "Disponha numa assadeira sem untar e asse por 30 minutos. Deixe esfriar e congele.",
        ],
        "notes": "Congelamento: saco plástico sem ar, etiquetado. Descongelamento: temperatura ambiente. Pode achatar as bolinhas para formato de bolachinha.",
    },
    {
        "cat": "doces",
        "subcat": "Biscoitos",
        "slug": "biscoitinhos-de-ameixa-preta",
        "title": "Biscoitinhos de ameixa-preta",
        "meta": [("Rendimento", "120 biscoitinhos")],
        "ingredients": [
            "1 xícara de manteiga",
            "1 xícara de açúcar mascavo",
            "1/2 xícara de açúcar",
            "2 ovos",
            "1 colher (sopa) de vinagre",
            "1 colher (chá) de essência de baunilha",
            "1 xícara de ameixas-pretas secas picadas",
            "4 xícaras de farinha de trigo",
            "1 colher (chá) de bicarbonato de sódio",
            "1 colher (chá) de sal",
            "1 xícara de nozes picadas",
        ],
        "steps": [
            "Bata a manteiga com os açúcares. Acrescente os ovos um a um até creme leve.",
            "Junte vinagre, baunilha, ameixas, ingredientes secos e nozes. Forme 3 rolos de cerca de 5 cm de diâmetro.",
            "Embrulhe em papel-alumínio e leve à geladeira por 1 noite.",
            "Preaqueça o forno em temperatura média (200 °C). Corte rodelas finas, disponha em assadeira sem untar e asse até sequinhos (cerca de 12 minutos). Deixe esfriar e congele.",
        ],
        "notes": "Congelamento: congele cobertos com plástico, passe para saco plástico sem ar. Descongelamento: temperatura ambiente por 1 hora. Também pode abrir a massa gelada e cortar com cortadores.",
    },
    {
        "cat": "doces",
        "subcat": "Biscoitos",
        "slug": "biscoitinhos-de-chocolate-e-coco",
        "title": "Biscoitinhos de chocolate e coco",
        "meta": [("Rendimento", "80 biscoitos")],
        "ingredients": [
            "1 1/4 xícara de margarina",
            "1 xícara de açúcar",
            "1 2/3 xícaras de farinha de trigo",
            "1 colher (sopa) de fermento em pó",
            "1/3 xícara de cacau em pó",
            "1 pitada de sal",
            "1 xícara de chocolate em pó",
            "3 pacotes pequenos (150 g) de coco ralado",
            "1/4 xícara de água fervente",
            "1 colher (chá) de café solúvel já preparado",
        ],
        "steps": [
            "Bata margarina e açúcar até creme leve e fofo.",
            "Peneire farinha, fermento, cacau, sal e chocolate em pó; misture com o coco.",
            "Misture água fervente com café solúvel.",
            "Incorpore os secos em três etapas alternando com a água com café, batendo na batedeira. Descanse 30 minutos na geladeira. Preaqueça o forno em temperatura média (200 °C).",
            "Faça bolinhas do tamanho de uma noz, disponha com 5 cm de espaço e asse. Deixe esfriar e congele.",
        ],
        "notes": "Congelamento: cubra com plástico, congele e passe para saco plástico sem ar. Descongelamento: temperatura ambiente por 1 hora.",
    },
    {
        "cat": "doces",
        "subcat": "Biscoitos",
        "slug": "biscoitinhos-de-caramelo",
        "title": "Biscoitinhos de caramelo",
        "meta": [("Rendimento", "50 biscoitos")],
        "ingredients": [
            "1/2 xícara de manteiga",
            "2/3 xícara de açúcar mascavo",
            "1 ovo",
            "1 1/3 xícara de farinha de trigo",
            "1/2 colher (chá) de fermento em pó",
            "1/2 colher (chá) de essência de baunilha",
            "1/3 xícara de nozes picadas",
        ],
        "steps": [
            "Derreta a manteiga em fogo baixo; retire e misture o açúcar mascavo.",
            "Acrescente o ovo e bata na batedeira até esbranquiçar (cerca de 10 minutos).",
            "Peneire a farinha com o fermento e incorpore. Junte baunilha e nozes. Leve à geladeira até firmar (~40 minutos).",
            "Preaqueça o forno em temperatura média (180 °C). Enrole bolinhas, disponha numa assadeira e asse. Deixe esfriar e congele.",
        ],
        "notes": "Congelamento: cubra com plástico, congele e passe para saco plástico sem ar. Descongelamento: temperatura ambiente por cerca de 1 hora. Congelados duram 3 a 6 meses.",
    },
    {
        "cat": "doces",
        "subcat": "Biscoitos",
        "slug": "esquecidos",
        "title": "Esquecidos",
        "meta": [("Rendimento", "50 a 60 biscoitos")],
        "ingredients": [
            "1 1/2 xícara de açúcar",
            "4 gemas",
            "1 clara",
            "4 xícaras de farinha de trigo",
            "1 pitada de sal",
            "1 colher (sopa) de água",
            "Manteiga para untar",
            "Farinha de trigo para polvilhar",
        ],
        "steps": [
            "Preaqueça o forno em temperatura média (180 °C). Bata açúcar e gemas na batedeira em velocidade média até creme esbranquiçado.",
            "Acrescente a clara e bata mais 5 minutos.",
            "Desligue, junte farinha peneirada e sal; misture à mão até massa que possa ser enrolada (use água se necessário).",
            "Faça bolinhas pequenas e disponha afastadas em duas assadeiras untadas e enfarinhadas. Asse 25 minutos. Deixe esfriar e congele.",
        ],
        "notes": "Congelamento: saco plástico sem ar, etiquetado. Descongelamento: temperatura ambiente por 1 hora e 6 minutos no forno. Polvilhe as mãos com farinha ao enrolar — a massa é mole.",
    },
    {
        "cat": "doces",
        "subcat": "Biscoitos",
        "slug": "casadinhos-recheados",
        "title": "Casadinhos recheados",
        "meta": [("Rendimento", "50 casadinhos")],
        "ingredients": [
            "1 1/4 xícara de margarina",
            "1 xícara mais 5 colheres (sopa) de açúcar",
            "1/2 colher (chá) de canela em pó",
            "1 pitada de sal",
            "1 ovo",
            "2 2/3 xícaras de farinha de trigo",
            "Farinha de trigo para polvilhar",
            "Manteiga para untar",
            "1 xícara de doce de leite",
            "1 pacote pequeno (50 g) de coco ralado",
        ],
        "steps": [
            "Bata a margarina amolecida até formar creme. Acrescente 1 xícara de açúcar, canela, sal e o ovo.",
            "Incorpore a farinha peneirada e trabalhe com as mãos. Abra com rolo até 0,5 cm e corte círculos de 4,5 cm.",
            "Preaqueça o forno em temperatura média (180 °C). Asse em formas levemente untadas por 10 a 15 minutos até dourar.",
            "Misture doce de leite com coco. Envolva os biscoitos no açúcar restante, recheie generosamente e congele.",
        ],
        "notes": "Congelamento: recipiente rígido com toalhas de papel entre camadas e nos espaços vazios. Descongelamento: temperatura ambiente por cerca de 1 hora. Sem recheio ficam crocantes; com recheio ficam mais macios.",
    },
    {
        "cat": "doces",
        "subcat": "Biscoitos",
        "slug": "sequilhos-de-coco",
        "title": "Sequilhos de coco",
        "meta": [("Rendimento", "90 sequilhos")],
        "ingredients": [
            "Manteiga para untar",
            "Farinha de trigo para polvilhar",
            "1 1/3 xícara de farinha de trigo",
            "3/4 xícara de açúcar",
            "1 colher (chá) de fermento em pó",
            "1 pacote pequeno (50 g) de coco ralado",
            "1 pitada de sal",
            "3/4 xícara de manteiga",
            "1 gema",
        ],
        "steps": [
            "Preaqueça o forno em temperatura média (180 °C). Unte e enfarinhe duas assadeiras grandes.",
            "Misture os ingredientes secos. Faça uma cova, coloque manteiga em pedacinhos e a gema; incorpore com a ponta dos dedos até massa ligada.",
            "Faça cordõezinhos, corte como nhoque e marque com garfo.",
            "Asse 15 minutos, trocando as assadeiras de lugar na metade do tempo. Deixe esfriar e congele.",
        ],
        "notes": "Congelamento: saco plástico sem ar, etiquetado. Descongelamento: temperatura ambiente por cerca de 1 hora.",
    },
    # --- SALGADOS / Petiscos ---
    {
        "cat": "salgados",
        "subcat": "Petiscos",
        "slug": "waffles-com-iogurte",
        "title": "Waffles com iogurte",
        "meta": [("Rendimento", "5 waffles")],
        "ingredients": [
            "1 3/4 xícara de farinha de trigo",
            "1 colher (chá) de fermento em pó",
            "1 colher (chá) de bicarbonato de sódio",
            "1/2 colher (chá) de sal",
            "2 xícaras de iogurte natural ou leite azedo",
            "1/3 xícara de óleo",
            "2 ovos",
        ],
        "steps": [
            "Aqueça a máquina de waffle conforme as instruções do fabricante. Misture farinha, fermento, bicarbonato e sal.",
            "Acrescente iogurte, óleo e ovos; bata até homogeneizar.",
            "Despeje no centro da parte inferior do ferro até 2,5 cm da borda. Feche e asse sem abrir durante o cozimento.",
            "Solte o waffle com garfo, reaqueça o ferro e repita. Deixe esfriar e congele.",
        ],
        "notes": "Congelamento: saco plástico sem ar, etiquetado. Descongelamento: temperatura ambiente por cerca de 1 hora; aqueça antes de servir. A massa crua também pode ser congelada em recipientes rígidos bem vedados.",
    },
    {
        "cat": "doces",
        "subcat": "Tortas e bolos",
        "slug": "bolo-de-chocolate-com-3-ingredientes",
        "title": "Bolo de chocolate com 3 ingredientes",
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


def category_display(r: dict) -> str:
    label = CATEGORIES[r["cat"]]
    sub = r.get("subcat")
    return f"{label} · {sub}" if sub else label


def render_recipe(r: dict) -> str:
    cat = r["cat"]
    cat_label = CATEGORIES[cat]
    title = r["title"]
    slug = r["slug"]
    display = category_display(r)
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
    notes_html = ""
    if r.get("notes"):
        notes_html = f"""
        <p class="notes">
          <strong>Observação:</strong> {html.escape(r["notes"])}
        </p>"""
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{html.escape(title)} — Livro de Receitas</title>
    <meta
      name="description"
      content="{desc}"
    />
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
        <p class="category">{html.escape(display)}</p>
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
        </ol>{notes_html}
      </article>
    </main>
    <script src="../../js/recipe-layout.js" defer></script>
  </body>
</html>
"""


def insert_into_index(
    index_text: str, cat: str, subcategory: str | None, slug: str, title: str
) -> str:
    href = f"./receitas/{cat}/{slug}.html"
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
            r"((?:\s*<li>.*?</li>)*)"
            r"(\s*</ul>)"
        )
        um = re.search(ul_pat, section, re.S)
        if not um:
            raise SystemExit(f"Subcategory not found: {cat}/{subcategory}")
        items = um.group(2)
        if href in items:
            return index_text
        items += new_li
        lis = re.findall(r"<li>.*?</li>\s*", items, re.S)
        lis.sort(key=lambda x: re.sub(r"<[^>]+>", "", x).strip().lower())
        new_items = "".join(lis)
        new_section = (
            section[: um.start()]
            + um.group(1)
            + new_items
            + um.group(3)
            + section[um.end() :]
        )
    else:
        ul_pat = r"(<ul class=\"recipe-list\">\s*)((?:.*?</li>\s*)*)(</ul>)"
        um = re.search(ul_pat, section, re.S)
        if not um:
            raise SystemExit(f"Recipe list not found in {cat}")
        items = um.group(2)
        if href in items:
            return index_text
        items += new_li
        lis = re.findall(r"<li>.*?</li>\s*", items, re.S)
        lis.sort(key=lambda x: re.sub(r"<[^>]+>", "", x).strip().lower())
        new_items = "".join(lis)
        new_section = (
            section[: um.start()]
            + um.group(1)
            + new_items
            + um.group(3)
            + section[um.end() :]
        )

    return index_text[: m.start()] + new_section + m.group(2) + index_text[m.end() :]


def write_recipes() -> list[dict]:
    written: list[dict] = []
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


def update_index(new_recipes: list[dict]) -> int:
    index_path = ROOT / "index.html"
    index_text = index_path.read_text(encoding="utf-8")
    updated = 0
    for r in new_recipes:
        before = index_text
        index_text = insert_into_index(
            index_text, r["cat"], r.get("subcat"), r["slug"], r["title"]
        )
        if index_text != before:
            updated += 1
            print(f"index + {r['title']} → {r['cat']}/{r.get('subcat', '(sem sub)')}")
    if updated:
        index_path.write_text(index_text, encoding="utf-8")
    return updated


def delete_pending_sources() -> list[str]:
    deleted: list[str] = []
    if not PENDING.is_dir():
        return deleted
    for path in PENDING.iterdir():
        if path.name == ".gitkeep":
            continue
        path.unlink()
        deleted.append(path.name)
        print(f"deleted pending/{path.name}")
    return deleted


def main() -> None:
    assert len(RECIPES) == 27, f"expected 27 recipes, got {len(RECIPES)}"
    written = write_recipes()
    index_updates = update_index(written)
    deleted = delete_pending_sources()
    print(
        f"\nSummary: {len(written)} HTML created, "
        f"{index_updates} index entries added, "
        f"{len(deleted)} pending files deleted"
    )


if __name__ == "__main__":
    main()
