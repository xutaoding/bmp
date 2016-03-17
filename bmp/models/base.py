from bmp import db
from sqlalchemy import or_
from bmp.database import Database
import re
from datetime import datetime
import pandas as pd

class BaseModel(object):

    def __init__(self,submit=None,callbacks={}):
        if not submit:
            return


        def set_attr(k,v):
            if "time" in k and not isinstance(v,datetime):
                dt=pd.to_datetime(v)
                if dt is not pd.NaT:
                    setattr(self,k,dt.to_datetime())
                else:
                    setattr(self,k,datetime.now())
            else:
                setattr(self,k,v)

        for k, v in submit.items():
            for cb in callbacks.keys():
                if k in cb:
                    set_attr(k,callbacks[cb]())

            set_attr( k, v)


    @classmethod
    def get(cls,_id,_filters=[]):
        _filters.append(cls.id==_id)
        result=cls.select(_filters=_filters)
        return result[0] if result else result


    @classmethod
    def select(cls,page=None,pre_page=None,_filters=[],_orders=[]):
        query=cls.query

        if not isinstance(_orders,list):
            _orders=[_orders]

        if not isinstance(_filters,list):
            _filters=[_filters]

        for _filter in _filters:
            query=query.filter(_filter)

        for _order in _orders:
            query=query.order_by(_order)

        if page:
            return query.paginate(page, pre_page, False).to_page(cls._to_dict)
        else:
            return [cls._to_dict(result) for result in query.all()]

    @classmethod
    @db.transaction
    def delete(cls,_ids):
        if not isinstance(_ids,list):
            _ids=[_ids]

        for _id in _ids:
            result = cls.query.filter(cls.id == _id).one()
            db.session.delete(result)
        db.session.flush()
        return True

    @classmethod
    def edit(cls,submit):
        idc_host = Database.to_cls(cls, submit)
        db.session.commit()
        return idc_host

    @classmethod
    @db.transaction
    def edit(cls,_dicts):
        if not isinstance(_dicts, list):
            _dicts = [_dicts]
        results = [Database.to_cls(cls, _dict) for _dict in _dicts]
        db.session.flush()
        return results



    @classmethod
    def add(cls,_dict):
        result=cls(_dict)
        db.session.add(result)
        db.session.commit()
        return result


    @staticmethod
    def _to_dict(self):
        return self.to_dict()

if __name__=="__main__":
    pass