import logging

from pytest_servicediscovery.exceptions import ProviderNotFoundException, DuplicateProvider
from six import add_metaclass


class PluginObject(dict):
    def __init__(self, **kwargs):
        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.DEBUG)

        super(PluginObject, self).__init__(**kwargs)

    def __getattr__(self, item):
        return self[item]

    def __getitem__(self, key):
        if key in self.keys():
            return dict.__getitem__(self, key)
        else:
            raise ProviderNotFoundException(key)

    def __setitem__(self, key, value):
        if key in self:
            raise DuplicateProvider(key)

        self.log.debug("Initialize \"%s\" with value \"%s\"" % (key, value))

        super(PluginObject, self).__setitem__(key, value)


class PluginMount(type):
    """
    Acts as a metaclass which creates anything inheriting from Plugin
    """

    def __init__(cls, name, bases, attrs):
        """Called when a Plugin derived class is imported"""

        super(PluginMount, cls).__init__(name, bases, attrs)

        if not hasattr(cls, 'plugins'):
            # Called when the metaclass is first instantiated
            cls.plugins = PluginObject()
        else:
            # Called when a plugin class is imported
            cls.register_plugin(cls)

    def register_plugin(cls, plugin):
        """Add the plugin to the plugin list and perform any registration logic"""

        # create a plugin instance and store it
        # optionally you could just store the plugin class and lazily instantiate
        instance = plugin()

        # save the plugin reference
        if hasattr(instance.__class__, "Meta") and hasattr(instance.__class__.Meta, "name") \
                and instance.__class__.Meta.name:

            cls.plugins[instance.__class__.Meta.name] = plugin

            # apply plugin logic - in this case connect the plugin to blinker signals
            # this must be defined in the derived class
            instance.register_signals()

    def __str__(self):
        return repr(self)

    def __repr__(self):
        __ = ", ".join(self.plugins.keys())

        return "\n{}({})".format(self.__class__.__name__, __)


@add_metaclass(PluginMount)
class PluginProvidersManager(object):
    """Class used for list plugins"""
    pass


@add_metaclass(PluginMount)
class ProviderManager(object):
    """Class used for list providers"""
    pass
