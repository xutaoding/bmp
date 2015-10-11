#coding: utf-8
from flask import render_template
from flask.views import View
from flask import flash
from flask import redirect

class IndexView(View):
    route=["/","/index","/<regex('.+\.html'):html>"]
    def dispatch_request(self,html=""):
        flash(html)
        return html