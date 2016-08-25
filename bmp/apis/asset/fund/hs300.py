# coding: utf-8

from datetime import datetime

import pandas
from sqlalchemy import create_engine

from bmp import app
from bmp.apis.base import BaseApi


class Hs300Api(BaseApi):
    route = [
        "/asset/fund/hs300/<string:start_date>/<string:end_date>",
        "/asset/fund/hs300/<string:start_date>"
    ]

    def get(self, start_date, end_date=None):
        end_date = end_date if end_date else datetime.now().strftime("%Y-%m-%d")

        data = pandas.read_sql_query(
            "select dt as date,close from hq_index where "
            "tick = '000300' and "
            "unix_timestamp(dt) between "
            "unix_timestamp('%s') and unix_timestamp('%s')" % (start_date, end_date),
            create_engine(app.config["ADA_FD_URI"]))

        return self.succ([{
                              "date": row["date"].strftime("%Y-%m-%d"),
                              "close": row["close"]
                          } for i, row in data.iterrows()])



if __name__ == "__main__":
    pass
