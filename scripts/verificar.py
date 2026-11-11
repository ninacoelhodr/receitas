#!/usr/bin/env python3
"""Confere a consistência do site: livros, páginas, fichas e links.

Uso:  python scripts/verificar.py      (sai com código 1 se houver problema)
"""
import glob
import json
import os
import re
import sys
from urllib.parse import unquote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
problemas = []


def ler(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def erro(msg):
    problemas.append(msg)


# ---- receitas x livros
receitas = {
    f"{os.path.basename(os.path.dirname(p))}/{os.path.basename(p)[:-5]}": p
    for p in glob.glob(os.path.join(ROOT, "receitas", "*", "*.html"))
}
livros = json.loads(ler(os.path.join(ROOT, "livros", "livros.json")))["livros"]
dono = {}
for lv in livros:
    paginas = {}
    for r in lv["receitas"]:
        k = r["slug"]
        if k not in receitas:
            erro(f"{lv['id']}: receita inexistente {k}")
        if k in dono and not lv.get("automatico"):
            erro(f"{k} está em dois livros: {dono[k]} e {lv['id']}")
        dono[k] = lv["id"]
        if r.get("pagina"):
            if r["pagina"] in paginas:
                erro(f"{lv['id']}: página {r['pagina']} repetida ({paginas[r['pagina']]} e {k})")
            paginas[r["pagina"]] = k
    for a in lv.get("artigos", []):
        if not os.path.exists(os.path.join(ROOT, a["href"])):
            erro(f"{lv['id']}: artigo inexistente {a['href']}")

for k, p in receitas.items():
    s = ler(p)
    if k not in dono and not any(l.get("automatico") for l in livros):
        erro(f"{k}: sem livro")
    if 'data-livro="' not in s or "livro-nav" not in s:
        erro(f"{k}: ficha sem navegação de livro (rode scripts/gerar-livros.py)")
    slug = k.split("/")[1]
    if not os.path.exists(os.path.join(ROOT, "imagens", slug + ".jpg")):
        erro(f"{k}: sem foto em imagens/{slug}.jpg")
    if re.search(r"<li>\s*[0-9]+\.\s", s):
        erro(f"{k}: passo com número escrito dentro do <li>")
    if '<ul class="ingredients">' not in s or '<ol class="steps">' not in s:
        erro(f"{k}: sem ingredientes ou modo de preparo")

# ---- catálogo lista todas as receitas
cat = ler(os.path.join(ROOT, "catalogo.html"))
no_catalogo = set(re.findall(r'href="\./receitas/([^"]+)\.html"', cat))
for k in receitas:
    if k not in no_catalogo:
        erro(f"{k}: fora do catalogo.html")
for k in no_catalogo - set(receitas):
    erro(f"catalogo.html aponta para ficha inexistente: {k}")

# ---- links relativos de todas as páginas
paginas_html = (
    [os.path.join(ROOT, "index.html"), os.path.join(ROOT, "catalogo.html")]
    + glob.glob(os.path.join(ROOT, "livros", "*", "index.html"))
    + list(receitas.values())
    + glob.glob(os.path.join(ROOT, "na-cozinha", "*.html"))
)
for p in paginas_html:
    base = os.path.dirname(p)
    for attr, url in re.findall(r'\b(href|src)="([^"]+)"', ler(p)):
        if re.match(r"^(https?:|mailto:|tel:|#|data:|javascript:|/)", url):
            continue
        alvo = unquote(re.split(r"[#?]", url)[0])
        if not alvo:
            continue
        caminho = os.path.normpath(os.path.join(base, alvo))
        if os.path.isdir(caminho):
            caminho = os.path.join(caminho, "index.html")
        if not os.path.exists(caminho):
            erro(f"{os.path.relpath(p, ROOT)}: link quebrado {url}")

print(f"{len(livros)} livros, {len(receitas)} receitas, {len(paginas_html)} páginas verificadas")
if problemas:
    print(f"\n{len(problemas)} problema(s):")
    for m in problemas[:60]:
        print(" -", m)
    sys.exit(1)
print("tudo certo")
