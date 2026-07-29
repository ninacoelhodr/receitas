#!/usr/bin/env bash
# Poll Telegram for recipe photos and save them under entradas/pending/
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

  caption="$(echo "$update" | jq -r '.message.caption // .message.text // empty')"
  # Skip pure /start and help texts without media
  file_id="$(echo "$update" | jq -r '
    if (.message.photo | type) == "array" and (.message.photo | length) > 0 then
      .message.photo[-1].file_id
    elif (.message.document.mime_type // "") | startswith("image/") then
      .message.document.file_id
    else
      empty
    end
  ')"

  if [[ -z "$file_id" ]]; then
    text="$(echo "$update" | jq -r '.message.text // empty')"
    if [[ "$text" == "/start" || "$text" == "/help" ]]; then
      curl -sS -X POST "${API}/sendMessage" \
        -d "chat_id=${chat_id}" \
        --data-urlencode "text=Olá! Envie a foto da receita (pode colocar a categoria ou o nome na legenda). Em alguns minutos ela aparece em entradas/pending no GitHub. Depois diga no Cursor: processa entradas." \
        >/dev/null
    fi
    continue
  fi

  file_info="$(curl -sS "${API}/getFile?file_id=${file_id}")"
  file_path="$(echo "$file_info" | jq -r '.result.file_path // empty')"
  if [[ -z "$file_path" ]]; then
    echo "Could not resolve file_path for update ${update_id}"
    continue
  fi

  ext="${file_path##*.}"
  [[ -z "$ext" || "$ext" == "$file_path" ]] && ext="jpg"

  slug="$(echo "${caption:-receita}" \
    | iconv -f utf-8 -t ascii//TRANSLIT 2>/dev/null || echo "${caption:-receita}")"
  slug="$(echo "$slug" | tr '[:upper:]' '[:lower:]' | sed -E 's/[^a-z0-9]+/-/g; s/^-+//; s/-+$//; s/^$/receita/')"
  slug="${slug:0:40}"
  ts="$(date -u +%Y%m%d-%H%M%S)"
  out="${PENDING_DIR}/${ts}-${update_id}-${slug}.${ext}"

  echo "Downloading -> ${out}"
  curl -sS -o "$out" "https://api.telegram.org/file/bot${TOKEN}/${file_path}"

  note=""
  if [[ -n "$caption" ]]; then
    printf '%s\n' "$caption" > "${out}.txt"
    note=" Legenda: ${caption}"
  fi

  curl -sS -X POST "${API}/sendMessage" \
    -d "chat_id=${chat_id}" \
    --data-urlencode "text=Recebido! Salvei como ${out}.${note} Quando quiser, no Cursor diga: processa entradas." \
    >/dev/null

  imported=$((imported + 1))
done

echo "$max_offset" > "$OFFSET_FILE"
echo "Imported ${imported} photo(s). Next offset: ${max_offset}"
