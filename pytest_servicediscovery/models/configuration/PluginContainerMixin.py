from schematics.exceptions import UnknownFieldError

from pytest_servicediscovery.exceptions import WrongImplementation
from pytest_servicediscovery.models.Base import Model
from pytest_servicediscovery.providers import PluginProvidersManager


class PluginContainerMixin(Model):
    def __new__(cls, model=None, raw_data=None, *args, **kwargs):
        pmclass = cls

        if raw_data is None:
            raw_data = {}

        __plugin = raw_data.get('__plugin')

        if __plugin:
            if not hasattr(PluginProvidersManager.plugins[__plugin]().__class__, 'Meta'):
                raise WrongImplementation("Meta class should be defined for %s class" %
                                          PluginProvidersManager.plugins[__plugin].__class__.__name__)

            if not hasattr(PluginProvidersManager.plugins[__plugin]().__class__.Meta, model):
                raise WrongImplementation("Attribute '%s' should be defined in Meta class for %s class" %
                                          (model, PluginProvidersManager.plugins[__plugin].__class__.__name__))

            pmclass = getattr(PluginProvidersManager.plugins[__plugin]().__class__.Meta, model)

        try:
            del raw_data['__plugin']
        except (UnknownFieldError, KeyError):
            pass

        return super(PluginContainerMixin, cls).__new__(pmclass, raw_data, *args, **kwargs)


class PluginConfiguration(PluginContainerMixin):
    def __new__(cls, raw_data=None, *args, **kwargs):
        return super(PluginConfiguration, cls).__new__(cls, 'model', raw_data, *args, **kwargs)
