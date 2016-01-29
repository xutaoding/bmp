# coding=utf-8
import urllib
import urllib2
import json


def test(method, url, data=None, exe=False):
    if not exe:
        return
    req = None
    if data == None:
        req = urllib2.Request(url)
    if method.upper() not in ["POST", "PUT", "DELETE", "GET"]:
        req = urllib2.Request(url, urllib.urlencode({"method": method, "submit": json.dumps(data)}))
        method = "POST"
    else:
        req = urllib2.Request(url, urllib.urlencode({"submit": json.dumps(data)}))
    req.get_method = lambda: method
    result = urllib2.urlopen(req).read()
    print(result)
    return result


if __name__ == "__main__":
    test("post","127.0.0.1:8080",data={"abc":"中文"},exe=True)
