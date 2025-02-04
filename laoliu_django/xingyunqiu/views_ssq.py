
import datetime
import json
import logging
import pandas as pd


from .decorators import url
from django.core.cache import cache

from .models import SsqOtherPredict
from .predict.ssq_predict import SsqPredict

logger = logging.getLogger(__name__)

from .utils import result_success, result_error  # 导入自定义的 JSON 响应方法

@url('laoliu/ssq/by_year/', name='by_year_api')
def get_data_by_year(request):
    # 得到传入的year
    year = request.GET.get('year')
    logger.info(f"正在获取年份: {year} 的数据...")
    # 如果year为空，默认取当前年
    if year is None:
        year = str(datetime.datetime.now().year)

        # 使用全局变量中的数据
    df =   cache.get('lottery_data_all')
    if df is None:
        logger.error("缓存中的数据为空")
        return result_error(None, message='缓存中的数据为空')

    # 使用字符串操作进行筛选
    data = df[df['drawTime'].str.startswith(year)].to_dict(orient='records')


    return result_success(data)

# 根据最后的多少期数取数据
@url('laoliu/ssq/by_periods/', name='by_periods_api')
def get_data_by_periods(request):
    # 得到传入的year
    periods = request.GET.get('periods')
    logger.info(f"正在获取: {periods} 的数据...")
    # 如果year为空，默认取当前年
    if periods is None:
        periods = 100

    # 使用全局变量中的数据
    df =   cache.get('lottery_data_all')
    if df is None:
        logger.error("缓存中的数据为空")
        return result_error(None, message='缓存中的数据为空')

    # 取最后100行数据。
    data = df.head(int(periods)).to_dict(orient='records')

    return result_success(data)

# 开始预测
@url('laoliu/ssq/predictByFrequency/', name='predictByFrequency_api')
def predictByFrequency(request):
    logger.info("正在预测...")
    # 得到页面上传过来的数据`?periods=${this.periods}&redBalls=${this.redBalls.join(",")}&blueBall=${this.blueBall}`
    periods = request.GET.get('periods')
    redBalls = request.GET.get('redBalls')
    blueBall = request.GET.get('blueBall')
    if redBalls is None or blueBall is None or periods is None:
        logger.error("预测数据为空")
        return result_error(None, message='预测数据为空')

    # 使用全局变量中的数据
    df = cache.get('lottery_data_all')
    if df is None:
        logger.error("缓存中的数据为空")
        return result_error(None, message='缓存中的数据为空')
    redBalls_list = list(map(int, redBalls.split(',')))
    data = df.head(int(periods)).to_dict(orient='records')
    # 将data转换为df数据类型
    data = pd.DataFrame(data)
    res = SsqPredict().predictByFrequency(data, redBalls_list)
    print('预测的结果',res)
    return result_success(res)

@url('laoliu/ssq/predictByIssue/', name='predictByIssue_api')
def predictByIssue(request):
    logger.info("正在预测...")
    # 得到页面上传过来的数据期数和期号
    periods = request.GET.get('periods')
    # 期号
    issue = request.GET.get('issue')

    # 使用全局变量中的数据
    df = cache.get('lottery_data_all')
    if df is None:
        logger.error("缓存中的数据为空")
        return result_error(None, message='缓存中的数据为空')
    if issue is None:
        issue = df.iloc[-1]['issueNumber']

    issue = int(issue)
    data = df.head(int(periods)).to_dict(orient='records')
    # 将data转换为df数据类型
    data = pd.DataFrame(data)
    res = SsqPredict().train_and_predict_by_issue(data, issue)
    print('预测的结果',res)
    return result_success(res)

