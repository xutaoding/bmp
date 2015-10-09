from bmp.views.base import BaseView
from flask import url_for,render_template


class MainView(BaseView):
    def auth(self):
        return True

    def dispatch(self):
        return render_template("main.html")