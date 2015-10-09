from bmp.views.base import BaseView


class LogoutView(BaseView):
    def auth(self):
        return True

    def dispatch(self):
        return self.redirect("login")