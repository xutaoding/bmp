# coding=utf-8
from datetime import datetime

from bmp.apis.base import BaseApi
from bmp.models.release import Release


class Release_appApi(BaseApi):
    route = ["/stats/release/app/<string:begin_time>/<string:end_time>"]

    def get(self, begin_time, end_time):
        result = {}
        for release in Release.between(
                datetime.strptime(begin_time, "%Y-%m-%d"),
                datetime.strptime(end_time, "%Y-%m-%d")):

            svc_name = release["service"]["name"]
            svc_type = release["service"]["type"]
            if not result.__contains__(svc_name):
                result[svc_name] = {}
            if not result[svc_name].__contains__(svc_type):
                result[svc_name][svc_type] = 1
            else:
                result[svc_name][svc_type] += 1

        return self.succ(result)


if __name__ == "__main__":
    pass
