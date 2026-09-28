#!/usr/bin/env python3
"""Gera fichas do lote Telegram ago/2026 e atualiza index.html."""
from __future__ import annotations

import html
import re
import subprocess
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECEITAS = ROOT / "receitas"
IMAGENS = ROOT / "imagens"
INDEX = ROOT / "index.html"

# cat_folder, category_label, subcategory, slug, title, ingredients[], steps[], notes
RECIPES: list[tuple] = [
    (
        "doces",
        "Doces",
        "Tortas e bolos",
        "cheesecake-basque-de-chocolate",
        "Cheesecake basco de chocolate",
        [
            "500 g de cream cheese em temperatura ambiente",
            "150 g de açúcar",
            "4 ovos",
            "150 g de chocolate meio amargo (70%)",
            "200 ml de creme de leite",
            "1 colher (chá) de essência de baunilha ou pitada de sal",
        ],
        [
            "Pré-aqueça o forno a 200 °C. Forre uma forma redonda com papel-manteiga.",
            "Bata o cream cheese com o açúcar até ficar liso.",
            "Acrescente os ovos um a um, batendo após cada adição.",
            "Incorpore o chocolate derretido e o creme de leite.",
            "Despeje na forma e asse até a superfície dourar e o centro ainda estiver levemente bamboleante (cerca de 35–45 min).",
            "Deixe esfriar completamente antes de desenformar.",
        ],
        "Receita adaptada de infográfico (Pinterest). Forno ~200 °C ≈ 400 °F do original.",
    ),
    (
        "doces",
        "Doces",
        "Tortas e bolos",
        "cheesecake-basque-de-matcha",
        "Cheesecake basco de matcha",
        [
            "500 g de cream cheese",
            "200 g de açúcar",
            "250 ml de creme de leite",
            "4 ovos",
            "1 colher e meia (sopa) de farinha de trigo",
            "1 colher e meia (sopa) de matcha em pó",
        ],
        [
            "Pré-aqueça o forno a 200 °C. Forre a forma com papel-manteiga.",
            "Bata o cream cheese com o açúcar até homogeneizar.",
            "Adicione os ovos um a um.",
            "Misture o creme de leite e a farinha peneirada.",
            "Incorpore o matcha delicadamente.",
            "Asse até dourar por cima e o centro ficar levemente tremido. Esfrie antes de cortar.",
        ],
        "Receita adaptada de infográfico (Pinterest).",
    ),
    (
        "salgados",
        "Salgados",
        "Massas fritas/assadas",
        "paezinhos-rapidos",
        "Pãezinhos rápidos",
        [
            "2 xícaras de farinha de trigo",
            "2 colheres e meia (chá) de fermento em pó",
            "1 colher (chá) de sal",
            "1/3 xícara de manteiga ou margarina gelada",
            "Farinha para polvilhar",
        ],
        [
            "Pré-aqueça o forno em temperatura alta (250 °C). Peneire farinha, fermento e sal; incorpore a manteiga com duas facas até virar farofa.",
            "Amasse na bancada até integrar; abra com 1 cm de espessura.",
            "Recorte com cortador de 5 cm e disponha em assadeira sem untar.",
            "Asse 12–15 min até levemente dourados. Esfrie e congele se desejar.",
        ],
        "Rendimento: 28 pãezinhos. Congele cobertos com plástico; descongele 1 h em temperatura ambiente. Varie com alcaravia, erva-doce ou linguiça antes de assar.",
    ),
    (
        "salgados",
        "Salgados",
        "Massas fritas/assadas",
        "pao-de-forma",
        "Pão de forma",
        [
            "5 1/2 a 6 1/2 xícaras de farinha de trigo",
            "2 colheres (chá) de sal",
            "2 colheres (sopa) de manteiga",
            "1 tablete (15 g) de fermento para pão",
            "1 3/4 xícara de água morna",
            "Farinha e manteiga para untar",
        ],
        [
            "Peneire farinha e sal; esfarele a manteiga. Faça um buraco no centro e adicione o fermento dissolvido na água morna.",
            "Misture e sove cerca de 10 min até liso e elástico.",
            "Deixe crescer até dobrar. Desgasifique, enrole em cilindro e coloque em forma de 900 g untada.",
            "Deixe crescer novamente. Asse em forno alto (230 °C) por 30–40 min até dourar e soar vazia ao bater na base.",
            "Esfrie em grade e congele embrulhado.",
        ],
        "Rendimento: 1 pão. Descongele ~2 h em temperatura ambiente.",
    ),
    (
        "salgados",
        "Salgados",
        "Massas fritas/assadas",
        "pao-integral",
        "Pão integral",
        [
            "3 colheres (sopa) de açúcar",
            "2 tabletes (30 g) de fermento para pão",
            "4 colheres (chá) de sal",
            "4 xícaras de farinha integral",
            "3 a 3 1/2 xícaras de farinha de trigo",
            "2 1/2 xícaras de leite",
            "1/3 xícara de manteiga ou margarina",
            "1/3 xícara de melado",
            "Farinha e manteiga para untar",
        ],
        [
            "Misture açúcar, fermento, sal e parte das farinhas. Aqueça leite, manteiga e melado até bem quente.",
            "Bata líquidos nos secos; acrescente farinhas até formar massa.",
            "Sove, deixe crescer, divida em dois e descanse 15 min.",
            "Abra cada porção, enrole como rocambole e coloque em formas de 13×23 cm untadas.",
            "Deixe crescer; asse a 200 °C por 30–35 min. Esfrie e congele.",
        ],
        "Rendimento: 2 pães. Dica: bolinha de massa em copo com água — quando subir, a massa cresceu.",
    ),
    (
        "salgados",
        "Salgados",
        "Massas fritas/assadas",
        "pao-sirio",
        "Pão sírio",
        [
            "6 xícaras de farinha de trigo",
            "1 tablete (15 g) de fermento para pão",
            "2 xícaras de água morna",
            "1 1/2 colher (chá) de sal",
            "1 colher (chá) de açúcar",
            "2 colheres (sopa) de óleo",
            "Farinha e óleo para untar",
        ],
        [
            "Dissolva o fermento em parte da água com sal e açúcar. Misture à farinha aquecida; sove 10 min com óleo.",
            "Deixe crescer 1 h. Divida em 10 bolas, abra discos de 20 cm e descanse 20 min.",
            "Pré-aqueça assadeira a 200 °C. Asse cada pão 4–5 min até inchar; envolva em pano limpo.",
        ],
        "Rendimento: 10 pães. Fermento biológico pode ser congelado em papel alumínio (3 meses).",
    ),
    (
        "doces",
        "Doces",
        "Biscoitos",
        "broinhas-de-fuba",
        "Broinhas de fubá",
        [
            "2 xícaras de açúcar",
            "1 xícara de manteiga",
            "5 gemas",
            "200 ml de leite de coco",
            "1 xícara de leite",
            "2 xícaras de fubá",
            "1 xícara de farinha de trigo",
            "1 colher (sopa) de fermento em pó",
            "5 claras em neve firme",
        ],
        [
            "Forre 40 forminhas de 7 cm com duas cápsulas cada. Pré-aqueça o forno a 180 °C.",
            "Bata açúcar e manteiga; alterne gemas com leites.",
            "Incorpore fubá, farinha e fermento; misture as claras delicadamente.",
            "Distribua nas forminhas e asse ~35 min até dourar. Esfrie e congele.",
        ],
        "Rendimento: 40 broinhas. Ao congelar, preencha espaços vazios com papel-toalha entre camadas.",
    ),
    (
        "doces",
        "Doces",
        "Outros doces",
        "muffins-com-passas",
        "Muffins com passas",
        [
            "Manteiga para untar",
            "1 xícara de farinha de trigo",
            "1 xícara de farinha integral",
            "1 colher (sopa) de açúcar",
            "1/2 colher (chá) de sal",
            "3 colheres (chá) de fermento em pó",
            "1 ovo",
            "1/4 xícara de óleo",
            "1 xícara de leite",
            "1/2 xícara de passas brancas embebidas em água morna e escorridas",
        ],
        [
            "Pré-aqueça o forno a 180 °C. Unte 12 forminhas de muffin.",
            "Peneire farinhas, açúcar, sal e fermento.",
            "Misture ovo, óleo e leite; junte à farinha com as passas, só até umedecer (massa irregular).",
            "Encha 2/3 das forminhas; asse ~25 min. Esfrie e congele.",
        ],
        "Rendimento: 12 muffins. Forminhas de empada de 7 cm também servem.",
    ),
    (
        "doces",
        "Doces",
        "Tortas e bolos",
        "rosca-de-natal",
        "Rosca de Natal",
        [
            "1 caixa (400 g) de mistura para salgados",
            "1/3 xícara de leite",
            "3 ovos",
            "1/4 xícara de manteiga",
            "1/2 xícara de açúcar cristal",
            "1/4 xícara de mel",
            "1 colher (chá) de canela",
            "1 1/2 xícara de nozes picadas",
            "2 colheres (chá) de suco de limão",
            "2 xícaras de passas e frutas cristalizadas em 2/3 xícara de Cointreau",
            "1 gema para pincelar",
        ],
        [
            "Misture a massa com 1/3 xícara de leite e 2 ovos.",
            "Prepare o recheio: manteiga, açúcar, leite, mel e canela; ferva, junte nozes, amorne, acrescente o terceiro ovo batido e limão.",
            "Abra a massa em retângulo 37×54 cm; espalhe recheio e frutas escorridas; enrole e forme rosca.",
            "Corte fatias inclinadas, deixe crescer 20 min. Asse a 200 °C, depois 180 °C até dourar.",
        ],
        "Rendimento: 10 porções. Massa crua não deve ser recongelada — asse antes de congelar.",
    ),
    (
        "doces",
        "Doces",
        "Tortas e bolos",
        "bolo-merenda",
        "Bolo merenda",
        [
            "3/4 xícara de manteiga",
            "3/4 xícara de açúcar",
            "3 gemas",
            "1 1/2 xícara de farinha de trigo",
            "1 colher (chá) de fermento em pó",
            "2 colheres (sopa) de leite",
            "3 claras em neve",
            "Manteiga para untar",
        ],
        [
            "Pré-aqueça o forno a 200 °C. Bata manteiga com açúcar e gemas até claro.",
            "Incorpore farinha peneirada com fermento e leite.",
            "Misture as claras delicadamente; asse em forma de 21 cm ~30 min.",
        ],
        "Rendimento: 8 porções. Varie com goiabada ou gotas de chocolate.",
    ),
    (
        "doces",
        "Doces",
        "Tortas e bolos",
        "bolo-de-especiarias",
        "Bolo de especiarias",
        [
            "2 xícaras de farinha de trigo",
            "1 xícara de açúcar",
            "1 colher de fermento em pó",
            "1 colher (chá) de sal",
            "1/2 colher (chá) de bicarbonato",
            "1/2 colher (sopa) de cravo em pó",
            "1 colher (sopa) de canela",
            "1/2 xícara de margarina",
            "3/4 xícara de açúcar mascavo",
            "1 xícara de creme de leite azedado com 1 colher (sopa) de limão",
            "3 ovos",
            "1/2 xícara de nozes picadas",
        ],
        [
            "Pré-aqueça o forno a 180 °C. Misture secos com especiarias.",
            "Incorpore margarina, mascavo e creme; bata 2 min. Junte ovos e nozes.",
            "Asse em forma inglesa untada 30–35 min. Esfrie e congele.",
        ],
        "Rendimento: 6–8 porções.",
    ),
    (
        "doces",
        "Doces",
        "Tortas e bolos",
        "bolo-de-mandioca",
        "Bolo de mandioca",
        [
            "2 1/4 xícaras de mandioca ralada fina",
            "2 1/4 xícaras de queijo-de-minas meia cura ralado",
            "2 1/4 xícaras de açúcar",
            "1 1/4 xícara de leite",
            "Canela e cravo em pó (1 colher café de cada)",
            "8 ovos ligeiramente batidos",
            "Manteiga, canela e açúcar para polvilhar",
        ],
        [
            "Pré-aqueça o forno a 180 °C. Misture mandioca, queijo, açúcar, leite e especiarias.",
            "Junte os ovos; asse em assadeira 24×34 cm ~45 min.",
            "Polvilhe canela com açúcar; esfrie, corte em quadrados e congele.",
        ],
        "Rendimento: 12 porções.",
    ),
    (
        "doces",
        "Doces",
        "Tortas e bolos",
        "bolo-de-chocolate",
        "Bolo de chocolate",
        [
            "50 g de chocolate amargo picado",
            "3/4 xícara de manteiga",
            "1 1/2 xícara de açúcar",
            "3 ovos",
            "1 colher (chá) de baunilha",
            "2 xícaras de farinha de trigo",
            "2 colheres (chá) de fermento",
            "1/2 colher (chá) de sal",
            "3/4 xícara de leite",
            "Calda: 1 colher (sopa) manteiga, 1 xícara açúcar, 1/2 xícara cacau, 1/4 xícara leite",
            "120 g de chocolate branco picado para decorar",
        ],
        [
            "Derreta o chocolate amargo. Bata manteiga e açúcar; acrescente ovos, baunilha e chocolate.",
            "Alterne farinha com fermento e sal com o leite. Asse em forma de 26 cm a 180 °C até firmar.",
            "Prepare a calda e espalhe no bolo frio; decore com chocolate branco derretido.",
        ],
        "Rendimento: 10 porções.",
    ),
    (
        "doces",
        "Doces",
        "Tortas e bolos",
        "bolo-de-laranja",
        "Bolo de laranja",
        [
            "1/2 xícara de óleo",
            "2 xícaras de açúcar",
            "4 gemas",
            "2 xícaras de fubá",
            "1 xícara de farinha de trigo",
            "1 colher (sopa) de fermento",
            "1 xícara de suco de laranja",
            "4 claras em neve",
            "Manteiga e farinha para untar",
        ],
        [
            "Pré-aqueça o forno a 180 °C. Bata óleo, açúcar e gemas.",
            "Alterne fubá, farinha e fermento com suco de laranja.",
            "Incorpore claras; asse em forma com furo central ~45 min.",
        ],
        "Rendimento: 8 porções. Preencha o buraco da forma com plástico ao congelar.",
    ),
    (
        "doces",
        "Doces",
        "Tortas e bolos",
        "bolo-de-abacaxi",
        "Bolo de abacaxi",
        [
            "1 colher (sopa) de manteiga",
            "1/4 xícara de açúcar demerara",
            "5 rodelas de abacaxi em conserva escorridas",
            "5 cerejas ao marasquino",
            "1 xícara de farinha",
            "3/4 xícara de açúcar",
            "1 pitada de sal",
            "1 ovo",
            "2 colheres (sopa) de margarina",
            "1/2 xícara da calda do abacaxi",
            "1 colher (chá) de baunilha",
            "1 colher (chá) de fermento",
        ],
        [
            "Pré-aqueça o forno a 180 °C. Derreta manteiga em forma de vidro de 25 cm; polvilhe demerara e arrume abacaxi e cerejas.",
            "Bata os demais ingredientes no liquidificador; espalhe sobre a fruta e asse até o palito sair limpo.",
            "Desenforme ainda morno; esfrie e congele.",
        ],
        "Rendimento: 8 porções.",
    ),
    (
        "doces",
        "Doces",
        "Tortas e bolos",
        "bolo-de-fuba-e-coco",
        "Bolo de fubá e coco",
        [
            "1 xícara de açúcar",
            "1/2 xícara de manteiga",
            "3 gemas",
            "1 vidro pequeno (200 ml) de leite de coco",
            "1 xícara de leite",
            "1 xícara de fubá",
            "1 pacote pequeno (50 g) de coco ralado",
            "1/2 xícara de farinha de trigo",
            "1 colher (sopa) de fermento em pó",
            "3 claras em neve bem firmes",
            "2 colheres (sopa) de açúcar (para regar)",
        ],
        [
            "Bata açúcar e manteiga; junte gemas e leites.",
            "Misture fubá, coco, farinha e fermento; incorpore claras.",
            "Asse em assadeira 20×30 cm: 20 min a 200 °C, depois 5 min a 150 °C.",
            "Misture o restante do leite de coco com açúcar e regue o bolo quente. Corte em quadrados.",
        ],
        "Rendimento: 24 porções.",
    ),
    (
        "doces",
        "Doces",
        "Tortas e bolos",
        "bolo-gelado-de-goiaba",
        "Bolo gelado de goiaba",
        [
            "Sorvete: 3 gemas, 1 xícara de açúcar, 1 xícara de leite morno, 500 ml suco de goiaba, 1/2 xícara de chantilly",
            "Rocambole: 4 gemas, 1/2 xícara de açúcar, 4 claras, 2/3 xícara de farinha, sal, 400 g de doce de goiaba em pasta",
        ],
        [
            "Prepare o sorvete batendo gemas com açúcar e leite morno; incorpore suco e chantilly; congele batendo uma vez.",
            "Faça dois rocamboles finos; recheie com goiaba, enrole e refrigere fatias.",
            "Forre tigela com fatias, encha com sorvete, cubra e congele.",
        ],
        "Rendimento: 10–12 porções. Pode usar sorvete industrializado.",
    ),
    (
        "doces",
        "Doces",
        "Tortas e bolos",
        "bolo-de-sorvete-com-cerejas",
        "Bolo de sorvete com cerejas",
        [
            "2 xícaras de sorvete crocante",
            "Cerca de 200 g de biscoitos champanhe",
            "Licor Cointreau",
            "2 xícaras de sorvete de baunilha ou creme",
            "1/3 xícara de chocolate cobertura ralado",
            "2 xícaras de creme de leite fresco",
            "1 1/2 xícara de cerejas em calda escorridas",
        ],
        [
            "Forre forma quadrada (~1,5 l) com papel-manteiga.",
            "Camadas: crocante, biscoitos molhados no licor, baunilha; congele.",
            "Derreta o chocolate; bata o creme com chocolate frio e congele separadamente.",
            "Monte, decore com cerejas e creme ao servir.",
        ],
        "Rendimento: 8 porções.",
    ),
    (
        "doces",
        "Doces",
        "Biscoitos",
        "biscoitinhos-coloridos",
        "Biscoitinhos coloridos",
        [
            "3/4 xícara de margarina",
            "1/2 xícara de açúcar",
            "1 1/2 xícara de farinha",
            "50 g de coco ralado",
            "1 colher (sopa) de água",
            "1 colher (sopa) de cacau em pó",
        ],
        [
            "Bata margarina e açúcar em banho-maria até cremoso.",
            "Misture farinha e coco; divida a massa e acrescente cacau a uma metade.",
            "Abra retângulos, sobreponha, enrole, geladeira 30 min.",
            "Corte fatias de 1 cm e asse a 180 °C ~25 min.",
        ],
        "Rendimento: 18 biscoitos.",
    ),
    (
        "doces",
        "Doces",
        "Biscoitos",
        "biscoitinhos-de-cerveja",
        "Biscoitinhos de cerveja",
        [
            "2 3/4 xícaras de farinha",
            "1 xícara de manteiga sem sal em temperatura ambiente",
            "2 colheres (sopa) de cerveja",
            "1 xícara de açúcar cristal",
        ],
        [
            "Misture farinha e manteiga; acrescente cerveja até ligar.",
            "Faça bolinhas de 1,5 cm, passe no açúcar e asse a 180 °C por 30 min.",
        ],
        "Rendimento: 45 biscoitos.",
    ),
    (
        "doces",
        "Doces",
        "Biscoitos",
        "biscoitinhos-de-ameixa-preta",
        "Biscoitinhos de ameixa-preta",
        [
            "1 xícara de manteiga",
            "1 xícara de açúcar mascavo",
            "1/2 xícara de açúcar",
            "2 ovos",
            "1 colher (sopa) de vinagre",
            "1 colher (chá) de baunilha",
            "1 xícara de ameixas secas picadas",
            "4 xícaras de farinha",
            "1 colher (chá) de bicarbonato e sal",
            "1 xícara de nozes picadas",
        ],
        [
            "Bata manteiga e açúcares; junte ovos, vinagre, baunilha, ameixas e secos.",
            "Forme 3 rolos; geladeira overnight.",
            "Corte rodelas finas e asse a 200 °C ~12 min.",
        ],
        "Rendimento: 120 biscoitos.",
    ),
    (
        "doces",
        "Doces",
        "Biscoitos",
        "biscoitinhos-de-chocolate-e-coco",
        "Biscoitinhos de chocolate e coco",
        [
            "1 1/4 xícara de margarina",
            "1 xícara de açúcar",
            "1 2/3 xícara de farinha",
            "1 colher (sopa) de fermento",
            "1/3 xícara de cacau",
            "Sal",
            "1 xícara de chocolate em pó",
            "150 g de coco ralado",
            "1/4 xícara de água fervente",
            "1 colher (chá) de café solúvel preparado",
        ],
        [
            "Bata margarina e açúcar; alterne secos com mistura de água e café.",
            "Geladeira 30 min. Faça bolas do tamanho de noz; asse a 200 °C.",
        ],
        "Rendimento: 80 biscoitos.",
    ),
    (
        "doces",
        "Doces",
        "Biscoitos",
        "biscoitinhos-de-caramelo",
        "Biscoitinhos de caramelo",
        [
            "1/2 xícara de manteiga",
            "2/3 xícara de açúcar mascavo",
            "1 ovo",
            "1 1/3 xícara de farinha",
            "1/2 colher (chá) de fermento",
            "1/2 colher (chá) de baunilha",
            "1/3 xícara de nozes picadas",
        ],
        [
            "Derreta a manteiga; misture mascavo e ovo batendo ~10 min.",
            "Incorpore farinha, fermento, baunilha e nozes; geladeira 40 min.",
            "Faça bolinhas e asse a 180 °C.",
        ],
        "Rendimento: 50 biscoitos.",
    ),
    (
        "doces",
        "Doces",
        "Biscoitos",
        "esquecidos",
        "Esquecidos",
        [
            "1 1/2 xícara de açúcar",
            "4 gemas",
            "1 clara",
            "4 xícaras de farinha",
            "Sal",
            "1 colher (sopa) de água",
            "Manteiga e farinha para assadeiras",
        ],
        [
            "Bata açúcar e gemas; junte clara e farinha até massa enrolável.",
            "Faça bolinhas; asse a 180 °C por 25 min.",
        ],
        "Rendimento: 50–60 biscoitos.",
    ),
    (
        "doces",
        "Doces",
        "Biscoitos",
        "casadinhos-recheados",
        "Casadinhos recheados",
        [
            "1 1/4 xícara de margarina",
            "1 xícara + 5 colheres (sopa) de açúcar",
            "1/2 colher (chá) de canela",
            "Sal",
            "1 ovo",
            "2 2/3 xícaras de farinha",
            "1 xícara de doce de leite",
            "50 g de coco ralado",
        ],
        [
            "Bata margarina com 1 xícara de açúcar, canela, sal e ovo; incorpore farinha.",
            "Abra 0,5 cm; corte círculos de 4,5 cm e asse a 180 °C 10–15 min.",
            "Envolva no açúcar restante; recheie com doce de leite e coco.",
        ],
        "Rendimento: 50 casadinhos.",
    ),
    (
        "doces",
        "Doces",
        "Biscoitos",
        "sequilhos-de-coco",
        "Sequilhos de coco",
        [
            "1 1/3 xícara de farinha",
            "3/4 xícara de açúcar",
            "1 colher (chá) de fermento",
            "50 g de coco ralado",
            "Sal",
            "3/4 xícara de manteiga",
            "1 gema",
        ],
        [
            "Misture secos; incorpore manteiga e gema até desgrudar das mãos.",
            "Faça cordões, corte como nhoque, marque com garfo; asse a 180 °C 15 min.",
        ],
        "Rendimento: 90 sequilhos.",
    ),
    (
        "doces",
        "Doces",
        "Outros doces",
        "waffles-com-iogurte",
        "Waffles com iogurte",
        [
            "1 3/4 xícara de farinha",
            "1 colher (chá) de fermento",
            "1 colher (chá) de bicarbonato",
            "1/2 colher (chá) de sal",
            "2 xícaras de iogurte natural ou leite azedo",
            "1/3 xícara de óleo",
            "2 ovos",
        ],
        [
            "Misture secos; junte iogurte, óleo e ovos.",
            "Despeje na máquina de waffle conforme o fabricante; asse sem abrir.",
            "Esfrie e congele em saco bem vedado.",
        ],
        "Rendimento: 5 waffles. Massa crua também pode ser congelada.",
    ),
]


