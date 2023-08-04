from apscheduler.schedulers.background import BackgroundScheduler
from .crawler import send_notifications


def start():
    scheduler = BackgroundScheduler()
    scheduler.add_job(send_notifications, 'interval', seconds=30)
    scheduler.start()
