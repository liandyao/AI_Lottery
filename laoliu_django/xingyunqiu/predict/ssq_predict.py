# predict/ssq_predict.py
import datetime
import random
from collections import Counter

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model._base import LinearRegression
from sklearn.model_selection import train_test_split

class SsqPredict:
    # 简单预测模型：输入6个红球和1个蓝球，返回下一个预测的号码
    def predictByFrequency(self, data, input_red_balls, num_predictions=5):
        print("正在预测...",input_red_balls)
        """
        简化的双色球预测模型
        输入历史数据 + 6个红球，输出多组预测结果。
        """
        """
           简化的双色球预测模型
           输入历史数据 + 6个红球，输出多组预测结果。
           """
        ### 数据预处理 ###
        # 确保输入的列名与数据对齐
        red_ball_columns = ['redBall1', 'redBall2', 'redBall3', 'redBall4', 'redBall5', 'redBall6']
        blue_ball_column = 'blueBall'

        # 构造特征列
        # 前一期的开奖结果
        data['prev_redBall1'] = data['redBall1'].shift(1)
        data['prev_redBall2'] = data['redBall2'].shift(1)
        data['prev_redBall3'] = data['redBall3'].shift(1)
        data['prev_redBall4'] = data['redBall4'].shift(1)
        data['prev_redBall5'] = data['redBall5'].shift(1)
        data['prev_redBall6'] = data['redBall6'].shift(1)
        data['prev_blueBall'] = data['blueBall'].shift(1)

        # 删除包含 NaN 的行
        data.dropna(inplace=True)

        ### 预测逻辑 ###
        formatted_predictions = []

        for i in range(num_predictions):
            ### 红球预测 ###
            # 构造特征列
            feature_columns = ['prev_redBall1', 'prev_redBall2', 'prev_redBall3', 'prev_redBall4', 'prev_redBall5',
                               'prev_redBall6', 'prev_blueBall']

            # 将输入的红球转换为 DataFrame，并指定列名
            input_data = pd.DataFrame([input_red_balls], columns=red_ball_columns)

            # 为输入数据构造特征列，并使用默认值填充
            for col in feature_columns:
                input_data[col] = 0  # 使用默认值 0 填充

            # 特征和目标变量
            X = data[feature_columns]  # 特征为前一期的开奖结果
            y = data[red_ball_columns]  # 获取所有红球的历史数据

            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42 + i)  # 使用不同的随机种子

            # 训练随机森林回归模型
            red_ball_model = RandomForestRegressor(n_estimators=100, random_state=42 + i)  # 使用不同的随机种子
            red_ball_model.fit(X_train, y_train)

            # 使用训练好的模型预测提供的输入
            predicted_red_balls = red_ball_model.predict(input_data[feature_columns])[0]
            predicted_red_balls = [int(round(ball)) for ball in predicted_red_balls]  # 将预测结果四舍五入并转换为整数

            ### 蓝球预测 ###
            # 创建蓝球模型
            X = data[feature_columns]  # 蓝球特征基于前一期的开奖结果
            y_blue = data[blue_ball_column]  # 蓝球目标

            X_train, X_test, y_train, y_test = train_test_split(X, y_blue, test_size=0.2,
                                                                random_state=42 + i)  # 使用不同的随机种子

            blue_ball_model = RandomForestRegressor(n_estimators=100, random_state=42 + i)  # 使用不同的随机种子
            blue_ball_model.fit(X_train, y_train)

            # 使用模型预测蓝球
            predicted_blue_ball = blue_ball_model.predict(input_data[feature_columns])[0]
            predicted_blue_ball = int(round(predicted_blue_ball))  # 将预测结果四舍五入并转换为整数

            # 将预测结果存储在字典中
            formatted_predictions.append({
                'redBalls': predicted_red_balls,
                'blueBall': predicted_blue_ball
            })

        # 返回结果为字典
        res = {
            'predictions': formatted_predictions
        }

        return res

    def train_and_predict_by_issue(self, data, start_issue, num_predictions=5):
        """
        通过期数的尾数后两位作为特征预测下一期的号码
        输入历史数据 + 起始期数，输出多组预测结果。
        """
        # 提取期数的尾数后两位
        data['issueNumber_last_two'] = data['issueNumber'].apply(lambda x: x % 100)

        # 特征和目标变量
        X = data[['issueNumber_last_two']]
        y_red = data[['redBall1', 'redBall2', 'redBall3', 'redBall4', 'redBall5', 'redBall6']]
        y_blue = data['blueBall']  # 注意这里直接使用 Series 而不是 DataFrame

        # 拆分数据集
        X_train, X_test, y_red_train, y_red_test, y_blue_train, y_blue_test = train_test_split(
            X, y_red, y_blue, test_size=0.2, random_state=42
        )

        # 创建模型
        red_model = RandomForestRegressor(n_estimators=100, random_state=42)
        blue_model = RandomForestRegressor(n_estimators=100, random_state=42)

        # 训练模型
        red_model.fit(X_train, y_red_train)
        blue_model.fit(X_train, y_blue_train)

        # 预测结果列表
        formatted_predictions = []

        for i in range(num_predictions):
            # 计算当前预测的期数
            current_issue = start_issue + i

            # 提取当前期数的尾数后两位
            current_issue_last_two = current_issue % 100

            # 确保 issue 以 DataFrame 形式传入
            issue_number_df = pd.DataFrame({'issueNumber_last_two': [current_issue_last_two]})

            # 在此输入特征进行预测
            red_balls = red_model.predict(issue_number_df)
            blue_ball = blue_model.predict(issue_number_df)

            # 使用 map 函数将 red_balls[0] 中的元素都转为整数
            red_balls_list = list(map(int, red_balls[0]))  # 取整

            # 引入随机性，确保每次预测结果不同
            red_balls_list = [ball + np.random.randint(-1, 2) for ball in red_balls_list]  # 随机调整红球号码
            blue_ball = blue_ball[0] + np.random.randint(-1, 2)  # 随机调整蓝球号码

            # 确保红球号码在有效范围内（1-33）
            red_balls_list = [max(1, min(33, ball)) for ball in red_balls_list]

            # 确保蓝球号码在有效范围内（1-16）
            blue_ball = max(1, min(16, blue_ball))

            # 将预测结果存储在字典中
            formatted_predictions.append({
                'redBalls': red_balls_list,
                'blueBall': int(blue_ball)
            })

        # 返回结果为字典
        res = {
            'predictions': formatted_predictions
        }

        return res


    '''
    要实现根据输入的星期对历史数据进行训练，并预测下一期的彩票号码，我们可以按照以下步骤进行：
数据预处理：将 drawTime 转换为星期，并提取红球和蓝球号码。
特征工程：统计每个星期中每个号码出现的频率。
模型训练：使用简单的统计方法（如频率最高的号码）进行预测。
由于彩票号码的预测是一个非常复杂的任务，通常需要更复杂的模型和更多的数据。这里我们使用简单的频率统计方法来进行预测。
    '''
    def predictByWeekday(self,data,weekday, num_predictions=3):

        weekday=int(weekday)
        # 将日期转换为星期
        def convert_draw_time_to_weekday(draw_time):
            return datetime.datetime.strptime(draw_time, '%Y-%m-%d').weekday() + 1  # 周日为7



        # 使用星期作为特征。预测下次的开奖结果
        # 例如，输入的是周二，那么将历史记录中的周二数据作为特征训练模型。当我输入周二那么可以预测下一期周二的结果。

        # 转换 drawTime 列为星期
        data['weekday'] = data['drawTime'].apply(convert_draw_time_to_weekday)

            # 过滤出目标星期的数据
        target_data = data[data['weekday'] == weekday]

        if target_data.empty:
            raise ValueError(f"No data found for weekday {weekday}")

        # 提取目标星期的红球和蓝球号码
        target_red_balls = target_data[
            ['redBall1', 'redBall2', 'redBall3', 'redBall4', 'redBall5', 'redBall6']].values.flatten()
        target_blue_balls = target_data['blueBall'].values

        # 统计红球和蓝球号码的频率
        red_ball_counts = Counter(target_red_balls)
        blue_ball_counts = Counter(target_blue_balls)

        # 找出频率最高的红球和蓝球号码
        most_common_red_balls = [ball for ball, _ in red_ball_counts.most_common(33)]  # 假设红球号码范围是1-36
        most_common_blue_balls = [ball for ball, _ in blue_ball_counts.most_common(16)]  # 假设蓝球号码范围是1-12


        predictions = []
        for _ in range(num_predictions):

            # 随机选择6个红球和1个蓝球
            selected_red_balls = np.random.choice(most_common_red_balls, 6, replace=False)
            selected_blue_ball = np.random.choice(most_common_blue_balls, 1)[0]
            print('----',selected_blue_ball)
            selected_red_balls = sorted(selected_red_balls.tolist())
            predictions.append({
                'redBalls': selected_red_balls,
                'blueBall': int(selected_blue_ball)
            })

        return predictions
    # 根据和值预测
    '''
    给出一个和值，将data中红球的数值累加，如果和值等于给定的和值，则为有效数据，使用该数据进行训练，
    然后使用下一期的和值作为特征，预测的开奖结果。
    预测结果为字典，包含红球号码和蓝球号码。
    [{
redBalls:[1,2,3,4,5,6],
blueBass:8
},{
redBalls:[1,2,3,4,5,6],
blueBass:8
},{
redBalls:[1,2,3,4,5,6],
blueBass:8
}]
请使用我的ssq_predict.py的规则写代码，不要使用你认为正确的方式，在我的代码中，每个函数都有各自的作用
    '''

    # 根据和值预测
    # 给出一个和值，将data中红球的数值累加，如果和值等于给定的和值，则为有效数据，使用该数据进行训练，
    # 然后使用下一期的和值作为特征，预测的开奖结果。
    # 预测结果为字典，包含红球号码和蓝球号码。
    def predictBySum(self, data, sum_value, num_predictions=3):
        sum_value = int(sum_value)

        # 计算红球和值
        data['redBallsSum'] = data[['redBall1', 'redBall2', 'redBall3', 'redBall4', 'redBall5', 'redBall6']].sum(axis=1)

        # 过滤出红球和值等于给定和值的数据
        filtered_data = data[data['redBallsSum'] == sum_value]
        print('filtered_data==>',filtered_data)
        if filtered_data.empty:
            raise ValueError(f"No data found for red balls sum {sum_value}")

        # 获取下一期的和值
        next_sum_values = []
        next_data = pd.DataFrame()
        for index, row in filtered_data.iterrows():
            next_index = index - 1
            if next_index < 0:
                next_index = 0
            print('next_index==>',next_index)
            # 将下一期的数据放入到next_data中
            next_data = pd.concat([next_data, data.loc[next_index:next_index]])
            if next_index < len(data):
                next_sum_values.append(data.at[next_index, 'redBallsSum'])

        if not next_sum_values:
            raise ValueError(f"No next sum values found for red balls sum {sum_value}")

        # 过滤出所有历史记录中红球和值等于 next_sum_value 的数据
        next_data = data[data['redBallsSum'].isin(next_sum_values)]

        if next_data.empty:
            raise ValueError(f"No data found for next red balls sum {next_sum_values}")

        # 提取所有红球和蓝球号码
        all_red_balls = next_data[
            ['redBall1', 'redBall2', 'redBall3', 'redBall4', 'redBall5', 'redBall6']].values.flatten()
        all_blue_balls = next_data['blueBall'].values

        # 确保有足够的红球和蓝球号码
        if len(all_red_balls) < 6:
            raise ValueError(f"Not enough red balls to form a prediction. Found {len(all_red_balls)} red balls.")
        if len(all_blue_balls) < 1:
            raise ValueError(f"Not enough blue balls to form a prediction. Found {len(all_blue_balls)} blue balls.")

        predictions = set()  # 使用集合来确保每组号码不完全相同

        while len(predictions) < num_predictions:
            # 随机选择6个红球
            selected_red_balls = np.random.choice(all_red_balls, 6, replace=True)
            # 随机选择1个蓝球
            selected_blue_ball = np.random.choice(all_blue_balls, 1, replace=True)[0]
            # 将选中的号码转换为元组并添加到集合中
            prediction = (tuple(selected_red_balls), selected_blue_ball)
            predictions.add(prediction)

            # 将集合转换为列表并格式化为字典
        formatted_predictions = []
        for prediction in predictions:
            red_balls, blue_ball = prediction
            # 将 np.int64 转换为普通整数
            red_balls = [int(ball) for ball in red_balls]
            formatted_predictions.append({
                'redBalls': sorted(red_balls, reverse=False),
                'blueBall': int(blue_ball)
            })
        # 将目标数据和预测结果返回
        # 将df的filtered_data数据转换为正常数组数据
        filtered_data = filtered_data.to_dict(orient='records')
        next_data = next_data.to_dict(orient='records')
        res ={
            'filtered_data':filtered_data,
            'next_data':next_data,
            'predictions':formatted_predictions
        }
        return res

    def predictByZone(self, data, front_count, middle_count, back_count, blue_count, num_predictions=3):
        # 解析参数
        front_count = int(front_count)
        middle_count = int(middle_count)
        back_count = int(back_count)
        blue_count = int(blue_count)

        # 定义红球的前区、中区、后区范围
        front_range = (1, 11)
        middle_range = (12, 22)
        back_range = (23, 33)

        # 提取所有红球和蓝球号码
        all_red_balls = data[
            ['redBall1', 'redBall2', 'redBall3', 'redBall4', 'redBall5', 'redBall6']].values.flatten()
        all_blue_balls = data['blueBall'].values

        # 筛选出前区、中区、后区的红球号码
        front_red_balls = [ball for ball in all_red_balls if front_range[0] <= ball <= front_range[1]]
        middle_red_balls = [ball for ball in all_red_balls if middle_range[0] <= ball <= middle_range[1]]
        back_red_balls = [ball for ball in all_red_balls if back_range[0] <= ball <= back_range[1]]

        # 确保有足够的红球和蓝球号码
        if len(front_red_balls) < front_count:
            raise ValueError(f"Not enough red balls in the front range. Found {len(front_red_balls)} red balls.")
        if len(middle_red_balls) < middle_count:
            raise ValueError(f"Not enough red balls in the middle range. Found {len(middle_red_balls)} red balls.")
        if len(back_red_balls) < back_count:
            raise ValueError(f"Not enough red balls in the back range. Found {len(back_red_balls)} red balls.")
        if len(all_blue_balls) < blue_count:
            raise ValueError(f"Not enough blue balls. Found {len(all_blue_balls)} blue balls.")

        predictions = []

        for _ in range(num_predictions):
            # 随机选择前区、中区、后区的红球号码
            selected_front_red_balls = np.random.choice(front_red_balls, front_count, replace=False)
            selected_middle_red_balls = np.random.choice(middle_red_balls, middle_count, replace=False)
            selected_back_red_balls = np.random.choice(back_red_balls, back_count, replace=False)

            # 合并所有选中的红球号码
            selected_red_balls = np.concatenate(
                (selected_front_red_balls, selected_middle_red_balls, selected_back_red_balls))

            # 随机选择蓝球号码
            selected_blue_balls = np.random.choice(all_blue_balls, blue_count, replace=False)

            # 将选中的号码转换为普通整数并排序
            selected_red_balls = sorted([int(ball) for ball in selected_red_balls])
            selected_blue_balls = sorted([int(ball) for ball in selected_blue_balls])

            # 确保红球号码总数为6
            if len(selected_red_balls) != 6:
                raise ValueError(f"Selected red balls count is not 6. Found {len(selected_red_balls)} red balls.")

            # 确保蓝球号码总数为1
            if len(selected_blue_balls) != 1:
                raise ValueError(f"Selected blue balls count is not 1. Found {len(selected_blue_balls)} blue balls.")

            # 添加到预测结果中
            predictions.append({
                'redBalls': selected_red_balls,
                'blueBall': selected_blue_balls[0]
            })

        return predictions

    # 热球推荐
    def predictByOther(self,data):
        # 提取龙头号码范围（红球最小号码范围，通常为01-05）
        # 提取龙头号码范围（红球最小号码范围，取最多2个号码）
        # 提取龙头号码范围（红球最小号码范围，基于概率选取最可能的2个号码）
        def calculate_longtou(data):
            # 提取历史数据中所有红球1（龙头位置）的号码
            longtou_numbers = data['redBall1'].values.flatten()
            # 统计每个号码出现的次数并排序
            counts = Counter(longtou_numbers).most_common()
            # 按出现次数排序后，选择最多2个出现概率最高的号码
            result = [str(num).zfill(2) for num, _ in counts[:2]]
            return result

            # 提取凤尾号码范围（红球最大号码范围，基于概率选取最可能的2个号码）

        def calculate_fengwei(data):
            # 提取历史数据中所有红球6（凤尾位置）的号码
            fengwei_numbers = data['redBall6'].values.flatten()
            # 统计每个号码出现的次数并排序
            counts = Counter(fengwei_numbers).most_common()
            # 按出现次数排序后，选择最多2个出现概率最高的号码
            result = [str(num).zfill(2) for num, _ in counts[:2]]
            return result

            # 提取重号（上期开奖号码中重复出现的号码）

        def calculate_chonghao(data):
            last_issue = data.iloc[0]
            current_issue = data.iloc[1]
            last_red_balls = set(last_issue[['redBall1', 'redBall2', 'redBall3', 'redBall4', 'redBall5', 'redBall6']])
            current_red_balls = set(
                current_issue[['redBall1', 'redBall2', 'redBall3', 'redBall4', 'redBall5', 'redBall6']])
            return sorted([str(x).zfill(2) for x in last_red_balls & current_red_balls])

            # 提取杀号（根据历史数据排除的号码）

        def calculate_shahao(data):
            all_red_balls = data[
                ['redBall1', 'redBall2', 'redBall3', 'redBall4', 'redBall5', 'redBall6']].values.flatten()
            red_ball_counts = Counter(all_red_balls)
            # 排除历史中出现次数最少的号码
            least_common = red_ball_counts.most_common()[-5:]  # 取出现次数最少的5个号码
            return sorted([str(num).zfill(2) for num, _ in least_common])

            # 提取邻号（与上期开奖号码相邻的号码）

        def calculate_linhao(data):
            last_issue = data.iloc[0]
            last_red_balls = set(last_issue[['redBall1', 'redBall2', 'redBall3', 'redBall4', 'redBall5', 'redBall6']])
            linhao = set()
            for num in last_red_balls:
                linhao.add(num - 1)
                linhao.add(num + 1)
            linhao = linhao - last_red_balls  # 去掉已经开出的号码
            return sorted([str(x).zfill(2) for x in linhao if 1 <= x <= 33])

            # 提取热号（近期出现频率较高的号码）

        def calculate_rehao(data):
            recent_data = data.tail(30)  # 取最近30期数据
            recent_red_balls = recent_data[
                ['redBall1', 'redBall2', 'redBall3', 'redBall4', 'redBall5', 'redBall6']].values.flatten()
            red_ball_counts = Counter(recent_red_balls)
            most_common = red_ball_counts.most_common(5)  # 取出现次数最多的5个号码
            return sorted([str(num).zfill(2) for num, _ in most_common])

            # 提取蓝球的基础选号范围（底码）

        def calculate_dima(data):
            all_blue_balls = data['blueBall'].values  # 获取所有历史蓝球数据
            blue_ball_counts = Counter(all_blue_balls)  # 统计蓝球的出现次数

            # 按频率排序（降序），相同频率则按号码大小排序，只获取前8个
            dima = sorted(blue_ball_counts.keys(), key=lambda x: (-blue_ball_counts[x], x))
            dima = [str(num).zfill(2) for num in dima[:8]]  # 格式化为两位字符串

            return dima

            # 提取精选蓝球号码

        def calculate_jingxuan(blue_base):

            return sorted(random.sample(blue_base, 4))  # 从底码中随机选择 4 个蓝球号码

            # 提取胆码（最有可能出现的蓝球号码）

        def calculate_danma(jingxuan_blue):

            return sorted(random.sample(jingxuan_blue, 2))  # 从精选码中随机选择 2 个蓝球号码

            # 生成方案数据

        # 生成精选5注，根据红球12码和蓝球4码生成5组精选号码
        def generate_scheme_data(red_data, blue_data):
            # 整合红球号码
            # 整合红球号码
            longTou = red_data.get("longTou", [])
            fengWei = red_data.get("fengWei", [])
            chongHao = red_data.get("chongHao", [])
            linHao = red_data.get("linHao", [])
            reHao = red_data.get("reHao", [])

            # 剔除杀号后，整合红球
            red12 = sorted(set(longTou + fengWei + chongHao + linHao + reHao))

            # 如果不足12个号码，则随机选取未使用的号码进行补足
            if len(red12) < 12:
                available_red = [f"{i:02}" for i in range(1, 34) if f"{i:02}" not in red12]
                red12 += random.sample(available_red, 12 - len(red12))
                red12 = sorted(red12)  # 再排序一下
            else:
                # 多于12个，则随机取12个
                red12 = sorted(random.sample(red12, 12))

            # 整合蓝球号码
            diMa = blue_data.get("diMa", [])
            jingXuan = blue_data.get("jingXuan", [])
            danMa = blue_data.get("danMa", [])

            # 挑选蓝球
            blue4 = sorted(set(diMa + jingXuan + danMa))

            # 如果不足4个号码，则随机选取未使用的号码进行补足
            if len(blue4) < 4:
                available_blue = [f"{i:02}" for i in range(1, 17) if f"{i:02}" not in blue4]
                blue4 += random.sample(available_blue, 4 - len(blue4))
                blue4 = sorted(blue4)
            else:
                # 多于4个，则随机取4个
                blue4 = sorted(random.sample(blue4, 4))


                # 精选5组方案
            jingxuan5 = []
            for i in range(5):
                red_group = sorted(random.sample(red12, 6))
                # 蓝球随机选择1个
                blue_ball = random.choice(blue4)
                # 组装精选号码
                jingxuan5.append({"red": red_group, "blue": blue_ball})

            return {
                "red12": red12,
                "blue4": blue4,
                "jingXuan5": jingxuan5,
            }

        red_data = {
            "longTou": calculate_longtou(data),
            "fengWei": calculate_fengwei(data),
            "chongHao": calculate_chonghao(data),
            "shaHao": calculate_shahao(data),
            "linHao": calculate_linhao(data),
            "reHao": calculate_rehao(data),
        }
        dima = calculate_dima(data)
        jingXuan = calculate_jingxuan(dima)
        danma = calculate_danma(jingXuan)
        blue_data = {
            "diMa": dima,
            "jingXuan": jingXuan,
            "danMa": danma,
        }

        scheme_data = generate_scheme_data(red_data, blue_data)

        result = {
            "redData": red_data,
            "blueData": blue_data,
            "schemeData": scheme_data,
        }
        print('result', result)
        return result

    # 示例：加载数据并调用函数
if __name__ == "__main__":
        # 替换为您的历史双色球数据文件路径
        data = pd.read_csv('../data/lottery_results_2003_2024.csv')

        # # 示例预测根据区间
        # front_count = 3
        # middle_count = 2
        # back_count = 1
        # blue_count = 1
        # predictions_zone = SsqPredict().predictByZone(data, front_count, middle_count, back_count, blue_count, 3)
        # for i, prediction in enumerate(predictions_zone, 1):
        #     print(f"预测组 {i}: 红球号码: {prediction['redBalls']}, 蓝球号码: {prediction['blueBall']}")

        # predictions_zone=SsqPredict().predictByOther(data)
        # print(predictions_zone)

        input_red_balls = [6,13,17,22,24,29]  # 你的输入红球
        num_predictions = 5  # 需要预测的组数

        res = SsqPredict().train_and_predict_by_issue(data, 2025011, num_predictions)
        print(res)