# myapp/urls.py
from django.urls import path
from .decorators import urlpatterns

# 这句必须加上，否则views文件加载不到
from . import views  # 显式导入 views.py 文件
from . import views_ssq
from . import views_common
urlpatterns = urlpatterns
