# coding=utf-8

import re
from datetime import datetime

import pymongo
from bmp.apis.base import BaseApi
from bson import Int64
from bson import ObjectId
from bson.binary import Binary
from bson.regex import Regex


def get_fields_iter(obj, path=None):
    path = path if path else []

    def fmt_data(obj):
        if isinstance(obj, (str, unicode)):
            return "String"
        elif isinstance(obj, datetime):
            return "Date"
        elif isinstance(obj, bool):
            return "Boolean"
        elif isinstance(obj, Int64):
            return "Int64"
        elif isinstance(obj, float):
            return "float"
        elif isinstance(obj, int):
            return "Int32"
        elif isinstance(obj, Regex):
            return "Regex"
        elif isinstance(obj, Binary):
            return "Binary"
        elif isinstance(obj, ObjectId):
            return "ObjectId"

        elif obj == None:
            return obj

        return re.compile("<type \'(.+)\'>").findall(str(type(obj)))[0]

    if isinstance(obj, dict):
        for name, value in obj.items():
            for p in get_fields_iter(value, path + [name]):
                yield p

    elif isinstance(obj, list):
        if not obj:
            yield ".".join(path), fmt_data(obj)
        else:
            for p in get_fields_iter(obj[0], path):
                yield p
    else:
        yield ".".join(path), fmt_data(obj)


def get_collect_info(host, database, table, limit):
    with pymongo.MongoClient(host="mongodb://%s/" % host) as client:

        db = client.get_database(database)
        collect = db.get_collection(table)
        fields = {}

        limit = 1 if limit <= 0 else limit
        for doc in list(collect.find(limit=1, skip=limit)):
            for name, typ in get_fields_iter(doc):
                if not fields.__contains__(name):
                    fields[name] = []
                if typ and typ not in fields[name]:
                    fields[name].append(typ)

        return {
            "indexs": collect.index_information(),
            "fields": fields
        }


class Doc_mongoApi(BaseApi):
    route = ["/doc/mongo/<string:host>/<string:database>/<string:table>/<int:limit>"]

    def get(self, host, database, table, limit):
        return self.succ(get_collect_info(host, database, table, limit))


if __name__ == "__main__":
    print get_collect_info("192.168.100.20:27017", "py_crawl", "guba", 100)
