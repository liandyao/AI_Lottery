#!/bin/bash

PROJECT_DIR="/home/xingyunqiu/AI_Lottery/laoliu_django"
#VENV_DIR="$PROJECT_DIR/venv"
# 激活虚拟环境
#source $VENV_DIR/bin/activate
# 设置Python路径
export PYTHONPATH=/home/xingyunqiu/AI_Lottery/laoliu_django
# 执行scheduler_getData.py脚本
python3 $PROJECT_DIR/xingyunqiu/getData/scheduler_getData.py