#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Cookie import SimpleCookie, CookieError
import urllib
import logging

class UserCookie(SimpleCookie):
    def __init__(self):
        SimpleCookie.__init__(self)

        self.username = ''
        self.userid = ''
        self.token = ''
        self.sessionid = ''
        self.auth = ''
        self.ykss = ''

        self._loaded = False

    def server_load(self, rawdata):
        """ cookies from server, with the keys:
            u, yktk (or k, v), YOUKUSESSID
        """
        assert not self._loaded
        self.load(rawdata)

        if 'u' in self:
            self.username = self._decode_plus('u')
        if 'yktk' in self:
            self.token = self._decode('yktk')
        if 'v' in self:
            self.auth = self._decode('v')
        if 'uid' in self:
            self.userid = self._decode('uid')
        if 'ykss' in self:
            self.ykss = self._decode('ykss')

        self._loaded = True

    def client_load(self, rawdata):
        """ cookies from client, with the keys:
            u, k, v, YOUKUSESSID, notused
        """
        assert not self._loaded
        try:
            # FIXME: 解决某些客户端会在cookie最前面加一个逗号的问题
            rawdata = rawdata.strip(',')
            self.load(rawdata)
        except CookieError as e:
            logging.exception(e)
            self.load('')

        if 'k' in self:
            self.username = self._decode('k')
        if 'v' in self:
            v = self._decode('v')
            try:
                cc = v.split(u'__')
                self.userid, self.token, self.auth = cc[:3]
                if len(cc) == 4:
                    self.ykss = cc[-1]
            except Exception as e:
                logging.error(e)
        if 'uid' in self:
            self.userid = self._decode('uid')
        if 'yktk' in self:
            self.token = self._decode('yktk')
        if 'ykss' in self:
            self.ykss = self._decode('ykss')

        self._loaded = True

    def server_output(self):
        assert self._loaded
        data = {}
        for k, m in self.items():
            if k not in ['u', 'k', 'v', 'yktk', 'ykss']:
                data[k] = m.coded_value

        if self.username:
            data['u'] = self._urlencode(self.username)

        if self.token:
            data['yktk'] = self._urlencode(self.token)
        else:
            if self.username:
                data['k'] = self._urlencode(self.username)
            if self.auth:
                data['v'] = self._urlencode(self.auth)

        return '; '.join(['{0}={1}'.format(x, y) for (x, y) in data.items()])

    def client_output(self):
        """ return list of cookie value """
        assert self._loaded

        data = self
        data['k'] = self._urlencode(self.username)
        data['v'] = self._urlencode(self._mix_v())
        return ['{0}={1}; path=/; domain=.youku.com'.format(c.key, c.coded_value) for c in data.values()]

    def android_output(self):
        assert self._loaded
        k = self._urlencode(self.username)
        v = self._urlencode(self._mix_v())
        result = '_1=1; k={0}; v={1}; _2=2'
        return result.format(k, v)

    def _mix_v(self):
        return u'__'.join([self.userid, self.token, self.auth, self.ykss])

    def _decode(self, key):
        value = self[key].coded_value
        return urllib.unquote(value).decode('utf-8')

    #################################################
    #  空格转换成＋
    #################################################

    def _decode_plus(self, key):
        value = self[key].coded_value
        return urllib.unquote_plus(value).decode("utf-8")

    def _urlencode(self, value):
        if isinstance(value, unicode):
            value = value.encode('utf-8')
        return urllib.quote(value, '')

    def is_login(self):
        # TODO: 判断还需要详细
        return bool(self.username) and bool(self.userid)
