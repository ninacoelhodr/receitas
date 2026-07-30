const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");
const { query } = require("./db");

const COOKIE_NAME = "receitas_session";
const TOKEN_TTL = "30d";

function getSecret() {
  const secret = process.env.SESSION_SECRET;
  if (!secret) {
    throw new Error("SESSION_SECRET is required");
  }
  return secret;
}

function cookieOptions() {
  const secure =
    process.env.COOKIE_SECURE === "true" ||
    process.env.NODE_ENV === "production";
  // Same-origin (site + API no Railway): SameSite=lax basta.
  return {
    httpOnly: true,
    secure,
    sameSite: "lax",
    maxAge: 30 * 24 * 60 * 60 * 1000,
    path: "/",
  };
}

function signToken(user) {
  return jwt.sign(
    { sub: user.id, email: user.email },
    getSecret(),
    { expiresIn: TOKEN_TTL }
  );
}

function setSessionCookie(res, user) {
  res.cookie(COOKIE_NAME, signToken(user), cookieOptions());
}

function clearSessionCookie(res) {
  const opts = cookieOptions();
  res.clearCookie(COOKIE_NAME, {
    httpOnly: opts.httpOnly,
    secure: opts.secure,
    sameSite: opts.sameSite,
    path: opts.path,
  });
}

function readUserFromRequest(req) {
  const token = req.cookies?.[COOKIE_NAME];
  if (!token) return null;
  try {
    const payload = jwt.verify(token, getSecret());
    return { id: payload.sub, email: payload.email };
  } catch {
    return null;
  }
}

function requireAuth(req, res, next) {
  const user = readUserFromRequest(req);
  if (!user) {
    return res.status(401).json({ error: "Não autenticado" });
  }
  req.user = user;
  next();
}

async function ensureAdminUser() {
  const email = (process.env.ADMIN_EMAIL || "").trim().toLowerCase();
  const password = process.env.ADMIN_PASSWORD || "";
  if (!email || !password) {
    console.warn(
      "[auth] ADMIN_EMAIL / ADMIN_PASSWORD não definidos — nenhum usuário seed."
    );
    return;
  }

  const existing = await query("SELECT id FROM users WHERE email = $1", [
    email,
  ]);
  if (existing.rowCount > 0) {
    return;
  }

  const passwordHash = await bcrypt.hash(password, 12);
  await query(
    "INSERT INTO users (email, password_hash) VALUES ($1, $2)",
    [email, passwordHash]
  );
  console.log(`[auth] Usuário admin criado: ${email}`);
}

async function authenticate(email, password) {
  const normalized = String(email || "").trim().toLowerCase();
  const result = await query(
    "SELECT id, email, password_hash FROM users WHERE email = $1",
    [normalized]
  );
  if (result.rowCount === 0) return null;

  const user = result.rows[0];
  const ok = await bcrypt.compare(String(password || ""), user.password_hash);
  if (!ok) return null;

  return { id: user.id, email: user.email };
}

module.exports = {
  COOKIE_NAME,
  setSessionCookie,
  clearSessionCookie,
  readUserFromRequest,
  requireAuth,
  ensureAdminUser,
  authenticate,
};
