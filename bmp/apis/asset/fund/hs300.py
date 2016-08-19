# coding: utf-8

import csf

from bmp.apis.base import BaseApi


class Hs300Api(BaseApi):
    route = [
        "/asset/fund/hs300/<string:start_date>/<string:end_date>"
    ]

    def get(self, start_date, end_date):
        csf.config.set_token("03255a3fbddc4c43fe5f01dc7a06f118", "6ZN2oID+6KHqZx68JpmTUDPFWRU=")
        csf.config.debug=True
        bars = csf.get_index_hist_bar(
            "000300",
            start_date=start_date,
            end_date=end_date,
            field=["date", "close"]
        ).reset_index().rename(columns={"index": "date"})

        return self.succ([{
                              "date": row["date"].strftime("%Y-%m-%d"),
                              "close": row["close"]
                          } for i, row in bars.iterrows()])
