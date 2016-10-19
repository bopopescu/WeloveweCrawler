#encoding=utf-8
import os
from tornado.web import url
from api_doc import api_manager, ApiDefined, API_TYPE_COLLECT
from doc import ApiDocHandler

class ExampleParam(dict):

    def __init__(self, parent, name):
        super(ExampleParam, self).__init__()

        self['_parent'] = parent
        self['_name'] = name

    def __getattr__(self, name):
        if not self.has_key(name):
            self[name] = ExampleParam(self, name)
        return self[name]

    def __str__(self):
        if self['_parent']:
            return '%s.%s' % (self['_parent'], self['_name'])
        else:
            return self['_name']

    def print_tree(self, pre=''):
        ps = ['%s%s%s' % (pre, k, (lambda vp: vp and ':\r\n%s' % vp or '')(v.print_tree(pre + '\t'))) for k, v in
              self.items() if k not in ('_parent', '_name')]
        if ps:
            return "%s" % '\r\n'.join(ps)
        else:
            return ""

class Param(dict):
    def __init__(self, name, required=False, param_type=str, default=None,
                 example=None, description="", hidden=False):
        dict.__init__(self)
        self['name'] = name
        self['required'] = required
        self['param_type'] = param_type
        self['default'] = default
        self['example'] = example
        self['description'] = description
        self['hidden'] = hidden

    def display_type(self, _t=None):
        _t = _t or self['param_type']
        if type(_t) in (list, tuple) and _t:
            return '[%s,..]' % self.display_type(_t[0])
        return _t.__name__

    def display_example(self):
        if self['hidden']: return ''
        if self['param_type'] is bool:
            return self['example'] and 'true' or 'false'
        else:
            return str(self['example'])

    def html_example(self):
        if self['hidden']: return ''
        if type(self['example']) is ExampleParam:
            return '<input  class="span2" type="text" class="example_input" name="%s" value=""><a class="example_value" val="%s">E</a>'\
            % (self['name'], str(self['example']))
        if self['param_type'] is file:
            return '<input class="span2" name="%s" type="file"/>' % self['name']
        if self['param_type'] is bool:
            return '<select name="%s"><option value="true"%s>True</option><option value="false"%s>False</option></select>' %\
                   (self['name'], self['example'] and ' selected' or '', (not self['example']) and ' selected' or '')
        elif self['param_type'] in (str, int, float):
            if type(self['example']) in (list, tuple):
                return '<select name="%s">%s</select>' % \
                       (self['name'],
                        ''.join(['<option value="%s">%s</option>' % \
                                (v, v) for v in self['example']]))
        return '<input  class="span2" type="text" name="%s" value="%s">' % \
               (self['name'], str(self['example']))

    def __getattr__(self, name):
        try:
            return self[name]
        except Exception:
            return None


def api_define(name, uri, params=[], result=None, filters=[], description='',
               add_user=False, beta=False, wiki='', source_wiki='',
               api_type=1, third_online_time='', offline=None):
    def wrap(method):
        if not hasattr(method, 'apis'):
            setattr(method, 'apis', [])

        if add_user:
            params.append(Param('_cookie', False, str, '', '_l_lgi%3D70994840%3B%20k%3D%25E7%25A2%258E%25E5%25BD%25AA%3B%20logintime%3D1348481501%3B%20u%3D%25E7%25A2%258E%25E5%25BD%25AA%3B%20v%3DUMjgzOTc5MzYw__1%257C1348481501%257C15%257CaWQ6NzA5OTQ4NDAsbm4656KO5b2q%257Cc2c9e54a6d75b1fd0888809efe1fde12%257Cf067914723d4925277d0e0f71fe05f716774c024%257C1____dd316050b67516220971eff7%3B%20ykss%3Ddd316050b67516220971eff7%3B%20yktk%3D1%257C1348481501%257C15%257CaWQ6NzA5OTQ4NDAsbm4656KO5b2q%257Cc2c9e54a6d75b1fd0888809efe1fde12%257Cf067914723d4925277d0e0f71fe05f716774c024%257C1%3B%20_1%3D1', u'cookie for test'))

        params.append(Param('guid', True, str, "9c553730ef5b6c8c542bfd31b5e25b69", "9c553730ef5b6c8c542bfd31b5e25b69", u'guid'))
        params.append(Param('_os_', True, str, "", ["Android", "iPhone"], u'os这个字段出自header，这里for test'))
        params.append(Param('_product_', True, str, "", ["Tudou", "Tudou HD"], u'product这个字段出自header，这里for test'))

        getattr(method, 'apis').append(
            ApiDefined(name, method.__name__.upper(), uri, params, result,
                       module=method.__module__, filters=filters,
                       description=description, wiki=wiki,
                       source_wiki=source_wiki, beta=beta,
                       api_type=api_type, third_online_time=third_online_time,
                       offline=offline))

        return method

    return wrap


def handler_define(cls):
    for m in [getattr(cls, i) for i in dir(cls) if callable(getattr(cls, i)) and hasattr(getattr(cls, i), 'apis')]:
        for api in m.apis:
            api['handler'] = cls
            if api['filters']:
                for f in api['filters']:
                    f(api)
            api_manager.addapi(api)
    return cls


def load_api_doc(path, debug=False):
    import api.urls

    apiurls = api_manager.get_urls()

    app_settings = {}

    if debug:
        apiurls = apiurls + [
            url(r"/doc$", ApiDocHandler),
        ]

        app_settings = {
            "template_path": os.path.join(path, "view"),
            "static_path": os.path.join(path, "view", "templates", "docs"),
            "static_url_prefix": '/doc/static/',
        }

    return apiurls, app_settings

