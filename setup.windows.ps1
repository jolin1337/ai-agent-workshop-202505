powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
uv sync
cd ingest
uv sync
cd -

#https://objects.githubusercontent.com/github-production-release-asset-2e65be/658928958/75176854-10de-45fe-be3e-4b97994453b5?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=releaseassetproduction%2F20250427%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250427T121030Z&X-Amz-Expires=300&X-Amz-Signature=b751b7ae7384ca67373b03b235a2f7dc0abfa267ec70d5024978fef4fdf031ae&X-Amz-SignedHeaders=host&response-content-disposition=attachment%3B%20filename%3DOllamaSetup.exe&response-content-type=application%2Foctet-stream
wget -O ollama.exe "https://objects.githubusercontent.com/github-production-release-asset-2e65be/658928958/75176854-10de-45fe-be3e-4b97994453b5?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=releaseassetproduction%2F20250427%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250427T121030Z&X-Amz-Expires=300&X-Amz-Signature=b751b7ae7384ca67373b03b235a2f7dc0abfa267ec70d5024978fef4fdf031ae&X-Amz-SignedHeaders=host&response-content-disposition=attachment%3B%20filename%3DOllamaSetup.exe&response-content-type=application%2Foctet-stream"

./ollama.exe pull llama3.2:1b
./ollama.exe pull llama3.2:3b
./ollama.exe pull qwen2.5-coder:7b

uv tool install open-webui
