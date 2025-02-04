# xingyunqiu/management/commands/run_scheduler.py
import datetime

from django.core.management.base import BaseCommand
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import logging
from xingyunqiu.getData.GetData_By_Year import getData  # 导入 getData 函数

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Runs APScheduler'

    def handle(self, *args, **options):
        scheduler = BackgroundScheduler()

        # 每晚10点运行 getData(2025)
        @scheduler.scheduled_job('cron', hour=22)  # 22 表示晚上10点
        def scheduled_get_data():
            logger.info("Running getData(2025) at 10 PM.")
            #2025表示当前年份
            year = datetime.datetime.now().strftime("%Y")
            getData(year)

        scheduler.start()
        self.stdout.write('Scheduler started.')

        try:
            # Keep the command running
            while True:
                pass
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()
