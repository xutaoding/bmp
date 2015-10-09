from bmp.views.base import BaseView
from flask import url_for,render_template
from bmp.forms import LoginForm
from flask import request


class LoginView(BaseView):
    def auth(self):
        return True

    def dispatch(self):
        form=LoginForm(request.form)
        if form.validate():
            return self.redirect("main")
        return render_template("login.html",form=form)