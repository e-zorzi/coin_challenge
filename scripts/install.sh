uv venv --no-project --relocatable
source .venv/bin/activate
uv pip install retrying flask gymnasium colorama accelerate transformers==4.43.1 Pillow opencv-python dotenv qwen-vl-utils huggingface_hub==1.14.0