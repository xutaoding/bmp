from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import sys

class Myapp(Flask):
    def __init__(self,name):
        Flask.__init__(self,name)
        self.config.from_object("bmp.config.Config")
        self.db=SQLAlchemy(self)
        self.db.Model.to_dict=lambda self:{c.name: getattr(self, c.name, None) for c in self.__table__.columns}

    def add_api_rule(self,route,module):
        self.add_rule(route,module,methods=["GET","POST","PUT","DELETE"])

    def add_rule(self,route,module,methods=["GET"]):
        #bmp.views.index
        '''
        from bmp.views.index import IndexView
        app.add_url_rule("/",view_func=IndexView.as_view("index"))
        '''
        view=module.split(".")[-1]
        cls="%sView"%view.capitalize()
        exec("from %s import %s"%(module,cls))
        cls=getattr(sys.modules[module],cls)
        self.add_url_rule(route,view_func=cls.as_view(view))
