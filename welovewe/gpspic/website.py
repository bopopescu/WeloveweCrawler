import sys
import os.path

# configure project path
SITE_PATH = os.path.realpath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.join(SITE_PATH, os.pardir)
sys.path.append(PROJECT_ROOT)
sys.path.append(os.path.join(PROJECT_ROOT, 'site-packages'))

from tornado.options import define, options, parse_command_line


define('server', default='tornado', type=str)
define('host', default='0.0.0.0', type=str)
define('port', default=8888, type=int)
parse_command_line()

import logging
LOG = logging.getLogger()

LOG.info('PROJECT_ROOT => [%s]', PROJECT_ROOT)

try:
    import tornado
    import Crypto
    import xlrd
except ImportError, e:
    LOG.error('%s, please install it before running', e)
    sys.exit(1)

def load_app_config():
    '''
    Load settings
    '''
    from conf.load_settings import load_tornado_settings,\
        load_global_settings, add_extra_tornado_settings
    from view import load_api_doc

    load_global_settings('gpspic')
    LOG.info('load global settings......done')

    tornado_settings = load_tornado_settings()
    LOG.info('load tornado settings.....done')

    apiurls, extra_config = load_api_doc(SITE_PATH, tornado_settings.get('debug', False))
    LOG.info('load api doc..............done')

    add_extra_tornado_settings(tornado_settings, extra_config)
    LOG.info('update tornado settings...done')

    return apiurls, tornado_settings

def main(apiurls, tornado_settings):
    from tornado.ioloop import IOLoop
    from tornado.web import Application
    from tornado.httpserver import HTTPServer

    if options.server == 'tornado':
        app = Application(apiurls, **tornado_settings)
        server = HTTPServer(app, no_keep_alive=True, xheaders=True)
        server.bind(options.port, address=options.host)
        server.start()
        LOG.info('******************************')
        LOG.info('**** start tornado server ****')
        LOG.info('******************************')
        IOLoop.current().start()

if __name__ == '__main__':
    main(*load_app_config())

