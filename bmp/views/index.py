#coding: utf-8
from flask import render_template
from flask.views import View

class IndexView(View):
    def dispatch_request(self):
        return render_template("release/home.html")