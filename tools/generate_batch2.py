#!/usr/bin/env python3
"""Part 2: savory / meat / seafood / pasta recipes + HTML generation."""
from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

from generate_batch import RECIPES as PART1, CATEGORIES  # noqa: E402

PART2: list[dict] = [
    # handwritten / notebook
    {
        "cat": "acompanhamentos",
        "slug": "molho-branco-sem-fogo",
        "title": "Molho branco (sem ir ao fogo)",
        "meta": None,
        "ingredients": [
            "½ lata de creme de leite",
            "1 copo de requeijão",
            "1 colher de farinha de trigo",
            "1 colher de tempero pronto",
            "1 pitada de noz-moscada",
            "2 colheres de queijo ralado",
        ],
        "steps": [
            "Misture todos os ingredientes até homogenizar.",
            "Espalhe sobre o frango (ou outro prato) e leve ao forno até dourar.",
        ],
        "notes": "Receita manuscrita da família; pensada para cobrir frango no forno.",
    },
    {
        "cat": "salgados",
        "slug": "waffle-salgado",
        "title": "Waffle salgado",
        "meta": None,
        "ingredients": [
            "175 g de farinha de trigo (cerca de 1½ xícara)",
            "2 colheres de fermento",
            "1 colher de sal",
            "2 colheres de açúcar",
            "2 gemas",
            "225 ml de leite",
            "85 g de margarina derretida",
            "Claras em neve (das 2 gemas)",
        ],
        "steps": [
            "Misture a farinha, o fermento, o sal, o açúcar, as gemas, o leite e a margarina.",
            "No fim, misture as claras em neve.",
            "Asse na máquina de waffle até dourar (tempo usual ~3–5 min por waffle).",
        ],
        "notes": "Título original «Waffer (salgado)». Temperatura/tempo da máquina inferidos.",
    },
    {
        "cat": "salgados",
        "slug": "pao-de-queijo",
        "title": "Pão de queijo",
        "meta": None,
        "ingredients": [
            "500 g de polvilho doce",
            "1 copo pequeno de óleo",
            "4 ovos",
            "½ copo de água",
            "½ copo de leite",
            "200 g de queijo ralado",
        ],
        "steps": [
            "Escalde o polvilho com o óleo, a água e o leite (líquidos quentes).",
            "Deixe esfriar, junte os ovos e o queijo; amasse bem.",
            "Faça bolinhas; congele ou asse cerca de 20 minutos.",
        ],
        "notes": "Receita manuscrita. Asse em forno médio preaquecido (~180–200 °C) até dourar.",
    },
    # Liquigás pastas
    {
        "cat": "massas",
        "slug": "espaguete-a-carbonara",
        "title": "Espaguete à carbonara",
        "meta": None,
        "ingredients": [
            "4 colheres (sopa) de azeite",
            "500 g de espaguete de sêmola cozido",
            "100 g de parmesão ralado",
            "1 pote de creme de leite fresco",
            "Salsinha a gosto e sal",
            "300 g de bacon",
            "6 gemas",
        ],
        "steps": [
            "Frite o bacon em 2 colheres de azeite até crocante; escorra em papel e esmigalhe.",
            "Bata gemas, queijo, creme de leite e sal até esbranquiçar. Cozinhe em banho-maria batendo, sem ferver.",
            "Acrescente aos poucos o restante do azeite aquecido; junte bacon e salsinha. Misture na massa. Opcional: fatias de bacon torradas por cima.",
        ],
        "notes": "Fonte: livretinho Liquigás.",
    },
    {
        "cat": "massas",
        "slug": "macarrao-a-moda-do-sul",
        "title": "Macarrão à moda do Sul",
        "meta": None,
        "ingredients": [
            "250 g de macarrão cozido em água e sal",
            "2 cubinhos de caldo de carne dissolvidos em 1 xícara de leite quente",
            "3 colheres (sopa) de queijo ralado",
            "1 colher (sopa) de margarina",
            "150 g de presunto picadinho",
            "3 claras em neve",
            "3 gemas",
        ],
        "steps": [
            "Coloque o macarrão em forma refratária untada e polvilhada com farinha de rosca. Espalhe queijo e presunto.",
            "Misture a margarina com o caldo e despeje sobre o macarrão.",
            "Bata ligeiramente as gemas com as claras; espalhe por cima. Leve ao forno quente por 15 minutos.",
        ],
    },
    {
        "cat": "massas",
        "slug": "macarrao-tentador",
        "title": "Macarrão tentador",
        "meta": None,
        "ingredients": [
            "300 g de talharim fresco fino",
            "2 xícaras (chá) de peito de frango cozido e desfiado",
            "5 xícaras (chá) de queijo ralado",
            "1½ xícara (chá) de caldo de galinha",
            "1½ xícara (chá) de leite",
            "1 colher (sopa) de amido de milho",
            "1 colher (chá) de pimenta-do-reino",
            "2 colheres (sopa) de manteiga",
            "100 g de queijo fundido",
            "1 pacote de batatas fritas",
            "2 gemas",
            "Sal",
        ],
        "steps": [
            "Cozinhe o macarrão em água salgada; escorra.",
            "Em panela, misture caldo, leite, amido, sal, gemas, metade da manteiga, pimenta e 2/5 do queijo ralado até engrossar. Junte o frango e o queijo fundido; misture à massa e despeje em pirex fundo.",
            "Esmague as batatas fritas com o restante do queijo; cubra e salpique o restante da manteiga. Asse até dourar; sirva bem quente.",
        ],
    },
    {
        "cat": "frutos-do-mar",
        "slug": "ravioli-a-camaresca",
        "title": "Ravioli à camaresca",
        "meta": None,
        "ingredients": [
            "200 g de ravioli recheado com ricota",
            "1 colher (sopa) de manteiga",
            "150 g de parmesão ralado",
            "150 g de requeijão cremoso",
            "400 ml de creme de leite fresco",
            "150 g de champignon",
            "4 camarões grandes",
            "Sal",
        ],
        "steps": [
            "Cozinhe o ravioli em água e sal; reserve.",
            "Derreta a manteiga com champignon e creme de leite; ferva. Ajuste o ponto com o parmesão.",
            "Junte o ravioli, passe a um refratário, cubra com os camarões e o requeijão e gratinize.",
        ],
    },
    {
        "cat": "massas",
        "slug": "lasanha-aos-quatro-queijos",
        "title": "Lasanha aos quatro queijos",
        "meta": None,
        "ingredients": [
            "1 xícara (chá) de leite",
            "4 latas de creme de leite com soro",
            "100 g de parmesão ralado",
            "2 copos de requeijão cremoso",
            "1 kg de massa de lasanha",
            "500 g de mussarela",
            "200 g de Catupiry",
            "400 g de ricota",
        ],
        "steps": [
            "Bata creme de leite, requeijão, leite, ricota e Catupiry; reserve. Rale a mussarela.",
            "No pirex, coloque um pouco de creme, massa, creme, mussarela; repita até preencher, finalizando com creme e parmesão.",
            "Asse a 180 °C até corar ou começar a ferver.",
        ],
        "notes": "A receita original não especifica se a massa é precocinada; use conforme a embalagem.",
    },
    # Sadia promotional
    {
        "cat": "aves",
        "slug": "fiesta-com-batatas-e-creme-azedo",
        "title": "Fiesta com batatas e creme azedo",
        "meta": [("Rendimento", "8 a 10 porções"), ("Tempo", "25 min prep + assado")],
        "ingredients": [
            "1 Fiesta Temperada Sadia (~4 kg)",
            "1 colher (sopa) de margarina",
            "Guarnição: 2½ xícaras (chá) de óleo (300 ml), 1 kg de batatas em cubos médios, sal, folhas de 3 ramos de manjericão",
            "Creme azedo: 2 xícaras (chá) de creme de leite fresco (400 ml), suco de 1 limão, sal e pimenta moída",
        ],
        "steps": [
            "Descongele a ave na embalagem na parte baixa da geladeira ~18 h.",
            "Retire a embalagem e o saquinho de miúdos. Unte com margarina, cubra com papel-alumínio e asse a 200 °C por 40 minutos. Retire o alumínio, regue com o caldo e continue até o termômetro saltar (~1 h 30 após retirar o alumínio).",
            "Frite as batatas no óleo quente; tempere. Frite o manjericão no óleo ainda quente.",
            "Bata o creme com limão, sal e pimenta até chantilly. Sirva as batatas ao redor com o creme e o manjericão por cima.",
        ],
        "notes": "Receita promocional Sadia/Qualy. Pode adaptar a qualquer ave temperada grande (~4 kg).",
    },
    {
        "cat": "aves",
        "slug": "peru-com-peras-e-arroz-de-nozes",
        "title": "Peru com pêras e arroz de nozes e gorgonzola",
        "meta": [("Rendimento", "11 porções"), ("Tempo", "2 h 30")],
        "ingredients": [
            "1 peru temperado congelado (~4,5 kg)",
            "3 colheres (sopa) de margarina (+ 2 colheres para as pêras e 2 para o arroz)",
            "3 pêras firmes cortadas no sentido do comprimento em 8 pedaços",
            "1 colher (sopa) de açúcar",
            "½ xícara (chá) de cebola picada",
            "2½ xícaras (chá) de arroz",
            "Sal",
            "2 xícaras (chá) de creme de leite fresco",
            "1 xícara (chá) de nozes grosseiramente picadas",
            "1 xícara (chá) de gorgonzola picado",
        ],
        "steps": [
            "Descongele o peru na embalagem na geladeira ~42 h. Pré-aqueça o forno a 200 °C.",
            "Prenda as asas e as coxas; cubra com alumínio e asse ~1 h. Retire o alumínio, pincele com margarina e continue até o termômetro saltar (~1 h 30), pincelando a cada 40 min. Descanse 5–10 min.",
            "Pêras: refogue na margarina com o açúcar. Arroz: refogue a cebola, junte o arroz, 3 xícaras de água quente e o creme; cozinhe semi-tampado. Finalize com pêras, nozes e gorgonzola. Sirva ao redor do peru.",
        ],
    },
    {
        "cat": "carnes",
        "slug": "tender-picante",
        "title": "Tender picante",
        "meta": [("Rendimento", "10 porções"), ("Tempo", "30 min prep + ~1 h 15 forno")],
        "ingredients": [
            "1 tender semi-desossado (~3 kg)",
            "½ garrafa de vinho branco seco (~400 ml)",
            "1 xícara (chá) de açúcar mascavo",
            "4 colheres (sopa) de mostarda",
            "3 cebolas grandes em gomos",
            "4 colheres (sopa) de catchup",
            "1 pimenta dedo-de-moça picada",
            "½ talo de cebolinha picada",
        ],
        "steps": [
            "Coloque o tender em assadeira funda, regue com o vinho e faça cortes na superfície.",
            "Espalhe a pasta de açúcar mascavo com mostarda; arrume as cebolas ao redor; cubra com alumínio e asse a 200 °C ~1 h.",
            "Retire o alumínio, regue e doure mais 15 minutos. Misture o caldo da assadeira com catchup, pimenta e cebolinha. Sirva com espinafre na manteiga.",
        ],
        "notes": "Acompanhamento de espinafre citado no final; não há lista detalhada — refogue espinafre em manteiga com sal.",
    },
    {
        "cat": "carnes",
        "slug": "pernil-recheado-com-canjiquinha",
        "title": "Pernil recheado com canjiquinha",
        "meta": [("Rendimento", "6 porções"), ("Tempo", "1 h 40")],
        "ingredients": [
            "1 pernil recheado com purê de maçã (tipo Sadia) ou similar",
            "2 colheres (sopa) de margarina (+ ½ xícara derretida para a berinjela)",
            "1½ xícara (chá) de vinho branco",
            "1 kg de berinjela em cubos médios",
            "4 xícaras (chá) de caldo de legumes",
            "2 xícaras (chá) de canjiquinha",
            "1 xícara (chá) de cebola roxa em tiras",
            "2 xícaras (chá) de tomate sem pele/sementes em tiras",
            "1 xícara (chá) de cebolinha picada",
            "½ xícara (chá) de manjericão",
            "½ xícara (chá) de azeite",
            "Suco de 1 limão, sal e pimenta",
            "Galhinhos de manjericão para enfeitar",
        ],
        "steps": [
            "Descongele o pernil na geladeira ~18 h. Asse a berinjela com margarina a 200 °C por ~1 h.",
            "Asse o pernil com ½ xícara de vinho coberto ~45 min; pincele com margarina e continue ~50 min, regando com o vinho restante se secar.",
            "Torre a canjiquinha; cozinhe no caldo fervente até secar. Misture berinjela, cebola, tomate, cebolinha, manjericão, azeite, limão, sal e pimenta. Sirva ao redor do pernil.",
        ],
    },
    # AnaMaria / Nestlé / magazine pasta & fish
    {
        "cat": "frutos-do-mar",
        "slug": "talharim-com-vongole",
        "title": "Talharim com vôngole",
        "meta": [("Rendimento", "5 porções")],
        "ingredients": [
            "1 kg de vôngole",
            "1 pacote de macarrão tipo talharim (500 g)",
            "6 colheres (sopa) de azeite",
            "3 dentes de alho",
            "4 colheres (sopa) de salsinha picada",
            "Sal e pimenta a gosto",
        ],
        "steps": [
            "Escove e lave bem os vôngoles.",
            "Aqueça o azeite, doure os alhos e retire-os. Junte vôngole, salsinha, sal e pimenta; tampe em fogo baixo até abrir as conchas.",
            "Cozinhe o macarrão al dente, escorra, regue com o líquido do vôngole, enfeite com as conchas e sirva.",
        ],
    },
    {
        "cat": "massas",
        "slug": "macarrao-ao-creme",
        "title": "Macarrão ao creme",
        "meta": [("Rendimento", "6 porções")],
        "ingredients": [
            "1 pacote de macarrão (500 g) de sua preferência",
            "1 lata de creme de leite",
            "4 colheres (sopa) de leite",
            "1 xícara (chá) de ervilha",
            "1 xícara (chá) de presunto em cubinhos",
            "1 colher (sopa) de manteiga",
            "Sal e pimenta a gosto",
        ],
        "steps": [
            "Cozinhe o macarrão em água salgada; escorra.",
            "Aqueça a manteiga, junte leite e creme de leite; tempere. Acrescente ervilha e presunto. Quando começar a ferver, retire do fogo e sirva com o macarrão.",
        ],
        "notes": "Receita do leitor (Eliana Cabral, Nova Iguaçu/RJ).",
    },
    {
        "cat": "frutos-do-mar",
        "slug": "peixe-a-thermidor",
        "title": "Peixe à Thermidor",
        "meta": [("Rendimento", "6 porções")],
        "ingredients": [
            "700 g de filé de linguado (~6 filés)",
            "Suco de 2 limões",
            "Sal e pimenta-do-reino",
            "6 ramos de coentro picado fino",
            "1 xícara (chá) de farinha de trigo",
            "2 colheres (sopa) de manteiga (para fritar)",
            "Molho: 1½ colher (sopa) de manteiga, 1½ colher (sopa) de farinha, 1 xícara (chá) de leite, 6 colheres (sopa) de parmesão ralado, sal, pimenta, noz-moscada, 1 lata de creme de leite",
        ],
        "steps": [
            "Tempere os filés com limão, sal, pimenta e coentro; descanse ~20 min. Empane leve na farinha e frite na manteiga; arrume em refratário.",
            "Molho: doure a farinha na manteiga, acrescente o leite aos poucos; tempere, junte metade do queijo e o creme de leite.",
            "Cubra o peixe, polvilhe o restante do queijo e gratine ~10 minutos.",
        ],
        "notes": "Fonte Nestlé. Linguado deve ter carne firme e cheiro característico, não forte.",
    },
    {
        "cat": "massas",
        "slug": "espaguete-aos-quatro-queijos",
        "title": "Espaguete aos quatro queijos",
        "meta": [("Rendimento", "5 porções")],
        "ingredients": [
            "1 pacote de espaguete (500 g) cozido",
            "4 xícaras (chá) de leite",
            "4 colheres (sopa) de farinha de trigo",
            "1 colher (sopa) de margarina",
            "1 colher (sopa) de gorgonzola picado",
            "1 colher (sopa) de queijo prato picado",
            "1 colher (sopa) de queijo ralado",
            "1 colher (sopa) de mussarela picada ou Catupiry",
            "Sal e noz-moscada a gosto",
        ],
        "steps": [
            "Aqueça a margarina; junte o leite misturado com a farinha; tempere e mexa até engrossar.",
            "Bata os queijos com metade do molho no liquidificador; devolva à panela até creme homogêneo. Sirva com o espaguete quente.",
        ],
        "notes": "Chef Natanael José Catarino.",
    },
    {
        "cat": "frutos-do-mar",
        "slug": "bucatini-com-atum-iogurte-e-pimenta",
        "title": "Bucatini com atum, iogurte e pimenta",
        "meta": [("Rendimento", "4 porções")],
        "ingredients": [
            "1 pacote de bucatini (500 g)",
            "1 lata de atum",
            "1 xícara (chá) de iogurte natural",
            "3 colheres (sopa) de azeite",
            "1 xícara (café) de pimenta verde",
            "1 cebola picada",
            "Sal a gosto",
        ],
        "steps": [
            "Cozinhe o macarrão; escorra.",
            "Refogue a cebola no azeite; junte atum e pimenta por 2 minutos; acrescente o iogurte, o sal e a massa. Sirva.",
        ],
        "notes": "Chef Maria Montanarini (Casa Europa, SP).",
    },
    {
        "cat": "aves",
        "slug": "gratinado-de-frango",
        "title": "Gratinado de frango",
        "meta": [("Rendimento", "4 porções")],
        "ingredients": [
            "4 colheres (sopa) de óleo",
            "½ kg de peito de frango em tirinhas",
            "2 alhos-porós em fatias finas",
            "1 colher (sopa) de tempero tipo Fondor",
            "2 colheres (sopa) de farinha de trigo",
            "2 xícaras (chá) de leite",
            "1 lata de creme de leite",
            "½ xícara (chá) de parmesão ralado",
        ],
        "steps": [
            "Doure o frango no óleo; junte os alhos-porós e o tempero até amolecer.",
            "Polvilhe a farinha e acrescente o leite aos poucos até creme; junte o creme de leite sem ferver.",
            "Despeje em refratário, polvilhe o queijo e asse a 220 °C ~15 minutos. Sirva na hora.",
        ],
    },
    {
        "cat": "frutos-do-mar",
        "slug": "ju-har-kow",
        "title": "Ju Har Kow (camarão empanado)",
        "meta": None,
        "ingredients": [
            "½ kg de camarão cru limpo",
            "1 colher (chá) de glutamato monossódico",
            "2 colheres (chá) de suco de limão",
            "Massa: 2 ovos, 4 colheres (sopa) de farinha, ½ colher (chá) de sal, 1 pitada de pimenta",
            "Molho: 1 colher (sopa) de shoyu, 1 pitada de gengibre em pó, 2 colheres (sopa) de catchup",
            "Óleo para fritar",
        ],
        "steps": [
            "Tempere o camarão com glutamato e limão. Bata a massa, empane e frite ~5 minutos até dourar.",
            "Misture o molho e sirva à parte.",
        ],
        "notes": "Receita chinesa (A Cozinha Brasileira). Glutamato pode ser omitido se preferir.",
    },
    {
        "cat": "carnes",
        "slug": "goo-low-yuke",
        "title": "Goo Low Yuke (porco agridoce)",
        "meta": None,
        "ingredients": [
            "½ xícara de farinha de trigo",
            "½ colher (chá) de glutamato + ½ colher (chá) de sal",
            "½ kg de lombo de porco em pedaços de 2 cm",
            "1 ovo batido",
            "Molho: ½ xícara de açúcar, ½ xícara de vinagre, ⅓ xícara de suco de abacaxi, ¼ xícara de catchup, 1 colher (chá) de shoyu",
            "2 colheres (sopa) de maisena + 2 colheres (sopa) de água",
            "1 xícara de abacaxi em pedaços escorrido",
            "1 pimentão verde em pedaços de 1 cm",
            "Óleo para fritar",
        ],
        "steps": [
            "Passe a carne no ovo e na farinha temperada; frite 6–8 min até dourar.",
            "Ferva o molho; engrosse com a maisena. Junte carne, abacaxi e pimentão; aqueça 5 minutos mexendo. Sirva com arroz.",
        ],
    },
    {
        "cat": "frutos-do-mar",
        "slug": "tempura-de-camarao",
        "title": "Tempura de camarão (Ebi no Tempura)",
        "meta": [("Rendimento", "20 a 30 unidades")],
        "ingredients": [
            "½ kg de camarões",
            "1 colher (chá) de sal",
            "½ colher (chá) de glutamato monossódico",
            "1 colher (sopa) de saquê",
            "Koromo: 1 ovo, 1 xícara de água bem gelada, 2 xícaras de farinha de trigo",
            "Óleo para fritar",
        ],
        "steps": [
            "Limpe os camarões deixando cabeça e cauda; abra pelo dorso. Tempere com sal, glutamato e saquê; faça pequenos cortes transversais.",
            "Aqueça o óleo. Misture ovo e água gelada; junte a farinha misturando de leve, sem bater. Empane e frite.",
        ],
        "notes": "Mantenha a massa gelada (cubos de gelo em saco na tigela). Fonte: Revista Nihon Ryoori / Cozinha Japonesa.",
    },
    # S.C.A. gourmet
    {
        "cat": "outros",
        "slug": "escalope-de-foie-gras-com-maca-verde",
        "title": "Escalope de foie gras com maçã verde glaçada",
        "meta": [("Rendimento", "4 porções")],
        "ingredients": [
            "320 g de escalope de foie gras",
            "Sal e pimenta",
            "50 g de manteiga sem sal + 50 g de açúcar + 1 maçã verde em fatias finas",
            "100 g de manteiga trufada, 50 ml de aceto balsâmico, 30 g de açúcar (molho)",
            "1 alho-poró em tiras finas, 500 ml de óleo de soja",
            "30 g de pistache triturado",
        ],
        "steps": [
            "Grelhe o foie gras temperado ~3 minutos de cada lado.",
            "Glaceie a maçã na manteiga com açúcar. Bata a manteiga trufada com balsâmico e açúcar; reduza e tempere.",
            "Frite o alho-poró. Monte com vazador: maçã + escalope; espalhe molho, pistache e alho-poró crocante.",
        ],
    },
    {
        "cat": "frutos-do-mar",
        "slug": "hadoque-defumado-com-maca",
        "title": "Hadoque defumado com maçã ao vinagrete de menta",
        "meta": [("Rendimento", "4 porções")],
        "ingredients": [
            "350 g de hadoque defumado fatiado",
            "500 g de maçãs verdes descascadas em fatias finas",
            "50 g de alface lisa em tiras",
            "4 talos de cebolinha",
            "Molho: 100 ml de iogurte integral + 50 ml de mel",
            "Vinagrete: 80 g de geleia de menta, 30 ml de vinagre de maçã, 40 ml de azeite",
        ],
        "steps": [
            "Misture iogurte e mel; junte as maçãs. Prepare o vinagrete.",
            "Branqueie as cebolinhas e amarre as fatias de hadoque em formato de rosas.",
            "No vazador, monte maçã + hadoque; arrume alface ao redor e regue com o vinagrete.",
        ],
    },
    {
        "cat": "frutos-do-mar",
        "slug": "pera-com-truta-defumada",
        "title": "Pêra com truta defumada ao molho de iogurte e mel",
        "meta": [("Rendimento", "4 porções")],
        "ingredients": [
            "250 g de filés de truta defumada",
            "100 ml de iogurte integral",
            "50 ml de mel",
            "250 g de pêras em bastõezinhos",
            "Mix de folhas: alface lisa, crespa, frisée e radicchio (~80 g no total)",
            "50 g de tomates-cereja cortados ao meio",
        ],
        "steps": [
            "Misture iogurte e mel; junte as pêras. Corte a truta em pedaços.",
            "Com vazador, molde as pêras, arrume as folhas ao redor, coloque a truta por cima, retire o vazador e decore com tomates.",
        ],
    },
    {
        "cat": "frutos-do-mar",
        "slug": "terrine-de-camarao-e-palmito",
        "title": "Terrine de camarão e palmito",
        "meta": [("Rendimento", "4 porções")],
        "ingredients": [
            "100 g de champignons; 1 folha de radicchio; 1 folha de alface frisée",
            "Palmito: ¼ cebola, 1 alho, 30 ml de azeite, 200 g de palmitos picados, 100 ml de creme de leite fresco, sal",
            "Camarão: ¼ cebola, 1 alho, 30 ml de azeite, 200 g de camarões médios partidos ao meio, 30 ml de vinho branco, sal",
            "Fundo: 1 kg de ossos de frango, 1 l de água, 1 cebola, ¼ salsão, ½ cenoura, 200 ml de vinho branco, sal, 60 g de gelatina sem sabor hidratada em ½ l de água",
        ],
        "steps": [
            "Refogue palmito e camarão separadamente conforme as listas; reserve.",
            "Cozinhe o fundo ~2 h; coe, junte gelatina hidratada, vinho e sal.",
            "Em terrine forrada com filme: champignons + fundo (½ h); palmito + fundo (½ h); camarão + restante do fundo (3 h). Fatias de 1 cm com folhas ao lado.",
        ],
    },
    {
        "cat": "frutos-do-mar",
        "slug": "vol-au-vent-de-vieiras",
        "title": "Vol-au-vent de vieiras flambadas ao Noilly Prat",
        "meta": [("Rendimento", "4 porções")],
        "ingredients": [
            "4 corações de alcachofra em quartos",
            "80 ml de azeite",
            "½ cebola média + 4 dentes de alho picados",
            "60 g de manteiga sem sal",
            "450 g de vieiras limpas",
            "60 ml de Noilly Prat (ou vermute seco)",
            "50 g de tomate seco em metades",
            "Sal e pimenta-branca",
            "80 ml de creme de leite fresco",
            "4 vol-au-vents (8 cm)",
            "50 g de parmesão ralado",
            "4 ramos de salsa crespa",
        ],
        "steps": [
            "Refogue metade da cebola/alho no azeite com a alcachofra ~4 min; reserve.",
            "Salteie as vieiras na manteiga e no restante do azeite/cebola/alho ~5 min; flambé com Noilly Prat. Junte alcachofra, tomate seco, temperos e creme ~3 min.",
            "Recheie os vol-au-vents, polvilhe queijo, gratine e sirva com salsa.",
        ],
        "notes": "Noilly Prat pode ser substituído por vermute seco.",
    },
    {
        "cat": "frutos-do-mar",
        "slug": "atum-fresco-grelhado-ao-curry",
        "title": "Atum fresco grelhado ao molho de curry e leite de coco",
        "meta": [("Rendimento", "4 porções")],
        "ingredients": [
            "680 g de filé de atum fresco temperado com sal e pimenta",
            "30 ml de azeite",
            "4 folhas de cebolinha picadas",
            "4 dentes de alho e ½ cebola média picados",
            "20 g de tomate maduro sem pele e sementes",
            "Curry a gosto",
            "70 ml de vinho branco seco",
            "100 ml de leite de coco",
            "Sal e pimenta-branca",
            "60 g de shimeji fresco grelhado",
        ],
        "steps": [
            "Frite o atum no azeite em fogo alto, pressionando levemente; baixe o fogo ~7 minutos; reserve.",
            "No mesmo fogão, refogue alho, cebola e tomate; junte curry, vinho e leite de coco 4–5 minutos; tempere.",
            "Sirva o atum sobre o shimeji com o molho ao redor e cebolinha.",
        ],
    },
    {
        "cat": "carnes",
        "slug": "ossobuco-de-vitela-com-risotto-de-rucula",
        "title": "Ossobuco de vitela com risotto de rúcula",
        "meta": [("Rendimento", "4 porções")],
        "ingredients": [
            "1 kg de ossobuco de vitela",
            "80 ml de vinho branco, 3 folhas de louro, sal, pimenta-branca",
            "80 ml de azeite; 4 dentes de alho; 1 cebola; 1 cenoura; 400 g de bacon defumado; ½ alho-poró",
            "2 l de caldo de carne; 200 g de purê de tomate; 100 g de champignon frito; 200 g de echalotas fritas",
            "Caldo: 300 g de músculo, sal, ½ cebola, 1 cenoura, 1 alho, 1 talo de salsão, 1 tomate, 1 batata",
            "Risotto: 400 g de arroz arbóreo pré-cozido, 1 maço de rúcula, 30 g de manteiga, 100 g de parmesão",
        ],
        "steps": [
            "Tempere o ossobuco. Refogue cebola, alho e cenoura; junte bacon e alho-poró. Cozinhe o ossobuco no caldo na pressão ~45 min. Reserve ¼ do líquido coado; junte o purê de tomate à carne.",
            "Prepare o caldo (~2 h) e use coado. Aqueça o arroz no líquido do ossobuco ~4 min; finalize com manteiga e rúcula.",
            "Sirva risotto com parmesão, ossobuco, champignon e echalotas.",
        ],
        "notes": "Dica: passe a carne na farinha e doure antes para mais sabor.",
    },
    {
        "cat": "carnes",
        "slug": "picanha-de-porco-ao-molho-de-tamarindo",
        "title": "Picanha de porco ao molho de tamarindo",
        "meta": [("Rendimento", "4 porções")],
        "ingredients": [
            "4 filés de picanha de porco",
            "Sal, pimenta-branca, ½ dos alhos, 1 limão, 80 ml de azeite",
            "400 g de batata pré-cozida; 2 cebolas médias; 4 alhos; 30 g de manteiga; salsa",
            "Molho: 30 g de tamarindos frescos, 10 ml de azeite, 100 ml de água, sal e pimenta",
            "Rodelas de limão e tomilho para decorar",
        ],
        "steps": [
            "Tempere e grelhe os filés até dourar.",
            "Rale a batata, tempere e frite em porções com manteiga e metade da cebola (estilo rösti).",
            "Cozinhe o tamarindo 5 min, retire sementes; refine com cebola, alho, água, sal e pimenta ~10 min; passe na peneira. Monte batata + picanha + molho.",
        ],
        "notes": "Tamarindo fresco pode ser trocado por pasta de tamarindo.",
    },
    {
        "cat": "frutos-do-mar",
        "slug": "camaraoes-com-vodca-ao-molho-de-salsa",
        "title": "Camarões com vodca ao molho de salsa",
        "meta": [("Rendimento", "4 porções")],
        "ingredients": [
            "200 g de arroz arbóreo cozido al dente",
            "24 camarões grandes temperados",
            "150 ml de azeite",
            "150 ml de vodca",
            "1 cebola picada",
            "350 ml de champagne brut",
            "200 ml de molho bechamel",
            "150 g de salsa bem picada",
            "200 ml de creme de leite fresco",
            "100 g de champignon de Paris",
            "60 g de gergelim ou amêndoas torradas",
        ],
        "steps": [
            "Doure a cebola no azeite; junte os camarões e flambé com a vodca. Cubra com champagne e cozinhe rápido.",
            "Acrescente bechamel, salsa e creme de leite até encorpar. Retire os camarões e faça risotto do arroz no molho restante com champignon e amêndoas. Sirva os camarões sobre o arroz.",
        ],
    },
    {
        "cat": "frutos-do-mar",
        "slug": "truta-grande-hotel-ao-molho-de-pinhao",
        "title": "Truta Grande Hotel ao molho de pinhão",
        "meta": [("Rendimento", "4 porções")],
        "ingredients": [
            "4 filés de truta com pele",
            "Sal, pimenta-branca, 30 ml de suco de limão, 100 ml de óleo",
            "200 g de manteiga sem sal; ½ cebola média",
            "100 g de pinhões cozidos, laminados e torrados",
            "200 ml de vinho branco seco; 200 ml de caldo de peixe; 200 ml de creme de leite fresco",
            "4 ramos de salsa picada",
            "200 g de cenoura + 200 g de batata + 200 g de brócolis ninja (cubos/cozidinhos no vapor)",
        ],
        "steps": [
            "Tempere e grelhe a truta no óleo; reserve.",
            "Na mesma frigideira, doure a cebola em parte da manteiga; junte pinhões, vinho, caldo, creme e salsa; ajuste o tempero.",
            "Salteie os legumes no restante da manteiga. Sirva a truta com legumes e molho.",
        ],
        "notes": "Variação tipicamente de Campos do Jordão usando pinhão no lugar de amêndoa.",
    },
    {
        "cat": "carnes",
        "slug": "avestruz-a-la-bourguignonne",
        "title": "Avestruz à la bourguignonne",
        "meta": [("Rendimento", "4 porções")],
        "ingredients": [
            "1 kg de filé de avestruz em cubos",
            "1 cebola média, 2 dentes de alho, 1 cenoura",
            "Sal e pimenta-branca",
            "120 g de bacon; 240 g de champignon; 240 g de cebolinhas brancas em conserva",
            "4 folhas de louro; 450 ml de vinho tinto seco; 500 ml de caldo de frango; 20 ml de purê de tomate",
            "40 g de farinha; 600 ml de óleo; 30 g de manteiga; 4 ramos de tomilho; 12 g de salsa",
        ],
        "steps": [
            "Tempere a carne com metade da cebola, alho, cenoura, sal e pimenta.",
            "Frite o bacon; refogue o restante dos aromáticos com champignon, cebolinhas, louro, vinho, caldo e purê ~10 min.",
            "Passe a carne na farinha, doure e junte ao molho ~20 min; finalize com manteiga. Sirva com tomilho e salsa (acompanhe arroz selvagem).",
        ],
    },
    {
        "cat": "carnes",
        "slug": "costeletas-de-cordeiro-com-menta",
        "title": "Costeletas de cordeiro com menta fresca",
        "meta": [("Rendimento", "4 porções")],
        "ingredients": [
            "800 g de costeletas de cordeiro",
            "Sal e pimenta-branca",
            "4 ramos de hortelã bem picada",
            "200 ml de azeite",
            "Batata dauphinoise: ½ kg de batatas em chips, sal, pimenta, ½ noz-moscada, ½ l de creme de leite, 5 ovos batidos, 50 g de parmesão",
        ],
        "steps": [
            "Tempere as costeletas e frite no azeite com parte da hortelã.",
            "Tempere as batatas; misture creme e ovos; despeje em refratário com queijo e asse a 180 °C ~20 min.",
            "Sirva as costeletas com a batata e o restante da hortelã.",
        ],
    },
    # AnaMaria tarts Sept 2008
    {
        "cat": "salgados",
        "slug": "torta-de-bacon-e-minicebola",
        "title": "Torta de bacon e minicebola",
        "meta": [("Rendimento", "12 porções"), ("Tempo", "40 min")],
        "ingredients": [
            "Massa: ¼ tablete de fermento biológico fresco, 1 colher (chá) de açúcar, 2 xícaras (chá) de farinha, 1 ovo, 1 colher (sopa) de margarina, 60 ml de água",
            "Recheio: 2 colheres (sopa) de azeite, 2 colheres (sopa) de margarina, 500 g de minicebolas, 2 potes de cream cheese (300 g), 100 g de bacon fatiado, orégano, sal e pimenta",
        ],
        "steps": [
            "Dissolva o fermento no açúcar; misture farinha, ovo, margarina e água; deixe dobrar. Abra e forre forma (~24 cm); descanse.",
            "Refogue as cebolas no azeite/margarina; esfrie. Espalhe cream cheese, cebolas e bacon; polvilhe orégano. Asse a 200 °C por 40 minutos.",
        ],
        "notes": "Para descascar minicebolas: 3 minutos em água fervente. Fonte: AnaMaria 26/09/2008.",
    },
    {
        "cat": "salgados",
        "slug": "torta-de-catalonia",
        "title": "Torta de catalônia",
        "meta": [("Rendimento", "8 porções"), ("Tempo", "40 min")],
        "ingredients": [
            "2 maços de catalônia",
            "100 g de bacon picado",
            "Sal e pimenta vermelha picada a gosto",
            "300 g de ricota",
            "500 g de massa folhada",
        ],
        "steps": [
            "Pré-aqueça a 200 °C. Escalde a catalônia, escorra, esprema e pique. Doure o bacon, junte a folha e tempere; esfrie e misture a ricota.",
            "Abra a massa (~3 mm), forre forma de 26 cm, recheie e faça grade. Asse 50 minutos até dourar.",
        ],
        "notes": "Catalônia é amarga; troque por escarola ou espinafre se preferir sabor mais suave.",
    },
    {
        "cat": "salgados",
        "slug": "folhado-de-linguica-e-ricota",
        "title": "Folhado de linguiça e ricota",
        "meta": [("Rendimento", "8 porções"), ("Tempo", "25 min")],
        "ingredients": [
            "400 g de massa folhada",
            "1 colher (sopa) de azeite",
            "1 cebola picada",
            "400 g de linguiça fresca",
            "100 ml de vinho branco seco",
            "2 tomates sem pele e sementes picados",
            "250 g de ricota esfarelada",
            "1 clara; 1 gema; 2 colheres (sopa) de leite",
            "Salsa, sal e pimenta",
        ],
        "steps": [
            "Refogue cebola e linguiça 5 minutos; evapore o vinho; cozinhe o tomate 10 minutos; misture a ricota e esfrie.",
            "Espalhe na massa, feche com clara nas bordas; pincele gema com leite. Asse a 220 °C por 30 minutos.",
        ],
    },
    {
        "cat": "salgados",
        "slug": "torta-de-cebola",
        "title": "Torta de cebola",
        "meta": [("Rendimento", "8 porções"), ("Tempo", "50 min")],
        "ingredients": [
            "Massa: 3 xícaras (chá) de farinha, 2 ovos, 2 colheres (sopa) de margarina, sal",
            "Recheio: 5 cebolas fatiadas, 2 colheres (sopa) de margarina, 2 cubinhos de caldo de carne, 2 ovos, 1 xícara (chá) de leite, 4 colheres (sopa) de farinha, 2 colheres (sopa) de queijo ralado",
        ],
        "steps": [
            "Massa: misture, faça bola, embrulhe e gele.",
            "Recheio: frite a cebola; junte caldo, ovos, leite e farinha até desgrudar; esfrie.",
            "Abra a massa, espalhe o recheio, polvilhe queijo e asse em forno médio até dourar. Decore com cebola frita escura se quiser.",
        ],
    },
    {
        "cat": "salgados",
        "slug": "torta-maravilha-de-frango-e-presunto",
        "title": "Torta maravilha de frango e presunto",
        "meta": [("Rendimento", "8 porções"), ("Tempo", "30 min")],
        "ingredients": [
            "Massa: 2 xícaras (chá) de farinha, ½ xícara (chá) de manteiga, 1 ovo, 1 colher (chá) de sal, 1 colher (café) de fermento",
            "Recheio: 2 colheres (sopa) de azeite, 1 cebola roxa, 1 dente de alho, 500 g de peito de frango em cubos, 80 g de presunto em cubos, sal, pimenta, 1 colher (sopa) de conhaque, 150 ml de creme de leite fresco, 2 ovos batidos, 40 g de queijo ralado, salsa, 1 gema para pincelar",
        ],
        "steps": [
            "Misture a massa; descanse 15 min. Forre forma 22 cm desmontável.",
            "Refogue cebola, alho, frango e presunto; flambé com conhaque; junte creme 5 min. Esfrie um pouco; junte ovos, queijo e salsa.",
            "Recheie, cubra com massa, pincele gema e asse a 180 °C por 50 minutos.",
        ],
        "notes": "Presunto pode ser trocado por peito de peru.",
    },
    {
        "cat": "salgados",
        "slug": "torta-de-escarola-com-requeijao",
        "title": "Torta de escarola com requeijão",
        "meta": [("Rendimento", "10 porções"), ("Tempo", "45 min")],
        "ingredients": [
            "Massa: 2 xícaras (chá) de leite, ¾ xícara (chá) de óleo, 2 xícaras (chá) de farinha, 1 colher (sopa) de fermento, 1 colher (chá) de sal, 2 colheres (sopa) de queijo ralado",
            "Recheio: 2 colheres (sopa) de azeite, 1 cebola pequena, 1 dente de alho, 1 pimentão vermelho, 1 maço de escarola, sal e pimenta",
            "Cobertura: 1 copo de requeijão cremoso (250 g), 3 colheres (sopa) de parmesão",
        ],
        "steps": [
            "Bata a massa no liquidificador. Refogue o recheio ~3 minutos.",
            "Em forma 22 cm untada, coloque ¾ da massa, o recheio, a massa nas bordas, o requeijão no centro e o parmesão. Asse a 200 °C por 30 minutos.",
        ],
        "notes": "Escarola pode ser trocada por acelga.",
    },
    {
        "cat": "salgados",
        "slug": "quiche-de-tomate-seco-e-peito-de-peru",
        "title": "Quiche de tomate seco e peito de peru",
        "meta": [("Rendimento", "8 porções"), ("Tempo", "30 min")],
        "ingredients": [
            "Massa: 2 xícaras (chá) de farinha, 1 ovo, 2 colheres (sopa) de água fria, 150 g de manteiga, sal",
            "Recheio: 1 colher (sopa) de azeite, 200 g de peito de peru em cubos, 100 g de tomate seco, 4 ovos, noz-moscada, 200 ml de creme de leite fresco, ½ xícara (chá) de parmesão, sal e pimenta",
        ],
        "steps": [
            "Misture a massa, gele 30 min e forre quicheira 22 cm.",
            "Doure o peru; espalhe com o tomate seco. Bata ovos, noz-moscada, creme, parmesão, sal e pimenta; despeje e asse 35 minutos.",
        ],
        "notes": "Creme fresco pode ser de lata ou caixinha.",
    },
    {
        "cat": "salgados",
        "slug": "torta-folhada-de-queijo",
        "title": "Torta folhada de queijo",
        "meta": [("Rendimento", "8 porções"), ("Tempo", "35 min")],
        "ingredients": [
            "3 xícaras (chá) de sobras de arroz",
            "100 g de mussarela ralada",
            "1 linguiça-calabresa defumada",
            "300 g de massa folhada laminada congelada",
            "2 colheres (sopa) de farinha de rosca",
            "Manjericão para decorar",
        ],
        "steps": [
            "Processe o arroz até pasta; junte mussarela e metade da calabresa picada.",
            "Em forma 25 cm de aro removível, forre fundo e laterais com a massa; polvilhe farinha de rosca; despeje o recheio; decore com rodelas de calabresa. Gele 20 min e asse em forno médio ~40 min. Decore com manjericão (opcional: amarre com ráfia).",
        ],
        "notes": "Boa opção de lanche; pode ser feita na véspera.",
    },
    {
        "cat": "salgados",
        "slug": "tortinhas-de-mussarela-de-bufala",
        "title": "Tortinhas de mussarela de búfala e tomate",
        "meta": [("Rendimento", "16 unidades")],
        "ingredients": [
            "2¼ xícaras (chá) de farinha de trigo",
            "140 g de manteiga",
            "1 ovo",
            "2 gemas",
            "200 g de mussarela de búfala",
            "16 tomates-cereja",
            "Azeite, sal e salsa picada a gosto",
        ],
        "steps": [
            "Misture farinha, manteiga, ovo e gemas até massa homogênea; forre forminhas individuais.",
            "Disponha pedaços de mussarela e 1 tomate-cereja por tortinha; regue azeite, sal e salsa.",
            "Asse em forno médio preaquecido (~180–200 °C) até a massa dourar (~20–25 min).",
        ],
        "notes": "Preparo e temperatura inferidos: a página do AnaMaria veio cortada; ingredientes literais da foto-irmã.",
    },
    {
        "cat": "salgados",
        "slug": "torta-pizza",
        "title": "Torta-pizza",
        "meta": [("Rendimento", "6 porções"), ("Tempo", "45 min")],
        "ingredients": [
            "3 xícaras (chá) de farinha de trigo",
            "125 ml de água",
            "Sal a gosto",
            "150 ml de azeite",
            "300 g de cream cheese",
            "200 g de tomate pelado escorrido",
            "100 g de azeitonas pretas sem caroço",
            "Sal grosso e orégano a gosto",
        ],
        "steps": [
            "Pré-aqueça a 200 °C. Misture farinha, água, sal e metade do azeite; divida e abra em duas partes.",
            "Forre assadeira untada com uma parte; espalhe cream cheese, tomate e azeitonas; regue o restante do azeite e polvilhe orégano. Cubra, feche laterais, polvilhe sal grosso e asse ~50 minutos.",
        ],
        "notes": "Cream cheese pode ser trocado por fatias de queijo branco.",
    },
    {
        "cat": "frutos-do-mar",
        "slug": "torta-de-atum-e-batata",
        "title": "Torta de atum e batata",
        "meta": [("Rendimento", "8 porções"), ("Tempo", "35 min")],
        "ingredients": [
            "Massa: 200 g de farinha, 100 g de manteiga, sal, 6 colheres (sopa) de água fria",
            "Recheio: 4 colheres (sopa) de azeite, 1 dente de alho, 6 batatas cozidas em cubos, 2 latas de atum, 3 ovos, 200 ml de creme de leite fresco, 1 xícara (chá) de parmesão, sal, pimenta, salsa",
        ],
        "steps": [
            "Faça a massa, gele 30 min e forre forma 24 cm.",
            "Refogue alho, batata, atum, temperos e salsa; espalhe sobre a massa. Bata ovos, creme e parmesão; despeje e asse até dourar.",
        ],
    },
    {
        "cat": "salgados",
        "slug": "torta-de-queijo-e-milho",
        "title": "Torta de queijo e milho",
        "meta": [("Rendimento", "10 porções"), ("Tempo", "50 min")],
        "ingredients": [
            "Recheio: 3 espigas de milho verde, ½ maço de couve, 2 colheres (sopa) de óleo, 1 cebola picada, ⅓ xícara (chá) de água quente, sal",
            "Massa: 2 colheres (sopa) de óleo, 3 xícaras (chá) de leite, 2 ovos, 1 xícara (chá) de farinha integral, 1 colher (chá) de sal, 1 xícara (chá) de queijo-de-minas curado ralado",
        ],
        "steps": [
            "Refogue cebola e milho 15 min; junte água, couve e sal.",
            "Bata óleo, leite, ovos, farinha e sal. Despeje metade em assadeira untada, o recheio, o restante da massa e o queijo. Asse em forno médio até dourar.",
        ],
        "notes": "Couve pode ser trocada por escarola, agrião ou talos de brócolis.",
    },
    {
        "cat": "salgados",
        "slug": "torta-de-frango-com-catupiry",
        "title": "Torta de frango com Catupiry",
        "meta": [("Rendimento", "12 porções"), ("Tempo", "50 min")],
        "ingredients": [
            "Massa: ½ lata de creme de leite, 4 xícaras (chá) de farinha, 2 ovos, 100 g de margarina, sal",
            "Recheio: 2 colheres (sopa) de azeite, 1 cebola grande, 2 tomates sem pele/sementes, 1 pote de cogumelo em lâminas, 1½ peito de frango cozido e desfiado, sal, pimenta, salsa, 400 g de requeijão tipo Catupiry, gema para pincelar",
        ],
        "steps": [
            "Misture a massa; forre forma 22 cm desmontável reservando tampa.",
            "Refogue cebola, tomate, cogumelo e frango; tempere e misture o Catupiry. Esfrie, recheie, cubra, pincele gema e asse a 200 °C até dourar.",
        ],
    },
    {
        "cat": "frutos-do-mar",
        "slug": "torta-de-atum",
        "title": "Torta de atum",
        "meta": [("Rendimento", "8 porções"), ("Tempo", "40 min")],
        "ingredients": [
            "1 xícara (chá) de farinha de trigo",
            "½ xícara (chá) de óleo",
            "1 colher (sopa) de fermento em pó",
            "½ xícara (chá) de queijo ralado",
            "4 ovos",
            "Pimenta-do-reino e sal",
            "2 latas de atum",
            "1 cebola picada",
            "100 g de sementes de gergelim cruas",
        ],
        "steps": [
            "Bata farinha, óleo, fermento, queijo e ovos; tempere. Misture atum amassado e cebola.",
            "Despeje em forma untada e enfarinhada; polvilhe gergelim. Asse em forno médio até dourar. Sirva quente ou morna com salada.",
        ],
        "notes": "Pode usar sobras de frango no lugar do atum.",
    },
]

