curl -Ls https://astral.sh/uv/install.sh | sh
uv python install 3.11
uv sync
cd ingest
uv sync
cd -

if command -v dockera >>/dev/null; then
  docker compose up -d
  docker compose stop
else
  curl -fsSL https://ollama.com/install.sh | sh
  uv tool install open-webui
  ollama pull llama3.2:1b
  ollama pull llama3.2:3b
  ollama pull qwen2.5-coder:7b
fi
uv tool install open-webui
