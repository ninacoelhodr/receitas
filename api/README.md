# API do livro de receitas (Railway)

App Express que:

1. Serve o site estático (HTML A5, CSS, JS, imagens) a partir da raiz do repo
2. Expõe autenticação e metadados pessoais (`recipe_meta`) em Postgres

## Variáveis de ambiente

| Variável | Obrigatória | Descrição |
|----------|-------------|-----------|
| `DATABASE_URL` | sim | Connection string Postgres |
| `SESSION_SECRET` | sim | Segredo para assinar o cookie JWT |
| `ADMIN_EMAIL` | sim (seed) | E-mail do usuário inicial |
| `ADMIN_PASSWORD` | sim (seed) | Senha do usuário inicial (hash no 1º boot) |
| `PORT` | não | Padrão `3000` (Railway injeta) |
| `SITE_ROOT` | não | Pasta do site; padrão `../` (raiz do repo) |
| `DATABASE_SSL` | não | `false` em local; em produção Railway deixa o padrão |
| `COOKIE_SECURE` | não | Em produção use cookies `Secure` |
| `NODE_ENV` | não | `production` no Railway |

O admin só é **criado** se ainda não existir. Trocar a senha depois exige update no banco ou novo e-mail.

## Endpoints

- `GET /health`
- `POST /api/auth/login` `{ email, password }`
- `POST /api/auth/logout`
- `GET /api/auth/me`
- `GET /api/recipes/:slug/meta` (auth) — slug com `/`, ex. `doces/bolo-de-cenoura`
- `PUT /api/recipes/:slug/meta` (auth) `{ status?, rating?, notes? }`

Status: `quero_fazer` \| `ja_fiz` \| `null`. Rating 1–5 só faz sentido com `ja_fiz`.

## Local

```bash
# Postgres local + .env a partir de .env.example
cd api
npm install
# defina DATABASE_URL, SESSION_SECRET, ADMIN_* 
npm run dev
```

Abra `http://localhost:3000`.

## Deploy

O `railway.toml` na **raiz do repo** faz build/start em `api/` e inclui o restante do site no deploy (HTML, imagens, etc.). Após `git push`, se o serviço estiver ligado ao GitHub, o Railway redeploya e as fichas novas (Telegram → Cursor → commit) passam a ser servidas.
