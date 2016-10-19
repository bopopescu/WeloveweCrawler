"""
inspired by django/conf/__init__.py
"""
#import warnings

from functional import LazyObject

class BaseSettings(object):
    """
    Common logic for settings whether set by a module or by the user.
    """
    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)

class LazySettings(LazyObject):
    """
    A lazy proxy for either global settings or a custom settings object
    """
    def _setup(self):
        raise RuntimeError("settings must be configured before using.")

    def configure(self, **options):
        """
        Called to manually configure the settings.
        """
        if self._wrapped != None:
            raise RuntimeError('Settings already configured.')
        holder = BaseSettings()
        for name, value in options.items():
            setattr(holder, name, value)
        self._wrapped = holder

    def configured(self):
        """
        Returns True if the settings have already been configured.
        """
        return bool(self._wrapped)
    configured = property(configured)

settings = LazySettings()