RECIPES = PART1 + PART2


def render_recipe(r: dict) -> str:
    cat = r["cat"]
    cat_label = CATEGORIES[cat]
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
        <a href="../../index.html#{cat}">{html.escape(cat_label)}</a>
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


def update_index(all_new: list[dict]) -> None:
    index_path = ROOT / "index.html"
    text = index_path.read_text(encoding="utf-8")

    # Collect all recipes from disk per category
    by_cat: dict[str, list[tuple[str, str]]] = {c: [] for c in CATEGORIES}
    for html_file in (ROOT / "receitas").rglob("*.html"):
        cat = html_file.parent.name
        if cat not in by_cat:
            continue
        content = html_file.read_text(encoding="utf-8")
        m = re.search(r"<h1>(.*?)</h1>", content, re.S)
        title = re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else html_file.stem
        by_cat[cat].append((html_file.stem, title))

    for cat in by_cat:
        by_cat[cat].sort(key=lambda x: x[1].lower())

    def section_html(cat: str) -> str:
        label = CATEGORIES[cat]
        items = by_cat[cat]
        if not items:
            lis = '          <li class="empty">Nenhuma receita ainda</li>\n'
        else:
            lis = "".join(
                f'          <li>\n            <a href="./receitas/{cat}/{slug}.html"\n              >{html.escape(title)}</a\n            >\n          </li>\n'
                for slug, title in items
            )
        return (
            f'      <section class="category-block" id="{cat}">\n'
            f"        <h2>{label}</h2>\n"
            f'        <ul class="recipe-list">\n'
            f"{lis}"
            f"        </ul>\n"
            f"      </section>"
        )

    # Replace entire recipe-index main inner sections
    sections = "\n\n".join(section_html(c) for c in CATEGORIES)
    new_main = f'    <main class="recipe-index" id="receitas">\n{sections}\n    </main>'
    text2, n = re.subn(
        r'    <main class="recipe-index" id="receitas">.*?</main>',
        new_main,
        text,
        count=1,
        flags=re.S,
    )
    if n != 1:
        raise SystemExit("Failed to update index.html main block")
    index_path.write_text(text2, encoding="utf-8")
    print(f"Updated index.html ({sum(len(v) for v in by_cat.values())} recipes)")


def main() -> None:
    written = write_recipes()
    update_index(written)
    print(f"Created {len(written)} new recipes; total defined {len(RECIPES)}")


if __name__ == "__main__":
    main()
