#coding: utf-8
from flask.views import MethodView
from flask import redirect
from flask import url_for
from flask import jsonify
from flask import session
from bmp.const import USER_SESSION
from flask import request
import json
import traceback
from bmp import log
from bmp import app

class BaseApi(MethodView):

    def auth(self):
        session.permanent = True
        if session.__contains__(USER_SESSION):
            return True
        return False

    def dispatch_request(self, *args, **kwargs):
        try:
            if self.auth():
                return super(BaseApi,self).dispatch_request(*args,**kwargs)
            else:
                return self.fail("未登录")
        except Exception,e:
            traceback.print_exc()
            log.exception(e)
            return self.fail("接口异常")


    def fail(self, error=""):
        return jsonify({
            "success":False,
            "error":error,
            "content":{}
        })

    def request(self):
        try:
            req=[j for j in request.form][0]
            return json.loads(req)
        except Exception,e:
            app.logger.exception(e)
        req=[request.form[j] for j in request.form][0]
        return json.loads(req)

    def succ(self, data={}):
        return jsonify({
            "success":True,
            "error":"",
            "content":data
        })

    def redirect(self,url):
        return redirect(url_for(url))

    def dispatch(self):
        pass