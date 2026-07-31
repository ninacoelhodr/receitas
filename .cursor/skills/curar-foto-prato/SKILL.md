---
name: curar-foto-prato
description: >-
  Curadoria da foto de referência do prato nas fichas A5: busca as 5 primeiras
  no Google Imagens pelo título, escolhe a mais bonita/apetitosa que cabe na
  receita e grava. Use when adding/replacing dish-photo, fixing missing/weird
  recipe images, or the user asks to curate/re-curate imagens/.
---

# Curar foto de referência do prato

## Objetivo

Cada ficha pode ter **uma** foto ilustrativa do prato pronto (`imagens/<slug>.jpg`
+ `figure.dish-photo.no-print`). Não é a foto do caderno da família.

**Meta:** a maioria das receitas deve ter foto. Tile vazio só em último caso.

## Critérios do usuário (seguir à risca)

1. Buscar no **Google Imagens** com o **título da receita** (query simples).
2. Pegar as **5 primeiras** candidatas distintas.
3. Olhar cada uma e escolher a que melhor cumpre:
   - **Cabe na descrição** — parece este prato (ingredientes/forma reconhecíveis)
   - **É bonita** — boa foto gastronômica, enquadramento ok
   - **Dá vontade de comer** — apetitosa, comida em evidência
4. **Colocar** a escolhida na ficha.
5. Só deixar **sem foto** se as 5 forem claramente ruins (embalagem, meme,
   diagrama, logo, pessoa cobrindo o prato, watermark gigante, ou prato
   totalmente outro). Na dúvida entre “meio serve” e “sem foto” → **coloca**.

Não exigir licença aberta / Wikimedia. Fonte tipicamente blogs e sites de receita.

## Quando aplicar

- Ao criar receita nova (depois do texto da ficha).
- “Corrigir fotos”, “curadoria”, “imagem estranha”, re-curar `imagens/`.
- Sempre que `processar-receitas-foto` pedir foto de referência.
- Lote de fichas sem `dish-photo` / sem `imagens/<slug>.jpg`.

## Fluxo

```
Task Progress:
- [ ] Ler título + ingredientes principais da ficha (o que o prato É)
- [ ] Buscar Google Imagens com o título (pt-BR; se fraco, tentar EN ou nome do prato)
- [ ] Baixar as 5 primeiras candidatas distintas
- [ ] Abrir/inspecionar as 5 (Read na imagem)
- [ ] Escolher a mais bonita + apetitosa + fiel; gravar
- [ ] Só omitir se nenhuma servir de verdade
```

### Busca

- Query = **título da receita** (ex. `Musse de amendoim`, `Torta de escarola com requeijão`).
- Se os 5 primeiros forem irrelevantes, refinar uma vez (ex. adicionar
  `receita`, nome clássico do prato, ou inglês: `four cheese lasagna`).
- Preferir fotos de prato pronto; evitar: embalagem, rótulo, print de revista
  ilegível, diagramas, arte sem comida real.
- Como obter URLs (prático no agente):

```bash
pip3 install -q ddgs   # se ainda não tiver
python3 << 'PY'
from ddgs import DDGS
q = "Título da receita"
with DDGS() as d:
    for i, r in enumerate(d.images(q, max_results=5)):
        print(i, r.get("image", ""))
PY
```

Baixar cada URL (`curl -L` / `urllib`), converter para JPEG se preciso (`sips`),
inspecionar com Read na imagem. Não usar screenshot da SERP.

### Escolha (obrigatório olhar as candidatas)

| Critério | Peso |
|----------|------|
| Dá vontade de comer / foto apetitosa | alto |
| Parece **este** prato | alto |
| Bonita (luz, enquadramento, comida preenchendo o quadro) | alto |
| Sem distrações graves (texto enorme, meme, mãos cobrindo tudo) | médio |

Aceitar watermark discreto se a comida estiver clara. Aceitar “próximo o bastante”
quando o prato for nichado (ex. musse com nome fantasia → musse do tipo certo).

### Aplicar

**Com foto (caso normal):**

1. Salvar como `imagens/<slug>.jpg` (JPEG; substituir se existir).
2. Garantir na ficha (após `h1`):

```html
<figure class="dish-photo no-print">
  <img src="../../imagens/<slug>.jpg" alt="Referência: <nome>" />
  <figcaption>Referência visual (não é a foto da receita da família).</figcaption>
</figure>
```

**Sem candidata boa (exceção):**

1. Remover `figure.dish-photo` da ficha (se houver).
2. Apagar `imagens/<slug>.jpg` se existir.
3. Não deixar `img` quebrada.

Não é obrigatório registrar crédito em `imagens/ATTRIBUTION.md` para hits do Google
(só manter/atualizar se a fonte for Wikimedia ou o usuário pedir).

### Re-curadoria em lote

Processar por categoria ou lista de slugs; pode paralelizar. Resumir ao final:
colocadas / trocadas / ainda sem foto (com motivo curto).

## Não fazer

- Não embutir foto manuscrita/Telegram (`source-photo`).
- Não inventar que a imagem “é da família”.
- Não aceitar a 1ª hit sem olhar as 5.
- Não deixar dezenas de fichas sem foto por rigor excessivo de licença ou
  matching perfeito.
