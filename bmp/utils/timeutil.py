# coding=utf-8
from datetime import datetime


def format(dt, fmt):
    if isinstance(dt, datetime):
        dt = dt.strftime(fmt)
    # dt=datetime.strptime(dt, fmt) - timedelta(hours=8)
    return dt.__str__()

from datetime import timedelta

if __name__ == "__main__":

    dt=datetime.now()
    print dt
    print(dt)





