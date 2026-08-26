#!/usr/bin/env python3
"""Batch 3: Telegram photos — A arte de congelar (receitas) + Pinterest cheesecakes."""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RECIPES: list[dict] = [
    {
        "cat": "doces",
        "sub": "Tortas e bolos",
        "slug": "cheesecake-basque-de-chocolate",
        "title": "Cheesecake basque de chocolate",
        "meta": [("Rendimento", "8 a 10 fatias")],
        "ingredients": [
            "500 g de cream cheese, em temperatura ambiente",
            "150 g de açúcar",
            "4 ovos",
            "150 g de chocolate amargo (70%)",
            "200 ml de creme de leite",
            "1 colher (chá) de essência de baunilha",
        ],
        "steps": [
            "Preaqueça o forno em temperatura alta (200 °C). Forre uma fôrma redonda de 20 cm com papel-manteiga.",
            "Derreta o chocolate e reserve.",
            "Bata o cream cheese com o açúcar até ficar liso. Acrescente os ovos, um a um.",
            "Junte o creme de leite, a baunilha e o chocolate derretido; misture até homogeneizar.",
            "Despeje na fôrma e asse até a superfície ficar bem escurecida e o centro ainda tremular (cerca de 35 a 45 min).",
            "Deixe esfriar completamente antes de desenformar. Sirva frio.",
        ],
        "notes": "Fonte: Pinterest (receita em inglês). Temperatura original 400 °F ≈ 200 °C.",
    },
    {
        "cat": "doces",
        "sub": "Tortas e bolos",
        "slug": "cheesecake-basque-de-matcha",
        "title": "Cheesecake basque de matcha",
        "meta": [("Rendimento", "8 a 10 fatias")],
        "ingredients": [
            "500 g de cream cheese, em temperatura ambiente",
            "200 g de açúcar",
            "4 ovos",
            "250 ml de creme de leite",
            "1 colher (sopa) e ½ de farinha de trigo",
            "1 colher (sopa) e ½ de matcha em pó",
        ],
        "steps": [
            "Preaqueça o forno em temperatura alta (200 °C). Forre uma fôrma redonda de 20 cm com papel-manteiga.",
            "Bata o cream cheese com o açúcar até ficar liso. Acrescente os ovos, um a um.",
            "Peneire a farinha e o matcha; misture ao creme junto com o creme de leite até homogeneizar.",
            "Despeje na fôrma e asse até a superfície escurecer e o centro ficar tremulo (cerca de 35 a 45 min).",
            "Deixe esfriar completamente antes de desenformar. Sirva frio.",
        ],
        "notes": "Fonte: Pinterest (receita em inglês). Temperatura original 400 °F ≈ 200 °C.",
    },
    {
        "cat": "acompanhamentos",
        "slug": "pao-de-forma",
        "title": "Pão de fôrma",
        "meta": [("Rendimento", "1 pão (900 g)")],
        "ingredients": [
            "5½ a 6½ xícaras de farinha de trigo",
            "2 colheres (chá) de sal",
            "2 colheres (sopa) de manteiga",
            "1 tablete (15 g) de fermento para pão",
            "1¾ xícara de água morna",
            "Farinha de trigo para polvilhar",
            "Manteiga para untar",
        ],
        "steps": [
            "Peneire a farinha com o sal; esfarele a manteiga. Faça um buraco no centro.",
            "Dissolva o fermento na água morna e junte à farinha; misture com colher de pau, acrescentando farinha se preciso.",
            "Sove na superfície enfarinhada por cerca de 10 min até ficar lisa e elástica.",
            "Forme uma bola, coloque em tigela untada, cubra com saco plástico untado e deixe dobrar de volume.",
            "Abaixe a massa, elimine bolhas de ar, modele um rocambole e coloque em fôrma de pão untada.",
            "Cubra e deixe dobrar de volume. Asse em forno alto preaquecido (230 °C) por 30 a 40 min até dourar.",
            "Deixe esfriar em grade e congele conforme as dicas.",
        ],
        "notes": "Congelamento: embrulhe em alumínio ou filme, saco sem ar, etiquete. Descongelamento: temperatura ambiente ~2 h.",
    },
    {
        "cat": "acompanhamentos",
        "slug": "pao-integral",
        "title": "Pão integral",
        "meta": [("Rendimento", "2 pães")],
        "ingredients": [
            "3 colheres (sopa) de açúcar",
            "2 tabletes (30 g) de fermento para pão",
            "4 colheres (chá) de sal",
            "4 xícaras de farinha integral",
            "3 a 3½ xícaras de farinha de trigo",
            "2½ xícaras de leite",
            "⅓ xícara de manteiga ou margarina",
            "⅓ xícara de melado",
            "Farinha de trigo para polvilhar",
            "Manteiga ou margarina para untar",
        ],
        "steps": [
            "Misture açúcar, fermento, sal, 2 xícaras de farinha integral e 1 xícara de farinha de trigo.",
            "Aqueça leite, manteiga e melado até bem quentes; junte aos secos com batedeira.",
            "Acrescente farinhas restantes e sove até elástica. Deixe dobrar de volume em tigela untada.",
            "Divida, descanse 15 min. Abra cada parte em retângulo, enrole como rocambole e coloque em fôrmas de bolo inglês (13 × 23 cm) untadas.",
            "Deixe dobrar de volume. Asse em forno médio (200 °C) por 30 a 35 min. Esfrie e congele.",
        ],
        "notes": "Congelamento: filme ou alumínio, saco sem ar. Descongelamento: temperatura ambiente ~2 h.",
    },
    {
        "cat": "acompanhamentos",
        "slug": "paezinhos-rapidos",
        "title": "Pãezinhos rápidos",
        "meta": [("Rendimento", "28 pãezinhos")],
        "ingredients": [
            "2 xícaras de farinha de trigo",
            "2½ colheres (chá) de fermento em pó",
            "1 colher (chá) de sal",
            "⅓ xícara de manteiga ou margarina gelada",
            "Farinha de trigo para polvilhar",
        ],
        "steps": [
            "Preaqueça o forno em temperatura alta (250 °C). Peneire farinha, fermento e sal.",
            "Corte a manteiga gelada na farinha com duas facas até formar farofa; sove até integrar.",
            "Abra a massa até 1 cm de espessura e corte com cortador de 5 cm.",
            "Coloque em assadeira sem untar e asse até levemente dourados (12 a 15 min). Esfrie e congele.",
        ],
        "notes": "Varie com alcaravia, erva-doce ou linguiça antes de assar. Congelamento: no freezer cobertos com plástico, depois saco sem ar. Descongelamento: ~1 h em temperatura ambiente.",
    },
    {
        "cat": "acompanhamentos",
        "slug": "pao-sirio",
        "title": "Pão sírio",
        "meta": [("Rendimento", "10 pães")],
        "ingredients": [
            "6 xícaras de farinha de trigo",
            "1 tablete (15 g) de fermento para pão",
            "2 xícaras de água morna",
            "1½ colheres (chá) de sal",
            "1 colher (chá) de açúcar",
            "2 colheres (sopa) de óleo",
            "Farinha de trigo para polvilhar",
            "Óleo para untar",
        ],
        "steps": [
            "Preaqueça o forno em temperatura baixa (100 °C). Peneire a farinha e aqueça levemente no forno.",
            "Dissolva o fermento em ¼ xícara de água morna; junte o restante da água, sal e açúcar.",
            "Misture 4 xícaras de farinha com o fermento até formar pasta; descanse até espumar.",
            "Acrescente a farinha reservada e o óleo; bata 10 min. Sove 10 min, forme bola untada com óleo e deixe crescer 1 h.",
            "Divida em 10 bolas, abra em discos de 20 cm e descanse 20 min. Preaqueça forno médio (200 °C).",
            "Asse cada pão em assadeira bem quente no topo do forno por 4 a 5 min até inchar. Enrole em pano limpo para manter macios.",
        ],
        "notes": "Congelamento: filme e saco sem ar. Descongelamento: temperatura ambiente ~1 h.",
    },
    {
        "cat": "doces",
        "sub": "Outros doces",
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
            "Forre 40 forminhas de empada (7 cm) com 2 discos de papel. Preaqueça forno médio (180 °C).",
            "Bata açúcar e manteiga até creme esbranquiçado. Junte gemas alternando com leite de coco e leite.",
            "Misture fubá, farinha e fermento. Incorpore as claras delicadamente.",
            "Distribua nas forminhas e asse até dourar (~35 min). Desenforme, esfrie e congele.",
        ],
        "notes": "Congelamento: recipiente rígido com broinhas próximas; preencha vazios com papel-toalha entre camadas. Descongelamento: ~1 h e aqueça no forno.",
    },
    {
        "cat": "doces",
        "sub": "Tortas e bolos",
        "slug": "muffins",
        "title": "Muffins",
        "meta": [("Rendimento", "12 muffins")],
        "ingredients": [
            "Manteiga para untar",
            "1 xícara de farinha de trigo",
            "1 xícara de farinha integral",
            "1 colher (sopa) de açúcar",
            "½ colher (chá) de sal",
            "3 colheres (chá) de fermento em pó",
            "1 ovo",
            "¼ xícara de óleo",
            "1 xícara de leite",
            "½ xícara de passas brancas hidratadas em água morna e escorridas",
        ],
        "steps": [
            "Preaqueça forno médio (180 °C). Unte 12 forminhas de muffin.",
            "Peneire farinhas, açúcar, sal e fermento.",
            "Misture ovo, óleo e leite; junte à farinha com passas, mexendo só até umedecer (massa empelotada).",
            "Distribua nas forminhas (⅔ de cada) e asse ~25 min até dourar. Esfrie e congele.",
        ],
        "notes": "Use forminhas de empada de 7 cm se não tiver de muffin. Congelamento: recipiente rígido com papel-toalha entre camadas. Sirva quente com manteiga e geléia.",
    },
    {
        "cat": "doces",
        "sub": "Tortas e bolos",
        "slug": "rosca-de-natal",
        "title": "Rosca de Natal",
        "meta": [("Rendimento", "10 porções")],
        "ingredients": [
            "1 caixa (400 g) de mistura para salgados",
            "⅓ xícara de leite",
            "3 ovos",
            "¼ xícara de manteiga",
            "½ xícara de açúcar cristal",
            "¼ xícara de mel",
            "1 colher (chá) de canela em pó",
            "1½ xícara de nozes picadas",
            "2 colheres (chá) de suco de limão",
            "2 xícaras de passas brancas e frutas cristalizadas picadas em ⅔ xícara de Cointreau",
            "1 gema batida",
        ],
        "steps": [
            "Misture a massa para salgados com ⅓ xícara de leite e 2 ovos.",
            "Prepare o recheio: ferva manteiga, açúcar, ¼ xícara de leite, mel e canela; junte nozes, ovo batido e limão.",
            "Abra a massa em retângulo (37 × 54 cm), espalhe recheio, passas e frutas. Enrole, pincele com gema.",
            "Forme rosca em assadeira untada, corte fatias até dois dedos do centro e incline cada fatia.",
            "Cubra com alumínio untado e deixe crescer 20 min. Asse 200 °C 15 min, depois 180 °C 10 min. Esfrie e congele.",
        ],
        "notes": "Descongelamento: ~2 h; glacê com 1 xícara de açúcar de confeiteiro e 1½ colheres (sopa) de limão. Massa crua não deve ser recongelada.",
    },
    {
        "cat": "doces",
        "sub": "Tortas e bolos",
        "slug": "bolo-merenda",
        "title": "Bolo merenda",
        "meta": [("Rendimento", "8 porções")],
        "ingredients": [
            "¾ xícara de manteiga",
            "¾ xícara de açúcar",
            "3 gemas",
            "1½ xícara de farinha de trigo",
            "1 colher (chá) de fermento em pó",
            "2 colheres (sopa) de leite",
            "3 claras",
            "Manteiga para untar",
        ],
        "steps": [
            "Preaqueça forno médio (200 °C). Bata manteiga até cremosa; acrescente açúcar e gemas até creme claro.",
            "Misture farinha peneirada com fermento e leite. Incorpore claras em neve delicadamente.",
            "Despeje em fôrma de abrir de 21 cm untada. Asse ~30 min até dourar. Esfrie, desenforme e congele.",
        ],
        "notes": "Variações: ½ xícara de goiabada em cubos ou ½ xícara de gotas de chocolate. Congelamento: plástico, filme, saco sem ar.",
    },
    {
        "cat": "doces",
        "sub": "Tortas e bolos",
        "slug": "bolo-de-especiarias",
        "title": "Bolo de especiarias",
        "meta": [("Rendimento", "6 a 8 porções")],
        "ingredients": [
            "2 xícaras de farinha de trigo",
            "1 xícara de açúcar",
            "1 colher de fermento em pó",
            "1 colher (chá) de sal",
            "½ colher (chá) de bicarbonato de sódio",
            "½ colher (sopa) de cravo em pó",
            "1 colher (sopa) de canela em pó",
            "½ xícara de margarina",
            "¾ xícara de açúcar mascavo",
            "1 xícara de creme de leite azedado com 1 colher (sopa) de limão",
            "3 ovos",
            "½ xícara de nozes picadas",
        ],
        "steps": [
            "Preaqueça forno médio (180 °C). Misture farinha, açúcar, fermento, sal, bicarbonato, cravo e canela.",
            "Acrescente margarina, mascavo e creme azedado; bata 2 min. Junte ovos e bata 2 min. Misture nozes.",
            "Despeje em forma de bolo inglês untada e enfarinhada (7,5 × 12 × 25 cm). Asse 30 a 35 min. Esfrie e congele.",
        ],
        "notes": "Bolos sem cremes congelam melhor. Descongelamento: temperatura ambiente 2 h, forno 10 min ou micro-ondas 3 min.",
    },
    {
        "cat": "doces",
        "sub": "Tortas e bolos",
        "slug": "bolo-de-mandioca",
        "title": "Bolo de mandioca",
        "meta": [("Rendimento", "12 porções")],
        "ingredients": [
            "2¼ xícaras de mandioca ralada fina",
            "2¼ xícaras de queijo-de-minas meia cura ralado fino",
            "2¼ xícaras de açúcar",
            "1¼ xícara de leite",
            "1 colher (café) de canela em pó",
            "1 colher (café) de cravo em pó",
            "8 ovos ligeiramente batidos",
            "Manteiga para untar",
            "Canela e açúcar para polvilhar",
        ],
        "steps": [
            "Preaqueça forno médio (180 °C). Misture mandioca, queijo, açúcar, leite, canela e cravo.",
            "Junte os ovos e misture bem. Despeje em assadeira 24 × 34 cm untada.",
            "Asse ~45 min até dourar. Polvilhe com canela e açúcar. Esfrie, corte em quadrados e congele.",
        ],
        "notes": "Congelamento: quadrados em assadeira cobertos com plástico, depois saco sem ar. Descongelamento: ~1 h.",
    },
    {
        "cat": "doces",
        "sub": "Tortas e bolos",
        "slug": "bolo-de-chocolate-com-calda",
        "title": "Bolo de chocolate com calda",
        "meta": [("Rendimento", "10 porções")],
        "ingredients": [
            "Massa: 50 g de chocolate amargo picado, ¾ xícara de manteiga, 1½ xícara de açúcar, 3 ovos, 1 colher (chá) de baunilha, 2 xícaras de farinha, 2 colheres (chá) de fermento, ½ colher (chá) de sal, ¾ xícara de leite",
            "Calda: 1 colher (sopa) de manteiga, 1 xícara de açúcar, ½ xícara de chocolate em pó, ¼ xícara de leite",
            "120 g de chocolate branco picado para decorar",
        ],
        "steps": [
            "Derreta o chocolate amargo. Misture manteiga e açúcar; junte ovos, baunilha e chocolate.",
            "Acrescente farinha, fermento e sal peneirados alternando com leite.",
            "Asse em forma de rosca de 26 cm untada, forno 180 °C, até firmar. Desenforme e esfrie.",
            "Para a calda: ferva manteiga, açúcar, chocolate em pó e leite; espalhe no bolo frio.",
            "Derreta o chocolate branco e faça fios decorativos. Congele.",
        ],
        "notes": "Congelamento: cobrir com plástico; depois saco sem ar. Descongelamento: ~2 h em temperatura ambiente.",
    },
    {
        "cat": "doces",
        "sub": "Tortas e bolos",
        "slug": "bolo-de-laranja",
        "title": "Bolo de laranja",
        "meta": [("Rendimento", "8 porções")],
        "ingredients": [
            "½ xícara de óleo",
            "2 xícaras de açúcar",
            "4 gemas",
            "2 xícaras de fubá",
            "1 xícara de farinha de trigo",
            "1 colher (sopa) de fermento em pó",
            "1 xícara de suco de laranja",
            "4 claras em neve",
            "Manteiga e farinha para untar e polvilhar",
        ],
        "steps": [
            "Preaqueça forno médio (180 °C). Bata óleo, açúcar e gemas até creme.",
            "Peneire fubá, farinha e fermento; misture ao creme alternando com suco de laranja.",
            "Junte claras em neve. Despeje em fôrma redonda grande com buraco, untada. Asse 45 min. Esfrie e congele.",
        ],
        "notes": "Preencha o buraco da fôrma com plástico antes de congelar.",
    },
    {
        "cat": "doces",
        "sub": "Tortas e bolos",
        "slug": "bolo-de-abacaxi",
        "title": "Bolo de abacaxi",
        "meta": [("Rendimento", "8 porções")],
        "ingredients": [
            "1 colher (sopa) de manteiga",
            "¼ xícara de açúcar demerara",
            "5 rodelas de abacaxi em conserva escorridas",
            "5 cerejas ao marasquino cortadas ao meio",
            "1 xícara de farinha de trigo",
            "¾ xícara de açúcar",
            "1 pitada de sal",
            "1 ovo",
            "2 colheres (sopa) de margarina cremosa",
            "½ xícara da calda do abacaxi",
            "1 colher (chá) de baunilha",
            "1 colher (chá) de fermento em pó",
        ],
        "steps": [
            "Preaqueça forno médio (180 °C). Derreta manteiga em fôrma de vidro de 25 cm e unte com o fundo coberto de demerara.",
            "Decore com rodelas de abacaxi e cerejas. Reserve.",
            "No liquidificador, bata farinha, açúcar, sal, ovo, margarina, calda e baunilha 3 min. Acrescente fermento.",
            "Espalhe sobre o abacaxi e asse até palito sair limpo. Desenforme, esfrie e congele.",
        ],
        "notes": "Açúcar demerara (Douradinho) em produtos naturais ou Açúcar União.",
    },
    {
        "cat": "doces",
        "sub": "Tortas e bolos",
        "slug": "bolo-de-fuba-e-coco",
        "title": "Bolo de fubá e coco",
        "meta": [("Rendimento", "24 porções")],
        "ingredients": [
            "1 xícara de açúcar",
            "½ xícara de manteiga ou margarina",
            "3 gemas",
            "1 vidro (200 ml) de leite de coco",
            "1 xícara de leite",
            "1 xícara de fubá",
            "1 pacote (50 g) de coco ralado",
            "½ xícara de farinha de trigo",
            "1 colher (sopa) de fermento em pó",
            "3 claras em neve firme",
            "Manteiga para untar",
            "2 colheres (sopa) de açúcar",
        ],
        "steps": [
            "Bata açúcar e manteiga; junte gemas, leite de coco e leite.",
            "Misture fubá, coco, farinha e fermento. Incorpore claras.",
            "Despeje em assadeira 20 × 30 cm untada. Asse 200 °C 20 min, depois 150 °C 5 min.",
            "Misture o leite de coco restante com 2 colheres de açúcar e regue o bolo quente. Esfrie, corte em quadrados e congele.",
        ],
        "notes": "Desenforme em grade para evitar umidade. Congelamento: quadrados em assadeira com plástico, depois saco sem ar.",
    },
    {
        "cat": "doces",
        "sub": "Tortas e bolos",
        "slug": "bolo-gelado-de-goiaba",
        "title": "Bolo gelado de goiaba",
        "meta": [("Rendimento", "10 a 12 porções")],
        "ingredients": [
            "Sorvete: 3 gemas, 1 xícara de açúcar, 1 xícara de leite morno, 500 ml de suco de goiaba, ½ xícara de chantilly",
            "Rocambole: 4 gemas, ½ xícara de açúcar, 4 claras em neve, ⅔ xícara de farinha, sal, manteiga, farinha, 400 g de doce de goiaba em pasta",
        ],
        "steps": [
            "Prepare o sorvete: bata gemas com açúcar, junte leite morno, suco e chantilly. Congele 1 h, bata e congele novamente.",
            "Rocambole: bata gemas com açúcar; misture farinha e claras. Divida em duas assadeiras forradas; asse ~10 min.",
            "Espalhe goiaba, enrole. Corte em fatias finas e refrigere 1 h.",
            "Forre tigela semi-esférica com fatias de rocambole; encha com sorvete, cubra com mais fatias e congele.",
        ],
        "notes": "Pode usar sorvete industrializado. Congelamento: filme plástico. Descongelamento: geladeira; decore com chantilly.",
    },
    {
        "cat": "doces",
        "sub": "Tortas e bolos",
        "slug": "bolo-de-sorvete-com-cerejas",
        "title": "Bolo de sorvete com cerejas",
        "meta": [("Rendimento", "8 porções")],
        "ingredients": [
            "2 xícaras de sorvete crocante industrializado",
            "Cerca de 200 g de biscoitos champanhe",
            "Licor Cointreau",
            "2 xícaras de sorvete de baunilha ou creme",
            "⅓ xícara de cobertura de chocolate ralada",
            "2 xícaras de creme de leite fresco",
            "1½ xícaras de cerejas em conserva ou cristalizadas",
        ],
        "steps": [
            "Forre o fundo de uma forma quadrada (~1,5 l) com papel-manteiga.",
            "Camada de sorvete crocante e biscoitos champanhe embebidos em Cointreau.",
            "Cubra com sorvete de baunilha; refrigere e congele.",
            "Derreta o chocolate; bata o creme de leite e misture o chocolate frio. Congele o creme separadamente.",
            "Descongele na geladeira; decore com creme em saco de confeitar e cerejas.",
        ],
        "notes": "Mantenha o chocolate derretido perto de fonte de calor ao esfriar para não endurecer.",
    },
    {
        "cat": "doces",
        "sub": "Biscoitos",
        "slug": "biscoitinhos-coloridos",
        "title": "Biscoitinhos coloridos",
        "meta": [("Rendimento", "18 biscoitos")],
        "ingredients": [
            "¾ xícara de margarina",
            "½ xícara de açúcar",
            "1½ xícara de farinha de trigo",
            "1 pacote (50 g) de coco ralado",
            "1 colher (sopa) de água",
            "1 colher (sopa) de chocolate em pó",
            "Margarina para untar",
        ],
        "steps": [
            "Em banho-maria, bata margarina e açúcar até cremoso. Junte farinha e coco; forme massa (use água se preciso).",
            "Divida a massa; acrescente chocolate em pó a uma metade.",
            "Abra cada parte em retângulo 17 × 22 cm sobre papel-manteiga. Empilhe e enrole como rocambole.",
            "Refrigere 30 min. Corte fatias de 1 cm; asse 180 °C ~25 min. Esfrie e congele.",
        ],
        "notes": "Descongelamento: ~1 h. Micro-ondas: potência descongelamento, 2 a 4 min conforme a massa.",
    },
    {
        "cat": "doces",
        "sub": "Biscoitos",
        "slug": "biscoitinhos-de-cerveja",
        "title": "Biscoitinhos de cerveja",
        "meta": [("Rendimento", "45 biscoitinhos")],
        "ingredients": [
            "2¾ xícaras de farinha de trigo",
            "1 xícara de manteiga sem sal em temperatura ambiente",
            "2 colheres (sopa) de cerveja",
            "1 xícara de açúcar cristal",
        ],
        "steps": [
            "Preaqueça forno médio (180 °C). Misture farinha e manteiga; amasse.",
            "Junte cerveja até massa enrolável. Faça bolinhas de 1,5 cm e passe no açúcar cristal.",
            "Asse em assadeira sem untar por 30 min. Esfrie e congele.",
        ],
        "notes": "Achate as bolinhas para formato de bolachinha. Congelamento: saco sem ar.",
    },
    {
        "cat": "doces",
        "sub": "Biscoitos",
        "slug": "biscoitinhos-de-ameixa-preta",
        "title": "Biscoitinhos de ameixa-preta",
        "meta": [("Rendimento", "120 biscoitinhos")],
        "ingredients": [
            "1 xícara de manteiga",
            "1 xícara de açúcar mascavo",
            "½ xícara de açúcar",
            "2 ovos",
            "1 colher (sopa) de vinagre",
            "1 colher (chá) de baunilha",
            "1 xícara de ameixas-pretas secas picadas",
            "4 xícaras de farinha de trigo",
            "1 colher (chá) de bicarbonato de sódio",
            "1 colher (chá) de sal",
            "1 xícara de nozes picadas",
        ],
        "steps": [
            "Bata manteiga e açúcares; junte ovos, vinagre, baunilha, ameixas e ingredientes secos. Misture nozes.",
            "Forme 3 rolos de 5 cm; embrulhe em alumínio e refrigere de um dia para o outro.",
            "Corte fatias finas; asse em assadeira sem untar, 200 °C, ~12 min. Esfrie e congele.",
        ],
        "notes": "Pode abrir com rolo e usar cortadores. Congelamento: cobertos com plástico, depois saco sem ar.",
    },
    {
        "cat": "doces",
        "sub": "Biscoitos",
        "slug": "biscoitinhos-de-chocolate-e-coco",
        "title": "Biscoitinhos de chocolate e coco",
        "meta": [("Rendimento", "80 biscoitos")],
        "ingredients": [
            "1¼ xícara de margarina",
            "1 xícara de açúcar",
            "1⅔ xícara de farinha de trigo",
            "1 colher (sopa) de fermento em pó",
            "⅓ xícara de cacau em pó",
            "1 pitada de sal",
            "1 xícara de chocolate em pó",
            "3 pacotes (150 g) de coco ralado",
            "¼ xícara de água fervente",
            "1 colher (chá) de café solúvel preparado",
        ],
        "steps": [
            "Bata margarina e açúcar. Peneire farinha, fermento, cacau, sal e chocolate; misture com coco.",
            "Prepare café solúvel (1 parte café, 2 partes água fervente).",
            "Alterne secos e café na batedeira. Refrigere 30 min. Preaqueça 200 °C.",
            "Faça bolinhas, disponha em assadeira com 5 cm de espaço. Asse. Esfrie e congele.",
        ],
        "notes": "Congelamento: plástico, depois saco sem ar. Descongelamento: ~1 h.",
    },
    {
        "cat": "doces",
        "sub": "Biscoitos",
        "slug": "biscoitinhos-de-caramelo",
        "title": "Biscoitinhos de caramelo",
        "meta": [("Rendimento", "50 biscoitos")],
        "ingredients": [
            "½ xícara de manteiga",
            "⅔ xícara de açúcar mascavo",
            "1 ovo",
            "1⅓ xícara de farinha de trigo",
            "½ colher (chá) de fermento em pó",
            "½ colher (chá) de baunilha",
            "⅓ xícara de nozes picadas",
        ],
        "steps": [
            "Derreta a manteiga; misture mascavo e ovo; bata ~10 min até esbranquiçar.",
            "Peneire farinha com fermento; junte baunilha e nozes. Refrigere ~40 min.",
            "Forme bolinhas; asse em forno médio (180 °C). Esfrie e congele.",
        ],
        "notes": "Em lata fechada duram 2 meses; congelados 3 a 6 meses.",
    },
    {
        "cat": "doces",
        "sub": "Biscoitos",
        "slug": "esquecidos",
        "title": "Esquecidos",
        "meta": [("Rendimento", "50 a 60 biscoitos")],
        "ingredients": [
            "1½ xícara de açúcar",
            "4 gemas",
            "1 clara",
            "4 xícaras de farinha de trigo",
            "1 pitada de sal",
            "1 colher (sopa) de água",
            "Manteiga e farinha para untar e polvilhar",
        ],
        "steps": [
            "Preaqueça forno médio (180 °C). Bata açúcar e gemas até creme esbranquiçado; junte clara e bata 5 min.",
            "Misture farinha e sal; adicione água se preciso para enrolar. Forme bolinhas.",
            "Asse em duas assadeiras untadas 25 min. Esfrie e congele.",
        ],
        "notes": "Polvilhe as mãos com farinha ao enrolar. Descongelamento: ~1 h e asse 6 min para ficar crocante.",
    },
    {
        "cat": "doces",
        "sub": "Biscoitos",
        "slug": "casadinhos-recheados",
        "title": "Casadinhos recheados",
        "meta": [("Rendimento", "50 casadinhos")],
        "ingredients": [
            "1¼ xícara de margarina",
            "1 xícara mais 5 colheres (sopa) de açúcar",
            "½ colher (chá) de canela em pó",
            "1 pitada de sal",
            "1 ovo",
            "2⅔ xícaras de farinha de trigo",
            "Farinha para polvilhar",
            "Manteiga para untar",
            "1 xícara de doce de leite",
            "1 pacote (50 g) de coco ralado",
        ],
        "steps": [
            "Bata margarina até creme; junte 1 xícara de açúcar, canela, sal e ovo.",
            "Acrescente farinha peneirada; sove. Abra 0,5 cm; corte círculos de 4,5 cm.",
            "Asse 180 °C 10 a 15 min em fôrmas levemente untadas.",
            "Envolva no açúcar restante; recheie com doce de leite e coco. Esfrie e congele.",
        ],
        "notes": "Congelamento: recipiente rígido com papel-toalha entre camadas.",
    },
    {
        "cat": "doces",
        "sub": "Biscoitos",
        "slug": "sequilhos-de-coco",
        "title": "Sequilhos de coco",
        "meta": [("Rendimento", "90 sequilhos")],
        "ingredients": [
            "Manteiga e farinha para untar e polvilhar",
            "1⅓ xícara de farinha de trigo",
            "¾ xícara de açúcar",
            "1 colher (chá) de fermento em pó",
            "1 pacote (50 g) de coco ralado",
            "1 pitada de sal",
            "¾ xícara de manteiga",
            "1 gema",
        ],
        "steps": [
            "Preaqueça forno médio (180 °C). Unte e enfarinhe duas assadeiras grandes.",
            "Misture ingredientes secos; faça um buraco e junte manteiga em cubos e gema. Forme massa lisa.",
            "Faça cordões e corte como nhoque; marque com garfo. Asse 15 min. Esfrie e congele.",
        ],
        "notes": "Troque as assadeiras de lugar na metade do cozimento. Congelamento: saco sem ar.",
    },
    {
        "cat": "salgados",
        "sub": "Petiscos",
        "slug": "waffles-com-iogurte",
        "title": "Waffles com iogurte",
        "meta": [("Rendimento", "5 waffles")],
        "ingredients": [
            "1¾ xícara de farinha de trigo",
            "1 colher (chá) de fermento em pó",
            "1 colher (chá) de bicarbonato de sódio",
            "½ colher (chá) de sal",
            "2 xícaras de iogurte natural ou leite azedo",
            "⅓ xícara de óleo",
            "2 ovos",
        ],
        "steps": [
            "Esquente o aparelho de waffles. Misture farinha, fermento, bicarbonato e sal.",
            "Junte iogurte, óleo e ovos; misture até homogeneizar.",
            "Despeje na máquina até 2,5 cm da borda; feche e asse sem abrir.",
            "Solte com garfo; repita. Esfrie e congele.",
        ],
        "notes": "Massa crua pode ser congelada em recipiente rígido; descongele na geladeira. Descongelamento dos waffles: ~1 h; aqueça antes de servir.",
    },
]


def render_recipe(r: dict) -> str:
    cat = r["cat"]
    cat_labels = {
        "doces": "Doces",
        "salgados": "Salgados",
        "acompanhamentos": "Acompanhamentos",
    }
    cat_label = cat_labels.get(cat, cat)
    sub = r.get("sub")
    category_line = f"{cat_label} · {sub}" if sub else cat_label
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
    ingredients = "\n".join(f"          <li>{html.escape(i)}</li>" for i in r["ingredients"])
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
    <script src="../../js/recipe-layout.js" defer></script>
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


def main() -> None:
    written = write_recipes()
    print(f"Created {len(written)} new recipes")


if __name__ == "__main__":
    main()
