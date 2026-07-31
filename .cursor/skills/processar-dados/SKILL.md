---
name: processar-dados
description: >-
  Classifica entradas (foto, link ou texto) em receita A5 ou artigo Na cozinha,
  grava no lugar certo e apaga a fonte. Use when the user says “processar dados”,
  “processa entradas”, or there are mixed items in entradas/pending/.
---

# Processar dados (receita ou Na cozinha)

## Quando aplicar

- Pedido **processar dados** ou **processa entradas**
- Itens em `entradas/pending/`
- Foto, link ou texto colado no chat (receita **ou** dica/técnica)

Esta skill é a **entrada única**. Não misturar: classificar primeiro, depois
rotear.

## Tipos de entrada

| Arquivo / origem | Como tratar |
|------------------|-------------|
| `.jpg` / `.png` / … (+ `.txt` de legenda) | Ler imagem; extrair conteúdo |
| `*.link.txt` | Fetch da URL; extrair conteúdo |
| `*.recipe.txt` | Ler bloco após `---`; estruturar |
| Anexo / texto no chat | Tratar como a fonte direta |

Formato `*.recipe.txt` (Telegram):

```
from: telegram
update_id: 123
type: recipe_text
---
<body>
```

O nome `recipe_text` **não** decide o destino — o conteúdo decide.

## Classificação

| Destino | Sinais |
|---------|--------|
| **Receita** | Lista de ingredientes com quantidades + modo de preparo (passos, forno, etc.) |
| **Na cozinha** | Dica, técnica, guia, conservação, organização (ex.: “a arte de congelar”) — sem ficha de prato |

Em **dúvida**: perguntar uma linha antes de gravar.

## Fluxo

```
Task Progress:
- [ ] Listar fontes (pending + anexos do chat)
- [ ] Classificar cada item (receita | Na cozinha | dúvida)
- [ ] Receita → skill processar-receitas-foto (ficha + index + foto)
- [ ] Artigo → criar na-cozinha/<slug>.html + atualizar na-cozinha/index.html
- [ ] DELETAR fonte processada em pending/ (não arquivar)
- [ ] Commit/push se pedido
```

### Receita

Seguir a skill `processar-receitas-foto` (molde A5, categorias, `curar-foto-prato`,
`index.html`). Não duplicar essas regras aqui.

No nav da ficha nova, incluir também:

```html
<a href="../../na-cozinha/">Na cozinha</a>
```

### Artigo (Na cozinha)

1. Inferir título (1ª linha útil) e slug (`kebab-case`, sem acento).
2. Criar `na-cozinha/<slug>.html` com o molde abaixo.
3. Em `na-cozinha/index.html`: remover o `<li class="empty">` se existir; acrescentar

```html
<li>
  <a href="./<slug>.html"><Título></a>
</li>
```

4. Foto opcional (não obrigatória; sem `curar-foto-prato` por padrão).
5. Sem botão Imprimir A5 e sem Meu caderno.
6. Deletar a fonte em `pending/`.

## Molde do artigo

```html
<!DOCTYPE html>
<html lang="pt-BR">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title><Título> — Na cozinha</title>
    <meta name="description" content="<resumo curto>" />
    <link rel="stylesheet" href="../css/site.css" />
    <link rel="stylesheet" href="../css/print.css" />
  </head>
  <body>
    <header class="site-header no-print">
      <a class="brand" href="../index.html">Livro de Receitas</a>
      <nav class="site-nav" aria-label="Principal">
        <a href="../index.html">Início</a>
        <a href="../index.html#categorias">Categorias</a>
        <a href="./">Na cozinha</a>
      </nav>
    </header>

    <main class="tip-page">
      <div class="tip-actions no-print">
        <a class="btn btn-ghost" href="./">← Voltar</a>
      </div>

      <article class="tip-article">
        <p class="eyebrow">Na cozinha</p>
        <h1><Título></h1>
        <!-- parágrafos, h2/h3, ul/ol conforme o texto -->
      </article>
    </main>
  </body>
</html>
```

CSS: classes `.tip-page`, `.tip-article`, `.tip-actions`, `.eyebrow` em
`css/site.css`.

## Regras

1. Classificar **antes** de escrever arquivos.
2. Fonte processada → **deletar** (foto, `.link.txt`, `.recipe.txt`).
3. Não embutir foto manuscrita/Telegram no HTML.
4. Duplicata de artigo: completar ou só deletar a entrada.
5. Commit/push só se a usuária pedir ou ao fechar o lote combinado.
