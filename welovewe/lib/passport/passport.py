import logging

from tornado.gen import coroutine, Return

#from livemp.utils.sign import convert_and_sign
from lib.base import BaseApi
from lib.passport import PASSPORT_HOST, TUDOU_UIS_HOST, TUDOU_AUTH_HOST
from lib.passport import CONNECT_TIMEOUT, REQUEST_TIMEOUT

LOG = logging.getLogger()

class PassportApi(BaseApi):
    HOST = PASSPORT_HOST
    CONNECT_TIMEOUT = CONNECT_TIMEOUT
    REQUEST_TIMEOUT = REQUEST_TIMEOUT

    @classmethod
    def verify_cookie(cls, req):
        path = "/passport/verify_cookie"
        msg, sign = convert_and_sign(req)
        params = {
            'msg': msg,
            'sign': sign,
        }
        return cls.post(path, params)


class PassportUserApi(BaseApi):
    HOST = TUDOU_AUTH_HOST
    CONNECT_TIMEOUT = CONNECT_TIMEOUT
    REQUEST_TIMEOUT = REQUEST_TIMEOUT

    @classmethod
    def login(cls, loginname, passwd, remember=0, code_id='', vcode='',
              source='', ip='', app=''):
        path = "/passport/ytLogin.do"
        params = {
            "loginname": loginname.encode('utf-8'),
            "passwd": passwd.encode('utf-8'),
            "remember": remember,
            "from": source,
            "ip": ip,
            "app": app,
            "codeId": code_id,
            "vcode": vcode.encode('utf-8'),
        }
        return cls.post_with_response(path, params)

    @classmethod
    def is_password_set(cls, uid, ip='', app='webapp'):
        path = "/passport/isPasswordSet.do"
        params = {
            "uid": uid,
            "ip": ip,
            "app": app,
        }
        return cls.get(path, params)

class UisUserApi(BaseApi):
    HOST = TUDOU_UIS_HOST
    CONNECT_TIMEOUT = CONNECT_TIMEOUT
    REQUEST_TIMEOUT = REQUEST_TIMEOUT

    @classmethod
    def find_user(cls, uid, rt=0, app='app'):
        path = "/uis/userInfo.action"
        params = {
            "uid": uid,
            'app': app,
            'rt': rt,
        }
        return cls.get(path, params)

