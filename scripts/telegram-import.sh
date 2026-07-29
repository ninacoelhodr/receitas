#!/usr/bin/env bash
# Poll Telegram for recipe photos and links → entradas/pending/
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
    send_msg "$chat_id" "Olá! Envie:
1) Foto da receita (legenda opcional com categoria/nome), ou
2) Link de uma receita na internet (share.google, blog, etc.).

Em alguns minutos aparece em entradas/pending no GitHub. Depois diga no Cursor: processa entradas."
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

    send_msg "$chat_id" "Foto recebida: ${out}. No Cursor: processa entradas."
    imported=$((imported + 1))
    continue
  fi

  # —— Links (plain text, entities, text_link) ——
  urls="$(echo "$update" | jq -r '
    [
      (.message.entities // []),
      (.message.caption_entities // [])
    ]
    | add
    | map(select(.type == "text_link") | .url)
    | .[]
  ' 2>/dev/null || true)"

  # URLs typed plainly in text/caption
  plain_urls="$(printf '%s\n' "$combined" | grep -oE 'https?://[^[:space:]<>\"]+' || true)"
  urls="$(printf '%s\n%s\n' "$urls" "$plain_urls" | sed '/^$/d' | awk '!seen[$0]++')"

  if [[ -z "$urls" ]]; then
    if [[ -n "$text" ]]; then
      send_msg "$chat_id" "Não achei foto nem link. Envie uma foto da receita ou um URL (https://...)."
    fi
    continue
  fi

  while IFS= read -r url; do
    [[ -z "$url" ]] && continue
    # strip trailing punctuation often glued by messengers
    url="$(echo "$url" | sed -E 's/[),.;:]+$//')"
    slug="$(slugify "$url")"
    ts="$(date -u +%Y%m%d-%H%M%S)"
    out="${PENDING_DIR}/${ts}-${update_id}-${slug}.link.txt"

    note="$(printf '%s\n' "$combined" | grep -vE 'https?://' | sed '/^$/d' | head -c 500 || true)"

    {
      echo "url: ${url}"
      if [[ -n "$note" ]]; then
        echo "note: ${note}"
      fi
      echo "from: telegram"
      echo "update_id: ${update_id}"
    } > "$out"

    echo "Saved link -> ${out}"
    send_msg "$chat_id" "Link recebido: ${url}
Salvei em ${out}. No Cursor: processa entradas."
    imported=$((imported + 1))
  done <<< "$urls"
done

echo "$max_offset" > "$OFFSET_FILE"
echo "Imported ${imported} item(s). Next offset: ${max_offset}"
