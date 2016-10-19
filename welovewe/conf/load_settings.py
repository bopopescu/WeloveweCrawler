import logging
import importlib

from conf import settings as global_settings

LOG = logging.getLogger()

def load_tornado_settings():
    """
    get settings for tornado Application
    """
    settings = {}

    try:
        settings_module = importlib.import_module("gpspic.settings")
    except ImportError:
        LOG.warn('no settings module...')
    else:
        if hasattr(settings_module, 'update_tornado_settings'):
            getattr(settings_module, 'update_tornado_settings')(settings)

    try:
        my_settings_module = importlib.import_module("gpspic.my_settings")
    except ImportError:
        LOG.warn('no mysettings module...')
    else:
        if hasattr(my_settings_module, 'update_tornado_settings'):
            getattr(my_settings_module, 'update_tornado_settings')(settings)
    return settings

def add_extra_tornado_settings(settings, config):
    """
    update tornado settings in place, return nothing
    """
    settings.update(config)

def load_global_settings(*modules):
    """
    get settings for global use
    """
    settings = {'MODULES': modules}
    mods = []

    for mod in modules:
        try:
            module = importlib.import_module("%s.settings" % mod)
        except ImportError:
            LOG.error("could not import %s.settings", mod)
        else:
            mods.append(module)

    try:
        module = importlib.import_module("gpspic.my_settings")
    except ImportError:
        LOG.error("could not import my_settings")
    else:
        mods.append(module)

    for mod in mods:
        if hasattr(mod, 'update_global_settings'):
            getattr(mod, 'update_global_settings')(settings)

    global_settings.configure(**settings)

