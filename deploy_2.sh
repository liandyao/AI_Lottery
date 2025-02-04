#!/bin/bash

# 设置项目路径
PROJECT_DIR="/home/xingyunqiu/AI_Lottery/laoliu_django"
VENV_DIR="$PROJECT_DIR/venv"

# 进入项目目录
cd $PROJECT_DIR

# 创建虚拟环境
echo "创建虚拟环境..."
python3 -m venv $VENV_DIR

# 激活虚拟环境
source $VENV_DIR/bin/activate

# 安装项目依赖
echo "安装项目依赖..."
pip install -r requirements.txt

# 配置环境变量（根据需要修改）
echo "配置环境变量..."
export DJANGO_SETTINGS_MODULE=laoliu_django.settings
export DEBUG=False
export DATABASE_URL='sqlite:///db.sqlite3'
export ALLOWED_HOSTS='0.0.0.0'

# 迁移数据库
echo "迁移数据库..."
python manage.py migrate

# 收集静态文件
echo "收集静态文件..."
python manage.py collectstatic --noinput

# 启动 Django 开发服务器
echo "启动 Django 开发服务器..."
nohup python manage.py runserver 0.0.0.0:9850 &

# 启动调度任务
echo "启动调度任务..."
nohup python manage.py run_scheduler &

echo "部署完成！"
