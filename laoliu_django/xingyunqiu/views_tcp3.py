
import datetime
import json
import logging
import pandas as pd


from .decorators import url
from django.core.cache import cache

from .predict.fc3d_predict import fc3dPredict

logger = logging.getLogger(__name__)

from .utils import result_success, result_error  # 导入自定义的 JSON 响应方法

@url('laoliu/tcp3/by_year/', name='tcp3_by_year_api')
def get_data_by_year(request):
    # 得到传入的year
    num = request.GET.get('num')
    logger.info(f"正在获取年份: {num} 的数据...")
    # 如果year为空，默认取当前年
    if num is None:
        num = 100

    num = int(num)
        # 使用全局变量中的数据
    df =   cache.get('tcp3_data_all')
    if df is None:
        logger.error("缓存中的数据为空")
        return result_error(None, message='缓存中的数据为空')

    # 显示head的100行数据。

    data = df.head(num).to_dict(orient='records')

    return result_success(data)

@url('laoliu/tcp3/predict/', name='tcp3_predict_api')
def predict(request):
    type = request.GET.get('type')
    df = cache.get('tcp3_data_all')
    if df is None:
        logger.error("缓存中的数据为空")
        return result_error(None, message='缓存中的数据为空')
    df = df.head(30)
    data = df

    print('data', data)
    res = {}
    if type == '1':
        res = fc3dPredict().predictByFrequencyHigh(data)
        pass
    elif type == '2':
        res = fc3dPredict().predictByFrequencyLow(data)
        pass
    elif type == '3':
        res = fc3dPredict().predictByFrequencyMiddle(data)
        pass

    return result_success(res)

@url('laoliu/tcp3/statisticsFrequency/', name='tcp3_statisticsFrequency_api')
def statisticsFrequency(request):
    num = request.GET.get('num') # 期数
    if num is None:
        num = 100
    num = int(num)
    df = cache.get('tcp3_data_all')
    data = df.head(num)
    res = fc3dPredict().statisticsFrequency(data)
    print(res)
    return result_success(res)