from apscheduler.schedulers.background import BlockingScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from bmp import app
from apscheduler.executors.pool import ProcessPoolExecutor

sched = BlockingScheduler(
            executors={
                "default": ProcessPoolExecutor(1)
            },
            job_defaults={"coalesce": False, "max_instances": 1}
        )

from datetime import datetime

def test():
    print "test"

#sched.add_job(test,next_run_time=datetime(2016,3,28,17,5),name="testabc")



sched.start()



