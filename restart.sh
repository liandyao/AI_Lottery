#!/bin/bash

# 设置项目路径
PROJECT_DIR="/home/xingyunqiu/AI_Lottery/laoliu_django"
VENV_DIR="$PROJECT_DIR/venv"

# 进入项目目录
cd $PROJECT_DIR

# 激活虚拟环境
source $VENV_DIR/bin/activate

# 获取 Django 开发服务器的进程 ID
DJANGO_PID=$(ps aux | grep 'manage.py runserver' | grep -v grep | awk '{print $2}')
if [ -n "$DJANGO_PID" ]; then
    echo "停止 Django 开发服务器 (PID: $DJANGO_PID)..."
    kill -9 $DJANGO_PID
else
    echo "Django 开发服务器未运行。"
fi

# 获取调度任务的进程 ID
SCHEDULER_PID=$(ps aux | grep 'manage.py run_scheduler' | grep -v grep | awk '{print $2}')
if [ -n "$SCHEDULER_PID" ]; then
    echo "停止调度任务 (PID: $SCHEDULER_PID)..."
    kill -9 $SCHEDULER_PID
else
    echo "调度任务未运行。"
fi

# 启动 Django 开发服务器
echo "启动 Django 开发服务器..."
nohup python manage.py runserver 8200 &

# 启动调度任务
echo "启动调度任务..."
nohup python manage.py run_scheduler &

echo "重启完成！"
