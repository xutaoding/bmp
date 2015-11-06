#coding=utf-8
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
from database import Database
from werkzeug.contrib.cache import SimpleCache

import os


class _RegexConverter(BaseConverter):
    def __init__(self, map, *args):
        BaseConverter.__init__(self,map)
        self.regex = args[0]


class Myapp(Flask):
    __app=None
    @staticmethod
    def get_instance(name):
        if Myapp.__app==None or not Myapp.__app.config["SINGLETON"]:
            Myapp.__app=Myapp(name)
        return Myapp.__app

    def __init_log(self):
        log_fmt=logging.Formatter("%(asctime)s %(message)s")
        fileHandler=logging.FileHandler("%s/bmp.log"%self.root_path)
        fileHandler.setLevel(logging.ERROR)
        fileHandler.setFormatter(log_fmt)
        streamHandler=logging.StreamHandler()
        streamHandler.setLevel(logging.ERROR)
        streamHandler.setFormatter(log_fmt)
        self.logger.addHandler(streamHandler)
        self.logger.addHandler(fileHandler)

    def __init_config(self):
        r=re.compile("(.+)\.cfg")
        cfg=[]
        for name in os.listdir("%s%s.."%(self.root_path,os.sep)):
            cfg=r.findall(name)
            if cfg:break
        cfg=cfg[0]
        self.config.from_object("bmp.config.%s"%cfg.capitalize())

    def __init__(self,name):
        Flask.__init__(self,name)
        self.__add_apis=False
        self.__add_views=False

        self.url_map.converters["regex"] = _RegexConverter
        self.__init_config()
        self.__init_log()
        self.db=Database(self)
        self.cache=SimpleCache()

    def __add_api_rule(self,module):
        self.__add_rule("bmp.apis.%s"%module,"Api",
                        methods=["GET","POST","PUT","DELETE","SAVE"],
                        root="/apis/%s"%self.config["API_VERSION"])

    def add_view_rule(self,module):
        if self.__add_views:return
        self.__add_rule("bmp.views.%s"%module,"View",methods=["GET"])
        self.__add_views=True

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
        if self.__add_apis:return
        apis="%s/apis"%self.root_path.replace("\\","/")
        regx=re.compile(r"^%s/(.+)\.py$"%apis)
        for name in path.files(apis,".+\.py$"):
            mod=regx.findall(name.replace("\\","/"))[0].replace("/",".")
            self.__add_api_rule(mod)
        self.__add_apis=True

    def run(self, host=None, port=None, debug=None, **options):
        print("root:"+self.root_path)
        super(Myapp,self).run(host,port,debug,**options)
