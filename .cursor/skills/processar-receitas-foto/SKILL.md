---
name: processar-receitas-foto
description: >-
  Analisa fotos de receitas e cria ou completa fichas HTML A5 no livro
  (receitas/<categoria>/<slug>.html + index.html), sem embutir a foto na ficha.
  Use when processing recipe photos from Telegram, entradas/pending/, fotos/,
  chat attachments, or when the user says processa entradas / processar fotos.
---

# Processar foto → ficha de receita

## Quando aplicar

Fotos em `entradas/pending/`, `fotos/`, anexos do chat, Telegram, ou pedido
explícito (“processa entradas”, “processar esta foto”).

## Regras obrigatórias

1. **Não adicionar a foto à receita.** Sem seção `source-photo`, sem `<img>` da
   foto original na ficha. A foto é só origem do texto; depois de usada, move
   ou apaga conforme o fluxo abaixo.
2. **Foto repetida** (mesma receita já em `index.html` / `receitas/`):
   - Revisar a ficha existente.
   - Se faltar algo → completar a ficha.
   - Se estiver completa → **só deletar a foto** (não recriar ficha, não
     duplicar no índice).
3. Várias fotos do mesmo cartão/página (espelho, ângulo, verso vazio) → tratar
   como **uma** receita; preferir a imagem mais legível.
4. Texto cortado/ilegível → completar com bom senso de cozinha ou receita
   clássica parecida (sem inventar outro prato). Marcar o que foi inferido em
   `<p class="notes">`.
5. Ficha compacta: cabe em **uma página A5** (ingredientes, preparo, dicas
   curtas).

## Fluxo

```
Task Progress:
- [ ] Ler a foto e extrair título, ingredientes, preparo, meta
- [ ] Buscar duplicata no índice / receitas/
- [ ] Criar OU completar ficha (nunca embutir foto)
- [ ] Atualizar index.html se receita nova
- [ ] Mover pending → processadas/ OU deletar se só repetição completa
- [ ] Commit/push só se a usuária pedir (ou lote que ela mandou processar)
```

### Nova receita

1. Escolher categoria: `bolos`, `doces`, `salgados`, `massas`, `carnes`,
   `aves`, `frutos-do-mar`, `sopas`, `acompanhamentos`, `bebidas`, `outros`.
2. Criar `receitas/<categoria>/<slug>.html` no molde abaixo (sem foto).
3. Incluir link em `index.html` na seção da categoria (ordem alfabética por
   título, se já houver lista ordenada).
4. Se veio de `entradas/pending/`, mover a foto para `entradas/processadas/`.

### Receita já existente

1. Abrir a ficha e comparar com a foto.
2. Completar lacunas se necessário.
3. Se nada a acrescentar: **deletar a foto** (pending ou o arquivo bruto) e
   parar. Não alterar o índice só por causa da foto.

## Molde da ficha (sem foto)

Copiar estrutura de fichas existentes (ex. `receitas/bolos/bolo-de-cenoura.html`).
Campos típicos:

- `p.category`, `h1`, `div.meta` (rendimento / tempo)
- `h2` + `ul.ingredients`
- `h2` + `ol.steps`
- opcional: `p.notes` com observações

**Proibido:** `<section class="source-photo">` e qualquer `<img>` da fonte.

CSS: `../../css/site.css` e `../../css/print.css`. Links do header/voltar para
`../../index.html` (e âncora da categoria).

## Depois do lote

Commit e push quando a usuária pedir, ou ao concluir um lote que ela mandou
processar. Mensagem clara (ex.: qual receita foi criada/completada).
