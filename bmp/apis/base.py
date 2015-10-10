#coding: utf-8
from flask.views import MethodView
from flask import redirect
from flask import url_for
from flask import jsonify
from flask import session
from bmp.const import USER_SESSION

class BaseView(MethodView):

    def auth(self):
        if session.__contains__(USER_SESSION):
            return True
        return False

    def dispatch_request(self, *args, **kwargs):
        if self.auth():
            return super(BaseView,self).dispatch_request(*args,**kwargs)
        else:
            return self.failure("未登录")

    def failure(self,error):
        return jsonify({
            "success":False,
            "error":error
        })

    def success(self,data):
        return jsonify(data)

    def redirect(self,url):
        return redirect(url_for(url))

    def dispatch(self):
        pass