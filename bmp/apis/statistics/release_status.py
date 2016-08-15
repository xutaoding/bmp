# coding=utf-8
from datetime import datetime

from bmp.apis.base import BaseApi
from bmp.const import RELEASE
from bmp.models.release import Release


class Release_statusApi(BaseApi):
    route = ["/stats/release/status/<string:begin_time>/<string:end_time>"]

    def check_approval(self, approvals):
        for approval in approvals:
            if approval["status"] == RELEASE.FAIL:
                return False, approval["options"]
        return True, ""

    def get(self, begin_time, end_time):
        result = {}
        opts, svc_names = set(), set()
        for release in Release.between(
                datetime.strptime(begin_time, "%Y-%m-%d"),
                datetime.strptime(end_time, "%Y-%m-%d")):
            proj = release["project"]
            svc_name = release["service"]["name"]
            svc_type = release["service"]["type"]
            is_pass, options = self.check_approval(release["approvals"])
            if is_pass and len(release["approvals"]) < 3:
                continue
            svc_names.add(svc_name)

            if not result.__contains__(proj):
                result[proj] = {RELEASE.FAIL: {}, RELEASE.PASS: {}, RELEASE.OPTIONS: {}}
            if not result[proj][RELEASE.PASS].__contains__(svc_name):
                result[proj][RELEASE.PASS][svc_name] = 0
                result[proj][RELEASE.FAIL][svc_name] = 0
            if is_pass:
                result[proj][RELEASE.PASS][svc_name] += 1
            else:
                result[proj][RELEASE.FAIL][svc_name] += 1
                for opt in options.split(","):
                    if not opt: continue
                    opts.add(opt)
                    if not result[proj][RELEASE.OPTIONS].__contains__(opt):
                        result[proj][RELEASE.OPTIONS][opt] = 0
                    result[proj][RELEASE.OPTIONS][opt] += 1

        for proj in result.values():
            for opt in opts:
                if not proj[RELEASE.OPTIONS].__contains__(opt):
                    proj[RELEASE.OPTIONS][opt] = 0
            for svc_name in svc_names:
                if not proj[RELEASE.PASS].__contains__(svc_name):
                    proj[RELEASE.PASS][svc_name] = 0
                    proj[RELEASE.FAIL][svc_name] = 0

        return self.succ(result)


if __name__ == "__main__":
    pass
