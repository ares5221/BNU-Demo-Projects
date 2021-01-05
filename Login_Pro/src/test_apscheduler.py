#!/usr/bin/env python
# _*_ coding:utf-8 _*_

from datetime import datetime
from datetime import date
from apscheduler.schedulers.blocking import BlockingScheduler

def job(text):
    print(text)

scheduler = BlockingScheduler()
# 在 2019-8-30 运行一次 job 方法
scheduler.add_job(job, 'date', run_date=date(2020, 8, 28), args=['text1'])
# # 在 2019-8-30 01:00:00 运行一次 job 方法
scheduler.add_job(job, 'date', run_date=datetime(2020, 8, 28, 13, 19, 0), args=['text2'])
# # 在 2019-8-30 01:00:01 运行一次 job 方法
scheduler.add_job(job, 'cron', hour=13,minute=25, args=['text3'])

scheduler.start()