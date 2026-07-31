#!/usr/bin/env bash
# Poll Telegram for recipe photos, links, and full recipe text → entradas/pending/
set -euo pipefail

TOKEN="${TELEGRAM_BOT_TOKEN:?TELEGRAM_BOT_TOKEN is required}"
API="https://api.telegram.org/bot${TOKEN}"
OFFSET_FILE=".github/telegram-offset"
PENDING_DIR="entradas/pending"
ALLOWED_CHAT_ID="${TELEGRAM_ALLOWED_CHAT_ID:-}"

mkdir -p "$PENDING_DIR" .github

offset=0
if [[ -f "$OFFSET_FILE" ]]; then
  offset="$(tr -d '[:space:]' < "$OFFSET_FILE" || true)"
  [[ -z "$offset" ]] && offset=0
fi

echo "Polling Telegram from offset ${offset}..."
updates="$(curl -sS "${API}/getUpdates?offset=${offset}&timeout=0")"

ok="$(echo "$updates" | jq -r '.ok')"
if [[ "$ok" != "true" ]]; then
  echo "Telegram API error:"
  echo "$updates" | jq .
  exit 1
fi

count="$(echo "$updates" | jq '.result | length')"
if [[ "$count" -eq 0 ]]; then
  echo "No new updates."
  exit 0
fi

max_offset="$offset"
imported=0

slugify() {
  local raw="${1:-entrada}"
  local s
  s="$(echo "$raw" | iconv -f utf-8 -t ascii//TRANSLIT 2>/dev/null || echo "$raw")"
  s="$(echo "$s" | tr '[:upper:]' '[:lower:]' | sed -E 's/https?:\/\///g; s/[^a-z0-9]+/-/g; s/^-+//; s/-+$//; s/^$/entrada/')"
  echo "${s:0:40}"
}

send_msg() {
  local chat="$1"
  local text="$2"
  curl -sS -X POST "${API}/sendMessage" \
    -d "chat_id=${chat}" \
    --data-urlencode "text=${text}" \
    >/dev/null
}

# Looks like a pasted full recipe (not a short chat line)
looks_like_recipe_text() {
  local t="$1"
  local len=${#t}
  if (( len < 80 )); then
    return 1
  fi
  if echo "$t" | grep -qiE 'ingrediente|modo de preparo|\bpreparo\b|x[ií]cara|colher|forno|rendimento|receita|massa|assado|cozinhe|bata |misture'; then
    return 0
  fi
  # Long paste without keywords still accepted (user said complete recipe text)
  if (( len >= 200 )); then
    return 0
  fi
  return 1
}

title_from_text() {
  # First non-empty line, stripped
  printf '%s\n' "$1" | sed '/^[[:space:]]*$/d' | head -n 1 | head -c 80
}

for i in $(seq 0 $((count - 1))); do
  update="$(echo "$updates" | jq -c ".result[$i]")"
  update_id="$(echo "$update" | jq -r '.update_id')"
  next_offset=$((update_id + 1))
  if (( next_offset > max_offset )); then
    max_offset=$next_offset
  fi

  chat_id="$(echo "$update" | jq -r '.message.chat.id // empty')"
  if [[ -z "$chat_id" ]]; then
    continue
  fi

  if [[ -n "$ALLOWED_CHAT_ID" && "$chat_id" != "$ALLOWED_CHAT_ID" ]]; then
    echo "Ignoring chat ${chat_id} (not allowed)."
    continue
  fi

  text="$(echo "$update" | jq -r '.message.text // empty')"
  caption="$(echo "$update" | jq -r '.message.caption // empty')"
  combined="${caption}"$'\n'"${text}"

  if [[ "$text" == "/start" || "$text" == "/help" ]]; then
    send_msg "$chat_id" "Olá! Envie de qualquer um destes jeitos:
1) Foto da receita (legenda opcional)
2) Link https://... de uma receita
3) Texto completo da receita (ingredientes + preparo)

