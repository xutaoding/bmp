# coding=utf-8
from datetime import datetime
import platform

from flask.ext.sqlalchemy import SQLAlchemy

import bmp.utils.timeutil as time
from bmp.utils.exception import ExceptionEx

from sqlalchemy.schema import MetaData


class Database(SQLAlchemy):
    def __init__(self, app):
        SQLAlchemy.__init__(self, app)
        self.app = app
        self.Model.to_dict = Database.__to_dict
        self.Query.paginate = Database.__paginate
        self.Query.to_page = Database.__to_page
        self.Query.to_json = Database.__to_json

    @staticmethod
    def __to_page(self, _to_dict):
        _dict = {}
        _dict["items"] = [_to_dict(item) for item in getattr(self, "items", None)]
        for name in ["page", "pages", "per_page", "total"]:
            attr = getattr(self, name, None)
            _dict[name] = attr
        return _dict

    @staticmethod
    def __paginate(self, page=None, per_page=None, error_out=True):
        all = self.all()
        beg = (page - 1) * per_page
        end = beg + per_page

        self.items = all[beg:end]
        self.total = len(all)
        self.page = page
        self.per_page = per_page
        self.pages = self.total / per_page
        if self.total % per_page:
            self.pages += 1

        return self

    @staticmethod
    def __to_json(self, cols=[]):
        _dict = {}
        for c in self.__table__.columns:
            attr = getattr(self, c.name, None)
            if isinstance(attr, datetime):
                _dict[c.name] = time.format(attr, "%Y-%m-%d %H:%M")
            else:
                _dict[c.name] = attr

        for c in cols:
            _dict[c] = getattr(self, c, None)
        return _dict

    @staticmethod
    def __to_dict(self, cols=[]):
        _dict = {}
        for c in self.__table__.columns:
            attr = getattr(self, c.name, None)
            if isinstance(attr, datetime):
                _dict[c.name] = time.format(attr, "%Y-%m-%d %H:%M")
            else:
                _dict[c.name] = attr

        for c in cols:
            _dict[c] = getattr(self, c, None)
        return _dict

    @staticmethod
    def to_cls(cls, _dict):
        self = None
        if _dict.__contains__("id"):
            self = cls.query.filter(cls.id == _dict["id"]).one()
            cls.__init__(self, _dict)
        else:
            self = cls(_dict)

        return self

    def log(self, fun):
        def __fun(*args, **kwargs):
            try:
                result = fun(*args, **kwargs)
                self.session.commit()
                return result
            except ExceptionEx, ex:
                raise ex
            except Exception, e:
                raise e
        return __fun

