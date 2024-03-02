import logging
from apscheduler.schedulers.background import BackgroundScheduler
from hollarek.tmpl.singleton import Singleton
from typing import Optional


class ScheduleHandler(Singleton):
    scheduler : Optional[BackgroundScheduler]= None
    logging.getLogger('apscheduler').setLevel(logging.ERROR)

    @classmethod
    def get_scheduler(cls):
        if not cls.scheduler:
            cls.scheduler = BackgroundScheduler()
            cls.scheduler.start()
        return cls.scheduler


def schedule(callback: callable, interval_in_sec: int):
    scheduler = ScheduleHandler.get_scheduler()
    scheduler.add_job(callback, 'interval', seconds=interval_in_sec)