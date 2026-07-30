# Livro de Receitas

Fichas de receita em **A5**, prontas para imprimir. O livro é **público**
(navegar, abrir, ler e imprimir sem login). O **caderno pessoal** (quero fazer /
já fiz, estrelas e notas) é opcional e exige login.

- **Site (Railway):** https://web-production-7896c2.up.railway.app/
- Conta / repo: [ninacoelhodr/receitas](https://github.com/ninacoelhodr/receitas)
- GitHub Pages (legado): https://ninacoelhodr.github.io/receitas/ — pode desligar
  depois que a URL do Railway estiver estável

## Como usar

1. Abra o site no Railway.
2. Busque ou escolha a receita na categoria.
3. Na tela, a ficha mostra uma **foto de referência** do prato (ilustrativa).
4. Clique em **Imprimir** (ou Ctrl+P / Cmd+P) — a foto e o painel **Meu caderno**
   **não** saem na folha A5.
5. Selecione papel **A5** e imprima uma página por receita.

### Meu caderno (só acompanhamento pessoal)

Receitas **não** pedem login. Use **Entrar** / **Meu caderno** no header (ou o
atalho na ficha) apenas para marcar o que você quer fazer / já fez:

- Status: *Quero fazer* / *Já fiz* / limpar
- Nota de 1 a 5 estrelas (quando *Já fiz*)
- Notas livres (ex.: “coloquei menos açúcar”)

Deslogada, a ficha continua legível; o formulário de login só aparece ao clicar
**Entrar**. Credenciais: `ADMIN_EMAIL` / `ADMIN_PASSWORD` no Railway (usuário
criado no primeiro boot). Sessão via cookie httpOnly.

A margem esquerda é um pouco maior para o furo do fichário.

## Adicionar uma receita nova

### Pelo Telegram (recomendado no celular) — inalterado

1. Abra o bot ([@Receitasnina_bot](https://t.me/Receitasnina_bot)) e envie:
   - a **foto** da receita (legenda opcional), **ou**
   - um **link** `https://...`, **ou**
   - o **texto completo** da receita (ingredientes + preparo).
2. Em até ~5 minutos (ou **Run workflow**) cai em `entradas/pending/`
   (imagem, `*.link.txt` ou `*.recipe.txt`).
3. No Cursor: **processa entradas**.
4. Commit/push no GitHub → o Railway redeploya e a ficha nova fica online.

Fonte processada é **deletada**. Foto do caderno nunca na ficha; referência do
prato na tela só com curadoria (`curar-foto-prato`).

O fluxo Telegram → GitHub Actions → Cursor **não muda**: continua gravando HTML
no repo. O app no Railway só **serve** esse conteúdo no deploy.

### Direto no chat

Envie foto, link ou texto da receita aqui.

Categorias: `doces`, `salgados`, `tortas-salgadas`, `massas`, `carnes`, `aves`, `frutos-do-mar`, `sopas`, `acompanhamentos`, `bebidas`.

Nas pastas com subcategorias, a ficha usa `Categoria · Subcategoria` em
`p.category` (ex.: `Doces · Musses`); o índice agrupa sob `<h3 class="subcategory">`
e o índice na home mostra subcategorias (ou receitas diretas se não houver sub);
clique na sub abre a lista (`#doces/musses`).
Categorias sem sub (Massas, Sopas, etc.) abrem a lista direto.

## Arquitetura

| Parte | Onde |
|-------|------|
| Fichas HTML A5, CSS, imagens, índice, busca | Repo (site estático) |
| Servidor + API do caderno | `api/` (Express) no **Railway** |
| Postgres (`users`, `recipe_meta`) | Railway |
| Import Telegram | GitHub Actions + `scripts/telegram-import.sh` |
| Processar / curar fotos | Skills Cursor |

Detalhes da API e variáveis: [`api/README.md`](api/README.md).

## Desenvolvimento local

```bash
cd api
cp .env.example .env   # ajuste DATABASE_URL, SESSION_SECRET, ADMIN_*
npm install
npm run dev
```

Abra `http://localhost:3000`. O servidor serve a raiz do repo e injeta o painel
Meu caderno nas fichas em `/receitas/**/*.html`.

Só o front estático (sem caderno): `npx --yes serve .`
