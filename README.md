# Livro de Receitas

Site estático com fichas de receita em **A5**, prontas para imprimir e guardar no fichário.

- Online: https://ninacoelhodr.github.io/receitas/
- Conta / repo: [ninacoelhodr/receitas](https://github.com/ninacoelhodr/receitas)

## Como usar

1. Abra o site (ou `index.html` no navegador).
2. Busque ou escolha a receita na categoria.
3. Na tela, a ficha mostra uma **foto de referência** do prato (ilustrativa).
4. Clique em **Imprimir** (ou Ctrl+P / Cmd+P) — a foto **não** sai na folha A5.
5. Selecione papel **A5** e imprima uma página por receita.


A margem esquerda é um pouco maior para o furo do fichário.

## Adicionar uma receita nova

### Pelo Telegram (recomendado no celular)

1. Abra o bot ([@Receitasnina_bot](https://t.me/Receitasnina_bot)) e envie:
   - a **foto** da receita (legenda opcional com categoria/nome), **ou**
   - um **link** `https://...` de receita na internet (share.google, blog, etc.).
2. Em até ~5 minutos (ou **Run workflow** em Actions → Telegram → entradas) o
   item aparece em `entradas/pending/` (fotos ou `*.link.txt`).
3. No Cursor, diga: **processa entradas**.

Ao processar: ignorar entradas repetidas; completar lacunas com bom senso.
Foto do caderno nunca na ficha; foto de referência do prato (tela) sim.

### Direto no chat

Envie a foto ou o link aqui. O fluxo é:

1. Transcrição e estruturação (título, categoria, ingredientes, modo de preparo).
2. Criação de `receitas/<categoria>/<slug>.html` no molde A5.
3. Atualização do `index.html`.
4. Commit/push quando você pedir.

Categorias: `bolos`, `doces`, `salgados`, `massas`, `carnes`, `aves`, `frutos-do-mar`, `sopas`, `acompanhamentos`, `bebidas`, `outros`.

## Publicação (GitHub Pages)

O site é estático na raiz do branch `main`. Em **Settings → Pages**:

- Source: Deploy from a branch
- Branch: `main` / `/ (root)`

## Desenvolvimento local

Não há build. Abra `index.html` direto no navegador ou sirva a pasta:

```bash
npx --yes serve .
```
