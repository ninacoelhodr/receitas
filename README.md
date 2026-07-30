# Livro de Receitas

Fichas de receita em **A5**, prontas para imprimir, com um **caderno pessoal**
(quero fazer / já fiz, estrelas e notas) por usuário.

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

### Meu caderno

No site (home ou ficha), use **Entrar** / **Meu caderno** no canto do header.
Nas fichas, o painel também fica sob os botões Voltar/Imprimir (só na tela):

- Status: *Quero fazer* / *Já fiz* / limpar
- Nota de 1 a 5 estrelas (quando *Já fiz*)
- Notas livres (ex.: “coloquei menos açúcar”)

**Login:** use o e-mail e a senha configurados em `ADMIN_EMAIL` / `ADMIN_PASSWORD`
no serviço Railway (usuário criado no primeiro boot). Sessão via cookie httpOnly.

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
e navega em três níveis: categorias → subcategorias → lista (hash `#doces/musses`).
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
