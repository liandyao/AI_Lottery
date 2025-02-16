# xingyunqiu/apps.py
import os
import pandas as pd
from django.apps import AppConfig
from django.core.cache import cache
from apscheduler.schedulers.background import BackgroundScheduler

class XingyunqiuConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'xingyunqiu'

    def ready(self):
        self.update_cache()

        # 启动定时任务
        scheduler = BackgroundScheduler()
        scheduler.add_job(self.update_cache, 'interval', minutes=5)
        scheduler.start()

    def update_cache(self):
        # 确保文件路径正确
        self.update_ssq_cache()
        self.update_fc3d_cache()
        self.update_tcp3_cache()

    def update_ssq_cache(self):
        # 确保文件路径正确
        file_path = os.path.join(os.path.dirname(__file__), 'data', 'lottery_results_2003_2024.csv')
        data_df = pd.read_csv(file_path)
        # 将数据缓存起来
        # cache.set('lottery_data_2024', data_df)

        # 缓存2025年的数据
        file_path = os.path.join(os.path.dirname(__file__), 'data', 'lottery_results_2025.csv')
        data_df_2025 = pd.read_csv(file_path)
        # cache.set('lottery_data_2025', data_df_2025)

        # 将2024和2025的数据整合到一个df
        data_df_all = pd.concat([data_df, data_df_2025], ignore_index=True)
        # data_df_all按期数排序，逆序，列名为：issueNumber
        data_df_all = data_df_all.sort_values(by='issueNumber', ascending=False)

        cache.set('lottery_data_all', data_df_all)
        print("数据已更新到缓存中lottery_data_all")

    def update_fc3d_cache(self):
        # 确保文件路径正确
        file_path = os.path.join(os.path.dirname(__file__), 'data', 'fc_3d_2003_2024.csv')
        data_df = pd.read_csv(file_path)
        # 将数据缓存起来
        #cache.set('fc3d_data_2024', data_df)

        # 缓存2025年的数据
        file_path = os.path.join(os.path.dirname(__file__), 'data', 'fc_3d_2025.csv')
        data_df_2025 = pd.read_csv(file_path)
        #cache.set('lottery_data_2025', data_df_2025)

        # 将2024和2025的数据整合到一个df
        data_df_all = pd.concat([data_df, data_df_2025], ignore_index=True)
        # data_df_all按期数排序，逆序，列名为：issueNumber
        data_df_all = data_df_all.sort_values(by='issue', ascending=False)

        cache.set('fc3d_data_all', data_df_all)
        print("数据已更新到缓存中fc3d_data_all")

    def update_tcp3_cache(self):
        # 确保文件路径正确
        file_path = os.path.join(os.path.dirname(__file__), 'data', 'tc_p3_2003_2024.csv')
        data_df = pd.read_csv(file_path)
        # 将数据缓存起来
        #cache.set('fc3d_data_2024', data_df)

        # 缓存2025年的数据
        file_path = os.path.join(os.path.dirname(__file__), 'data', 'tc_p3_2025.csv')
        data_df_2025 = pd.read_csv(file_path)
        #cache.set('lottery_data_2025', data_df_2025)

        # 将2024和2025的数据整合到一个df
        data_df_all = pd.concat([data_df, data_df_2025], ignore_index=True)
        # data_df_all按期数排序，逆序，列名为：issueNumber
        data_df_all = data_df_all.sort_values(by='issue', ascending=False)

        cache.set('tcp3_data_all', data_df_all)
        print("数据已更新到缓存中tc_p3_data_all")