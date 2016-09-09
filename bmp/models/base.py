from datetime import datetime

import pandas as pd

from bmp import db
from bmp.database import Database


class BaseModel(object):
    def __init__(self, submit=None):
        if not submit:
            return

        def set_attr(k, v):
            if ("time" in k or "date" in k) and not isinstance(v, datetime):
                try:
                    dt = pd.to_datetime(v)
                    if dt is not pd.NaT:
                        setattr(self, k, dt.to_datetime())
                    else:
                        setattr(self, k, datetime.now())
                except:
                    setattr(self, k, v)
            else:
                setattr(self, k, v)

        for k, v in submit.items():
            if hasattr(self, k):
                set_attr(k, v)

    @classmethod
    def get(cls, _id, _filters=None):
        if _filters is None:
            _filters = []

        _filters.append(cls.id == _id)
        result = cls.select(_filters=_filters)
        return result[0] if result else result

    @classmethod
    def select(cls, page=None, pre_page=None, _filters=None, _orders=None, _joins=None, format=None):
        query = cls.query
        if _filters is None:
            _filters = []
        if _orders is None:
            _orders = []
        if _joins is None:
            _joins = []

        if not isinstance(_joins, list):
            _joins = [_joins]

        if not isinstance(_orders, list):
            _orders = [_orders]

        if not isinstance(_filters, list):
            _filters = [_filters]

        for _join in _joins:
            query = query.join(_join)

        for _filter in _filters:
            query = query.filter(_filter)

        if hasattr(cls, "is_del"):
            query = query.filter(cls.is_del != True)

        for _order in _orders:
            query = query.order_by(_order)

        _format = format if format else cls._to_dict

        if page:
            return query.paginate(page, pre_page, False).to_page(_format)
        else:
            return [_format(result) for result in query.all()]

    @classmethod
    def delete(cls, _ids, auto_commit=True):
        results = []
        if not isinstance(_ids, list):
            _ids = [_ids]

        for _id in _ids:
            result = cls.query.filter(cls.id == _id).one()
            results.append(result)
            if hasattr(result, "is_del"):
                result.is_del = True
            else:
                db.session.delete(result)
        if auto_commit:
            db.session.commit()
        else:
            db.session.flush()

        return results[0] if len(results) == 1 else results

    @classmethod
    def edit(cls, _dicts, auto_commit=True):
        if not isinstance(_dicts, list):
            _dicts = [_dicts]
        results = [Database.to_cls(cls, _dict) for _dict in _dicts]
        if auto_commit:
            db.session.commit()
        else:
            db.session.flush()
        return results[0] if len(results) == 1 else results

    @classmethod
    def add(cls, _dicts, auto_commit=True):
        results = []
        if not isinstance(_dicts, list):
            _dicts = [_dicts]

        for _dict in _dicts:
            result = cls(_dict)
            db.session.add(result)
            results.append(result)
        if auto_commit:
            db.session.commit()
        else:
            db.session.flush()
        return results[0] if len(results) == 1 else results

    @staticmethod
    def _to_dict(self):
        return self.to_dict()


if __name__ == "__main__":
    pass
