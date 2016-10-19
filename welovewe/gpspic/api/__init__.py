#encoding=utf-8
import logging
import datetime
import traceback
import json

from tornado.web import RequestHandler, HTTPError
from tornado.ioloop import IOLoop
from tornado.gen import coroutine, Return
from concurrent.futures import ThreadPoolExecutor

from conf import settings
from utils.password_enc import encrypt, encrypt_base64
from utils.service_cookie import UserCookie

GMT_FORMAT = "%a, %d-%b-%Y %H:%M:%S GMT"
_M3U8_URL = 'http://vr.tudou.com/v2proxy/v2.m3u8?it=%s&st=%s'
_M3U8_META_URL = 'http://%(domain)s/%(version)s/video/m3u8_info?itemid=%(iid)s'
_M3U8_META_URL_WITH_ICODE = 'http://%(domain)s/%(version)s/video/m3u8_info?itemcode=%(icode)s'
_WEB_URL = 'http://www.tudou.com/programs/view/%s'
_WANHUO_URL = 'http://wanhuo.tudou.com/programs/view/%s/?wanhuo=V'

LOG = logging.getLogger()

class RequestClient(object):
    u"""当前请求的客户端"""

    def __init__(self, handler):
        self.handler = handler
        self.request = handler.request
        self.headers = self.request.headers
        self.user_agent = self.headers.get('User-Agent', '')

        ua_items = self._parse_ua(self.user_agent)
        self.product = ua_items[0]
        self.product_ver = ua_items[1]
        self.os = ua_items[2]
        self.os_ver = ua_items[3]
        self.device_model = ua_items[4]

        self._device_type = None
        self._real_ip = None
        self._user_cookie = None

    @property
    def user_ip(self):
        if self._real_ip is None:
            self._real_ip = self.request.headers.get('X-Real-Ip',
                                                     self.request.remote_ip)
        return self._real_ip

    def _parse_ua(self, ua):
        items = ua.split(';', 5)
        if len(items) == 5:
            return tuple(items)
        else:
            return tuple([''] * 5)

    @property
    def user_cookie_raw(self):
        # 优先取参数中传的cookie，解决js传cookie的问题
        cookie_data = self.handler.get_argument('_cookie', '')
        cookie_data = cookie_data.encode('utf-8')
        cookie_data = cookie_data or self.headers.get('Cookie', '')
        return cookie_data

    @property
    def user_cookie(self):
        if self._user_cookie is None:
            self._user_cookie = UserCookie()
            self._user_cookie.client_load(self.user_cookie_raw)
        return self._user_cookie

class InvalidArgumentError(HTTPError):

    def __init__(self, log_message, arg_name):
        super(InvalidArgumentError, self).__init__(
            400, "%s: %s" % (log_message, arg_name))
        self.arg_name = arg_name

