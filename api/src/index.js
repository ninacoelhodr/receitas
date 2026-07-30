const path = require("path");
const fs = require("fs");
const express = require("express");
const cookieParser = require("cookie-parser");
const { migrate } = require("./db");
const { ensureAdminUser } = require("./auth");
const authRoutes = require("./routes/auth");
const recipeRoutes = require("./routes/recipes");

const PORT = Number(process.env.PORT) || 3000;
const SITE_ROOT = path.resolve(
  process.env.SITE_ROOT || path.join(__dirname, "..", "..")
);
const RECEITAS_ROOT = path.join(SITE_ROOT, "receitas");

const CADERNO_INJECT = `
<link rel="stylesheet" href="/css/caderno.css" />
<script src="/js/config.js" defer></script>
<script src="/js/caderno.js" defer></script>
`;

const app = express();

app.set("trust proxy", 1);
app.use(express.json({ limit: "64kb" }));
app.use(cookieParser());

app.get("/health", (_req, res) => {
  res.json({ ok: true });
});

app.use("/api/auth", authRoutes);
app.use("/api/recipes", recipeRoutes);

function sendHtmlWithCaderno(res, filePath) {
  let html = fs.readFileSync(filePath, "utf8");
  if (!html.includes("caderno.js")) {
    if (/<\/body>/i.test(html)) {
      html = html.replace(/<\/body>/i, `${CADERNO_INJECT}</body>`);
    } else {
      html += CADERNO_INJECT;
    }
  }
  res.type("html").send(html);
}

function serveIndexWithCaderno(_req, res, next) {
  const filePath = path.join(SITE_ROOT, "index.html");
  if (!fs.existsSync(filePath) || !fs.statSync(filePath).isFile()) {
    return next();
  }
  return sendHtmlWithCaderno(res, filePath);
}

app.get("/", serveIndexWithCaderno);
app.get("/index.html", serveIndexWithCaderno);

app.use((req, res, next) => {
  if (req.method !== "GET" && req.method !== "HEAD") return next();
  if (!req.path.startsWith("/receitas/")) return next();
  if (!/\.html$/i.test(req.path)) return next();

  try {
    const rel = decodeURIComponent(req.path.slice("/receitas/".length));
    const filePath = path.normalize(path.join(RECEITAS_ROOT, rel));
    if (!filePath.startsWith(RECEITAS_ROOT)) {
      return res.status(400).send("Caminho inválido");
    }
    if (!fs.existsSync(filePath) || !fs.statSync(filePath).isFile()) {
      return next();
    }
    return sendHtmlWithCaderno(res, filePath);
  } catch (err) {
    return next(err);
  }
});

app.use(
  express.static(SITE_ROOT, {
    extensions: ["html"],
    index: ["index.html"],
    setHeaders(res, filePath) {
      if (filePath.endsWith(".html")) {
        res.setHeader("Cache-Control", "no-cache");
      }
    },
  })
);

app.use((err, _req, res, _next) => {
  console.error(err);
  res.status(500).json({ error: "Erro interno" });
});

async function start() {
  if (!process.env.DATABASE_URL) {
    console.warn("[boot] DATABASE_URL ausente — API de caderno pode falhar.");
  } else {
    await migrate();
    await ensureAdminUser();
  }

  if (!fs.existsSync(path.join(SITE_ROOT, "index.html"))) {
    console.warn(`[boot] index.html não encontrado em ${SITE_ROOT}`);
  } else {
    console.log(`[boot] Site estático: ${SITE_ROOT}`);
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`[boot] Listening on :${PORT}`);
  });
}

start().catch((err) => {
  console.error("[boot] Falha ao iniciar:", err);
  process.exit(1);
});
