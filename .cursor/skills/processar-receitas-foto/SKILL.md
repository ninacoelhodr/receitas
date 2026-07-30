---
name: processar-receitas-foto
description: >-
  Analisa fotos, links ou texto completo de receitas (Telegram/entradas) e cria
  fichas HTML A5. Fonte processada: DELETAR. Foto de prato com curadoria.
  Use when processing entradas/pending or “processa entradas”.
---

# Processar foto / link / texto → ficha de receita

## Quando aplicar

Itens em `entradas/pending/`, ou pedido “processa entradas”.

## Tipos de entrada

| Arquivo | Origem | Como tratar |
|---------|--------|-------------|
| `.jpg` / `.png` / … (+ `.txt` de legenda) | Foto | Ler imagem; extrair receita |
| `*.link.txt` | Link | Fetch da URL; extrair receita |
| `*.recipe.txt` | Texto colado no Telegram | Ler o texto após `---`; estruturar ficha |

Formato `*.recipe.txt`:

```
from: telegram
update_id: 123
type: recipe_text
---
<título e corpo completo da receita>
```

## Regras obrigatórias

1. **Não embutir foto manuscrita/fonte** na ficha.
2. **Depois de processar → deletar a fonte** em `pending/` (foto, `.link.txt` ou
   `.recipe.txt`). Não arquivar em `processadas/`.
3. **Foto de referência do prato:** skill `curar-foto-prato` (~5 candidatas;
   senão sem foto).
4. **Duplicata:** completar ficha ou só deletar a entrada.
5. Texto incompleto → bom senso / receita clássica; marcar em notes.
6. Ficha compacta A5.

## Fluxo

```
Task Progress:
- [ ] Listar pending (fotos + *.link.txt + *.recipe.txt)
- [ ] Extrair receita (imagem / URL / texto)
- [ ] Duplicata? criar ou completar
- [ ] curar-foto-prato
- [ ] Atualizar index se nova
- [ ] DELETAR fonte em pending/
- [ ] Commit/push se pedido
```

### Texto completo (`*.recipe.txt`)

1. Ler o bloco depois de `---`.
2. Inferir título (1ª linha útil), categoria, ingredientes, preparo, meta.
3. Mesmo molde HTML das outras fichas; depois deletar o `.recipe.txt`.

### Links

1. `url:` (+ `note:` opcional).
2. Fetch após redirects; estruturar; deletar `.link.txt`.

### Nova receita

Categorias: `doces`, `salgados`, `tortas-salgadas`, `massas`, `carnes`,
`aves`, `frutos-do-mar`, `sopas`, `acompanhamentos`, `bebidas`.

(Sem `bolos` nem `outros` — bolos entram em doces; use a categoria mais
próxima em vez de “outros”.)

**Subcategorias** (quando a pasta tiver): em `p.category` use
`Categoria · Subcategoria` (ex.: `Doces · Musses`). O índice agrupa por esse
campo. Mapa:

| Categoria | Subcategorias |
|-----------|----------------|
| Doces | Biscoitos · Musses · Tortas e bolos · Outros doces |
| Salgados | Petiscos · Massas fritas/assadas · Outros |
| Carnes | Bovinos · Suínos · Outros |
| Aves | Frango · Outras aves |
| Frutos do mar | Peixes · Camarões e frutos · Massas com frutos do mar |

Sem subcategoria: Sopas, Acompanhamentos, Bebidas, Tortas salgadas, Massas
(massas com frutos do mar ficam em `frutos-do-mar`). No index: `<h3 class="subcategory">`
+ `data-subcategory` na lista (o JS monta o drill-down Categoria → Sub → receitas;
hash `#<categoria>/<sub-slug>`). Nav da ficha: link `../../index.html#<categoria>`.

**Categorias extras** (aparecer em mais de um lugar no índice, sem duplicar o
HTML da ficha):

1. Pasta / URL / nav primária / `p.category` = **categoria primária**.
2. Na ficha: `data-also="…"` no `<article>` **e** linha visível
   `<p class="category-also">Também em …</p>`; no nav, link também para o extra
   (`#categoria/sub` quando houver sub).
3. No index: `data-also` no `<li>` da entrada **primária** (o JS mostra
   “também em …” e clona se faltar). **Também** incluir o mesmo link
   (mesmo `href` da pasta primária) na lista da categoria extra — assim a
   dual listing aparece mesmo sem JS. Aceita `Categoria` ou `Categoria · Sub`.

## Molde (referência visual, só se curada)

```html
<figure class="dish-photo no-print">
  <img src="../../imagens/<slug>.jpg" alt="Referência: <nome>" />
  <figcaption>Referência visual (não é a foto da receita da família).</figcaption>
</figure>
```

CSS: `../../css/site.css` e `../../css/print.css`.

**Meu caderno:** o app no Railway injeta `caderno.css` / `config.js` / `caderno.js`
na home e nas fichas ao servir (botão **Entrar** no header). **Não** é preciso
incluir esses scripts no HTML da ficha. Após commit/push, o redeploy do Railway
publica a receita nova.
