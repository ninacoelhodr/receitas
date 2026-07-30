#!/usr/bin/env python3
"""Fetch up to 5 Wikimedia Commons candidate thumbs for recipe slugs.

Scratch output: imagens/_cands/<slug>/{1..5}.jpg (gitignored).
User-Agent: ReceitasNinaBot/1.0
"""
from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

UA = "ReceitasNinaBot/1.0 (https://github.com/ninacoelhodr/receitas; personal cookbook) python-urllib"
API = "https://commons.wikimedia.org/w/api.php"
SLEEP = 1.5
RETRY_SLEEP = 10
ROOT = Path(__file__).resolve().parents[1]

SKIP_WORDS = (
    "logo", "icon", "flag", "map", "diagram", "chart", "svg",
    "coat of arms", "watermark", "barcode", "packaging", ".djvu",
    "cookbook", "magazine of culinary",
)


def api_get(params: dict, retries: int = 5) -> dict:
    qs = urllib.parse.urlencode(params)
    req = urllib.request.Request(f"{API}?{qs}", headers={"User-Agent": UA})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                data = json.loads(r.read().decode("utf-8"))
            time.sleep(SLEEP)
            return data
        except urllib.error.HTTPError as e:
            if e.code in (429, 503) and attempt < retries - 1:
                wait = RETRY_SLEEP * (attempt + 1)
                print(f"  API {e.code}, sleep {wait}s", file=sys.stderr)
                time.sleep(wait)
                continue
            raise
    return {}


def search_files(query: str, limit: int = 20) -> list[dict]:
    data = api_get(
        {
            "action": "query",
            "format": "json",
            "generator": "search",
            "gsrsearch": query,
            "gsrnamespace": "6",
            "gsrlimit": str(limit),
            "prop": "imageinfo",
            "iiprop": "url|mime|size",
            "iiurlwidth": "960",
        }
    )
    pages = (data.get("query") or {}).get("pages") or {}
    out = []
    for page in pages.values():
        info = (page.get("imageinfo") or [None])[0]
        if not info:
            continue
        mime = info.get("mime") or ""
        if not mime.startswith("image/") or mime in ("image/svg+xml", "image/gif"):
            continue
        title = page.get("title") or ""
        low = title.lower()
        if any(w in low for w in SKIP_WORDS):
            continue
        url = info.get("thumburl") or info.get("url")
        if url:
            out.append({"title": title, "url": url})
    return out


def download(url: str, dest: Path, retries: int = 5) -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
            if len(data) < 2000:
                return False
            dest.write_bytes(data)
            time.sleep(0.7)
            return True
        except urllib.error.HTTPError as e:
            if e.code in (429, 503) and attempt < retries - 1:
                wait = RETRY_SLEEP * (attempt + 1)
                print(f"  DL {e.code}, sleep {wait}s", file=sys.stderr)
                time.sleep(wait)
                continue
            print(f"  download fail: {e}", file=sys.stderr)
            return False
        except Exception as e:
            print(f"  download fail: {e}", file=sys.stderr)
            return False
    return False


def fetch_candidates(slug: str, queries: list[str], max_n: int = 5, force: bool = False) -> int:
    dest_dir = ROOT / "imagens" / "_cands" / slug
    dest_dir.mkdir(parents=True, exist_ok=True)
    existing = sorted(dest_dir.glob("*.jpg"))
    if existing and not force and len(existing) >= 3:
        print(f"  skip (already {len(existing)} cands)")
        return len(existing)
    if force or len(existing) < 3:
        for old in dest_dir.iterdir():
            old.unlink()

    seen: set[str] = set()
    saved = 0
    meta = []
    for q in queries:
        if saved >= max_n:
            break
        print(f"  query: {q}")
        try:
            hits = search_files(q, limit=20)
        except Exception as e:
            print(f"  search fail: {e}", file=sys.stderr)
            time.sleep(RETRY_SLEEP)
            continue
        for h in hits:
            if saved >= max_n:
                break
            url = h.get("url")
            if not url or url in seen:
                continue
            seen.add(url)
            dest = dest_dir / f"{saved + 1}.jpg"
            if download(url, dest):
                saved += 1
                meta.append({"n": saved, "title": h["title"], "url": url, "query": q})
                print(f"  saved {saved}: {h['title']}")
    (dest_dir / "meta.json").write_text(
        json.dumps({"slug": slug, "queries": queries, "files": meta}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return saved


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--from-batch", required=True)
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--only-missing", action="store_true")
    args = ap.parse_args()
    batch = json.loads(Path(args.from_batch).read_text(encoding="utf-8"))
    for item in batch:
        slug = item["slug"]
        queries = item["queries"]
        dest_dir = ROOT / "imagens" / "_cands" / slug
        n_exist = len(list(dest_dir.glob("*.jpg"))) if dest_dir.exists() else 0
        if args.only_missing and n_exist >= 3:
            print(f"=== {slug} === skip ({n_exist})")
            continue
        print(f"=== {slug} ===")
        n = fetch_candidates(slug, queries, force=args.force)
        print(f"  got {n} candidates")


if __name__ == "__main__":
    main()
