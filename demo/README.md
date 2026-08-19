# Prévia visual — Livro de Receitas

Esta pasta é uma **prévia isolada** para comparar duas direções de design antes de alterar o site principal. Nada fora de `demo/` foi modificado.

## Como abrir

1. Abra [`index.html`](index.html) no navegador (duplo-clique ou servidor local).
2. Use a barra fixa no topo para alternar **Clássico** e **Moderno**.
3. Navegue pela capa, uma receita de exemplo e um artigo de Na cozinha.

## O que comparar

| Página | O que observar |
|--------|----------------|
| [index.html](index.html) | Capa de livro, capítulos, grid de receitas |
| [frango-na-pucara.html](frango-na-pucara.html) | Ficha: clássico = 2 colunas; moderno = coluna única |
| [na-cozinha/](na-cozinha/) | Artigos longos, tipografia editorial |

## Temas

- **Clássico editorial** — papel creme, filetes finos, numeração de capítulo, serif nos títulos dos tiles.
- **Moderno acolhedor** — fundo limpo, mais respiro, fotos maiores, sans nos tiles.

A preferência fica salva no navegador (`localStorage`, chave `demo-theme`).

## Voltar ao site atual

Use o link **Voltar ao site atual** na barra de prévia, ou abra [`../index.html`](../index.html).

## Arquivos

```
demo/
  index.html
  frango-na-pucara.html
  na-cozinha/
  css/demo.css
  js/theme.js
```

Alguns links do índice apontam para receitas reais em `../receitas/` (com o CSS antigo) — só para mostrar fotos reais nos tiles. A receita **Frango na Púcara** e os artigos em `na-cozinha/` usam o CSS da prévia.
