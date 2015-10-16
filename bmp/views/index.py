#coding: utf-8
from flask import render_template
from flask.views import View
from flask import request

class IndexView(View):
    route=["/","/index","/<regex('.+\.html'):html>"]
    def dispatch_request(self,html=""):
        print(request.headers)
        if html=="":
            return render_template("index.html")
        return render_template(html)