# coding=utf-8
from datetime import datetime
from bmp.apis.base import BaseApi
from bmp.models.release import Release, ReleaseApproval
from bmp.tasks.release import mail_to
from datetime import datetime
import pandas as pd
import json
from bmp.utils import time


class Release_typeApi(BaseApi):
    route = ["/stats/release/type/<string:begin_time>/<string:end_time>"]

    def get(self, begin_time,end_time):
        result={}
        release=pd.read_json(
            json.dumps(Release.between(begin_time,end_time)))\
            .set_index("release_time")

        for name,g in release.groupby("release_type"):
            result[name]=[]
            ids=g.resample("m",how="count").id
            for ix in ids.index:
                date=time.format(ix.to_datetime(),"%Y-%m-%d")
                result[name].append({date:ids[ix]})

        return self.succ(result)



if __name__ == "__main__":
    result={}
    release=pd.read_json(json.dumps(Release.between("2015-01-01","2015-12-12"))).set_index("release_time")
    for name,g in release.groupby("release_type"):
        result[name]=[]
        ids=g.resample("m",how="count").id
        for ix in ids.index:
            date=time.format(ix.to_datetime(),"%Y-%m-%d")
            result[name].append({date:ids[ix]})

    print(result)


