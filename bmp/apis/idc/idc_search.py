# coding: utf-8

from bmp.apis.base import BaseApi
from bmp.models.idc import Idc_host, Idc_host_disk, Idc_host_interface, Idc_host_ps


class Idc_searchApi(BaseApi):
    route = ["/idc/search/<int:page>/<int:pre_page>", "/idc/search/<int:page>/<int:pre_page>/<int:is_fuzzy>"]

    def get(self, page, pre_page, is_fuzzy=0):
        return self.succ(Idc_host.select(
            page,
            pre_page,
            _joins=[Idc_host_disk, Idc_host_interface, Idc_host_ps],
            _filters=self.get_search_fields([Idc_host, Idc_host_ps, Idc_host_disk, Idc_host_interface], is_fuzzy))
        )


if __name__ == "__main__":
    for host in Idc_host.select(1, 10, _joins=[Idc_host_disk, Idc_host_interface, Idc_host_ps],
                                _filters=Idc_host_interface.ip_address.like("122.144.134.9"))["items"]:
        print host
