'''

@date 2024年11月20日
@author liandyao
抖音号: liandyao
'''
import csv
import time

import numpy as np
import requests
from bs4 import BeautifulSoup

# 定义 URL
url = "https://kaijiang.78500.cn/ssq/"

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
    'cookie': '__jsluid_s=5cbbf684106add1620b7f5ce24625702; Hm_lvt_04f41dcf6d388d39feb87abb77da8596=1732092072,1732159935; Hm_lpvt_04f41dcf6d388d39feb87abb77da8596=1732159935; HMACCOUNT=99BF57D36F600EB6',
    'referer': 'https://kaijiang.78500.cn/ssq/'
}

data = []  # 用于存储提取的数据
# 循环从 2004 年到 2024 年
for year in range(2003, 2025):  # 2025 是上限，因此将终止于 2024
    params = {
        "startqi": "",  # 空字符串
        "endqi": "",  # 空字符串
        "year": str(year),  # 当前年份
        "action": "years"
    }

    # 发送 POST 请求
    response = requests.post(url, data=params,headers=header)
    time.sleep(np.random.randint(1, 5))

    # 输出请求状态码和返回内容的前100个字符
    print(f"年份: {year}, 状态码: {response.status_code}, 返回内容: {response.text[:100]}")  # 只输出前100个字符
    # 检查请求是否成功


    # 检查请求是否成功
    if response.status_code == 200:
        # 解析 HTML 内容
        soup = BeautifulSoup(response.text, 'html.parser')

        # 查找 tbody 下的所有 tr
        tbody = soup.find('tbody', class_='list-tr')
        if tbody:
            rows = tbody.find_all('tr')
            for row in rows:
                # 提取期号和开奖时间
                tds = row.find_all('td')
                if len(tds) >= 3:  # 确保有足够的 td
                    issue_number = tds[0].text.strip()  # 期号
                    draw_time = tds[1].text.strip()  # 开奖时间

                    # 提取开奖号码
                    numbers_div = tds[2].find('div')  # 找到包含号码的 div
                    red_numbers = [num.text.strip() for num in numbers_div.find_all('span', class_='red')]
                    # 注意,这里的蓝球是一个列表,有时会开出快乐星期天的另一个篮球,所以我们只取第一个篮球
                    blue_numbers = [num.text.strip() for num in numbers_div.find_all('span', class_='blue')]


                    top1 = tds[5].text.strip()  # 一等奖
                    top2 = tds[7].text.strip()  # 二等奖
                    top3 = tds[9].text.strip()  # 三等奖

                    # 整合数据
                    data.append([issue_number, draw_time] + red_numbers + [blue_numbers[0]] +[top1,top2,top3])

            # 导出为 CSV 文件
with open('../data/lottery_results_2003_2024.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csv_writer = csv.writer(csvfile)
    # 写入标题行
    #csv_writer.writerow(['期号', '开奖时间', '红球1', '红球2', '红球3', '红球4', '红球5', '红球6', '蓝球', '一等奖', '二等奖', '三等奖'])
    csv_writer.writerow(
        ['issueNumber', 'drawTime', 'redBall1', 'redBall2', 'redBall3', 'redBall4', 'redBall5', 'redBall6',
         'blueBall', 'firstPrize', 'secondPrize', 'thirdPrize'])
    # 写入数据
    csv_writer.writerows(data)

print("数据已成功导出为 lottery_results_2003_2024.csv")