# coding=utf-8

import requests
import xml.dom.minidom as dom
from xml.dom.minidom import Element
from bmp import log, app


def send(mobile, content):
    try:
        root = dom.parseString(requests.post(
            app.config["SMS_GATEWAY"],
            {
                "method": "Submit",
                "account": app.config["SMS_USER"],
                "password": app.config["SMS_PASSWORD"],
                "mobile": mobile,
                "content": content
            }
        ).text.encode("utf-8"))

        code, msg, smsid = [
            node.childNodes[0].data
            for node in root.getElementsByTagName("SubmitResult")[0].childNodes
            if isinstance(node, Element)]

        if code != "2":
            raise Exception("短信发送失败 %s %s  手机号%s 内容%s" % (code, msg, mobile, content))
    except Exception, e:
        log.exception(e)
        raise e


if __name__ == "__main__":
    send("15618226618", "神盾局OPS系统：前方英雄【域名】即将在【2016-01-05】过期，请及时充能！！")
