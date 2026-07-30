const express = require("express");
const {
  authenticate,
  setSessionCookie,
  clearSessionCookie,
  readUserFromRequest,
} = require("../auth");

const router = express.Router();

router.post("/login", async (req, res) => {
  try {
    const { email, password } = req.body || {};
    const user = await authenticate(email, password);
    if (!user) {
      return res.status(401).json({ error: "E-mail ou senha inválidos" });
    }
    setSessionCookie(res, user);
    res.json({ user: { id: user.id, email: user.email } });
  } catch (err) {
    console.error("[auth/login]", err);
    res.status(500).json({ error: "Erro ao entrar" });
  }
});

router.post("/logout", (req, res) => {
  clearSessionCookie(res);
  res.json({ ok: true });
});

router.get("/me", (req, res) => {
  const user = readUserFromRequest(req);
  if (!user) {
    return res.status(401).json({ error: "Não autenticado" });
  }
  res.json({ user: { id: user.id, email: user.email } });
});

module.exports = router;
