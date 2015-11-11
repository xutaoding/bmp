# coding=utf-8
import os
import re


def files(sub="", filter=".*"):
    lst = []
    regx = re.compile(filter)
    for cur, subs, names in os.walk(sub):
        for name in names:
            if regx.match(name):
                lst.append("%s\\%s" % (cur, name))
    return lst
