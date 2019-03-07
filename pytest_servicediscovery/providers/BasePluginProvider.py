import logging

from pytest_servicediscovery.providers import PluginProvidersManager


class BasePluginProvider(PluginProvidersManager):
    class Meta(object):
        name = None
        model = None
        model_parameters = None

    def __init__(self, *args, **kwargs):
        super(PluginProvidersManager, self).__init__(*args, **kwargs)

        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.DEBUG)

        self.cfg = None
        self.parameters = None

    def register_signals(self):
        """Method to notice when class is registered"""
        print("Plugin \"%s\" registered as \"%s\"" % (self.__class__.__name__,
                                                      self.__class__.Meta.name))

    def new(self, cfg, name=None):
        """Abstract method to construct class

        :param name:
        :param cfg: Cfg
        :return: self
        :rtype: object
        """
        for c in cfg:
            self.__class__.Meta.model(c).validate()

        self.cfg = cfg
        if not self.cfg:
            self.cfg = [self.__class__.Meta.model()]

        if name:
            self.log.info("Initializing provider \"%s\" with plugin \"%s\"" % (name, self.__class__.Meta.name))

        self.log.debug("\"%s\" provider configuration: %s" % (name, repr(self.cfg).replace('\n', '')))

        return self

    def call(self, parameters):
        for p in parameters:
            self.__class__.Meta.model_parameters(p).validate()

        self.parameters = parameters

        if not self.parameters:
            self.parameters = [self.__class__.Meta.model_parameters()]

        return self

    def __str__(self):
        return repr(self)

    def __repr__(self):
        klass = self.__class__.__name__

        return "{}(cfg={})(parameters={})".format(klass, self.cfg, self.parameters)
