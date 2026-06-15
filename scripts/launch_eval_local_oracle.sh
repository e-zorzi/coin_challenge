#!/bin/bash
export ORACLE_MODEL_ID="Qwen/Qwen3-VL-30B-A3B-Instruct"
export MY_VLLM_PORT=8001

source $ vllm_env/bin/activate && CUDA_VISIBLE_DEVICES=1 vllm serve ${ORACLE_MODEL_ID} --local 1 --max-model-len 8192 --gpu-memory-utilization 0.90 & 

sleep 120

source  coin_env/bin/activate && python3 eval_model.py 0 70 --local 1 --task-type category &
# source  coin_env/bin/activate && python3 eval_model.py 0 70 --local 1 --task-type color &
# source  coin_env/bin/activate && python3 eval_model.py 0 70 --local 1 --task-type context &
# source  coin_env/bin/activate && python3 eval_model.py 0 70 --local 1 --task-type color_feature &
# source  coin_env/bin/activate && python3 eval_model.py 0 70 --local 1 --task-type color_context &
# source  coin_env/bin/activate && python3 eval_model.py 0 70 --local 1 --task-type color_context_feature &