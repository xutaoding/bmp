from flask.views import View
from flask import redirect
from flask import url_for
from flask import session
from flask import render_template

class BaseView(View):

    def auth(self):
        return False

    def dispatch_request(self):
        if self.auth():
            return self.dispatch()
        else:
            return self.redirect("login")
        #return self.dispatch(request)

    def render(self,name):pass
        #return render_template("%s.html"%(name.replace(".","\\")))


    def redirect(self,url):
        return redirect(url_for(url))

    def dispatch(self):
        pass