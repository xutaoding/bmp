# coding: utf-8
from bmp.apis.base import BaseApi
from bmp.models.asset import StockOpt


class ScrapApi(BaseApi):
    route = ["/asset/scrap/<int:page>/<int:pre_page>"]

    def get(self, page=0, pre_page=None):
        return self.succ(StockOpt.approvals(page, pre_page))


if __name__ == "__main__":
    pass
