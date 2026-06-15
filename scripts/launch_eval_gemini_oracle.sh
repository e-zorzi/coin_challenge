#!/bin/bash

source  coin_env/bin/activate && python3 eval_model.py 0 70 --local 0 --task-type category &
# source  coin_env/bin/activate && python3 eval_model.py 0 70 --local 0 --task-type color &
# source  coin_env/bin/activate && python3 eval_model.py 0 70 --local 0 --task-type context &
# source  coin_env/bin/activate && python3 eval_model.py 0 70 --local 0 --task-type color_feature &
# source  coin_env/bin/activate && python3 eval_model.py 0 70 --local 0 --task-type color_context &
# source  coin_env/bin/activate && python3 eval_model.py 0 70 --local 0 --task-type color_context_feature &
