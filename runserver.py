#!/usr/bin/python
# coding: utf-8

'''
git clone git@gitlab.chinascope.net:web/ops.git
ln -s ops/static/static/ bmp/static/
ln -s ops/static/templates/ bmp/templates/
'''
import sys

sys.path.append("/var/www/scope/bmp")



from bmp import app as application

application.add_view_rule("index")    # 放这儿！！！ 数据库中会调用
application.add_api_rule()    # 放这儿！！！

if __name__=="__main__":
    application.run(host="192.168.0.57",port=5000,debug=True)
