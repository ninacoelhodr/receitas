#!/usr/bin/env python3
"""Build Wikimedia Commons search query batches from recipe inventory."""
from __future__ import annotations

import json
import pathlib
import re
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parent
inv = json.loads((ROOT / "_inventory.json").read_text(encoding="utf-8"))

OVERRIDES = {
    "talharim-com-vongole": [
        "spaghetti alle vongole",
        "linguine vongole",
        "clam pasta bowl",
    ],
    "espaguete-ao-vongole": ["spaghetti alle vongole", "spaghetti with clams"],
    "espaguete-a-carbonara": ["spaghetti carbonara plate", "pasta carbonara bowl"],
    "espaguete-a-bolonhesa": ["spaghetti bolognese plate", "spaghetti meat sauce"],
    "espaguete-aos-quatro-queijos": [
        "four cheese pasta",
        "pasta ai quattro formaggi",
    ],
    "macarrao-ao-creme": ["creamy pasta alfredo", "pasta cream sauce plate"],
    "macarrao-a-napolitana": ["pasta napoletana tomato", "spaghetti marinara plate"],
    "macarrao-a-moda-do-sul": ["sausage pasta tomato", "pasta with sausage plate"],
    "macarrao-tentador": ["baked pasta cheese", "pasta casserole cheese"],
    "macarrao-com-azeitonas": ["pasta olives tomato", "pasta with black olives"],
    "lasanha-aos-quatro-queijos": ["four cheese lasagna", "lasagna formaggi"],
    "ravioli-a-camaresca": ["seafood ravioli", "shrimp ravioli plate"],
    "bucatini-com-atum-iogurte-e-pimenta": [
        "bucatini tuna pasta",
        "pasta with tuna chili",
    ],
    "pao-de-queijo": ["pao de queijo Brazilian", "cheese bread Brazilian"],
    "bolo-de-cenoura": [
        "Brazilian carrot cake chocolate frosting",
        "bolo de cenoura cobertura",
    ],
    "rabada": ["oxtail stew bowl", "rabada Brazilian stew"],
    "ossobuco-de-vitela-com-risotto-de-rucula": [
        "ossobuco risotto",
        "osso buco milanese",
    ],
    "tempura-de-camarao": ["shrimp tempura plate", "ebi tempura"],
    "vol-au-vent-de-vieiras": ["vol au vent scallops", "scallop vol-au-vent"],
    "goo-low-yuke": ["sweet and sour pork", "gu lou rou"],
    "ju-har-kow": ["shrimp dumpling har gow", "har gow dim sum"],
    "hang-yang-peang": ["almond jelly dessert", "xingren doufu"],
    "mousse-de-chocolate": ["chocolate mousse dessert cup", "mousse au chocolat"],
    "musse-de-morango": ["strawberry mousse dessert", "mousse de fraise"],
    "musse-de-maracuja": ["passion fruit mousse", "mousse maracuja"],
    "costeletas-de-cordeiro-com-menta": [
        "lamb chops mint",
        "grilled lamb chops plate",
    ],
    "avestruz-a-la-bourguignonne": [
        "beef bourguignon stew",
        "boeuf bourguignon bowl",
    ],
    "escalope-de-foie-gras-com-maca-verde": [
        "foie gras seared apple",
        "escalope foie gras",
    ],
    "ponche-quero-karo": ["fruit punch bowl", "ponche fruits"],
    "xixi-de-anjo": ["angel hair pudding dessert", "fios de ovos dessert"],
    "compota-de-tomate": ["tomato jam jar", "tomato compote dessert"],
    "calda-de-maracuja-para-torta": [
        "passion fruit sauce dessert",
        "passion fruit coulis",
    ],
    "molho-branco-sem-fogo": ["bechamel sauce bowl", "white cream sauce"],
    "sorvete-de-especiarias": ["spiced ice cream scoop", "cinnamon ice cream"],
    "bolinho-de-chuva": ["bolinho de chuva Brazilian", "fried dough cinnamon sugar"],
    "waffle-salgado": ["savory waffle cheese", "cheese waffle savory"],
    "sanduiche-prensado": ["pressed sandwich panini", "toasted sandwich press"],
    "torta-pizza": ["savory pizza pie", "pizza tart"],
    "quiche-de-tomate-seco-e-peito-de-peru": [
        "quiche turkey tomato",
        "vegetable turkey quiche",
    ],
    "pate-de-miudos-de-frango": ["chicken liver pate", "pate foie volaille"],
    "camarao-imperial": ["garlic butter shrimp plate", "shrimp scampi plated"],
    "arroz-do-mar": ["seafood rice platter", "shrimp rice dish"],
    "peixe-a-thermidor": ["fish thermidor", "lobster thermidor"],
    "fervido": ["fish stew bowl", "Brazilian fish stew"],
    "tender-picante": ["glazed ham roast", "honey glazed ham"],
    "picanha-de-porco-ao-molho-de-tamarindo": [
        "pork steak tamarind",
        "grilled pork with sauce",
    ],
    "pernil-recheado-com-canjiquinha": [
        "stuffed pork roast",
        "roast pork with cornmeal",
    ],
    "atum-fresco-grelhado-ao-curry": ["grilled tuna curry", "tuna steak curry sauce"],
    "camaraoes-com-vodca-ao-molho-de-salsa": [
        "shrimp vodka sauce",
        "shrimp parsley sauce plate",
    ],
    "terrine-de-camarao-e-palmito": ["shrimp terrine", "seafood terrine slice"],
    "pera-com-truta-defumada": ["smoked trout pear salad", "smoked trout plated"],
    "hadoque-defumado-com-maca": ["smoked haddock apple", "smoked fish with apple"],
    "truta-grande-hotel-ao-molho-de-pinhao": [
        "trout with pine nuts",
        "baked trout plate",
    ],
    "fiesta-com-batatas-e-creme-azedo": [
        "chicken potatoes sour cream",
        "baked chicken potato casserole",
    ],
    "peru-com-peras-e-arroz-de-nozes": [
        "roast turkey pears",
        "turkey with fruit nuts",
    ],
    "gratinado-de-frango": ["chicken gratin casserole", "chicken potato gratin"],
    "pato-com-repolho-roxo": ["duck red cabbage", "roast duck cabbage"],
    "frango-macedo-a-napolitana": ["chicken napoletana tomato", "chicken tomato cheese"],
    "souffle-de-frango-macedo": ["chicken souffle", "souffle savoureux"],
    "salpicao-de-galinha": ["chicken salad Brazilian salpicao", "chicken salad platter"],
    "frango-com-iogurte-e-hortela": ["yogurt mint chicken", "chicken yogurt sauce"],
    "frango-com-creme-de-milho": ["chicken corn cream casserole", "chicken with corn"],
    "fricasse-de-frango": ["chicken fricassee", "fricassee chicken cream"],
    "frango-dourado": ["golden fried chicken cutlets", "breaded chicken plate"],
    "frango-ao-forno": ["roast chicken oven plate", "whole roast chicken"],
    "torta-de-frango-com-catupiry": [
        "chicken pie Brazilian",
        "chicken cream cheese pie",
    ],
    "torta-maravilha-de-frango-e-presunto": [
        "chicken ham pie",
        "savory chicken pie",
    ],
    "torta-de-atum": ["tuna pie savory", "tuna quiche"],
    "torta-de-atum-e-batata": ["tuna potato pie", "tuna potato casserole"],
    "musse-napolitana": ["neapolitan mousse layered", "three layer mousse dessert"],
    "musse-brigadeiro-branco": ["white chocolate mousse", "white brigadeiro mousse"],
    "musse-bombom-de-chocolate": ["chocolate bombom mousse", "chocolate mousse cup"],
    "musse-bis": ["chocolate cookie mousse", "mousse with biscuits"],
    "musse-chic": ["elegant chocolate cream dessert", "layered chocolate mousse"],
    "musse-delicia": ["fruit cream mousse dessert", "layered mousse dessert"],
    "musse-especial": ["specialty cream dessert", "cream mousse parfait"],
    "musse-paixao": ["passion fruit cream dessert", "layered passion mousse"],
    "musse-requintada": ["elegant mousse dessert", "cream dessert cup"],
    "musse-de-festa": ["party mousse dessert", "festive layered mousse"],
    "musse-de-guarana": ["guarana cream dessert", "yellow cream mousse"],
    "musse-caramelada-de-banana-e-gengibre": [
        "banana caramel mousse",
        "banana ginger dessert",
    ],
    "musse-de-abobora-com-amendoim": [
        "pumpkin peanut mousse",
        "pumpkin mousse dessert",
    ],
    "musse-de-amendoim": ["peanut mousse dessert", "peanut butter mousse"],
    "musse-de-amora": ["blackberry mousse", "mousse mure"],
    "musse-de-baunilha-e-compota-de-uva": [
        "vanilla mousse grape compote",
        "vanilla cream dessert grapes",
    ],
    "musse-de-biscoito-com-mel": ["cookie honey mousse", "biscuit honey dessert"],
    "musse-de-castanha": ["chestnut mousse dessert", "mousse chataigne"],
    "musse-de-coco-com-calda-de-pessego": [
        "coconut mousse peach",
        "coconut cream peach dessert",
    ],
    "musse-de-manga-com-leite-de-coco": [
        "mango coconut mousse",
        "mango coconut cream dessert",
    ],
    "musse-de-tangerina-e-chocolate-branco": [
        "tangerine white chocolate mousse",
        "citrus white chocolate mousse",
    ],
    "musse-espuma-de-pessego": ["peach foam dessert", "peach mousse cup"],
    "musse-limonada": ["lemon mousse dessert", "limonade mousse"],
    "musse-torta-de-limao": ["lemon pie mousse", "lemon meringue mousse"],
    "musse-caramelo": ["caramel mousse dessert", "mousse caramel"],
    "flan-de-chocolate-e-creme": ["chocolate flan", "flan chocolate cream"],
    "sufle-de-damasco": ["apricot souffle", "souffle abricot"],
    "terrine-de-pistache": ["pistachio terrine dessert", "pistachio dessert slice"],
    "torta-de-maracuja-com-ganache": [
        "passion fruit tart ganache",
        "passion fruit chocolate tart",
    ],
    "tortinhas-de-banana": ["banana tartlets", "mini banana tart"],
    "morango-ao-creme": ["strawberries and cream", "fraise a la creme"],
    "biscoitos-amanteigados": ["butter cookies plate", "shortbread cookies"],
    "biscoitos-amanteigados-de-laranja": [
        "orange butter cookies",
        "orange shortbread",
    ],
    "biscoitos-de-chocolate": ["chocolate cookies plate", "chocolate biscuits"],
    "biscoitos-de-limao": ["lemon cookies plate", "lemon biscuits"],
    "biscoitos-de-maracuja": ["passion fruit cookies", "fruit cookies plate"],
    "biscoitos-de-nata": ["cream biscuits", "butter cream cookies"],
    "bolachinha-croc-de-chocolate": [
        "crispy chocolate cookies",
        "chocolate crunch biscuits",
    ],
    "biscoito-de-araruta-vo-marli": ["arrowroot cookies", "biscoito de araruta"],
    "pudim-de-claras": ["egg white pudding Brazilian", "pudim de claras"],
    "bolo-de-panquecas-de-natal": [
        "pancake cake Christmas",
        "layered pancake cake",
    ],
    "assado-de-panela": ["pot roast beef", "braised beef pot"],
    "croquete-de-carne-cozida": ["meat croquettes", "croquetes carne"],
    "croquete-de-peixe": ["fish croquettes", "croquetas de pescado"],
    "espetinhos-temperados": ["seasoned meat skewers", "grilled kebabs"],
    "lingua-com-pure-de-ervilhas-e-bacon": [
        "beef tongue peas bacon",
        "tongue with pea puree",
    ],
    "lombo-a-fantasia-com-pure-de-maca": [
        "pork loin apple puree",
        "pork with applesauce",
    ],
    "lombo-de-porco-com-tomate-e-ervas": [
        "pork loin tomato herbs",
        "roasted pork tomato",
    ],
    "lombo-de-porco-delicioso": ["roast pork loin plate", "sliced pork loin"],
    "pernil-de-vitela-assado": ["roast veal leg", "roast veal plate"],
    "enroladinhos-de-queijo": ["cheese rolls fried", "cheese roll pastry"],
    "maxipasteis-de-forno": ["baked pastels Brazilian", "baked savory pastry"],
    "pasteis-cozidos": ["boiled pastry Brazilian", "savory boiled pastels"],
    "tortinhas-de-cebola-e-queijo": ["onion cheese tartlets", "mini onion quiche"],
    "tortinhas-de-mussarela-de-bufala": [
        "buffalo mozzarella tartlets",
        "mozzarella tartlets",
    ],
    "torta-de-bacon-e-minicebola": ["bacon onion tart", "quiche bacon onion"],
    "torta-de-catalonia": ["chicory savory tart", "escarole tart"],
    "torta-de-cebola": ["onion tart", "tarte a l oignon"],
    "torta-de-escarola-com-requeijao": [
        "escarole cream cheese pie",
        "greens ricotta pie",
    ],
    "torta-de-queijo-e-milho": ["cheese corn pie", "corn cheese tart"],
    "torta-folhada-de-queijo": ["puff pastry cheese tart", "cheese puff pastry"],
    "folhado-de-linguica-e-ricota": [
        "sausage ricotta puff pastry",
        "linguica ricotta pastry",
    ],
}


