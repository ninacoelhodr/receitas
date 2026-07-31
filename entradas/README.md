# Entradas (fotos, links e texto)

Itens do bot Telegram caem em [`pending/`](pending/).

## O que enviar no bot

1. **Foto** da receita ou da dica (legenda opcional).
2. **Link** `https://...`.
3. **Texto** completo — receita (ingredientes + preparo) **ou** artigo/dica
   (ex.: técnicas, conservação).

## Fluxo

1. Envie no [@Receitasnina_bot](https://t.me/Receitasnina_bot).
2. O Actions grava em `pending/` (imagem, `*.link.txt` ou `*.recipe.txt`).
3. No Cursor: **processar dados** (skill `processar-dados`).
4. O agente classifica:
   - **Receita** → ficha A5 em `receitas/`
   - **Na cozinha** → artigo em `na-cozinha/`
5. Depois de gravar, a **fonte é deletada**.
