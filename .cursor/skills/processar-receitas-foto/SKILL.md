---
name: processar-receitas-foto
description: >-
  Analisa fotos ou links de receitas (Telegram/entradas) e cria ou completa
  fichas HTML A5. Foto manuscrita nunca na ficha; foto de referência do prato
  (tela) é desejável. Use when processing entradas/pending, Telegram photos or
  links, fotos/, chat attachments, or “processa entradas”.
---

# Processar foto/link → ficha de receita

## Quando aplicar

Itens em `entradas/pending/` (fotos **ou** `*.link.txt`), `fotos/`, anexos do
chat, Telegram, ou pedido explícito (“processa entradas”).

## Tipos de entrada

| Arquivo | Origem | Como tratar |
|---------|--------|-------------|
| `.jpg` / `.png` / … (+ opcional `.txt` de legenda) | Foto no Telegram | Ler a imagem; extrair texto da receita |
| `*.link.txt` | Link no Telegram | Abrir/fetch a URL; extrair ingredientes e preparo |

Formato típico de `*.link.txt`:

```
url: https://...
note: Doces — opcional
from: telegram
update_id: 123
```

## Regras obrigatórias

1. **Não adicionar a foto manuscrita/fonte à receita.** Sem `source-photo`.
2. **Foto de referência do prato (desejável)** em `imagens/<slug>.jpg` +
   `figure.dish-photo.no-print` (só tela).
3. **Duplicata:** revisar/completar a ficha; se completa, só arquivar/deletar a
   entrada (foto ou `.link.txt`).
4. Texto incompleto → bom senso / receita clássica parecida; marcar em notes.
5. Ficha compacta para **uma página A5**.

## Fluxo

```
Task Progress:
- [ ] Listar entradas/pending (fotos + *.link.txt)
- [ ] Para cada item: ler foto OU fetch do link
- [ ] Buscar duplicata no índice / receitas/
- [ ] Criar OU completar ficha (+ dish-photo se possível)
- [ ] Atualizar index.html se receita nova
- [ ] Mover pending → processadas/ (ou deletar se só repetição completa)
- [ ] Commit/push se a usuária pediu / lote pedido
```

### Links

1. Ler `url:` do `.link.txt` (e `note:` se houver — categoria/nome).
2. Buscar o conteúdo (WebFetch / browser). Preferir página final após redirects
   (ex.: share.google).
3. Extrair título, ingredientes, modo de preparo, rendimento/tempo.
4. Seguir o mesmo molde HTML das outras fichas.

### Nova receita

Categorias: `bolos`, `doces`, `salgados`, `massas`, `carnes`, `aves`,
`frutos-do-mar`, `sopas`, `acompanhamentos`, `bebidas`, `outros`.

Criar `receitas/<categoria>/<slug>.html` + link no `index.html`.

## Molde (trecho foto de referência)

```html
<figure class="dish-photo no-print">
  <img src="../../imagens/<slug>.jpg" alt="Referência: <nome>" />
  <figcaption>Referência visual (não é a foto da receita da família).</figcaption>
</figure>
```

**Proibido:** embutir foto do caderno/Telegram.

CSS: `../../css/site.css` e `../../css/print.css`.