class ApiHandler(RequestHandler):

    #################### overrided parent methods ######################
    def __init__(self, application, request, **kwargs):
        super(ApiHandler, self).__init__(application, request, **kwargs)

        self._current_user_id = None
        self._current_user_code = None
        self._current_user_yktk = None
        self.__request_client__ = None

    def write_error(self, status_code, **kwargs):
        '''
        Override to implement custom error message
        '''
        if self.settings.get("serve_traceback") and "exc_info" in kwargs:
            # in debug mode, try to send a traceback
            self.set_header('Content-Type', 'text/plain')
            for line in traceback.format_exception(*kwargs["exc_info"]):
                self.write(line)
            self.finish()
        else:
            msg = kwargs['msg'] if 'msg' in kwargs else 'error'
            self.finish({'code': -1, 'msg': msg, 'reason': self._reason})

    def data_received(self, chunk):
        pass
    #################### self-defined methods ##########################

    _ARG_DEFAULT = RequestHandler._ARG_DEFAULT

    def get_int_argument(self, name, default=_ARG_DEFAULT, strip=True, scope=_ARG_DEFAULT):
        '''
        NOTE: negative will be false when test arg.isdigit(), so return 400
        '''
        arg = self.get_argument(name, default, strip)
        if isinstance(arg, basestring) and not arg.isdigit():
            raise InvalidArgumentError('integer required', name)
        arg = int(arg)
        if scope is not self._ARG_DEFAULT and arg not in scope:
            raise InvalidArgumentError('fixed value required', name)
        return arg

    def get_str_argument(self, name, default=_ARG_DEFAULT, strip=True,
                         max_len=128, scope=_ARG_DEFAULT):
        arg = self.get_argument(name, default, strip)
        if max_len and len(arg) > max_len:
            raise InvalidArgumentError('argument too long', name)
        if scope is not self._ARG_DEFAULT and arg not in scope:
            raise InvalidArgumentError('fixed value required', name)
        return arg

    def log_request_time(self, if_str, req_time):
        LOG.info('[LIB] %s cost %.2fms', if_str, 1000 * req_time)

    def get_ip(self):
        return self.request.remote_ip

    def has_arg(self, name):
        return self.request.arguments.has_key(name)

    @property
    def current_user_id(self):
        if self._current_user_id is None:
            user_id = self.get_secure_cookie("user_id")
            if user_id:
                self._current_user_id = user_id
        return self._current_user_id

    @property
    def current_user_yktk(self):
        if self._current_user_yktk is None:
            user_yktk = self.get_secure_cookie("yktk")
            if user_yktk:
                self._current_user_yktk = user_yktk
        return self._current_user_yktk

    @property
    def current_user_code(self):
        if self._current_user_code is None:
            user_code = self.get_secure_cookie("user_code")
            if user_code:
                self._current_user_code = user_code
        return self._current_user_code

    def get_encrypted_user_id(self):
        dus = settings.dm_uid_secret
        uids = str(self.current_user_id)
        return "".join([dus[:2], uids[:2], dus[2:4], uids[2:4],
                        dus[4:8], uids[4:6], dus[8:16], uids[6:8],
                        dus[16:], uids[8:]])

    def auth_login(self, user_id, expires_days=settings.expires_days,
                   domain=settings.server_domain):

        expires = datetime.datetime.utcnow() + \
                  datetime.timedelta(seconds=settings.expires) if settings.expires >= 0 else None

        user_key = self.create_signed_value("user_id", str(user_id))
        self.set_cookie("user_id", user_key, expires=expires,
                        expires_days=expires_days, domain=domain)
        self._current_user_id = user_id

    def yktk_auth_login(self, user_id, yktk, user_code,
                        expires_days=settings.expires_days,
                        domain=settings.server_domain):

        expires = datetime.datetime.utcnow() + \
                  datetime.timedelta(seconds=settings.expires) if settings.expires >= 0 else None

        user_key = self.create_signed_value("user_id", str(user_id))
        self.set_cookie("user_id", user_key, expires=expires,
                        expires_days=expires_days, domain=domain)
        self._current_user_id = user_id

        #将yktk放到cookie中
        self.user_yktk_key = self.create_signed_value("yktk", str(yktk))
        self.set_cookie("yktk", self.user_yktk_key, expires=expires,
                        expires_days=expires_days, domain=domain)
        self._current_user_yktk = yktk

        #将user code放到cookie中
        ucode = self.create_signed_value("user_code", str(user_code))
        self.set_cookie("user_code", ucode, expires=expires,
                        expires_days=expires_days, domain=domain)
        self._current_user_code = user_code

        encrypted_user_id = self.get_encrypted_user_id()
        self.set_cookie("encrypted_user_id", encrypted_user_id, expires=expires,
                        expires_days=expires_days, domain=domain)

    def set_cookies_with_aes(self, key, value):
        value = encrypt(value)
        expires = datetime.datetime.utcnow() + \
                datetime.timedelta(seconds=settings.expires) if settings.expires >= 0 else None
        self.set_secure_cookie(key, value, expires=expires,
                               expires_days=settings.expires_days,
                               domain=settings.server_domain)

    def set_cookies_from_back(self, cookies):
        for cookie in cookies.split('; Path=/,'):
            if cookie.startswith("u") and not cookie.startswith("u_passport_info"):
                key = None
                key_value = None
                expires = None
                domain = None
                items = cookie.split("; ")
                for item in items:
                    if item.startswith("u"):
                        index = item.find("=")
                        if index >= 0:
                            key = item[:index]
                            key_value = item[index+1:]
                    elif item.startswith("Expires"):
                        index = item.find("=")
                        if index >= 0:
                            expires = datetime.datetime.strptime(item[index+1:], GMT_FORMAT)
                    elif item.startswith("Domain"):
                        index = item.find("=")
                        if index >= 0:
                            domain = item[index+1:]
                self.set_cookie(key, key_value, expires=expires,
                                expires_days=settings.expires_days,
                                domain=settings.server_domain)

    @property
    def convert_cookies(self):
        keys = ["u_login", "u_key", "u_nick", "u_user", "u_id", "u_code",
                "u_pic", "u_l", "u_member"]
        cookies = self.request.headers["Cookie"]
        for key in keys:
            value_secure = self.get_secure_cookie(key)
            value = self.get_cookie(key)
            if value_secure is not None and value is not None:
                cookies = cookies.replace(value, value_secure)
        return cookies

    @property
    def apply_vip_client_type(self):
        sources = 2 if self.is_android_platform else 3
        device = 3 if self.is_pad else 2
        return sources, device

    @property
    def is_debug(self):
        return self.settings.get('debug')

    @property
    def is_doc(self):
        return self.settings.get('doc')

    @property
    def client(self):
        if self.__request_client__ is None:
            self.__request_client__ = RequestClient(self)
        return self.__request_client__

    @property
    def is_android_platform(self):
        if (self.is_debug or self.is_doc) and self.has_arg("_os_"):
            self.client.os = self.get_argument("_os_", "")
        return self.client.os == "Android" or self.get_argument("os", "") == "android"

    @property
    def is_ios_platform(self):
        if (self.is_debug or self.is_doc) and self.has_arg("_os_"):
            self.client.os = self.get_argument("_os_", "").replace("+", " ")
        return self.client.os == "iPhone OS" or self.get_argument("os", "") == "ios"

    @property
    def is_wp_platform(self):
        if (self.is_debug or self.is_doc) and self.has_arg("_os_"):
            self.client.os = self.get_argument("_os_")
        return self.client.user_agent.find("WindowsPhone") != -1

    @property
    def is_pad(self):
        if (self.is_debug or self.is_doc) and self.has_arg("_product_"):
            self.client.product = self.get_argument("_product_", "").replace("+", " ")
        return self.client.product == "Tudou HD"

    @property
    def is_phone(self):
        if (self.is_debug or self.is_doc) and self.has_arg("_product_"):
            self.client.product = self.get_argument("_product_", "").replace("+", " ")
        return self.client.product == "Tudou"

    def _get_type(self):
        if self.is_android_platform:
            if self.is_phone:
                return 6
            return 7
        elif self.is_ios_platform:
            if self.is_phone:
                return 4
            return 5
        return 10

    def get_m3u8_url(self, itemid, st=2):
        return _M3U8_URL % (itemid, st)

    def get_m3u8_url_with_aes(self, itemid, st=2):
        return encrypt_base64(_M3U8_URL % (itemid, st))

    #TODO: test
    def get_m3u8_meta_url_with_aes(self, itemid, ver='v1'):
        url = _M3U8_META_URL % {'domain': settings.m3u8_info_domain,
                                'iid': itemid, 'version': ver}
        return encrypt_base64(url)

    def get_encrypt_play_url(self, itemcode, ver='v2'):
        url = _M3U8_META_URL_WITH_ICODE % {'domain': settings.m3u8_info_domain,
                                           'icode': itemcode, 'version': ver}
        return encrypt_base64(url)

    def get_web_url(self, itemcode):
        return _WEB_URL % itemcode

    def get_wanhuo_url(self, itemcode):
        return _WANHUO_URL % itemcode

    def get_url_params(self,url):
        values = url.split('?')[-1]
        paramsDict = {}
        for key_value in values.split('&'):
            key = key_value.split('=')[0]
            value = key_value.split('=')[1]
            paramsDict[key] = value
        return paramsDict

class CacheApiHandler(ApiHandler):

    def __init__(self, application, request, **kwargs):
        self._cache_buffer = []
        super(ApiHandler, self).__init__(application, request, **kwargs)

    def write(self, chunk):
        if isinstance(chunk, dict):
            self._cache_buffer.append(chunk)
        super(ApiHandler, self).write(chunk)

    @property
    def cache_buffer(self):
        return self._cache_buffer
