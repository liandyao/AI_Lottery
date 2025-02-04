# 自定义装饰器，使用该代码之后，可以在views的函数上直接定义url地址，不需要再配置urls
# myapp/decorators.py
from django.urls import path
from django.conf import settings


urlpatterns = []

def url(route, **kwargs):
    print('----->decorator-----')
    def decorator(view_func):
        urlpatterns.append(path(route, view_func, **kwargs))
        print('----->',urlpatterns)
        return view_func
    return decorator
