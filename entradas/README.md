# Entradas (fotos e links)

Itens enviados ao bot do Telegram caem em [`pending/`](pending/).

## O que enviar no bot

1. **Foto** da receita (legenda opcional: categoria ou nome).
2. **Link** de uma receita na internet (`https://...` — share.google, blog, etc.).

## Fluxo

1. Envie foto ou link no [@Receitasnina_bot](https://t.me/Receitasnina_bot).
2. Em até ~5 minutos (ou após **Run workflow**), o Actions grava em `pending/`:
   - fotos: `*.jpg` / `*.png` (+ `*.txt` de legenda)
   - links: `*.link.txt` com o URL
3. No Cursor, diga: **processa entradas**.

Arquivos processados vão para [`processadas/`](processadas/).
