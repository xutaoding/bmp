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


if __name__=="__main__":
    application.run(host="0.0.0.0",port=5000,debug=True)
