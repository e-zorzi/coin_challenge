uv venv --no-project --relocatable
mv .venv .venv2
source .venv2/bin/activate
uv pip install vllm --torch-backend=auto
echo "Remember to export your GEMINI_API_KEY login token. Check the README for instructions."
