#!/usr/bin/env python3
"""Gera fichas do lote 'A arte de congelar' (pães, bolos, biscoitos)."""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

RECIPES = [
    {
        "slug": "pao-de-forma",
        "title": "Pão de fôrma",
        "cat": "salgados",
        "sub": "Massas fritas/assadas",
        "ingredients": [
            "5½ a 6½ xícaras de farinha de trigo",
            "2 colheres (chá) de sal",
            "2 colheres (sopa) de manteiga",
            "1 tablete (15 g) de fermento para pão",
            "1¾ xícara de água morna",
            "farinha de trigo para polvilhar",
            "manteiga para untar",
        ],
        "steps": [
            "Numa tigela, peneire a farinha com o sal. Adicione a manteiga e esfarele. Faça uma cova no centro. À parte, dissolva o fermento na água morna.",
            "Acrescente o fermento dissolvido à farinha de uma vez e mexa bem com colher de pau, juntando mais farinha se necessário para obter massa consistente.",
            "Vire a massa sobre superfície polvilhada e amasse por uns 10 minutos até ficar lisa e elástica, sem estar pegajosa.",
            "Forme uma bola, coloque numa tigela grande untada com manteiga, cubra com saco plástico untado e deixe crescer até dobrar de volume.",
            "Abaixe a massa com o punho para eliminar bolhas de ar. Amasse mais um pouco. Unte fôrma para 1 pão de 900 g.",
            "Abra a massa em oval com a largura da fôrma, enrole, dobre as pontas para baixo e coloque na fôrma.",
            "Cubra com plástico untado e deixe crescer até dobrar. Preaqueça o forno em temperatura alta (230 °C).",
            "Asse 30 a 40 minutos até dourar. Deve soar oco ao bater no fundo. Deixe esfriar sobre grade e congele.",
        ],
        "notes": "Rendimento: 1 pão. Congelamento: embale em alumínio ou filme e saco plástico sem ar. Descongelamento: temperatura ambiente por cerca de 2 horas. Sobras com manteiga podem ser congeladas com as metades unidas pelo lado da manteiga.",
    },
    {
        "slug": "pao-integral",
        "title": "Pão integral",
        "cat": "salgados",
        "sub": "Massas fritas/assadas",
        "ingredients": [
            "3 colheres (sopa) de açúcar",
            "2 tabletes (30 g) de fermento para pão",
            "4 colheres (chá) de sal",
            "4 xícaras de farinha integral",
            "3 a 3½ xícaras de farinha de trigo",
            "2½ xícaras de leite",
            "⅓ xícara de manteiga ou margarina",
            "⅓ xícara de melado",
            "farinha de trigo para polvilhar",
            "manteiga ou margarina para untar",
        ],
        "steps": [
            "Numa tigela grande, misture açúcar, fermento, sal, 2 xícaras de farinha integral e 1 xícara de farinha de trigo.",
            "Aqueça leite, manteiga e melado em fogo brando até ficar bem quente.",
            "Na batedeira em velocidade baixa, incorpore o líquido aos secos. Em velocidade média, bata 2 minutos. Junte ½ xícara de farinha de trigo e bata mais 2 minutos.",
            "Adicione 1½ xícara de farinha integral e cerca de 1½ xícara de farinha de trigo, batendo com colher de pau.",
            "Sobre superfície polvilhada, amasse até elástica. Forme bola, coloque em tigela untada, vire a massa e deixe crescer em lugar morno até dobrar.",
            "Despeje, corte ao meio, cubra com pano e descanse 15 minutos. Unte duas fôrmas de 13 × 23 cm.",
            "Abra cada pedaço em retângulo de 20 × 30,5 cm, enrole como rocambole, sele as pontas e coloque nas fôrmas.",
            "Cubra, deixe dobrar de volume. Asse em forno médio (200 °C) por 30 a 35 minutos. Desenforme, esfrie e congele.",
        ],
        "notes": "Rendimento: 2 pães. Para testar o crescimento, coloque uma bolinha de massa num copo d'água: quando subir, a massa cresceu. Congelamento e descongelamento como pão de fôrma.",
    },
    {
        "slug": "paezinhos-rapidos",
        "title": "Pãezinhos rápidos",
        "cat": "salgados",
        "sub": "Massas fritas/assadas",
        "ingredients": [
            "2 xícaras de farinha de trigo",
            "2½ colheres (chá) de fermento em pó",
            "1 colher (chá) de sal",
            "⅓ xícara de manteiga ou margarina gelada",
            "farinha de trigo para polvilhar",
        ],
        "steps": [
            "Preaqueça o forno em temperatura alta (250 °C). Peneire farinha, fermento e sal. Adicione a manteiga e, com duas facas, corte em pedacinhos até formar farofa.",
            "Amasse na bancada até incorporar. Polvilhe com farinha e abra até 1 cm de espessura.",
            "Recorte com cortador de 5 cm de diâmetro.",
            "Coloque numa assadeira sem untar e asse até dourar levemente (12 a 15 minutos). Esfrie e congele.",
        ],
        "notes": "Rendimento: 28 pãezinhos. Varie com alcaravia, erva-doce ou linguiça antes de assar. Congelamento: freezer coberto com plástico, depois saco sem ar. Descongelamento: 1 hora em temperatura ambiente.",
    },
    {
        "slug": "pao-sirio",
        "title": "Pão sírio",
        "cat": "salgados",
        "sub": "Massas fritas/assadas",
        "ingredients": [
            "6 xícaras de farinha de trigo",
            "1 tablete (15 g) de fermento para pão",
            "2 xícaras de água morna",
            "1½ colher (chá) de sal",
            "1 colher (chá) de açúcar",
            "2 colheres (sopa) de óleo",
            "farinha de trigo para polvilhar",
            "óleo para untar",
        ],
        "steps": [
            "Preaqueça o forno em temperatura baixa (100 °C). Peneire a farinha numa tigela grande e deixe aquecendo no forno.",
            "Dissolva o fermento em ¼ xícara de água morna. Junte o restante da água, sal e açúcar.",
            "Retire a farinha do forno. Reserve 2 xícaras. Faça cova na farinha restante, adicione o fermento e mexa até formar pasta. Cubra e deixe espumar.",
            "Acrescente a farinha reservada e o óleo gradualmente; bata bem por 10 minutos.",
            "Sobre superfície polvilhada, amasse 10 minutos até lisa por dentro e levemente enrugada por fora.",
            "Forme bola, unte com óleo, cubra com plástico e deixe crescer 1 hora em lugar protegido.",
            "Abaixe a massa, amasse 1 minuto e forme 10 bolas iguais.",
            "Abra cada bola em disco de 20 cm sobre pano polvilhado. Cubra e descanse 20 minutos. Preaqueça forno médio (200 °C).",
            "Unte assadeira com óleo e aqueça na parte superior do forno. Asse um pão por vez 4 a 5 minutos até incharem. Enrole em pano limpo para manter macios.",
        ],
        "notes": "Rendimento: 10 pães. Fermento biológico fresco pode ser congelado em papel alumínio (3 meses). Congelamento: embrulhe em filme, congele, depois saco sem ar. Descongelamento: 1 hora em temperatura ambiente.",
    },
    {
        "slug": "broinhas-de-fuba",
        "title": "Broinhas de fubá",
        "cat": "doces",
        "sub": "Tortas e bolos",
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
            "Forre 40 forminhas de empada (7 cm) com 2 discos de papel cada.",
            "Preaqueça forno médio (180 °C). Bata açúcar e manteiga até creme esbranquiçado.",
            "Junte as gemas uma a uma, alternando com leite de coco e leite.",
            "Acrescente fubá, farinha e fermento; misture com colher de pau.",
            "Incorpore as claras com cuidado para não perder volume.",
            "Distribua nas forminhas e asse até dourar (cerca de 35 minutos). Desenforme, esfrie e congele.",
        ],
        "notes": "Rendimento: 40 broinhas. Congelamento: recipiente rígido com toalhas de papel entre camadas. Descongelamento: 1 hora em temperatura ambiente e aqueça no forno.",
    },
    {
        "slug": "muffins",
        "title": "Muffins",
        "cat": "doces",
        "sub": "Tortas e bolos",
        "ingredients": [
            "manteiga para untar",
            "1 xícara de farinha de trigo",
            "1 xícara de farinha integral",
            "1 colher (sopa) de açúcar",
            "½ colher (chá) de sal",
            "3 colheres (chá) de fermento em pó",
            "1 ovo",
            "¼ xícara de óleo",
            "1 xícara de leite",
            "½ xícara de passas brancas de molho em água morna e escorridas",
        ],
        "steps": [
            "Preaqueça forno médio (180 °C). Unte 12 forminhas de muffin.",
            "Peneire farinhas, açúcar, sal e fermento numa tigela.",
            "Numa jarra, misture ovo, óleo e leite.",
            "Despeje líquidos e passas na farinha; misture rapidamente com colher de pau só até umedecer (massa empelotada).",
            "Distribua nas forminhas até ⅔ da altura. Asse 25 minutos até dourar. Desenforme, esfrie e congele.",
        ],
        "notes": "Rendimento: 12 muffins. Sem fôrmas de muffin, use forminhas de empada de 7 cm untadas. Congelamento: recipiente rígido com toalhas de papel. Descongelamento: 1 hora e aqueça no forno.",
    },
    {
        "slug": "rosca-de-natal",
        "title": "Rosca de Natal",
        "cat": "doces",
        "sub": "Tortas e bolos",
        "ingredients": [
            "1 caixa (400 g) de mistura para salgados",
            "⅓ xícara de leite",
            "3 ovos",
            "¼ xícara de manteiga",
            "½ xícara de açúcar cristal",
            "¼ xícara de leite",
            "¼ xícara de mel",
            "1 colher (chá) de canela em pó",
            "1½ xícara de nozes picadas",
            "2 colheres (chá) de suco de limão",
            "2 xícaras de passas brancas e frutas cristalizadas de molho em ⅔ xícara de Cointreau",
            "1 gema batida",
        ],
        "steps": [
            "Misture a mistura para salgados, ⅓ xícara de leite e 2 ovos; reserve.",
            "Para o recheio: derreta manteiga com açúcar, ¼ xícara de leite, mel e canela; ferva. Junte nozes, retire do fogo, acrescente o terceiro ovo batido e o limão.",
            "Abra a massa em retângulo de 37 × 54 cm. Espalhe o recheio, escorra frutas e distribua. Enrole pelo lado comprido e pincele com gema.",
            "Coloque em assadeira untada, una as pontas com água, corte fatias até dois dedos do centro e incline levemente. Cubra com alumínio untado e deixe crescer 20 minutos.",
            "Preaqueça forno médio (200 °C). Retire o alumínio e asse 15 minutos. Baixe para 180 °C e asse mais 10 minutos até dourar. Esfrie e congele.",
        ],
        "notes": "Rendimento: 10 porções. Massa crua de pão não deve ser recongelada — se precisar, asse antes. Descongelamento: 2 horas; glaceie com 1 xícara de açúcar de confeiteiro e 1½ colher de suco de limão.",
    },
    {
        "slug": "bolo-merenda",
        "title": "Bolo merenda",
        "cat": "doces",
        "sub": "Tortas e bolos",
        "ingredients": [
            "¾ xícara de manteiga",
            "¾ xícara de açúcar",
            "3 gemas",
            "1½ xícara de farinha de trigo",
            "1 colher (chá) de fermento em pó",
            "2 colheres (sopa) de leite",
            "3 claras",
            "manteiga para untar",
        ],
        "steps": [
            "Preaqueça forno médio (200 °C). Bata manteiga com açúcar até cremoso. Junte gemas uma a uma.",
            "Acrescente farinha peneirada com fermento, misturando com colher e o leite aos poucos.",
            "Bata claras em neve e incorpore delicadamente.",
            "Despeje em fôrma de 21 cm untada. Asse cerca de 30 minutos até dourar. Desenforme, esfrie e congele.",
        ],
        "notes": "Rendimento: 8 porções. Variações: goiabada em cubos (½ xícara) ou gotas de chocolate (½ xícara). Congelamento: filme e saco sem ar. Descongelamento: 2 horas.",
    },
    {
        "slug": "bolo-de-especiarias",
        "title": "Bolo de especiarias",
        "cat": "doces",
        "sub": "Tortas e bolos",
        "ingredients": [
            "2 xícaras de farinha de trigo",
            "1 xícara de açúcar",
            "1 colher de fermento em pó",
            "1 colher (chá) de sal",
            "½ colher (chá) de bicarbonato de sódio",
            "½ colher (sopa) de cravo-da-índia em pó",
            "1 colher (sopa) de canela em pó",
            "½ xícara de margarina",
            "¾ xícara de açúcar mascavo",
            "1 xícara de creme de leite azedado com 1 colher (sopa) de suco de limão",
            "3 ovos",
            "½ xícara de nozes picadas",
        ],
        "steps": [
            "Preaqueça forno médio (180 °C). Misture farinha, açúcar, fermento, sal, bicarbonato, cravo e canela.",
            "Junte margarina, açúcar mascavo e creme azedado até umedecer a farinha.",
            "Bata 2 minutos em velocidade média. Acrescente ovos e bata mais 2 minutos. Misture as nozes.",
            "Despeje em forma de 7,5 × 12 × 25 cm untada e polvilhada. Asse 30 a 35 minutos. Desenforme após 10 minutos, esfrie e congele.",
        ],
        "notes": "Rendimento: 6 a 8 porções. Congelamento: filme, depois alumínio e saco. Descongelamento: 2 horas, ou 10 minutos no forno, ou 3 minutos no micro-ondas em descongelar.",
    },
    {
        "slug": "bolo-de-mandioca",
        "title": "Bolo de mandioca",
        "cat": "doces",
        "sub": "Tortas e bolos",
        "ingredients": [
            "2¼ xícaras de mandioca ralada fina",
            "2¼ xícaras de queijo-de-minas meia cura ralado fino",
            "2¼ xícaras de açúcar",
            "1¼ xícara de leite",
            "1 colher (café) de canela em pó",
            "1 colher (café) de cravo-da-índia em pó",
            "8 ovos ligeiramente batidos",
            "manteiga para untar",
            "canela e açúcar para polvilhar",
        ],
        "steps": [
            "Preaqueça forno médio (180 °C). Misture mandioca, queijo, açúcar, leite, canela e cravo.",
            "Junte os ovos e misture bem.",
            "Despeje em assadeira 24 × 34 cm untada. Asse 45 minutos até dourar.",
            "Polvilhe com mistura de canela e açúcar. Esfrie, corte em quadrados e congele.",
        ],
        "notes": "Rendimento: 12 porções. Congelamento: quadrados em assadeira com plástico, depois saco. Descongelamento: 1 hora.",
    },
    {
        "slug": "bolo-de-chocolate",
        "title": "Bolo de chocolate",
        "cat": "doces",
        "sub": "Tortas e bolos",
        "ingredients": [
            "50 g de chocolate amargo picado",
            "¾ xícara de manteiga",
            "1½ xícara de açúcar",
            "3 ovos",
            "1 colher (chá) de essência de baunilha",
            "2 xícaras de farinha de trigo",
            "2 colheres (chá) de fermento em pó",
            "½ colher (chá) de sal",
            "¾ xícara de leite",
            "1 colher (sopa) de manteiga (calda)",
            "1 xícara de açúcar (calda)",
            "½ xícara de chocolate em pó (calda)",
            "¼ xícara de leite (calda)",
            "120 g de chocolate branco picado para decorar",
        ],
        "steps": [
            "Derreta o chocolate amargo em banho-maria e reserve.",
            "Bata manteiga e açúcar até cremoso. Junte ovos um a um, baunilha e chocolate derretido.",
            "Peneire farinha, fermento e sal. Incorpore alternando com o leite.",
            "Preaqueça forno médio (180 °C). Unte fôrma de 26 cm com buraco. Asse até firmar. Desenforme após 10 minutos e esfrie.",
            "Para a calda: derreta manteiga, junte açúcar, chocolate em pó e leite; cozinhe em fogo brando mexendo. Espalhe sobre o bolo frio.",
            "Derreta o chocolate branco, bata até liso e regue o bolo em fios finos. Deixe firmar e congele.",
        ],
        "notes": "Rendimento: 10 porções. Congelamento: cubra com plástico, congele, depois saco. Descongelamento: 2 horas.",
    },
    {
        "slug": "bolo-de-laranja",
        "title": "Bolo de laranja",
        "cat": "doces",
        "sub": "Tortas e bolos",
        "ingredients": [
            "½ xícara de óleo",
            "2 xícaras de açúcar",
            "4 gemas",
            "2 xícaras de fubá",
            "1 xícara de farinha de trigo",
            "1 colher (sopa) de fermento em pó",
            "1 xícara de suco de laranja",
            "4 claras em neve",
            "manteiga e farinha para untar e polvilhar",
        ],
        "steps": [
            "Preaqueça forno médio (180 °C). Bata óleo, açúcar e gemas até creme.",
            "Peneire fubá, farinha e fermento; incorpore ao creme alternando com suco de laranja.",
            "Junte as claras em neve. Despeje em fôrma redonda grande com buraco, untada e polvilhada.",
            "Asse 45 minutos. Desenforme, esfrie e congele.",
        ],
        "notes": "Rendimento: 8 porções. Em fôrmas com buraco, preencha o centro com plástico antes de congelar. Descongelamento: 2 horas.",
    },
    {
        "slug": "bolo-de-abacaxi",
        "title": "Bolo de abacaxi",
        "cat": "doces",
        "sub": "Tortas e bolos",
        "ingredients": [
            "1 colher (sopa) de manteiga",
            "¼ xícara de açúcar demerara",
            "5 rodelas de abacaxi em conserva escorridas",
            "5 cerejas ao marasquino escorridas e cortadas ao meio",
            "1 xícara de farinha de trigo",
            "¾ xícara de açúcar",
            "1 pitada de sal",
            "1 ovo",
            "2 colheres (sopa) de margarina cremosa",
            "½ xícara da calda do abacaxi",
            "1 colher (chá) de essência de baunilha",
            "1 colher (chá) de fermento em pó",
        ],
        "steps": [
            "Preaqueça forno médio (180 °C). Derreta manteiga numa travessa de vidro de 25 cm; espalhe açúcar demerara.",
            "Arrume abacaxi decorativamente e preencha com cerejas.",
            "No liquidificador, bata farinha, açúcar, sal, ovo, margarina, calda e baunilha por 3 minutos. Pulse o fermento.",
            "Espalhe sobre o abacaxi. Asse até palito sair limpo. Desenforme, esfrie e congele.",
        ],
        "notes": "Rendimento: 8 porções. Açúcar demerara também é vendido como Douradinho (União). Descongelamento: 2 horas.",
    },
    {
        "slug": "bolo-de-fuba-e-coco",
        "title": "Bolo de fubá e coco",
        "cat": "doces",
        "sub": "Tortas e bolos",
        "ingredients": [
            "1 xícara de açúcar",
            "½ xícara de manteiga ou margarina",
            "3 gemas",
            "1 vidro pequeno (200 ml) de leite de coco",
            "1 xícara de leite",
            "1 xícara de fubá",
            "1 pacote pequeno (50 g) de coco ralado",
            "½ xícara de farinha de trigo",
            "1 colher (sopa) de fermento em pó",
            "3 claras em neve firme",
            "2 colheres (sopa) de açúcar (cobertura)",
        ],
        "steps": [
            "Preaqueça forno médio-alto (200 °C). Bata açúcar e manteiga até creme esbranquiçado.",
            "Junte gemas, metade do leite de coco e todo o leite.",
            "Acrescente fubá, coco, farinha e fermento.",
            "Incorpore claras. Despeje em assadeira 20 × 30 cm untada.",
            "Asse 20 minutos, reduza para 150 °C e asse mais 5 minutos.",
            "Misture leite de coco restante com açúcar e regue o bolo quente. Esfrie, corte em quadrados e congele.",
        ],
        "notes": "Rendimento: 24 porções. Desenforme sobre grade para evitar umidade. Descongelamento: 1 hora.",
    },
    {
        "slug": "bolo-gelado-de-goiaba",
        "title": "Bolo gelado de goiaba",
        "cat": "doces",
        "sub": "Tortas e bolos",
        "ingredients": [
            "3 gemas",
            "1 xícara de açúcar",
            "1 xícara de leite morno",
            "1 garrafa (500 ml) de suco de goiaba",
            "½ xícara de creme de leite em chantilly",
            "4 gemas (rocambole)",
            "½ xícara de açúcar (rocambole)",
            "4 claras em neve",
            "⅔ xícara de farinha de trigo",
            "pitada de sal",
            "400 g de doce de goiaba em pasta",
            "manteiga e farinha para untar",
        ],
        "steps": [
            "Bata gemas com açúcar, junte leite morno, suco e chantilly. Congele, batendo de novo após 1 hora.",
            "Preaqueça forno 200 °C. Para o rocambole: bata gemas com açúcar, incorpore claras e farinha com sal.",
            "Divida em duas assadeiras 21 × 31 cm forradas. Asse 10 minutos, vire sobre pano úmido, recheie com goiaba e enrole.",
            "Refrigere, fatie fino e forre tigela semiesférica untada e forrada com plástico.",
            "Recheie com sorvete de goiaba, cubra com fatias e congele.",
        ],
        "notes": "Rendimento: 10 a 12 porções. Versão rápida: sorvete industrializado. Descongelamento: geladeira antes de desenformar; decore com chantilly.",
    },
    {
        "slug": "bolo-de-sorvete-com-cerejas",
        "title": "Bolo de sorvete com cerejas",
        "cat": "doces",
        "sub": "Tortas e bolos",
        "ingredients": [
            "2 xícaras de sorvete crocante",
            "cerca de 200 g de biscoitos champanha",
            "licor Cointreau",
            "2 xícaras de sorvete de baunilha ou creme",
            "⅓ xícara de chocolate cobertura ralado",
            "2 xícaras de creme de leite fresco",
            "cerca de 1½ xícara de cerejas em calda ou cristalizadas",
        ],
        "steps": [
            "Forre fôrma quadrada (~1½ litro) com papel-manteiga esticado.",
            "Espalhe sorvete crocante e cubra com biscoitos champanha molhados no Cointreau.",
            "Por cima, sorvete de baunilha. Leve à geladeira para firmar e congele.",
            "Derreta chocolate em fogo brando e deixe esfriar perto de chama para não endurecer.",
            "Bata creme de leite firme, incorpore chocolate frio e congele separadamente.",
        ],
        "notes": "Rendimento: 8 porções. Descongele bolo e creme na geladeira; decore borda com creme e superfície com cerejas.",
    },
    {
        "slug": "biscoitinhos-coloridos",
        "title": "Biscoitinhos coloridos",
        "cat": "doces",
        "sub": "Biscoitos",
        "ingredients": [
            "¾ xícara de margarina",
            "½ xícara de açúcar",
            "1½ xícara de farinha de trigo",
            "1 pacote pequeno (50 g) de coco ralado",
            "1 colher (sopa) de água",
            "1 colher (sopa) de chocolate em pó",
            "margarina para untar",
        ],
        "steps": [
            "Em banho-maria, bata margarina e açúcar até cremoso.",
            "Junte farinha e coco; amasse até massa compacta (água se precisar).",
            "Divida a massa; acrescente chocolate em pó a uma metade.",
            "Abra cada metade em retângulo 17 × 22 cm sobre papel-manteiga.",
            "Sobreponha e enrole como rocambole. Refrigere 30 minutos.",
            "Corte fatias de 1 cm. Asse em assadeira untada 25 minutos até dourar. Esfrie e congele.",
        ],
        "notes": "Rendimento: 18 biscoitos. Descongelamento: 1 hora; no micro-ondas em descongelar: 2 a 4 minutos.",
    },
    {
        "slug": "biscoitinhos-de-cerveja",
        "title": "Biscoitinhos de cerveja",
        "cat": "doces",
        "sub": "Biscoitos",
        "ingredients": [
            "2¾ xícaras de farinha de trigo",
            "1 xícara de manteiga sem sal em temperatura ambiente",
            "2 colheres (sopa) de cerveja",
            "1 xícara de açúcar cristal",
        ],
        "steps": [
            "Preaqueça forno médio (180 °C). Misture farinha e manteiga com as mãos.",
            "Junte cerveja e amasse até enrolar.",
            "Faça bolinhas de 1,5 cm e passe no açúcar cristal.",
            "Asse em assadeira sem untar por 30 minutos. Esfrie e congele.",
        ],
        "notes": "Rendimento: 45 biscoitinhos. Achate as bolinhas para formato de bolacha. Descongelamento: temperatura ambiente.",
    },
    {
        "slug": "biscoitinhos-de-ameixa-preta",
        "title": "Biscoitinhos de ameixa-preta",
        "cat": "doces",
        "sub": "Biscoitos",
        "ingredients": [
            "1 xícara de manteiga",
            "1 xícara de açúcar mascavo",
            "½ xícara de açúcar",
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
            "Bata manteiga e açúcares. Junte ovos um a um.",
            "Acrescente vinagre, baunilha, ameixas, secos e nozes. Forme 3 rolos de 5 cm; embrulhe em alumínio e refrigere de um dia para o outro.",
            "Preaqueça forno 200 °C. Corte fatias finas, asse em assadeira sem untar cerca de 12 minutos. Esfrie e congele.",
        ],
        "notes": "Rendimento: 120 biscoitinhos. Também pode abrir a massa fria e usar cortadores. Descongelamento: 1 hora.",
    },
    {
        "slug": "biscoitinhos-de-chocolate-e-coco",
        "title": "Biscoitinhos de chocolate e coco",
        "cat": "doces",
        "sub": "Biscoitos",
        "ingredients": [
            "1¼ xícara de margarina",
            "1 xícara de açúcar",
            "1⅔ xícara de farinha de trigo",
            "1 colher (sopa) de fermento em pó",
            "⅓ xícara de cacau em pó",
            "pitada de sal",
            "1 xícara de chocolate em pó",
            "3 pacotes pequenos (150 g) de coco ralado",
            "¼ xícara de água fervente",
            "1 colher (chá) de café solúvel preparado",
        ],
        "steps": [
            "Bata margarina e açúcar até fofo.",
            "Peneire farinha, fermento, cacau, sal e chocolate; misture o coco.",
            "Dissolva café na água fervente.",
            "Incorpore secos e café em três etapas na batedeira. Refrigere 30 minutos. Preaqueça forno 200 °C.",
            "Forme bolinhas do tamanho de noz, espaçadas 5 cm. Asse, esfrie e congele.",
        ],
        "notes": "Rendimento: 80 biscoitos. Café solúvel: 1 parte café, 2 partes água fervente. Descongelamento: 1 hora.",
    },
    {
        "slug": "biscoitinhos-de-caramelo",
        "title": "Biscoitinhos de caramelo",
        "cat": "doces",
        "sub": "Biscoitos",
        "ingredients": [
            "½ xícara de manteiga",
            "⅔ xícara de açúcar mascavo",
            "1 ovo",
            "1⅓ xícara de farinha de trigo",
            "½ colher (chá) de fermento em pó",
            "½ colher (chá) de essência de baunilha",
            "⅓ xícara de nozes picadas",
        ],
        "steps": [
            "Derreta a manteiga. Junte açúcar mascavo e misture. Adicione ovo e bata até esbranquiçar (~10 minutos).",
            "Peneire farinha com fermento e incorpore. Junte baunilha e nozes.",
            "Refrigere até firmar (~40 minutos). Preaqueça forno 180 °C.",
            "Faça bolinhas, asse e esfrie. Congele.",
        ],
        "notes": "Rendimento: 50 biscoitos. Em lata fechada duram 2 meses; congelados, 3 a 6 meses. Descongelamento: 1 hora.",
    },
    {
        "slug": "esquecidos",
        "title": "Esquecidos",
        "cat": "doces",
        "sub": "Biscoitos",
        "ingredients": [
            "1½ xícara de açúcar",
            "4 gemas",
            "1 clara",
            "4 xícaras de farinha de trigo",
            "pitada de sal",
            "1 colher (sopa) de água",
            "manteiga e farinha para untar e polvilhar",
        ],
        "steps": [
            "Preaqueça forno médio (180 °C). Bata açúcar e gemas até creme esbranquiçado.",
            "Junte a clara e bata mais 5 minutos.",
            "Incorpore farinha e sal com as mãos até massa enrolável (água se precisar).",
            "Faça bolinhas em duas assadeiras untadas e polvilhadas. Asse 25 minutos. Esfrie e congele.",
        ],
        "notes": "Rendimento: 50 a 60 biscoitos. Polvilhe as mãos com farinha ao enrolar. Descongelamento: 1 hora e 6 minutos no forno.",
    },
    {
        "slug": "casadinhos-recheados",
        "title": "Casadinhos recheados",
        "cat": "doces",
        "sub": "Biscoitos",
        "ingredients": [
            "1¼ xícara de margarina",
            "1 xícara mais 5 colheres (sopa) de açúcar",
            "½ colher (chá) de canela em pó",
            "pitada de sal",
            "1 ovo",
            "2⅔ xícaras de farinha de trigo",
            "farinha e manteiga para polvilhar e untar",
            "1 xícara de doce de leite",
            "1 pacote pequeno (50 g) de coco ralado",
        ],
        "steps": [
            "Bata margarina amolecida até creme. Junte 1 xícara de açúcar, canela, sal e ovo.",
            "Acrescente farinha peneirada; trabalhe com as mãos. Abra 0,5 cm e corte círculos de 4,5 cm.",
            "Preaqueça forno 180 °C. Asse em fôrmas levemente untadas 10 a 15 minutos.",
            "Envolva no açúcar restante. Recheie com doce de leite misturado ao coco. Esfrie e congele.",
        ],
        "notes": "Rendimento: 50 casadinhos. Sem recheio ficam crocantes; com creme ficam mais macios. Descongelamento: 1 hora.",
    },
    {
        "slug": "sequilhos-de-coco",
        "title": "Sequilhos de coco",
        "cat": "doces",
        "sub": "Biscoitos",
        "ingredients": [
            "manteiga e farinha para untar e polvilhar",
            "1⅓ xícara de farinha de trigo",
            "¾ xícara de açúcar",
            "1 colher (chá) de fermento em pó",
            "1 pacote pequeno (50 g) de coco ralado",
            "pitada de sal",
            "¾ xícara de manteiga",
            "1 gema",
        ],
        "steps": [
            "Preaqueça forno 180 °C. Unte e polvilhe duas assadeiras grandes.",
            "Misture secos. Faça cova, coloque manteiga em pedaços e gema; amasse com os dedos até desgrudar das mãos.",
            "Faça cordões, corte como nhoque e marque com garfo.",
            "Asse 15 minutos, trocando as assadeiras na metade do tempo. Esfrie e congele.",
        ],
        "notes": "Rendimento: 90 sequilhos. Descongelamento: 1 hora.",
    },
    {
        "slug": "waffles-com-iogurte",
        "title": "Waffles com iogurte",
        "cat": "doces",
        "sub": "Outros doces",
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
            "Esquente o aparelho de waffles conforme o fabricante.",
            "Misture farinha, fermento, bicarbonato e sal.",
            "Junte iogurte, óleo e ovos; bata até homogêneo.",
            "Despeje no aparelho até 2,5 cm da borda. Feche e asse sem abrir.",
            "Solte com garfo, reaqueça o aparelho entre waffles. Esfrie e congele.",
        ],
        "notes": "Rendimento: 5 waffles. Massa crua pode ser congelada em recipiente rígido; descongele na geladeira. Descongelamento: 1 hora e aqueça antes de servir.",
    },
    {
        "slug": "cheesecake-basco-de-chocolate",
        "title": "Cheesecake basco de chocolate",
        "cat": "doces",
        "sub": "Tortas e bolos",
        "ingredients": [
            "500 g de cream cheese em temperatura ambiente",
            "150 g de açúcar",
            "4 ovos",
            "150 g de chocolate amargo 70%",
            "200 ml de creme de leite",
            "1 colher (chá) de essência de baunilha",
        ],
        "steps": [
            "Preaqueça o forno a 200 °C. Forre fôrma de aro removível com papel manteiga.",
            "Bata cream cheese e açúcar até liso.",
            "Junte ovos um a um.",
            "Derreta o chocolate e incorpore com o creme de leite e baunilha.",
            "Despeje na forma e asse até a superfície ficar bem queimada e o centro ainda tremulo (cerca de 35 a 45 minutos).",
            "Esfrie completamente e refrigere antes de servir.",
        ],
        "notes": "Receita adaptada de infográfico (Pinterest). Forno bem quente é essencial para a crosta caramelizada típica do basque.",
    },
]


