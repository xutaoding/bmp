#!/usr/bin/python
#coding: utf-8

'''
git clone git@gitlab.chinascope.net:web/ops.git
ln -s ops/static/static/ bmp/static/
ln -s ops/static/templates/ bmp/templates/
'''
import sys

sys.path.append("/var/www/scope/bmp")



from bmp import app as application

application.add_view_rule("index")
application.add_api_rule()

if __name__ == "__main__":
    application.run(host=application.config["HOST"],port=application.config["PORT"],debug=True)
