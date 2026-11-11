#!/usr/bin/env python3
"""Gera a estante (index.html), as páginas de cada livro (livros/<id>/index.html)
e a navegação "Neste livro" dentro de cada ficha, a partir de livros/livros.json.

É idempotente: pode rodar de novo a cada lote de receitas.
Uso:  python scripts/gerar-livros.py
"""
import glob
import html
import json
import os
import re
import sys
import unicodedata

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CATEGORIAS = [
    ("doces", "Doces"),
    ("salgados", "Salgados"),
    ("tortas-salgadas", "Tortas salgadas"),
    ("massas", "Massas"),
    ("carnes", "Carnes"),
    ("aves", "Aves"),
    ("frutos-do-mar", "Frutos do mar"),
    ("sopas", "Sopas"),
    ("acompanhamentos", "Acompanhamentos"),
    ("bebidas", "Bebidas"),
]
CAT_ORDEM = {c: i for i, (c, _) in enumerate(CATEGORIAS)}
CAT_NOME = dict(CATEGORIAS)
CSS_V = "livros2"


def norm(t):
    t = unicodedata.normalize("NFD", t.lower())
    return "".join(c for c in t if unicodedata.category(c) != "Mn")


def esc(t):
    return html.escape(t, quote=True)


def ler(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def gravar(path, s):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(s)


# ---------------------------------------------------------------- receitas
def varrer_receitas():
    rec = {}
    for p in sorted(glob.glob(os.path.join(ROOT, "receitas", "*", "*.html"))):
        cat = os.path.basename(os.path.dirname(p))
        slug = os.path.basename(p)[:-5]
        s = ler(p)
        m = re.search(r"<h1[^>]*>(.*?)</h1>", s, re.S)
        titulo = html.unescape(re.sub(r"<[^>]+>", "", m.group(1))).strip() if m else slug
        rec[f"{cat}/{slug}"] = {
            "key": f"{cat}/{slug}",
            "cat": cat,
            "slug": slug,
            "titulo": titulo,
            "path": p,
            "foto": os.path.exists(os.path.join(ROOT, "imagens", slug + ".jpg")),
        }
    return rec


def carregar():
    data = json.loads(ler(os.path.join(ROOT, "livros", "livros.json")))
    rec = varrer_receitas()
    usados = {}
    for lv in data["livros"]:
        for r in lv["receitas"]:
            k = r["slug"]
            if k not in rec:
                sys.exit(f"ERRO: receita inexistente em {lv['id']}: {k}")
            if k in usados:
                sys.exit(f"ERRO: {k} está em dois livros: {usados[k]} e {lv['id']}")
            usados[k] = lv["id"]
    for lv in data["livros"]:
        if lv.get("automatico"):
            restantes = [r for k, r in rec.items() if k not in usados]
            restantes.sort(key=lambda r: (CAT_ORDEM.get(r["cat"], 99), norm(r["titulo"])))
            lv["receitas"] = [{"slug": r["key"]} for r in restantes]
            for r in restantes:
                usados[r["key"]] = lv["id"]
    sem = [k for k in rec if k not in usados]
    if sem:
        sys.exit(f"ERRO: receitas sem livro: {sem[:5]} (+{len(sem) - 5})")
    return data["livros"], rec


# ---------------------------------------------------------------- pedaços HTML
def capa_html(lv, grande=False):
    estilo = f"--capa:{esc(lv['cor'])};--capa-texto:{esc(lv.get('texto', '#fff'))}"
    serie = f'<span class="capa-serie">{esc(lv["serie"])}</span>' if lv.get("serie") else ""
    classe = "capa capa-grande" if grande else "capa"
    return (
        f'<span class="{classe}" style="{estilo}">'
        f"{serie}"
        f'<span class="capa-titulo">{esc(lv["titulo"])}</span>'
        f'<span class="capa-orn" aria-hidden="true"></span>'
        f'<span class="capa-sub">{esc(lv["subtitulo"])}</span>'
        f"</span>"
    )


def paginas_txt(lv):
    pgs = [r["pagina"] for r in lv["receitas"] if r.get("pagina")]
    return f"páginas {min(pgs)} a {max(pgs)}" if pgs else ""


def cabecalho(prefix, ativo):
    def a(href, texto, chave):
        cur = ' aria-current="true"' if ativo == chave else ""
        return f'<a href="{prefix}{href}"{cur}>{texto}</a>'

    return f"""    <header class="site-header no-print">
      <a class="brand" href="{prefix}index.html">Livro de Receitas</a>
      <nav class="site-nav" aria-label="Principal">
        {a("index.html", "Estante", "estante")}
        {a("catalogo.html", "Por categoria", "catalogo")}
        {a("na-cozinha/", "Na cozinha", "cozinha")}
      </nav>
    </header>"""


def pagina(titulo, desc, prefix, corpo, ativo, extra_body=""):
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{esc(titulo)}</title>
    <meta name="description" content="{esc(desc)}" />
    <link rel="stylesheet" href="{prefix}css/site.css?v=caderno6" />
    <link rel="stylesheet" href="{prefix}css/livros.css?v={CSS_V}" />
    <link rel="stylesheet" href="{prefix}css/print.css" />
  </head>
  <body{extra_body}>
{cabecalho(prefix, ativo)}

{corpo}
  </body>
</html>
"""


# ---------------------------------------------------------------- estante
def gerar_estante(livros):
    itens = []
    for lv in livros:
        n = len(lv["receitas"])
        itens.append(
            f"""        <li class="livro">
          <a class="livro-link" href="./livros/{lv['id']}/">
            <span class="prateleira">{capa_html(lv)}</span>
            <span class="livro-legenda"><strong>{esc(lv['titulo'])}</strong>
              <em>{esc(lv['subtitulo'])}</em>
              <small>{n} receita{'s' if n != 1 else ''}</small></span>
          </a>
        </li>"""
        )
    total = sum(len(lv["receitas"]) for lv in livros)
    corpo = f"""    <section class="hero">
      <p class="hero-eyebrow">biblioteca de receitas</p>
      <h1>Livro de Receitas</h1>
      <p>
        Escolha um livro na estante e folheie as receitas na ordem original,
        como se estivesse com ele nas mãos.
      </p>
      <form class="busca-estante no-print" action="./catalogo.html" method="get" role="search">
        <label class="visually-hidden" for="q">Buscar receita em todos os livros</label>
        <input id="q" name="q" class="recipe-search" type="search" placeholder="Buscar receita em todos os livros…" autocomplete="off" />
      </form>
    </section>

    <main class="estante">
      <ul class="estante-lista">
{chr(10).join(itens)}
      </ul>
      <p class="estante-nota no-print">
        {total} receitas em {len(livros)} livros ·
        <a href="./catalogo.html">ver todas por categoria</a>
      </p>
    </main>"""
    gravar(
        os.path.join(ROOT, "index.html"),
        pagina(
            "Livro de Receitas — Estante",
            "Biblioteca de receitas da família: escolha um livro e folheie.",
            "./",
            corpo,
            "estante",
        ),
    )


# ---------------------------------------------------------------- livro
def link_receita(r, prefix="../../"):
    return f"{prefix}receitas/{r['key']}.html"


def gerar_livro(lv, rec):
    itens = []
    for r in lv["receitas"]:
        d = dict(rec[r["slug"]])
        d["pagina"] = r.get("pagina")
        itens.append(d)

    entradas = []
    if lv.get("agrupar") == "categoria":
        atual = None
        for d in itens:
            if d["cat"] != atual:
                if atual is not None:
                    entradas.append("          </ol>")
                entradas.append(f'          <h3 class="sumario-capitulo">{esc(CAT_NOME.get(d["cat"], d["cat"]))}</h3>')
                entradas.append('          <ol class="sumario-lista">')
                atual = d["cat"]
            entradas.append(
                f'            <li><a href="{link_receita(d)}"><span class="sum-titulo">{esc(d["titulo"])}</span></a></li>'
            )
        if atual is not None:
            entradas.append("          </ol>")
        sumario = "\n".join(entradas)
    else:
        linhas = [(d["pagina"], d["titulo"], link_receita(d), False) for d in itens]
        for a in lv.get("artigos", []):
            if a.get("pagina"):
                linhas.append((a["pagina"], a["titulo"], "../../" + a["href"], True))
        linhas.sort(key=lambda t: (t[0] if t[0] is not None else 9999))
        li = []
        for pg, titulo, href, artigo in linhas:
            classe = ' class="sum-artigo"' if artigo else ""
            pag = f'<span class="sum-pag">{pg}</span>' if pg is not None else ""
            li.append(
                f'            <li{classe}><a href="{href}"><span class="sum-titulo">{esc(titulo)}</span>'
                f'<span class="sum-pontos" aria-hidden="true"></span>{pag}</a></li>'
            )
        sumario = '          <ol class="sumario-lista">\n' + "\n".join(li) + "\n          </ol>"

    artigos = [a for a in lv.get("artigos", []) if not a.get("pagina")]
    bloco_art = ""
    if artigos:
        lis = "\n".join(
            f'          <li><a href="../../{a["href"]}">{esc(a["titulo"])}</a></li>' for a in artigos
        )
        bloco_art = f"""
        <div class="livro-artigos">
          <h3>Na cozinha</h3>
          <ul>
{lis}
          </ul>
        </div>"""

    pgs = paginas_txt(lv)
    meta = f"{len(itens)} receitas" + (f" · {pgs}" if pgs else "")
    primeira = link_receita(itens[0]) if itens else "#"
    provisoria = (
        '<p class="capa-aviso no-print">Capa provisória — será trocada pela capa do livro.</p>'
        if lv.get("capa_provisoria")
        else ""
    )
    serie = f'<p class="livro-serie">{esc(lv["serie"])}</p>' if lv.get("serie") else ""
    corpo = f"""    <main class="livro-page" data-livro="{lv['id']}" style="--livro:{esc(lv['cor'])}">
      <div class="livro-topo">
        <div class="livro-capa-wrap">{capa_html(lv, grande=True)}</div>
        <div class="livro-detalhes">
          {serie}
          <h1>{esc(lv['titulo'])}</h1>
          <p class="livro-sub">{esc(lv['subtitulo'])}</p>
          <p class="livro-meta">{esc(meta)}</p>
          <p class="livro-botoes no-print">
            <a class="btn" href="{primeira}">Começar a ler</a>
            <a class="btn btn-ghost" href="../../index.html">← Estante</a>
          </p>
          {provisoria}{bloco_art}
        </div>
      </div>

      <section class="sumario">
        <h2>Sumário</h2>
{sumario}
      </section>
    </main>"""
    titulo = f"{lv['titulo']} — {lv['subtitulo']} · Livro de Receitas"
    gravar(
        os.path.join(ROOT, "livros", lv["id"], "index.html"),
        pagina(titulo, f"{lv['titulo']}: {lv['subtitulo']} — {meta}.", "../../", corpo, "estante"),
    )


# ---------------------------------------------------------------- fichas
def anotar_ficha(lv, i, itens, rec):
    d = itens[i]
    p = d["path"]
    s = ler(p)
    # limpa o que o gerador colocou antes
    s = re.sub(r"[ \t]*<!-- livro:inicio -->.*?<!-- livro:fim -->\n?", "", s, flags=re.S)

    def limpar_attrs(m):
        attrs = m.group(1)
        attrs = re.sub(r'\s+data-(livro|pagina|layout)="[^"]*"', "", attrs)
        attrs = re.sub(r'\s+style="--livro:[^"]*"', "", attrs)
        novo = f' data-livro="{lv["id"]}"'
        if d.get("pagina"):
            novo += f' data-pagina="{d["pagina"]}"'
        novo += f' data-layout="{lv.get("layout", "simples")}" style="--livro:{lv["cor"]}"'
        return f'<article class="recipe-card"{attrs}{novo}>'

    s, n = re.subn(r'<article class="recipe-card"([^>]*)>', limpar_attrs, s, count=1)
    if n != 1:
        sys.exit(f"ERRO: <article class=recipe-card> não encontrado em {p}")

    prev = itens[i - 1] if i > 0 else None
    prox = itens[i + 1] if i + 1 < len(itens) else None

    def seta(alvo, rel, rotulo):
        if not alvo:
            return f'<span class="livro-nav-off">{rotulo}</span>'
        return f'<a rel="{rel}" href="../{alvo["cat"]}/{alvo["slug"]}.html" title="{esc(alvo["titulo"])}">{rotulo}</a>'

    pag = f'<span class="livro-nav-pag">pág. {d["pagina"]}</span>' if d.get("pagina") else ""
    nome = f'{lv["titulo"]} — {lv["subtitulo"]}'
    nav = f"""    <!-- livro:inicio -->
    <nav class="livro-nav no-print" aria-label="Neste livro" style="--livro:{lv['cor']}">
      <a class="livro-nav-livro" href="../../livros/{lv['id']}/">{esc(nome)}</a>
      {pag}
      <span class="livro-nav-setas">{seta(prev, "prev", "← Anterior")}{seta(prox, "next", "Próxima →")}</span>
    </nav>
    <!-- livro:fim -->
"""
    s = re.sub(r"(\n[ \t]*)(<article class=\"recipe-card\")", lambda m: "\n" + nav + m.group(1).lstrip("\n") + m.group(2), s, count=1)

    # voltar -> sumário do livro; categoria do cabeçalho -> catálogo
    s = re.sub(
        r'(<a class="btn btn-ghost" href=")[^"]*(">)',
        lambda m: f'{m.group(1)}../../livros/{lv["id"]}/{m.group(2)}',
        s,
        count=1,
    )
    s = s.replace('href="../../index.html#', 'href="../../catalogo.html#')
    # css e script de layout
    if "css/livros.css" not in s:
        s = s.replace(
            '<link rel="stylesheet" href="../../css/print.css" />',
            '<link rel="stylesheet" href="../../css/print.css" />\n    <link rel="stylesheet" href="../../css/livros.css" />',
            1,
        )
    if "recipe-layout" not in s:
        s = s.replace("</body>", '    <script src="../../js/recipe-layout.js" defer></script>\n  </body>', 1)
    gravar(p, s)


def ajustar_na_cozinha():
    for p in glob.glob(os.path.join(ROOT, "na-cozinha", "*.html")):
        s = ler(p)
        n = s.replace('../index.html#categorias', '../catalogo.html#categorias')
        if n != s:
            gravar(p, n)


def main():
    livros, rec = carregar()
    gerar_estante(livros)
    for lv in livros:
        gerar_livro(lv, rec)
        itens = [dict(rec[r["slug"]], pagina=r.get("pagina")) for r in lv["receitas"]]
        for i in range(len(itens)):
            anotar_ficha(lv, i, itens, rec)
    ajustar_na_cozinha()
    print(f"ok: {len(livros)} livros, {sum(len(l['receitas']) for l in livros)} receitas")


if __name__ == "__main__":
    main()
