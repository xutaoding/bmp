# coding=utf-8
import json

import pandas as pd

from bmp.apis.base import BaseApi
from bmp.models.leave import Leave


class Leave_daysApi(BaseApi):
    route = ["/stats/leave/days/<string:begin_time>/<string:end_time>"]

    def get(self, begin_time, end_time):
        result = pd.DataFrame(columns=["name", "days"])
        leaves = pd.read_json(
            json.dumps(Leave.between(begin_time, end_time)))

        if leaves.empty:
            return self.succ([])

        for name, g in leaves.groupby("uid"):
            result.set_value(len(result), ["name", "days"], [name, g.days.sum()])

        result_lst = []
        result.sort_values("days", ascending=False).apply(
            lambda x: result_lst.append({"name": x["name"], "days": x["days"]}), axis=1)

        return self.succ(result_lst)


if __name__ == "__main__":
    result = pd.DataFrame(columns=["name", "days"])

    leaves = pd.read_json(
        json.dumps(Leave.between("2016-01-01", "2016-03-07")))

    for name, g in leaves.groupby("uid"):
        result.set_value(len(result), ["name", "days"], [name, g.days.sum()])

    print(result)
