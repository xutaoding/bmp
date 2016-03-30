from bmp import sched, log
from datetime import datetime, timedelta
from uuid import uuid1
import traceback


def _wrap_job(_id, args, job, minutes):
    try:
        job(*args)
    except Exception, e:
        traceback.print_exc()
        log.exception(e)
        if minutes < 120:
            minutes += 10
            sched.add_job(job,
                          "date",
                          id=_id,
                          run_date=datetime.now() + timedelta(minutes=minutes),
                          misfire_grace_time=60 * 60 * 24 * 365 * 100,
                          args=(_id, args, job, minutes),
                          replace_existing=True)


class BaseTask:
    def add_job(self, job, args=None, date=None, _id=None):
        run_date = datetime.now()
        if date: run_date = date
        if not _id:
            _id = "%s" % (uuid1())

        minutes = 1

        sched.add_job(_wrap_job,
                      "date",
                      id=_id,
                      run_date=run_date,
                      misfire_grace_time=60 * 60 * 24 * 365 * 100,
                      args=(_id, args, job, minutes),
                      replace_existing=True)

        if not sched.running:
            sched.start()


if __name__ == "__main__":
    pass
