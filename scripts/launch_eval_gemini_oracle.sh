#!/bin/bash
RUN_TYPE="train"

source .venv/bin/activate && python3 eval_model.py 0 70 --local 0 --task-type category --run-type ${RUN_TYPE} &
# source .venv/bin/activate && python3 eval_model.py 0 70 --local 0 --task-type color --run-type ${RUN_TYPE} &
# source .venv/bin/activate && python3 eval_model.py 0 70 --local 0 --task-type context --run-type ${RUN_TYPE} &
# source .venv/bin/activate && python3 eval_model.py 0 70 --local 0 --task-type color_feature --run-type ${RUN_TYPE} &
# source .venv/bin/activate && python3 eval_model.py 0 70 --local 0 --task-type color_context --run-type ${RUN_TYPE} &
# source .venv/bin/activate && python3 eval_model.py 0 70 --local 0 --task-type color_context_feature --run-type ${RUN_TYPE} &
