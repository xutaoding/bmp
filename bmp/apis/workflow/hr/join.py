# coding=utf-8
import pymongo

from bmp import app
from bmp.apis.base import BaseApi
from bmp.utils.mongo import MongoDB
from datetime import datetime

class JoinApi(BaseApi):
    route = ["/hr/join"]
    collect_name = "join"

    def get(self):
        db = MongoDB(app.config["MONGO_HR_HOST"], app.config["MONGO_HR_DATABASE"])
        joins = list(db.get_collect(self.collect_name).find().sort("crt",pymongo.DESCENDING))
        results = []
        for join in joins:
            join.pop("_id")
            join["crt"] = join["crt"].strftime("%Y-%m-%d %H:%M:%S")
            results.append(join)

        return self.succ(results)
