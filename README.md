# Livro de Receitas

Site estático com fichas de receita em **A5**, prontas para imprimir e guardar no fichário.

- Online: https://ninacoelhodr.github.io/receitas/
- Conta / repo: [ninacoelhodr/receitas](https://github.com/ninacoelhodr/receitas)

## Como usar

1. Abra o site (ou `index.html` no navegador).
2. Escolha a receita na categoria.
3. Clique em **Imprimir** (ou Ctrl+P / Cmd+P).
4. No diálogo de impressão, selecione papel **A5** (ou “Ajustar à página” se a impressora não listar A5) e imprima **uma página** por receita.

A margem esquerda é um pouco maior para o furo do fichário.

## Adicionar uma receita nova

Envie a foto da receita no chat (com o agente neste repositório). O fluxo é:

1. Transcrição e estruturação (título, categoria, ingredientes, modo de preparo).
2. Criação de `receitas/<categoria>/<slug>.html` no molde A5.
3. Atualização do `index.html`.
4. Commit/push quando você pedir.

Categorias: `bolos`, `doces`, `salgados`, `massas`, `carnes`, `aves`, `sopas`, `acompanhamentos`, `bebidas`, `outros`.

## Publicação (GitHub Pages)

O site é estático na raiz do branch `main`. Em **Settings → Pages**:

- Source: Deploy from a branch
- Branch: `main` / `/ (root)`

## Desenvolvimento local

Não há build. Abra `index.html` direto no navegador ou sirva a pasta:

```bash
npx --yes serve .
```