@url('laoliu/ssq/predictByWeekday/', name='predictByWeekday_api')
def predictByWeekday(request):
    logger.info("正在预测...")
    # 得到页面上传过来的数据期数和期号
    periods = request.GET.get('periods')
    # 星期
    weekday = request.GET.get('weekday')

    # 使用全局变量中的数据
    df = cache.get('lottery_data_all')
    if df is None:
        logger.error("缓存中的数据为空")
        return result_error(None, message='缓存中的数据为空')

    data = df.head(int(periods)).to_dict(orient='records')
    # 将data转换为df数据类型
    data = pd.DataFrame(data)
    res = SsqPredict().predictByWeekday(data, weekday, 5)

    print('预测的结果',res)
    return result_success(res)

@url('laoliu/ssq/predictBySum/', name='predictBySum_api')
def predictBySum(request):
    logger.info("正在预测...")
    # 得到页面上传过来的数据期数和期号
    periods = request.GET.get('periods')
    # 和值
    sumValue = request.GET.get('sumValue')

    # 使用全局变量中的数据
    df = cache.get('lottery_data_all')
    if df is None:
        logger.error("缓存中的数据为空")
        return result_error(None, message='缓存中的数据为空')

    data = df.head(int(periods)).to_dict(orient='records')
    # 将data转换为df数据类型
    data = pd.DataFrame(data)
    try:
        res = SsqPredict().predictBySum(data, sumValue, 5)
    except Exception as e:
        logger.error(e)
        return result_error(None, message='预测失败')
    print('预测的结果',res)
    return result_success(res)

# 区间预测
@url('laoliu/ssq/predictByZone/', name='predictByZone_api')
def predictByZone(request):
    logger.info("正在预测...")
    # 得到页面上传过来的数据期数和期号
    periods = request.GET.get('periods')
    # 红球前区数量
    front_count = request.GET.get('frontRange')
    # 红球中区数量
    middle_count = request.GET.get('middleRange')
    # 红球后区数量
    back_count = request.GET.get('backRange')
    # 蓝球数量
    blue_count = request.GET.get('blueRange')

    # 使用全局变量中的数据
    df = cache.get('lottery_data_all')
    if df is None:
        logger.error("缓存中的数据为空")
        return result_error(None, message='缓存中的数据为空')

    data = df.head(int(periods)).to_dict(orient='records')
    # 将data转换为df数据类型
    data = pd.DataFrame(data)
    try:
        res = SsqPredict().predictByZone(data, front_count, middle_count, back_count, blue_count, 5)
    except Exception as e:
        logger.error(e)
        return result_error(None, message='预测失败')
    print('预测的结果', res)
    return result_success(res)

# 推荐号码
'''
我们需要修改 predictByOther 方法，
使其在第一次访问时将数据保存到 SQLite 数据库中，并在后续访问时检查数据库中是否存在该数据，如果存在则直接返回。
'''
@url('laoliu/ssq/predictByOther/', name='predictByOther_api')
def predictByOther(request):
    logger.info("正在预测...")
    # 得到页面上传过来的数据期数和期号
    periods = request.GET.get('periods')
    if periods is None:
        logger.error("预测数据为空")
        periods = 30

    # 使用全局变量中的数据
    df = cache.get('lottery_data_all')
    if df is None:
        logger.error("缓存中的数据为空")
        return result_error(None, message='缓存中的数据为空')

    data = df.head(int(periods)).to_dict(orient='records')
    # 将data转换为df数据类型
    data = pd.DataFrame(data)
    # 获取第一条数据的 issueNumber
    issueNumber = data.iloc[0]['issueNumber']

    # 查询数据库中是否存在该 issueNumber
    try:
        prediction = SsqOtherPredict.objects.get(issueNumber=issueNumber)
        result = prediction.result
        # 将result转换为字典
        result = json.loads(result)
        print('sqlite中查询到')
    except SsqOtherPredict.DoesNotExist:
        # 如果不存在，保存结果到数据库并返回
        try:

            result = SsqPredict().predictByOther(data)
            #print('计算得到', result)
            result_str = json.dumps(result)
            SsqOtherPredict.objects.create(issueNumber=issueNumber, result=result_str)
        except Exception as e:
            logger.error(e)
            return result_error(None, message='预测失败')


    return result_success(result)