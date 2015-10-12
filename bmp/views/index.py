#coding: utf-8
from flask import render_template
from flask.views import View


class IndexView(View):
    route=["/","/index","/<regex('.+\.html'):html>"]
    def dispatch_request(self,html=""):
        if html=="":
            return render_template("release/home.html")
        return render_template("release/%s"%html)