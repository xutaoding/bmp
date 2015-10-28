#coding=utf-8
from flask.ext.sqlalchemy import SQLAlchemy,Pagination
from datetime import datetime
import bmp.utils.time as time


class Database(SQLAlchemy):
    def __init__(self,app):
        SQLAlchemy.__init__(self,app)
        self.Model.to_dict=Database.__to_dict

    @staticmethod
    def __to_dict(self):
        _dict={}
        for c in self.__table__.columns:
            attr=getattr(self, c.name, None)
            if isinstance(attr,datetime):
                _dict[c.name]=time.format(attr,"%Y-%m-%d %H:%M")
            else:
                _dict[c.name]=attr
        return _dict

    @staticmethod
    def to_cls(cls,_dict):
        self=None
        if _dict.__contains__("id"):
            self=cls.query.filter(cls.id==_dict["id"]).one()
            cls.__init__(self,_dict)
        else:
            self=cls(_dict)

        return self

    def transaction(self,fun):
        def __fun(*args,**kwargs):
            self.session.begin(subtransactions=True)
            try:
                result=fun(*args,**kwargs)
                self.session.commit()
                return result
            except:
                self.session.rollback()
                raise
        return __fun



def __to_page(self,_to_dict):
    _dict={}

    _dict["items"]=[_to_dict(item) for item in getattr(self,"items",None)]

    for name in ["page","pages","per_page","total"]:
        attr=getattr(self,name,None)
        _dict[name]=attr

    return _dict


Pagination.to_page=__to_page