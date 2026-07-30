---
name: processar-receitas-foto
description: >-
  Analisa fotos ou links de receitas (Telegram/entradas) e cria ou completa
  fichas HTML A5. Foto manuscrita nunca na ficha; foto de referência do prato
  com curadoria. Fonte processada: DELETAR. Use when processing
  entradas/pending, Telegram, or “processa entradas”.
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

## Regras obrigatórias

1. **Não adicionar a foto manuscrita/fonte à receita.** Sem `source-photo`.
2. **Depois de processar → deletar a fonte.** Quando a foto/link já virou
   (ou atualizou) a ficha, **apagar** o arquivo em `entradas/pending/` (e
   legenda `.txt` junto). **Não** arquivar em `processadas/`. O certo é ir
   deletando as fotos que já foram processadas.
3. **Foto de referência do prato.** Skill `.cursor/skills/curar-foto-prato/`:
   ~5 candidatas → a que mais bate (boa composição); senão **sem foto**.
4. **Duplicata:** revisar/completar a ficha; se completa, **só deletar** a
   entrada fonte.
5. Texto incompleto → bom senso / receita clássica; marcar em notes.
6. Ficha compacta para **uma página A5**.

## Fluxo

```
Task Progress:
- [ ] Listar entradas/pending (fotos + *.link.txt)
- [ ] Para cada item: ler foto OU fetch do link
- [ ] Buscar duplicata no índice / receitas/
- [ ] Criar OU completar ficha
- [ ] Foto do prato via **curar-foto-prato** (5 candidatas → melhor ou sem)
- [ ] Atualizar index.html se receita nova
- [ ] DELETAR a fonte em pending/ (já virou receita)
- [ ] Commit/push se a usuária pediu / lote pedido
```

### Links

1. Ler `url:` do `.link.txt` (e `note:` se houver).
2. Fetch da URL (após redirects).
3. Extrair título, ingredientes, preparo, meta.
4. Seguir o molde HTML; depois **deletar** o `.link.txt`.

### Nova receita

Categorias: `bolos`, `doces`, `salgados`, `massas`, `carnes`, `aves`,
`frutos-do-mar`, `sopas`, `acompanhamentos`, `bebidas`, `outros`.

Criar `receitas/<categoria>/<slug>.html` + link no `index.html`.

## Molde (foto de referência, só se curada)

```html
<figure class="dish-photo no-print">
  <img src="../../imagens/<slug>.jpg" alt="Referência: <nome>" />
  <figcaption>Referência visual (não é a foto da receita da família).</figcaption>
</figure>
```

**Proibido:** embutir foto do caderno/Telegram; guardar fontes processadas.

CSS: `../../css/site.css` e `../../css/print.css`.
