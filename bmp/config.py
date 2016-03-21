# coding=utf-8
from datetime import timedelta


class Config(object):
    LDAP_HOST = "ldap://ldap.chinascopefinancial.com"
    LDAP_PORT = "389"
    LDAP_ACCOUNT = "cn=emp_user,dc=employees,dc=acl,dc=people,dc=chinascopefinancial,dc=com"
    LDAP_PASSWORD = "\X'94ORKWV#4gCyHFzPV"
    LDAP_BASE_DN = "dc=chinascopefinancial,dc=com"

    SQLALCHEMY_DATABASE_URI = "mysql://ops:Ops@192.168.250.10:3306/bmp"
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    SECRET_KEY = "scope"  # os.urandom(1024)
    SESSION_TYPE = "filesystem"
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)

    API_VERSION = "v1.0"

    MAIL_SERVER = "mail.chinascopefinancial.com"
    MAIL_USERNAME = "ops@chinascopefinancial.com"
    MAIL_PASSWORD = "GmgW3UXF"
    MAIL_DEFAULT_SENDER = "ops@chinascopefinancial.com"
    MAIL_ALERT = "it@chinascopefinancial.com"

    LOG_PATH = "bmp.log"
    LOG_MAX = ""

    UPLOAD_FOLDER = "/static/upload"
    SINGLETON = True
    HOST = ""
    PORT = 5000
    MAX_CONTENT_LENGTH = 1 * 1023 * 1024 * 1024
    DOMAIN = "http://ops.chinascope.net/"

    SSH_HOST = "192.168.250.200"
    SSH_USER = "depops"
    SSH_PASSWORD = "Vulooz5S"


class Test(Config):
    SQLALCHEMY_DATABASE_URI = "mysql://ops:Ops@192.168.250.10:3306/bmp_test"
    HOST = "localhost"
    MAIL_ALERT = "chenglong.yan@chinascopefinancial.com"
    SSH_HOST = "192.168.250.253"
    SSH_USER = "depops"
    SSH_PASSWORD = "Passwd@!"
