# Automated check of every model below (also runs in GitHub Actions):
#   scripts/smoke_api.sh
#
# The CloudFormation stack is gone; resolve the URL from the Lambda directly.
FUNCTION_URL=$(aws lambda get-function-url-config \
  --region us-east-1 \
  --function-name bedrock-inference-mvp \
  --query FunctionUrl \
  --output text)
INFERENCE_API_KEY=1234
# max_tokens is capped at 4096 by the endpoint (400 above that).

# Non-stream responses are JSON → pipe to jq.
# Stream responses are SSE (text/event-stream) → use curl -N, do NOT pipe to jq.
# Full stream examples: https://github.com/taixingbi/mvp-bedrock/blob/main/example.md

# Amazon Nova Pro (marketplace)
curl -sS -X POST "${FUNCTION_URL}v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${INFERENCE_API_KEY}" \
  -d '{
    "model": "nova-pro",
    "messages": [{"role": "user", "content": "Say hello in one short sentence."}],
    "max_tokens": 64,
    "temperature": 0
  }' | jq '{error, detail, model, answer: .choices[0].message.content, usage}'
echo

# Meta Llama 3.3 (marketplace)
curl -sS -X POST "${FUNCTION_URL}v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${INFERENCE_API_KEY}" \
  -d '{
    "model": "llama",
    "messages": [{"role": "user", "content": "Say hello in one short sentence."}],
    "max_tokens": 64,
    "temperature": 0
  }' | jq '{error, detail, model, answer: .choices[0].message.content, usage}'
echo

# OpenAI GPT-OSS (marketplace)
curl -sS -X POST "${FUNCTION_URL}v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${INFERENCE_API_KEY}" \
  -d '{
    "model": "gpt-oss",
    "messages": [{"role": "user", "content": "Say hello in one short sentence."}],
    "max_tokens": 64,
    "temperature": 0
  }' | jq '{error, detail, model, answer: .choices[0].message.content, usage}'
echo

# DeepSeek V3.2 (marketplace)
curl -sS -X POST "${FUNCTION_URL}v1/chat/completions" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${INFERENCE_API_KEY}" \
  -d '{
    "model": "deepseek",
    "messages": [{"role": "user", "content": "Say hello in one short sentence."}],
    "max_tokens": 64,
    "temperature": 0
  }' | jq '{error, detail, model, answer: .choices[0].message.content, usage}'
echo
