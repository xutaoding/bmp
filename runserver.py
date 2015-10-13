#coding: utf-8

'''
git clone git@gitlab.chinascope.net:web/ops.git
ln -s ops/static/static/ bmp/static/
ln -s ops/static/templates/ bmp/templates/
'''

from bmp import app
app.run(host="192.168.0.143",port=5000,debug=True)