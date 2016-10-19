import tornado

from tornado.web import RequestHandler
from api_doc import api_manager
from conf import settings

class ApiDocHandler(RequestHandler):

    def get(self):
        '''
        Api documentation for development
        '''
        beta = bool(int(self.get_argument('beta', 0)))
        api_type = self.get_argument('api_type', '1')

        all_apis = api_manager.get_apis(name=self.get_argument('name', None),
                                        module=self.get_argument('module', None),
                                        handler=self.get_argument('handler', None),
                                        beta=beta, api_type=api_type)
        apis = {}
        for api in all_apis:
            if not apis.has_key(api.module):
                apis[api.module] = []
            apis[api.module].append(api)
        App = type('App', (object,), {'name': "api",})
        app = App()

        channel_ids = settings.channel_ids
        self.render('templates/docs/api_docs.html',
                    **{
                        'tornado': tornado, 'apis': apis,
                        'api_base': self.settings.get("api_base", ''),
                        'test_app_key': "", 'test_app': app,
                        'test_user_name': self.settings.get("test_user_name", ''),
                        'beta': beta, 'channel_ids': channel_ids,
                        'api_type': api_type
                    })


