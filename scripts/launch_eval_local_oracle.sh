#!/bin/bash
export ORACLE_MODEL_ID="Qwen/Qwen3-VL-30B-A3B-Instruct"
export MY_VLLM_PORT=8001

RUN_TYPE="train"

source $.venv2/bin/activate && CUDA_VISIBLE_DEVICES=1 vllm serve ${ORACLE_MODEL_ID} --local 1 --max-model-len 8192 --gpu-memory-utilization 0.90 & 

sleep 120

source .venv/bin/activate && python3 eval_model.py 0 70 --local 1 --task-type category --run-type ${RUN_TYPE} &
# source .venv/bin/activate && python3 eval_model.py 0 70 --local 1 --task-type color --run-type ${RUN_TYPE} &
# source .venv/bin/activate && python3 eval_model.py 0 70 --local 1 --task-type context --run-type ${RUN_TYPE} &
# source .venv/bin/activate && python3 eval_model.py 0 70 --local 1 --task-type color_feature --run-type ${RUN_TYPE} &
# source .venv/bin/activate && python3 eval_model.py 0 70 --local 1 --task-type color_context --run-type ${RUN_TYPE} &
# source .venv/bin/activate && python3 eval_model.py 0 70 --local 1 --task-type color_context_feature --run-type ${RUN_TYPE} &