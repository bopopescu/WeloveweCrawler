#encoding=utf-8
from api import ApiHandler
from view import api_define, handler_define

@handler_define
class LvsHealthCheckHandler(ApiHandler):

    @api_define('Health Check', '/lvs/lvs', params=[],
                filters=[], beta=True, description=u'lvs负载均衡健康检查')
    def get(self):
        self.write('ok')

    @api_define('Health Check', '/lvs/lvs', params=[],
                filters=[], beta=True, description=u'lvs负载均衡健康检查')
    def head(self):
        pass

