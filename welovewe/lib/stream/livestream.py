import logging

from lib.base import BaseApi
from lib.stream import LIVESTREAM_HOST
from lib.stream import CONNECT_TIMEOUT, REQUEST_TIMEOUT

LOG = logging.getLogger()

class LiveStreamApi(BaseApi):
    HOST = LIVESTREAM_HOST
    CONNECT_TIMEOUT = CONNECT_TIMEOUT
    REQUEST_TIMEOUT = REQUEST_TIMEOUT

    @classmethod
    def create_live(cls, req):
        path = "/LiveCdnManage/liveManage/create_live.do"
        return cls.get(path, req)

    @classmethod
    def destroy_live(cls, req):
        path = "/LiveCdnManage/liveManage/destroy_live.do"
        return cls.post(path, req)
