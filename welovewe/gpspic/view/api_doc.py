#coding=utf-8

from tornado.web import url

API_TYPE_COLLECT = 1       #采集API

class ApiDefined(dict):

    def __init__(self, name, method, uri, params=None, result=None,
                 need_login=False, need_appkey=False, handler=None,
                 module=None, filters=None, description='', wiki='',
                 source_wiki='', beta=False, api_type=1, third_online_time="",
                 offline=None):
        dict.__init__(self)
        self['name'] = name
        self['method'] = method
        self['module'] = module
        self['uri'] = uri
        self['handler'] = handler
        self['params'] = params or []
        self['result'] = result
        self['need_login'] = need_login
        self['need_appkey'] = need_appkey
        self['filters'] = filters or []
        self['description'] = description
        self['wiki'] = wiki
        self['api_type'] = api_type
        if source_wiki:
            source_wiki = source_wiki.split(';')
        self['source_wiki'] = source_wiki
        self['beta'] = beta
        self['third_online_time'] = third_online_time
        self['offline'] = offline

    def get_handler_name(self):
        return self['handler'].__name__

    def doc(self):
        d = '%s\n%s %s' % (self['name'], self['method'], self['uri'])
        d = d + '\nname\trequired\ttype\tdefault\texample\t\tdesc'
        d = d + '\n------------------------------------------------'
        for p in self['params']:
            d = d + '\n%s\t%s\t%s\t%s\t%s\t%s' % (
                p.name, p.required, p.param_type.__name__,
                p.default, p.display_example(), p.description)
        if self['result']:
            d = d + '\nResult:\n%s' % self['result']
        return d

    def __getattr__(self, name):
        try:
            return self[name]
        except Exception:
            return None


class ApiHolder(object):
    apis = []

    def __init__(self):
        pass

    def addapi(self, api):
        api['id'] = len(self.apis) + 1
        self.apis.append(api)

    def get_apis(self, name=None, module=None, handler=None,
                 beta=None, api_type=None, offline=None):
        all_apis = self.apis
        if name:
            name = name.replace(' ', '_').lower()
            all_apis = filter(lambda api: api.name.lower().replace(' ', '_') == name, all_apis)

        if api_type:
            api_type = int(api_type)
            if api_type == API_TYPE_COLLECT:
                all_apis = filter(lambda api: api.api_type == API_TYPE_COLLECT, all_apis)

        all_apis = filter(lambda api: api.beta == beta, all_apis)
        all_apis = filter(lambda api: api.offline == offline, all_apis)

        if module:
            all_apis = filter(lambda api: api['module'] == module, all_apis)
        if handler:
            handler = handler.lower()
            all_apis = filter(lambda api: api['handler'].__name__.lower() == handler or \
                              api['handler'].__name__.lower() == '%shandler' % handler,
                              all_apis)
        return all_apis

    def get_urls(self):
        urls = {}
        for api in self.apis:
            if not urls.has_key(api['uri']):
                urls[api['uri']] = api['handler']
        return [url(r'%s$' % uri, handler) for uri, handler in urls.items()]

api_manager = ApiHolder()