Em breve aparece em entradas/pending. Depois no Cursor: processar dados."
    continue
  fi

  # —— Photos / image documents ——
  file_id="$(echo "$update" | jq -r '
    if (.message.photo | type) == "array" and (.message.photo | length) > 0 then
      .message.photo[-1].file_id
    elif (.message.document.mime_type // "") | startswith("image/") then
      .message.document.file_id
    else
      empty
    end
  ')"

  if [[ -n "$file_id" ]]; then
    file_info="$(curl -sS "${API}/getFile?file_id=${file_id}")"
    file_path="$(echo "$file_info" | jq -r '.result.file_path // empty')"
    if [[ -z "$file_path" ]]; then
      echo "Could not resolve file_path for update ${update_id}"
      continue
    fi

    ext="${file_path##*.}"
    [[ -z "$ext" || "$ext" == "$file_path" ]] && ext="jpg"

    label="${caption:-receita}"
    slug="$(slugify "$label")"
    ts="$(date -u +%Y%m%d-%H%M%S)"
    out="${PENDING_DIR}/${ts}-${update_id}-${slug}.${ext}"

    echo "Downloading photo -> ${out}"
    curl -sS -o "$out" "https://api.telegram.org/file/bot${TOKEN}/${file_path}"

    if [[ -n "$caption" ]]; then
      printf '%s\n' "$caption" > "${out}.txt"
    fi

    send_msg "$chat_id" "Foto recebida. No Cursor: processar dados."
    imported=$((imported + 1))
    continue
  fi

  # —— Links ——
  urls="$(echo "$update" | jq -r '
    [
      (.message.entities // []),
      (.message.caption_entities // [])
    ]
    | add
    | map(select(.type == "text_link") | .url)
    | .[]
  ' 2>/dev/null || true)"

  plain_urls="$(printf '%s\n' "$combined" | grep -oE 'https?://[^[:space:]<>\"]+' || true)"
  urls="$(printf '%s\n%s\n' "$urls" "$plain_urls" | sed '/^$/d' | awk '!seen[$0]++')"

  if [[ -n "$urls" ]]; then
    while IFS= read -r url; do
      [[ -z "$url" ]] && continue
      url="$(echo "$url" | sed -E 's/[),.;:]+$//')"
      slug="$(slugify "$url")"
      ts="$(date -u +%Y%m%d-%H%M%S)"
      out="${PENDING_DIR}/${ts}-${update_id}-${slug}.link.txt"

      note="$(printf '%s\n' "$combined" | grep -vE 'https?://' | sed '/^$/d' | head -c 2000 || true)"

      {
        echo "url: ${url}"
        if [[ -n "$note" ]]; then
          echo "note: ${note}"
        fi
        echo "from: telegram"
        echo "update_id: ${update_id}"
      } > "$out"

      echo "Saved link -> ${out}"
      send_msg "$chat_id" "Link recebido. No Cursor: processar dados."
      imported=$((imported + 1))
    done <<< "$urls"

    # If the same message also has a long recipe body, save it too
    body_only="$(printf '%s\n' "$text" | grep -vE 'https?://' || true)"
    if looks_like_recipe_text "$body_only"; then
      title="$(title_from_text "$body_only")"
      slug="$(slugify "${title:-receita-texto}")"
      ts="$(date -u +%Y%m%d-%H%M%S)"
      out="${PENDING_DIR}/${ts}-${update_id}-${slug}.recipe.txt"
      {
        echo "from: telegram"
        echo "update_id: ${update_id}"
        echo "type: recipe_text"
        echo "---"
        printf '%s\n' "$body_only"
      } > "$out"
      echo "Saved recipe text (with link msg) -> ${out}"
      imported=$((imported + 1))
    fi
    continue
  fi

  # —— Full recipe text (no photo, no URL) ——
  if [[ -n "$text" ]] && looks_like_recipe_text "$text"; then
    title="$(title_from_text "$text")"
    slug="$(slugify "${title:-receita-texto}")"
    ts="$(date -u +%Y%m%d-%H%M%S)"
    out="${PENDING_DIR}/${ts}-${update_id}-${slug}.recipe.txt"
    {
      echo "from: telegram"
      echo "update_id: ${update_id}"
      echo "type: recipe_text"
      echo "---"
      printf '%s\n' "$text"
    } > "$out"
    echo "Saved recipe text -> ${out}"
    send_msg "$chat_id" "Texto recebido. No Cursor: processar dados."
    imported=$((imported + 1))
    continue
  fi

  if [[ -n "$text" ]]; then
    send_msg "$chat_id" "Não reconheci. Envie: foto, link https://... ou o texto completo da receita (ingredientes + preparo)."
  fi
done

echo "$max_offset" > "$OFFSET_FILE"
echo "Imported ${imported} item(s). Next offset: ${max_offset}"
