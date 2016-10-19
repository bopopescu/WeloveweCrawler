#coding=utf-8
import logging
import json
import traceback

from urllib import urlencode
from tornado.httputil import url_concat
from tornado.httpclient import AsyncHTTPClient
from tornado.gen import coroutine, Return

LOG = logging.getLogger()
AsyncHTTPClient.configure(AsyncHTTPClient.configurable_default(),
                          **{'max_clients': 65535})

class BaseApi(object):
    HEADERS = {
        'Accept-Language': 'zh-cn',
        'User-Agent': 'Tudou API',
        "Accept-Charset": "utf-8"
    }

    @classmethod
    @coroutine
    def get(cls, path, params='', host='', header=None,
            conn_timeout=None, req_timeout=None):
        '''
        normal get request
        '''

        host = host or cls.HOST
        conn_timeout = conn_timeout or cls.CONNECT_TIMEOUT
        req_timeout = req_timeout or cls.REQUEST_TIMEOUT

        headers = cls.HEADERS.copy()
        if isinstance(header, dict):
            headers.update(header)

        url = url_concat('http://' + host + path, params)
        LOG.debug('[GET] %s', url)

        request = AsyncHTTPClient()
        try:
            response = yield request.fetch(url, headers=headers,
                                           connect_timeout=conn_timeout,
                                           request_timeout=req_timeout)
            LOG.debug('[API] request time: %.2fms',
                      1000 * response.request_time)
            result = json.loads(response.body)
        except Exception, e:
            LOG.error(traceback.format_exc())
            result = {}

        raise Return(result)

    @classmethod
    @coroutine
    def post(cls, path, params='', host='', header=None,
             conn_timeout=None, req_timeout=None):
        '''
        normal post request,
        body has type of application/x-www-form-urlencoded
        '''

        host = host or cls.HOST
        conn_timeout = conn_timeout or cls.CONNECT_TIMEOUT
        req_timeout = req_timeout or cls.REQUEST_TIMEOUT

        headers = cls.HEADERS.copy()
        if isinstance(header, dict):
            headers.update(header)

        url = 'http://' + host + path
        body = urlencode(params)
        LOG.debug('[POST] %s %s', url, body)

        request = AsyncHTTPClient()
        try:
            response = yield request.fetch(url, method='POST',
                                           headers=headers, body=body,
                                           connect_timeout=conn_timeout,
                                           request_timeout=req_timeout)
            LOG.debug('[API] request time: %.2fms',
                      1000 * response.request_time)
            result = json.loads(response.body)
        except Exception, e:
            LOG.error(traceback.format_exc())
            result = {}

        raise Return(result)

    @classmethod
    @coroutine
    def post_with_response(cls, path, params='', host='', header=None,
                           conn_timeout=None, req_timeout=None):
        '''
        normal post request,
        body has type of application/x-www-form-urlencoded
        '''

        host = host or cls.HOST
        conn_timeout = conn_timeout or cls.CONNECT_TIMEOUT
        req_timeout = req_timeout or cls.REQUEST_TIMEOUT

        headers = cls.HEADERS.copy()
        if isinstance(header, dict):
            headers.update(header)

        url = 'http://' + host + path
        body = urlencode(params)
        LOG.debug('[POST] %s %s', url, params)

        request = AsyncHTTPClient()
        try:
            response = yield request.fetch(url, method='POST',
                                           headers=headers, body=body,
                                           connect_timeout=conn_timeout,
                                           request_timeout=req_timeout)
            LOG.debug('[API] request time: %.2fms',
                      1000 * response.request_time)
            result = json.loads(response.body)
        except Exception, e:
            LOG.error(traceback.format_exc())
            result = {}

        raise Return((response, result))

    @classmethod
    @coroutine
    def special_post(cls, path, params='', body=None, host='', header=None,
                     conn_timeout=None, req_timeout=None):
        '''
        special post, body is json string
        '''

        host = host or cls.HOST
        conn_timeout = conn_timeout or cls.CONNECT_TIMEOUT
        req_timeout = req_timeout or cls.REQUEST_TIMEOUT

        headers = cls.HEADERS.copy()
        if isinstance(header, dict):
            headers.update(header)
        headers['Accept'] = 'application/json'
        headers['Content-Type'] = 'application/json'

        url = url_concat('http://' + host + path, params)
        LOG.debug('[SPECIAL POST] %s %s', url, body)

        request = AsyncHTTPClient()
        try:
            response = yield request.fetch(url, method='POST',
                                           headers=headers, body=body,
                                           connect_timeout=conn_timeout,
                                           request_timeout=req_timeout)
            LOG.debug('[API] request time: %.2fms',
                      1000 * response.request_time)
            result = json.loads(response.body)
        except Exception, e:
            LOG.error(traceback.format_exc())
            result = {}

        raise Return(result)

    @classmethod
    @coroutine
    def special_put(cls, path, params='', body=None, host='', header=None,
                     conn_timeout=None, req_timeout=None):
        '''
        special put, body is json string
        '''

        host = host or cls.HOST
        conn_timeout = conn_timeout or cls.CONNECT_TIMEOUT
        req_timeout = req_timeout or cls.REQUEST_TIMEOUT

        headers = cls.HEADERS.copy()
        if isinstance(header, dict):
            headers.update(header)
        headers['Accept'] = 'application/json'
        headers['Content-Type'] = 'application/json'

        url = url_concat('http://' + host + path, params)
        LOG.debug('[SPECIAL PUT] %s %s', url, body)

        request = AsyncHTTPClient()
        try:
            response = yield request.fetch(url, method='PUT',
                                           headers=headers, body=body,
                                           connect_timeout=conn_timeout,
                                           request_timeout=req_timeout)
            LOG.debug('[API] request time: %.2fms',
                      1000 * response.request_time)
            result = json.loads(response.body)
        except Exception, e:
            LOG.error(traceback.format_exc())
            result = {}

        raise Return(result)

class FormdataApi(BaseApi):
    HEADERS = {
        'Accept': '*/*',
        'Expect': '100-continue',
    }

class BinaryPostApi(BaseApi):
    HEADERS = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/octet-stream',
    }

class AsciiPostApi(BaseApi):
    HEADERS = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencode',
    }

