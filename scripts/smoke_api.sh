#!/usr/bin/env bash
# Smoke test for the Bedrock inference endpoint used by GURMA.
# Usage: GURMA_INFERENCE_URL=https://....lambda-url.us-east-1.on.aws/ scripts/smoke_api.sh
# Falls back to .env, then to the Lambda function URL via the AWS CLI.
set -uo pipefail

if [[ -z "${GURMA_INFERENCE_URL:-}" && -f .env ]]; then
  set -a; source .env; set +a
fi
if [[ -z "${GURMA_INFERENCE_URL:-}" ]]; then
  GURMA_INFERENCE_URL=$(aws lambda get-function-url-config \
    --region us-east-1 \
    --function-name bedrock-inference-mvp \
    --query FunctionUrl --output text 2>/dev/null || true)
fi
if [[ -z "${GURMA_INFERENCE_URL:-}" ]]; then
  echo "GURMA_INFERENCE_URL is not set" >&2
  exit 2
fi

URL="${GURMA_INFERENCE_URL%/}/v1/chat/completions"
KEY="${GURMA_INFERENCE_API_KEY:-1234}"
failures=0

# check <label> <model> <max_tokens> <prompt>
check() {
  local label=$1 model=$2 max_tokens=$3 prompt=$4 body status
  body=$(jq -n --arg m "$model" --arg p "$prompt" --argjson n "$max_tokens" \
    '{model: $m, messages: [{role: "user", content: $p}], max_tokens: $n, temperature: 0}')
  local out
  out=$(mktemp)
  status=$(curl -sS -m 120 -o "$out" -w '%{http_code}' -X POST "$URL" \
    -H "Content-Type: application/json" \
    -H "Authorization: Bearer ${KEY}" \
    -d "$body") || status="curl_error"
  local content error
  content=$(jq -r '.choices[0].message.content // empty' "$out" 2>/dev/null)
  error=$(jq -r '.error // empty' "$out" 2>/dev/null)
  if [[ "$status" == "200" && -z "$error" && -n "$content" ]]; then
    printf 'PASS  %-24s %s\n' "$label" "$(jq -c '.usage' "$out")"
  else
    printf 'FAIL  %-24s HTTP %s %s\n' "$label" "$status" "$(head -c 300 "$out")"
    failures=$((failures + 1))
  fi
  rm -f "$out"
}

for model in nova-pro llama gpt-oss deepseek; do
  check "$model" "$model" 64 "Say hello in one short sentence."
done
# Guard budget the pipeline relies on (endpoint caps max_tokens at 4096)
check "gpt-oss max_tokens=4096" gpt-oss 4096 "Reply with the single word OK."

if (( failures > 0 )); then
  echo "$failures check(s) failed" >&2
  exit 1
fi
echo "all checks passed"
