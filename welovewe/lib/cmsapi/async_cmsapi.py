#encoding=utf-8
import logging
import traceback
import json
import time
import datetime

from tornado.gen import coroutine, Return

from conf import settings
from lib.base import BaseApi
from lib.cmsapi import CMS_HOST
from lib.cmsapi import CONNECT_TIMEOUT, REQUEST_TIMEOUT

LOG = logging.getLogger()

class CMSApi(BaseApi):
    HOST = CMS_HOST
    CONNECT_TIMEOUT = CONNECT_TIMEOUT
    REQUEST_TIMEOUT = REQUEST_TIMEOUT

    @classmethod
    def query_user(cls, uid):
        path = "/sharedapi/users/q"
        req = {
            'ssoId': uid,
        }
        return cls.get(path, req)

    @classmethod
    def insert_user(cls, uid, name='', phone='', email='', reason=''):
        path = "/sharedapi/users"
        req = {
            'ssoId': uid,
        }
        if name:
            req['name'] = name.encode('utf-8')
        if phone:
            req['phone'] = phone
        if email:
            req['email'] = email
        if reason:
            req['certificate'] = reason.encode('utf-8')
        body = json.dumps(req)
        return cls.special_post(path, body=body)

    @classmethod
    def query_liveshow(cls, uid, number, size):
        path = "/sharedapi/users/%s/liveshow/" % uid
        req = {
            'pn': number,
            'rs': size,
        }
        return cls.get(path, req)

    @classmethod
    def create_liveshow(cls, title, token, testable, start_time):
        path = "/sharedapi/liveshow"
        now = datetime.datetime.fromtimestamp(start_time)
        req = {
            'title': title.encode('utf-8'),
            'status': 0,
            'startDate': now.strftime("%Y-%m-%d %H:%M:%S"),
            'testable': int(testable) == 1,
        }
        body = json.dumps(req)
        return cls.special_post(path, body=body, header={'token': token})

    @classmethod
    def update_liveshow(cls, showid, token, **kwargs):
        path = "/sharedapi/liveshow/%s" % showid
        body = json.dumps(kwargs)
        return cls.special_put(path, body=body, header={'token': token})

    @classmethod
    def query_livestream(cls, showid):
        path = "/sharedapi/liveshow/%s/streams" % showid
        return cls.get(path)

    @classmethod
    def query_livestream_by_token(cls, token):
        path = "/sharedapi/streams/q"
        return cls.get(path, header={'token': token})

    @classmethod
    def create_livestream(cls, showid, token, hds, data):
        path = "/sharedapi/liveshow/%s/streams" % showid
        now = datetime.datetime.utcnow()
        req = {
            'definition': hds,
            'priority': 0,
            'status': 0,
            'data': data,
        }
        body = json.dumps(req)
        return cls.special_post(path, body=body, header={'token': token})

    @classmethod
    def update_livestream(cls, streamid, showid, token, hds, data):
        path = "/sharedapi/streams/%s" % streamid
        req = {
            'definition': hds,
            'showId': showid,
            'status': 0,
            'data': data,
        }
        body = json.dumps(req)
        return cls.special_post(path, body=body, header={'token': token})
