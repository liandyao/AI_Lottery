## 部署说明文档

### 如何制定定时任务，获取ssq的记录
1. 在 `xingyunqiu/management/commands/run_scheduler.py` 中添加任务。
2. 直接使用 `python manage.py run_scheduler`。

**注意**: `management/commands` 目录结构是固定的，不能更改。具体目录结构如下：
 

    laoliu_django/ 
            xingyunqiu/ 
                management/ 
                    commands/ 
                        run_scheduler.py
 
    

    **以下作废：
    1. 首先安装两个包
        pip install celery django-celery-beat 
    2. 配置Celery： 在你的Django项目中创建一个celery.py文件，通常放在与settings.py相同的目录下。
       1.然后在你的__init__.py文件中导入Celery应用：
       2.创建Celery任务： 在你的应用目录下创建一个tasks.py文件，并定义一个Celery任务来运行GetData_By_Year.py中的代码。
       3. 配置django-celery-beat： 在Django的settings.py文件中添加django_celery_beat到INSTALLED_APPS中，并配置Celery Beat调度器。
        4. 创建定时任务： 运行迁移命令来创建必要的数据库表：
        5.然后在Django管理后台中创建一个定时任务：
            运行Django开发服务器并访问管理后台（通常是http://127.0.0.1:8000/admin/）。
            进入Periodic Tasks部分，点击“Add periodic task”。
            填写任务名称，选择xingyunqiu.tasks.run_get_data_by_year作为任务。
            设置定时任务的时间为每晚22点。Crontab Schedule:0 22 * * *（表示每晚22点运行）
            启动Celery Worker和Beat： 在终端中启动Celery Worker和Beat：
                celery -A laoliu_django worker --loglevel=info
                celery -A laoliu_django beat --loglevel=info
    3. 项目目录
    laoliu_django/
        laoliu_django/
            __init__.py
            settings.py
            urls.py
            wsgi.py
            celery.py
        xingyunqiu/
            __init__.py
            tasks.py
            ...
    **以上作废

### 创建管理员账号
    1，同步数据库  python manage.py migrate
    2，创建管理员账号 python manage.py createsuperuser

