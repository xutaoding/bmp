# coding=utf-8
from datetime import datetime


def format(dt, fmt):
    if isinstance(dt, datetime):
        dt = dt.strftime(fmt)
    # dt=datetime.strptime(dt, fmt) - timedelta(hours=8)
    return dt.__str__()





if __name__ == "__main__":
    print format("2015-01-01 01:01", "%Y-%m-%d %H:%M")
