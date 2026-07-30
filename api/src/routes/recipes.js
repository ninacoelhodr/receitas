const express = require("express");
const { query } = require("../db");
const { requireAuth } = require("../auth");

const router = express.Router();

const VALID_STATUS = new Set([null, "quero_fazer", "ja_fiz"]);

function normalizeSlug(raw) {
  return String(raw || "")
    .trim()
    .replace(/^\/+|\/+$/g, "")
    .replace(/\.html$/i, "");
}

function parseMetaBody(body) {
  const out = {};

  if ("status" in body) {
    let status = body.status;
    if (status === "" || status === undefined) status = null;
    if (!VALID_STATUS.has(status)) {
      return { error: "status inválido (quero_fazer | ja_fiz | null)" };
    }
    out.status = status;
  }

  if ("rating" in body) {
    let rating = body.rating;
    if (rating === "" || rating === undefined || rating === null) {
      out.rating = null;
    } else {
      rating = Number(rating);
      if (!Number.isInteger(rating) || rating < 1 || rating > 5) {
        return { error: "rating deve ser 1–5 ou null" };
      }
      out.rating = rating;
    }
  }

  if ("notes" in body) {
    const notes = body.notes == null ? null : String(body.notes);
    if (notes && notes.length > 8000) {
      return { error: "notes muito longas" };
    }
    out.notes = notes;
  }

  return { data: out };
}

async function getMeta(req, res) {
  try {
    const slug = normalizeSlug(req.params[0]);
    if (!slug) {
      return res.status(400).json({ error: "slug obrigatório" });
    }

    const result = await query(
      `SELECT recipe_slug, status, rating, notes, updated_at
       FROM recipe_meta
       WHERE user_id = $1 AND recipe_slug = $2`,
      [req.user.id, slug]
    );

    if (result.rowCount === 0) {
      return res.json({
        recipe_slug: slug,
        status: null,
        rating: null,
        notes: null,
        updated_at: null,
      });
    }

    res.json(result.rows[0]);
  } catch (err) {
    console.error("[recipes/get meta]", err);
    res.status(500).json({ error: "Erro ao ler metadados" });
  }
}

async function putMeta(req, res) {
  try {
    const slug = normalizeSlug(req.params[0]);
    if (!slug) {
      return res.status(400).json({ error: "slug obrigatório" });
    }

    const parsed = parseMetaBody(req.body || {});
    if (parsed.error) {
      return res.status(400).json({ error: parsed.error });
    }

    const existing = await query(
      `SELECT status, rating, notes FROM recipe_meta
       WHERE user_id = $1 AND recipe_slug = $2`,
      [req.user.id, slug]
    );

    const current =
      existing.rowCount > 0
        ? existing.rows[0]
        : { status: null, rating: null, notes: null };

    const next = {
      status: "status" in parsed.data ? parsed.data.status : current.status,
      rating: "rating" in parsed.data ? parsed.data.rating : current.rating,
      notes: "notes" in parsed.data ? parsed.data.notes : current.notes,
    };

    if (next.status !== "ja_fiz") {
      next.rating = null;
    }

    const result = await query(
      `INSERT INTO recipe_meta (user_id, recipe_slug, status, rating, notes, updated_at)
       VALUES ($1, $2, $3, $4, $5, NOW())
       ON CONFLICT (user_id, recipe_slug)
       DO UPDATE SET
         status = EXCLUDED.status,
         rating = EXCLUDED.rating,
         notes = EXCLUDED.notes,
         updated_at = NOW()
       RETURNING recipe_slug, status, rating, notes, updated_at`,
      [req.user.id, slug, next.status, next.rating, next.notes]
    );

    res.json(result.rows[0]);
  } catch (err) {
    console.error("[recipes/put meta]", err);
    res.status(500).json({ error: "Erro ao salvar metadados" });
  }
}

// Express 4: splat captura doces/bolo-de-cenoura antes de /meta
router.get(/^\/(.+)\/meta\/?$/, requireAuth, getMeta);
router.put(/^\/(.+)\/meta\/?$/, requireAuth, putMeta);

module.exports = router;
