
import datetime
import logging
import pandas as pd


from .decorators import url
from django.core.cache import cache

from .predict.ssq_predict import SsqPredict

logger = logging.getLogger(__name__)

from .utils import result_success, result_error  # 导入自定义的 JSON 响应方法

@url('laoliu/common/notice/', name='comm_notice_api')
def get_notice(request):
    logger.info("正在查询公告...")
    return result_success(data="其余功能正在抓紧开发中，敬请期待！", message="公告查询成功！")