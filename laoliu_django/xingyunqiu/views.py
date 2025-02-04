import datetime
import logging
import pandas as pd

# Create your views here.
from django.http import JsonResponse

from .decorators import url
from django.core.cache import cache

from .predict.ssq_predict import SsqPredict

logger = logging.getLogger(__name__)

from .utils import result_success, result_error  # 导入自定义的 JSON 响应方法



@url('laoliu/simple/', name='simple_api')
def simple_api(request):
    data = {
        'message': 'Hello, World!'
    }
    return JsonResponse(data)

# 根据年份取数据
