import datetime

from xingyunqiu.getData import GetData_By_Year, GetData_3D


def main():

    year = datetime.datetime.now().strftime("%Y")
    print(f"开始执行获取{year}数据-双色球的数据")
    GetData_By_Year.getData(year)
    print(f"{year}数据-双色球数据获取完毕")
    print(f"开始执行获取{year}数据-3D球的数据")
    GetData_3D.getData(year)
    print(f"{year}数据-3D球数据获取完毕")

if __name__ == '__main__':
    main()