def strip_acc(s: str) -> str:
    return "".join(
        c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn"
    )


def auto_queries(title: str, ings: list[str], slug: str, cat: str) -> list[str]:
    if slug in OVERRIDES and OVERRIDES[slug]:
        return OVERRIDES[slug]
    t = title.strip()
    qs = [t, f"{t} plated", f"{t} food"]
    low = strip_acc(t.lower())
    if "musse" in low or "mousse" in low:
        base = t.replace("Musse", "mousse").replace("Mousse", "mousse")
        qs = [f"{base} dessert", f"{base} cup"]
    seen: set[str] = set()
    out: list[str] = []
    for q in qs:
        q = q.strip()
        if q and q.lower() not in seen:
            seen.add(q.lower())
            out.append(q)
    return out[:3]


batches: dict[str, list] = {}
for item in inv:
    qs = auto_queries(item["title"], item["ings"], item["slug"], item["cat"])
    batches.setdefault(item["cat"], []).append(
        {
            "slug": item["slug"],
            "title": item["title"],
            "queries": qs,
            "ings": item["ings"][:5],
            "path": item["path"],
        }
    )

out_dir = ROOT / "_batches"
out_dir.mkdir(exist_ok=True)
for cat, items in batches.items():
    (out_dir / f"{cat}.json").write_text(
        json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(cat, len(items), "eg", items[0]["queries"])
print("cats", len(batches))
