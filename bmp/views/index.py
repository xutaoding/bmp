from bmp.views.base import BaseView

class IndexView(BaseView):
    def dispatch(self):
        return self.redirect("main")
