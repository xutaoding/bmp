#coding: utf-8
from flask.views import MethodView
from flask import redirect
from flask import url_for
from flask import session
from flask import render_template

class BaseView(MethodView):

    def auth(self):
        return True

    def dispatch_request(self, *args, **kwargs):
        if self.auth():
            return super(BaseView,self).dispatch_request(*args,**kwargs)
        else:
            return "err"

    def redirect(self,url):
        return redirect(url_for(url))

    def dispatch(self):
        pass