def render_recipe(r: dict) -> str:
    cat_label = {"doces": "Doces", "salgados": "Salgados"}[r["cat"]]
    category = f"{cat_label} · {r['sub']}"
    ing = "\n".join(f"          <li>{html.escape(i)}</li>" for i in r["ingredients"])
    steps = "\n".join(f"          <li>{html.escape(s)}</li>" for s in r["steps"])
    notes = html.escape(r.get("notes", ""))
    slug = r["slug"]
    title = r["title"]
    cat_hash = r["cat"]

    return f"""<!DOCTYPE html>
<html lang="pt-BR">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{html.escape(title)} — Livro de Receitas</title>
    <meta name="description" content="{html.escape(title)} — ficha A5 para imprimir." />
    <link rel="stylesheet" href="../../css/site.css" />
    <link rel="stylesheet" href="../../css/print.css" />
  </head>
  <body>
    <header class="site-header no-print">
      <a class="brand" href="../../index.html">Livro de Receitas</a>
      <nav class="site-nav" aria-label="Principal">
        <a href="../../index.html#{cat_hash}">{cat_label}</a>
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
        <h1>{html.escape(title)}</h1>
        <figure class="dish-photo no-print">
  <img src="../../imagens/{slug}.jpg" alt="Referência: {html.escape(title)}" />
  <figcaption>Referência visual (não é a foto da receita da família).</figcaption>
</figure>
        <h2>Ingredientes</h2>
        <ul class="ingredients">
{ing}
        </ul>

        <h2>Modo de preparo</h2>
        <ol class="steps">
{steps}
        </ol>
        <h2>Observação</h2>
        <p class="notes">{notes}</p>
      </article>
    </main>
    <script src="../../js/recipe-layout.js" defer></script>
  </body>
</html>
"""


def main() -> None:
    for r in RECIPES:
        path = ROOT / "receitas" / r["cat"] / f"{r['slug']}.html"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_recipe(r), encoding="utf-8")
        print(f"Wrote {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
