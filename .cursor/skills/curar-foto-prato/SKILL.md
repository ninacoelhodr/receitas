---
name: curar-foto-prato
description: >-
  Curadoria da foto de referência do prato nas fichas A5: busca várias
  candidatas, escolhe a que mais bate com a receita (composição ok), ou remove
  a foto se nenhuma servir. Use when adding/replacing dish-photo, fixing weird
  recipe images, or the user asks to curate/re-curate imagens/.
---

# Curar foto de referência do prato

## Objetivo

Cada ficha pode ter **uma** foto ilustrativa do prato pronto (`imagens/<slug>.jpg`
+ `figure.dish-photo.no-print`). Não é a foto do caderno da família.

Critérios do usuário (seguir à risca):

- Pegar **~5 imagens** candidatas e ver **qual mais bate com a receita**.
- Se **nenhuma** realmente bater → **deixar sem foto** (melhor que imagem estranha).
- Evitar foto **mal enquadrada** (corte ruim, assunto minúsculo, só embalagem,
  meme, diagrama, pessoa cobrindo o prato, watermark gigante).

## Quando aplicar

- Ao criar receita nova (depois do texto da ficha).
- “Corrigir fotos”, “curadoria”, “imagem estranha”, re-curar `imagens/`.
- Sempre que `processar-receitas-foto` pedir foto de referência.

## Fluxo

```
Task Progress:
- [ ] Ler título + ingredientes principais da ficha (o que o prato É)
- [ ] Montar 1–3 queries de busca específicas (prato + técnica + idioma útil)
- [ ] Baixar/obter até 5 candidatas distintas
- [ ] Abrir/inspecionar as 5 (Read na imagem)
- [ ] Escolher a melhor OU descartar todas
- [ ] Gravar imagens/<slug>.jpg + dish-photo na ficha, OU remover foto e bloco HTML
```

### Busca

- Preferir Wikimedia Commons (licença aberta) via API `generator=search` +
  `imageinfo` (thumb ~960px). `User-Agent` identificável do projeto.
- Queries **específicas**: ex. `spaghetti alle vongole`, `carrot cake slice`,
  `oxtail stew bowl` — não termos genéricos tipo `food`, `dinner`, `meat`.
- Evitar resultados que sejam: logo de marca, embalagem, rótulo, captura de
  revista sem comida clara, artes sem comida real.

### Escolha (obrigatório olhar as candidatas)

Pontuar mentalmente cada candidata:

| Critério | Peso |
|----------|------|
| Parece **este** prato (ingredientes/forma reconhecíveis) | alto |
| Comida em evidência, boa foto gastronômica | alto |
| Enquadramento: prato preenche bem o quadro, sem cortes estranhos | alto |
| Sem distrações (texto enorme, pessoas, meme) | médio |

**Regra de ouro:** na dúvida entre “meio parece” e “sem foto” → **sem foto**.

Não escolher só porque “é comida” ou “é do mesmo país”.

### Aplicar

**Com foto boa:**

1. Salvar como `imagens/<slug>.jpg` (substituir se existir).
2. Garantir na ficha (após `meta` ou `h1`):

```html
<figure class="dish-photo no-print">
  <img src="../../imagens/<slug>.jpg" alt="Referência: <nome>" />
  <figcaption>Referência visual (não é a foto da receita da família).</figcaption>
</figure>
```

**Sem candidata boa:**

1. Remover `figure.dish-photo` da ficha (se houver).
2. Apagar `imagens/<slug>.jpg` se existir.
3. Não deixar `img` quebrada.

### Re-curadoria em lote

Para muitas fichas: processar por categoria ou lista de slugs; commitar em
lotes se o push ficar grande. Resumir ao final: trocadas / removidas /
mantidas.

## Não fazer

- Não embutir foto manuscrita/Telegram (`source-photo`).
- Não inventar que a imagem “é da família”.
- Não aceitar a primeira hit da busca sem comparar as 5.
