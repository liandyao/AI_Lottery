import time

import requests
from bs4 import BeautifulSoup
import csv

# 1. 设置请求的 URL 和表单数据
url = "https://kaijiang.78500.cn/3d/"


# 2. 设置请求头，包括 User-Agent
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0'
}

def getData(year=2025):

    form_data = {
        'startqi': '2023001',
        'endqi': '2023351',
        'year': year,
        'action': 'years'
    }
    # 3. 发送 POST 请求
    response = requests.post(url, data=form_data, headers=headers)
    response.encoding = response.apparent_encoding  # 确保正确编码
    html = response.text

    # 4. 解析网页
    soup = BeautifulSoup(html, 'html.parser')

    # 5. 找到目标table
    table = soup.find('table', class_='kjls')

    # 6. 获取第二个<tbody>
    tbody = table.find_all('tbody')[1]

    # 7. 提取数据
    results = []
    for tr in tbody.find_all('tr'):
        tds = tr.find_all('td')
        if len(tds) >= 4:  # 确保有足够的td
            issue = tds[0].text.strip()  # 期数
            draw_date = tds[1].text.strip()  # 开奖日期
            sales_amount = tds[2].text.strip()  # 销售金额
            numbers = tds[3].text.strip().split()  # 开奖结果
            if len(numbers) >= 3:
                result = {
                    'issue': issue,
                    'draw_date': draw_date,
                    'sales_amount': sales_amount,
                    'one': numbers[0],
                    'two': numbers[1],
                    'three': numbers[2]
                }
                results.append(result)

    # 8. 将数据导出到 CSV 文件
    csv_file_name = f"../data/fc_3d_{year}.csv"
    with open(csv_file_name, mode='w', newline='', encoding='utf-8') as csv_file:
        fieldnames = ['issue', 'draw_date', 'sales_amount', 'one', 'two', 'three']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()  # 写入表头
        for result in results:
            writer.writerow(result)  # 写入数据

    print(f"数据已成功导出到 {csv_file_name}")



if __name__ == "__main__":
    getData(2025)