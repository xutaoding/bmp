# coding=utf-8

import pymongo

from bmp.apis.base import BaseApi


def get_fields_iter(obj, path=None):
    path = path if path else []

    if isinstance(obj, dict):
        for name, value in obj.items():
            for p in get_fields_iter(value, path + [name]):
                yield p

    elif isinstance(obj, list):
        if not obj:
            yield ".".join(path)
        else:
            for p in get_fields_iter(obj[0], path):
                yield p
    else:
        yield ".".join(path)


def get_collect_info(host, database, table):
    with pymongo.MongoClient(host="mongodb://%s/" % host) as client:
        db = client.get_database(database)
        collect = db.get_collection(table)
        fields  = collect.find_one()
        return {
            "indexs": collect.index_information().keys(),
            "fields": list(get_fields_iter(fields))
        }


class Doc_mongoApi(BaseApi):
    route = ["/doc/mongo/<string:host>/<string:database>/<string:table>"]

    def get(self, host, database, table):
        return self.succ(get_collect_info(host, database, table))

