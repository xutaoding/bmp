from flask import Flask
from flask import session
from flask.ext.sqlalchemy import SQLAlchemy,Pagination
from werkzeug.routing import BaseConverter
from utils import path
import logging
import sys
import re
from datetime import datetime
from bmp.utils import time


class _RegexConverter(BaseConverter):
    def __init__(self, map, *args):
        BaseConverter.__init__(self,map)
        self.regex = args[0]


class Myapp(Flask):
    __app=None
    @staticmethod
    def get_instance(name):
        if Myapp.__app==None:
            Myapp.__app=Myapp(name)
        return Myapp.__app

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
        #return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}

    @staticmethod
    def __to_page(self,_to_dict):
        _dict={}

        _dict["items"]=[_to_dict(item) for item in getattr(self,"items",None)]

        for name in ["page","pages","per_page","total"]:
            attr=getattr(self,name,None)
            _dict[name]=attr

        return _dict

    def __init__(self,name):
        Flask.__init__(self,name)

        self.config.from_object("bmp.config.Config")

        self.db=SQLAlchemy(self)
        self.db.Model.to_dict=Myapp.__to_dict
        Pagination.to_page=Myapp.__to_page



        log_fmt=logging.Formatter("%(asctime)s %(message)s")
        fileHandler=logging.FileHandler("%s/bmp.log"%self.root_path)
        fileHandler.setLevel(logging.ERROR)
        fileHandler.setFormatter(log_fmt)
        streamHandler=logging.StreamHandler()
        streamHandler.setLevel(logging.ERROR)
        streamHandler.setFormatter(log_fmt)
        self.logger.addHandler(streamHandler)
        self.logger.addHandler(fileHandler)

        self.url_map.converters["regex"] = _RegexConverter

    def __add_api_rule(self,module):
        self.__add_rule("bmp.apis.%s"%module,"Api",
                        methods=["GET","POST","PUT","DELETE"],
                        root="/apis/%s"%self.config["API_VERSION"])

    def add_view_rule(self,module):
        self.__add_rule("bmp.views.%s"%module,"View",methods=["GET"])

    def __add_rule(self,module,suffix,methods,root=""):
        #bmp.views.index
        '''
        from bmp.views.index import IndexView
        app.add_url_rule("/",view_func=IndexView.as_view("index"))
        '''
        cls_name=module.split(".")[-1]

        exec("import %s"%(module))

        cls_name=cls_name.capitalize()+suffix
        if not hasattr(sys.modules[module],cls_name):
            return
        cls=getattr(sys.modules[module],cls_name)
        if not hasattr(cls,"route"):
            return

        if not isinstance(cls.route,list):
            route=root+cls.route
            self.add_url_rule(route,view_func=cls.as_view(route),methods=methods)
        else:
            for route in cls.route:
                route=root+route
                self.add_url_rule(route,view_func=cls.as_view(route),methods=methods)

    def add_api_rule(self):
        apis="%s/apis"%self.root_path.replace("\\","/")
        regx=re.compile(r"^%s/(.+)\.py$"%apis)
        for name in path.files(apis,".+\.py$"):
            mod=regx.findall(name.replace("\\","/"))[0].replace("/",".")
            self.__add_api_rule(mod)

    def run(self, host=None, port=None, debug=None, **options):
        super(Myapp,self).run(host,port,debug,**options)
