# Entradas (fotos, links e texto)

Itens do bot Telegram caem em [`pending/`](pending/).

## O que enviar no bot

1. **Foto** da receita (legenda opcional).
2. **Link** `https://...` de uma receita.
3. **Texto completo** da receita (título, ingredientes, modo de preparo).

## Fluxo

1. Envie no [@Receitasnina_bot](https://t.me/Receitasnina_bot).
2. O Actions grava em `pending/` (imagem, `*.link.txt` ou `*.recipe.txt`).
3. No Cursor: **processa entradas**.
4. Depois que vira ficha, a **fonte é deletada**.
