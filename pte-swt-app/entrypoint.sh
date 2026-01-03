#!/bin/bash
set -e

echo "Starting vLLM server..."

python -m vllm.entrypoints.openai.api_server \
  --model meta-llama/Meta-Llama-3.1-8B-Instruct \
  --host 0.0.0.0 \
  --port 8000 \
  --dtype float16 \
  --max-model-len 8192 &

echo "Waiting for vLLM to become ready..."

until curl -s http://localhost:8000/v1/models > /dev/null; do
  sleep 2
done

echo "vLLM is ready. Starting FastAPI..."

exec uvicorn api.main:app \
  --host 0.0.0.0 \
  --port 8080
