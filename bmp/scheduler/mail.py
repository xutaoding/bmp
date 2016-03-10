from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from bmp.models.mail import Mail
import bmp.utils.mail as mail
from bmp import app



sched = BackgroundScheduler(
    jobstores={
        "default": SQLAlchemyJobStore(url="sqlite:///mails.sqlite")
    }
)

def monitor_mail():
    from flask import app
    with app.app_context():
        for m in Mail.select():
            mail.send(m.sub,m.html,m.receiver,m.copyto)


sched.add_job(monitor_mail,"cron", second="*/3", hour="*")