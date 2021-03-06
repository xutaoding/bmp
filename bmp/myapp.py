# coding=utf-8
import logging
import os
import re
import sys

from apscheduler.executors.pool import ProcessPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_sqlalchemy import before_models_committed
from werkzeug.contrib.cache import SimpleCache
from werkzeug.routing import BaseConverter

from database import Database
from utils import path


class _RegexConverter(BaseConverter):
    def __init__(self, map, *args):
        BaseConverter.__init__(self, map)
        self.regex = args[0]


class Myapp(Flask):
    __app = None
    __is_add_apis = False

    @staticmethod
    def get_instance(name):
        if Myapp.__app == None or not Myapp.__app.config["SINGLETON"]:
            Myapp.__app = Myapp(name)
        return Myapp.__app

    def __init_log(self):
        log_fmt = logging.Formatter("%(asctime)s %(message)s")

        streamHandler = logging.StreamHandler()
        streamHandler.setLevel(logging.NOTSET)
        streamHandler.setFormatter(log_fmt)

        self.logger.addHandler(streamHandler)

    def __init_config(self):
        r = re.compile("(.+)\.cfg")
        cfg = []
        for name in os.listdir("%s%s.." % (self.root_path, os.sep)):
            cfg = r.findall(name)
            if cfg: break
        cfg = cfg[0]
        self.config.from_object("bmp.config.%s" % cfg.capitalize())

    def __init_sched(self):
        self.sched = BackgroundScheduler(
            jobstores={
                "default": SQLAlchemyJobStore(url=self.config["SQLALCHEMY_DATABASE_URI"])
            },
            executors={
                "default": ProcessPoolExecutor(10)
            },
            job_defaults={"coalesce": False, "max_instances": 1}
        )

        if not self.sched.running:
            self.sched.start()

    def __init_signals(self):
        from bmp.signals.db_log import log
        before_models_committed.connect(log, self)

    def __init__(self, name):
        Flask.__init__(self, name)
        self.__add_apis = False
        self.__add_views = False
        self.__name = name

        self.url_map.converters["regex"] = _RegexConverter
        self.__init_config()
        self.__init_log()
        self.__init_sched()
        self.db = Database(self)
        self.cache = SimpleCache()
        self.__init_signals()

    def __add_api_rule(self, module):
        self.__add_rule("bmp.apis.%s" % module, "Api",
                        methods=["GET", "POST", "PUT", "DELETE", "SAVE"],
                        root="/apis/%s" % self.config["API_VERSION"])

    def add_view_rule(self, module):
        if self.__add_views: return
        self.__add_rule("bmp.views.%s" % module, "View", methods=["GET"])
        self.__add_views = True

    def __add_rule(self, module, suffix, methods, root=""):
        # bmp.views.index
        '''
        from bmp.views.index import IndexView
        app.add_url_rule("/",view_func=IndexView.as_view("index"))
        '''
        cls_name = module.split(".")[-1]
        print "import %s" % module
        exec ("import %s" % (module))

        cls_name = cls_name.capitalize() + suffix
        if not hasattr(sys.modules[module], cls_name):
            return
        cls = getattr(sys.modules[module], cls_name)
        if not hasattr(cls, "route"):
            return

        if not isinstance(cls.route, list):
            route = root + cls.route
            self.add_url_rule(route, view_func=cls.as_view(route), methods=methods)
        else:
            for route in cls.route:
                route = root + route
                self.add_url_rule(route, view_func=cls.as_view(route), methods=methods)

    def add_api_rule(self):
        if self.__add_apis: return
        apis = "%s/apis" % self.root_path.replace("\\", "/")
        regx = re.compile(r"^%s/(.+)\.py$" % apis)
        for name in path.files(apis, ".+\.py$"):
            mod = regx.findall(name.replace("\\", "/"))[0].replace("/", ".")

            self.__add_api_rule(mod)
        self.__add_apis = True

    def run(self, host=None, port=None, debug=None, **options):
        super(Myapp, self).run(host, port, debug, **options)
