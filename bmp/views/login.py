#coding: utf-8
from bmp.views.base import BaseView
from bmp.models import user_ldap

class LoginView(BaseView):
    def get(self,user,pwd):pass

