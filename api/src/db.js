const { Pool } = require("pg");

const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl:
    process.env.DATABASE_SSL === "false"
      ? false
      : process.env.NODE_ENV === "production"
        ? { rejectUnauthorized: false }
        : false,
});

async function query(text, params) {
  return pool.query(text, params);
}

async function migrate() {
  await query(`
    CREATE TABLE IF NOT EXISTS users (
      id SERIAL PRIMARY KEY,
      email TEXT UNIQUE NOT NULL,
      password_hash TEXT NOT NULL,
      created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
    );

    CREATE TABLE IF NOT EXISTS recipe_meta (
      id SERIAL PRIMARY KEY,
      user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
      recipe_slug TEXT NOT NULL,
      status TEXT CHECK (status IS NULL OR status IN ('quero_fazer', 'ja_fiz')),
      rating SMALLINT CHECK (rating IS NULL OR (rating BETWEEN 1 AND 5)),
      notes TEXT,
      updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
      UNIQUE (user_id, recipe_slug)
    );

    CREATE INDEX IF NOT EXISTS idx_recipe_meta_user_slug
      ON recipe_meta (user_id, recipe_slug);
  `);
}

module.exports = { pool, query, migrate };
