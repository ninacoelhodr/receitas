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
   - a **foto** da receita (legenda opcional), **ou**
   - um **link** `https://...`, **ou**
   - o **texto completo** da receita (ingredientes + preparo).
2. Em até ~5 minutos (ou **Run workflow**) cai em `entradas/pending/`
   (imagem, `*.link.txt` ou `*.recipe.txt`).
3. No Cursor: **processa entradas**.

Fonte processada é **deletada**. Foto do caderno nunca na ficha; referência do
prato na tela só com curadoria (`curar-foto-prato`).

### Direto no chat

Envie foto, link ou texto da receita aqui.

Categorias: `doces`, `salgados`, `tortas-salgadas`, `massas`, `carnes`, `aves`, `frutos-do-mar`, `sopas`, `acompanhamentos`, `bebidas`.

## Publicação (GitHub Pages)

O site é estático na raiz do branch `main`. Em **Settings → Pages**:

- Source: Deploy from a branch
- Branch: `main` / `/ (root)`

## Desenvolvimento local

Não há build. Abra `index.html` direto no navegador ou sirva a pasta:

```bash
npx --yes serve .
```
