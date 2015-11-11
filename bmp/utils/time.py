# coding=utf-8
from datetime import datetime
from datetime import timedelta


def format(dt, fmt):
    if isinstance(dt, datetime):
        dt = dt.strftime(fmt)
    return datetime.strptime(dt, fmt) - timedelta(hours=8)


if __name__ == "__main__":
    print format("2015-01-01 01:01", "%Y-%m-%d %H:%M")
