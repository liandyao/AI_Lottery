
import datetime
import json
import logging
import pandas as pd


from .decorators import url
from django.core.cache import cache

from .predict.fc3d_predict import fc3dPredict

logger = logging.getLogger(__name__)

from .utils import result_success, result_error  # 导入自定义的 JSON 响应方法

@url('laoliu/fc3d/by_year/', name='fc3d_by_year_api')
def get_data_by_year(request):
    # 得到传入的year
    year = request.GET.get('year')
    logger.info(f"正在获取年份: {year} 的数据...")
    # 如果year为空，默认取当前年
    if year is None:
        year = str(datetime.datetime.now().year)

        # 使用全局变量中的数据
    df =   cache.get('fc3d_data_all')
    if df is None:
        logger.error("缓存中的数据为空")
        return result_error(None, message='缓存中的数据为空')

    # 使用字符串操作进行筛选
    data = df[df['draw_date'].str.startswith(year)].to_dict(orient='records')

    return result_success(data)

@url('laoliu/fc3d/predict/', name='fc3d_predict_api')
def predict(request):
    type = request.GET.get('type')
    df = cache.get('fc3d_data_all')
    if df is None:
        logger.error("缓存中的数据为空")
        return result_error(None, message='缓存中的数据为空')
    df = df.head(90)
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