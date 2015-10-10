#coding: utf-8

'''
git clone git@gitlab.chinascope.net:web/ops.git
ln -s ops/static/static/ bmp/static/
ln -s ops/static/templates/ bmp/templates/
'''

from bmp import app
app.run(debug=True)