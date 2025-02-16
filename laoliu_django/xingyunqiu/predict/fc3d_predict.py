# predict/ssq_predict.py
import datetime
import random
from collections import Counter

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model._base import LinearRegression
from sklearn.model_selection import train_test_split

class fc3dPredict:
    # 简单预测模型：输入6个红球和1个蓝球，返回下一个预测的号码
    def predictByFrequencyLow(self, df):
        # 获取所有列
        # 获取所有列
        columns = ["one", "two", "three"]

        # 定义获取每列频率最低的3个数字的函数
        def find_least_frequent_values(column):
            freq = Counter(df[column])

            # 直接获取出现次数和数字，进行排序
            least_common = freq.most_common()[:-4:-1]  # 取出频率最低的三个数字
            least_frequent_values = [num for num, count in least_common]

            return tuple(sorted(least_frequent_values))

            # 生成结果字典

        result = {column: find_least_frequent_values(column) for column in columns}

        # 打印结果
        print("每列频率最低的3个数字：", result)
        return result

    def predictByFrequencyHigh(self, df):
        # 获取所有列
        # 获取所有列
        columns = ["one", "two", "three"]

        # 定义获取每列频率最低的3个数字的函数
        def find_least_frequent_values(column):
            freq = Counter(df[column])

            # 直接获取出现次数和数字，进行排序
            least_common = freq.most_common(3)  # 取出频率最低的三个数字
            least_frequent_values = [num for num, count in least_common]

            return tuple(sorted(least_frequent_values))

            # 生成结果字典

        result = {column: find_least_frequent_values(column) for column in columns}

        # 打印结果
        print("每列频率最高的3个数字：", result)
        return result

    def predictByFrequencyMiddle(self, df):
        # 获取所有列
        columns = ["one", "two", "three"]

        # 定义获取每列中间频率的3个数字的函数
        def find_middle_frequent_values(column):
            freq = Counter(df[column])

            # 对频率按照出现次数进行排序
            sorted_freq = sorted(freq.items(), key=lambda x: x[1])  # [(数字, 次数), ...]

            # 如果有三种或更多不同的频率
            if len(sorted_freq) > 2:
                # 去掉最大频率和最小频率的项
                middle_frequencies = sorted_freq[1:-1]
            else:
                # 如果只有两种或更少频率，直接返回空元组
                middle_frequencies = []

            print("middle", middle_frequencies)
                # 提取与中间频率对应的数字
            middle_freq_numbers = [num for num, count in middle_frequencies]

            # 返回最多3个数字
            return tuple(middle_freq_numbers[:3])

            # 生成结果字典

        result = {column: find_middle_frequent_values(column) for column in columns}

        # 打印结果
        print("每列中间频率的3个数字：", result)
        return result

    def statisticsFrequency(self, df):
        one_freq = df['one'].value_counts().sort_index().to_dict()
        two_freq = df['two'].value_counts().sort_index().to_dict()
        three_freq = df['three'].value_counts().sort_index().to_dict()
        # 补全所有数字（0-9）的频率
        for num in range(10):
            if num not in one_freq:
                one_freq[num] = 0
            if num not in two_freq:
                two_freq[num] = 0
            if num not in three_freq:
                three_freq[num] = 0

        # 重新排序
        one_freq = dict(sorted(one_freq.items()))
        two_freq = dict(sorted(two_freq.items()))
        three_freq = dict(sorted(three_freq.items()))
        # 将结果合并为一个字典
        result = {
            'one': one_freq,
            'two': two_freq,
            'three': three_freq
        }
        return result


if __name__ == "__main__":
        # 替换为您的历史双色球数据文件路径
        data = pd.read_csv('../data/fc_3d_2025.csv')

        res = fc3dPredict().statisticsFrequency(data)
        print(res)

