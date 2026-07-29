---
name: processar-receitas-foto
description: >-
  Analisa fotos de receitas e cria ou completa fichas HTML A5 no livro
  (receitas/<categoria>/<slug>.html + index.html). Foto manuscrita nunca vai
  na ficha; foto de referência do prato pronto (tela) é desejável.
  Use when processing recipe photos from Telegram, entradas/pending/, fotos/,
  chat attachments, or when the user says processa entradas / processar fotos.
---

# Processar foto → ficha de receita

## Quando aplicar

Fotos em `entradas/pending/`, `fotos/`, anexos do chat, Telegram, ou pedido
explícito (“processa entradas”, “processar esta foto”).

## Regras obrigatórias

1. **Não adicionar a foto manuscrita/fonte à receita.** Sem `source-photo`, sem
   `<img>` da foto do caderno/Telegram. Essa foto é só origem do texto; depois
   move para `entradas/processadas/` ou apaga.
2. **Foto de referência do prato (desejável).** Depois de criar/completar a
   ficha, incluir (se possível) uma imagem ilustrativa do **prato pronto** —
   de uso livre (Wikimedia Commons, etc.) ou gerada — em
   `imagens/<slug>.jpg` + bloco `figure.dish-photo.no-print` na ficha.
   Só na tela (classe `no-print`); não sai na impressão A5. Legenda curta
   tipo “Referência visual (não é a foto da receita da família).”
3. **Foto repetida** (mesma receita já em `index.html` / `receitas/`):
   - Revisar a ficha existente.
   - Se faltar algo → completar a ficha (e a referência visual se ainda não
     houver).
   - Se estiver completa → **só deletar a foto fonte** (não recriar ficha).
4. Várias fotos do mesmo cartão/página → **uma** receita; preferir a mais
   legível.
5. Texto cortado/ilegível → completar com bom senso ou receita clássica
   parecida. Marcar o inferido em `<p class="notes">`.
6. Ficha compacta para **uma página A5** (a foto de referência não conta —
   some na impressão).

## Fluxo

```
Task Progress:
- [ ] Ler a foto fonte e extrair título, ingredientes, preparo, meta
- [ ] Buscar duplicata no índice / receitas/
- [ ] Criar OU completar ficha (nunca embutir a foto fonte)
- [ ] Garantir foto de referência do prato (imagens/ + dish-photo)
- [ ] Atualizar index.html se receita nova
- [ ] Mover pending → processadas/ OU deletar se só repetição completa
- [ ] Commit/push só se a usuária pedir (ou lote que ela mandou processar)
```

### Nova receita

1. Categoria: `bolos`, `doces`, `salgados`, `massas`, `carnes`, `aves`,
   `frutos-do-mar`, `sopas`, `acompanhamentos`, `bebidas`, `outros`.
2. Criar `receitas/<categoria>/<slug>.html` no molde (com `dish-photo` se
   houver imagem).
3. Link em `index.html` na categoria.
4. Se veio de `entradas/pending/`, mover a fonte para `processadas/`.

### Receita já existente

1. Comparar ficha com a foto fonte.
2. Completar lacunas se necessário.
3. Se nada a acrescentar: **deletar a foto fonte** e parar.

## Molde da ficha

Depois de `div.meta` (ou do `h1` se não houver meta):

```html
<figure class="dish-photo no-print">
  <img src="../../imagens/<slug>.jpg" alt="Referência: <nome do prato>" />
  <figcaption>Referência visual (não é a foto da receita da família).</figcaption>
</figure>
```

Campos: `p.category`, `h1`, `div.meta`, dish-photo, ingredientes, passos, notes.

**Proibido:** `<section class="source-photo">` e `<img>` da foto manuscrita.

CSS: `../../css/site.css` e `../../css/print.css`.
