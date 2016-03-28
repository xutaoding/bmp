from bmp import db
from sqlalchemy import or_
from bmp.database import Database
import re
from datetime import datetime
import pandas as pd


class BaseModel(object):
    def __init__(self, submit=None):
        if not submit:
            return

        def set_attr(k, v):
            if "time" in k and not isinstance(v, datetime):
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
            set_attr(k, v)

    @classmethod
    def get(cls, _id, _filters=None):
        if _filters is None:
            _filters=[]

        _filters.append(cls.id == _id)
        result = cls.select(_filters=_filters)
        return result[0] if result else result

    @classmethod
    def select(cls, page=None, pre_page=None, _filters=None, _orders=None):
        query = cls.query
        if _filters is None:
            _filters=[]
        if _orders is None:
            _orders=[]

        if not isinstance(_orders, list):
            _orders = [_orders]

        if not isinstance(_filters, list):
            _filters = [_filters]

        for _filter in _filters:
            query = query.filter(_filter)

        if hasattr(cls, "is_del"):
            query = query.filter(cls.is_del != True)

        for _order in _orders:
            query = query.order_by(_order)

        if page:
            return query.paginate(page, pre_page, False).to_page(cls._to_dict)
        else:
            return [cls._to_dict(result) for result in query.all()]

    @classmethod
    def delete(cls, _ids):
        if not isinstance(_ids, list):
            _ids = [_ids]

        for _id in _ids:
            result = cls.query.filter(cls.id == _id).one()
            if hasattr(result,"is_del"):
                result.is_del=True
            else:
                db.session.delete(result)
        db.session.commit()
        return True

    @classmethod
    def edit(cls, _dicts):
        if not isinstance(_dicts, list):
            _dicts = [_dicts]
        results = [Database.to_cls(cls, _dict) for _dict in _dicts]
        db.session.commit()
        return results

    @classmethod
    def add(cls, _dicts):
        results=[]
        if not isinstance(_dicts,list):
            _dicts=[_dicts]

        for _dict in _dicts:
            result=cls(_dict)
            db.session.add(result)
            results.append(result)
        db.session.commit()

        return results[0] if len(results)==1 else results

    @staticmethod
    def _to_dict(self):
        return self.to_dict()


if __name__ == "__main__":
    pass