def render_ficha(
    folder: str,
    category: str,
    subcategory: str,
    slug: str,
    title: str,
    ingredients: list[str],
    steps: list[str],
    notes: str,
) -> str:
    cat_line = f"{category} · {subcategory}" if subcategory else category
    hash_cat = folder
    ing_li = "\n".join(f"          <li>{html.escape(i)}</li>" for i in ingredients)
    steps_li = "\n".join(f"          <li>{html.escape(s)}</li>" for s in steps)
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
        <a href="../../index.html#{hash_cat}">{html.escape(category)}</a>
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
        <h1>{html.escape(title)}</h1>
        <figure class="dish-photo no-print">
  <img src="../../imagens/{slug}.jpg" alt="Referência: {html.escape(title)}" />
  <figcaption>Referência visual (não é a foto da receita da família).</figcaption>
</figure>
        <h2>Ingredientes</h2>
        <ul class="ingredients">
{ing_li}
        </ul>

        <h2>Modo de preparo</h2>
        <ol class="steps">
{steps_li}
        </ol>
        <h2>Observação</h2>
        <p class="notes">{html.escape(notes)}</p>
      </article>
    </main>
    <script src="../../js/recipe-layout.js" defer></script>
  </body>
</html>
"""


def fetch_dish_image(slug: str, title: str) -> bool:
    try:
        from ddgs import DDGS
    except ImportError:
        subprocess.check_call(["pip3", "install", "-q", "ddgs"])
        from ddgs import DDGS

    dest = IMAGENS / f"{slug}.jpg"
    if dest.exists() and dest.stat().st_size > 5000:
        return True
    query = f"{title} receita"
    url = None
    for attempt in range(3):
        try:
            with DDGS() as d:
                for r in d.images(query, max_results=8):
                    u = r.get("image") or ""
                    if u.startswith("http"):
                        url = u
                        break
            break
        except Exception:
            import time

            time.sleep(2 * (attempt + 1))
    if not url:
        return False
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0 (compatible; receitas-bot/1.0)"},
    )
    try:
        data = urllib.request.urlopen(req, timeout=25).read()
        if len(data) < 3000:
            return False
        dest.write_bytes(data)
        return True
    except Exception:
        return False


def insert_index_entries():
    text = INDEX.read_text(encoding="utf-8")
    by_sub: dict[str, list[tuple[str, str, str]]] = {}
    for folder, category, sub, slug, title, *_ in RECIPES:
        href = f"./receitas/{folder}/{slug}.html"
        by_sub.setdefault(sub, []).append((title.lower(), href, title))

    for sub, items in by_sub.items():
        items.sort(key=lambda x: x[0])
        lis = "\n".join(
            f'          <li>\n            <a href="{href}">{html.escape(title)}</a>\n          </li>'
            for _, href, title in items
        )
        pattern = (
            rf'(<ul class="recipe-list" data-subcategory="{re.escape(sub)}">\n)'
            rf'((?:.*?\n)*?)'
            rf'(        </ul>)'
        )
        m = re.search(pattern, text, re.DOTALL)
        if not m:
            raise SystemExit(f"Subcategoria não encontrada no index: {sub}")
        block = m.group(2)
        for _, href, title in items:
            if href in block:
                continue
            block += f'          <li>\n            <a href="{href}">{title}</a>\n          </li>\n'
        # re-sort all li in block
        existing = re.findall(
            r'          <li>\s*<a href="([^"]+)">([^<]+)</a>\s*</li>',
            block,
        )
        merged = {(t.lower(), h, t) for h, t in existing}
        for _, href, title in items:
            merged.add((title.lower(), href, title))
        sorted_items = sorted(merged, key=lambda x: x[0])
        new_block = "".join(
            f'          <li>\n            <a href="{h}">{t}</a>\n          </li>\n'
            for _, h, t in sorted_items
        )
        text = text[: m.start(2)] + new_block + text[m.end(2) :]

    INDEX.write_text(text, encoding="utf-8")


def main() -> None:
    IMAGENS.mkdir(exist_ok=True)
    for row in RECIPES:
        folder, category, sub, slug, title, ingredients, steps, notes = row
        out_dir = RECEITAS / folder
        out_dir.mkdir(parents=True, exist_ok=True)
        path = out_dir / f"{slug}.html"
        path.write_text(
            render_ficha(folder, category, sub, slug, title, ingredients, steps, notes),
            encoding="utf-8",
        )
        try:
            ok = fetch_dish_image(slug, title)
        except Exception as exc:
            ok = False
            print(f"{slug}: imagem erro {exc}")
        else:
            print(f"{slug}: html ok, imagem={'ok' if ok else 'falhou'}")

    insert_index_entries()
    print("index.html atualizado")


if __name__ == "__main__":
    main()
