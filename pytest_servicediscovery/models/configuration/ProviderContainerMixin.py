from schematics.exceptions import UnknownFieldError

from pytest_servicediscovery.exceptions import WrongImplementation
from pytest_servicediscovery.models.Base import Model
from pytest_servicediscovery.providers import ProviderManager


class ProviderContainerMixin(Model):
    def __new__(cls, model=None, raw_data=None, *args, **kwargs):
        pmclass = cls

        if raw_data is None:
            raw_data = {}

        __provider = raw_data.get('__provider')

        if __provider:
            if not hasattr(ProviderManager.plugins[__provider].__class__, 'Meta'):
                raise WrongImplementation("Meta class should be defined for %s class" %
                                          ProviderManager.plugins[__provider].__class__.__name__)

            if not hasattr(ProviderManager.plugins[__provider].__class__.Meta, model):
                raise WrongImplementation("Attribute '%s' should be defined in Meta class for %s class" %
                                          (model, ProviderManager.plugins[__provider].__class__.__name__))

            pmclass = getattr(ProviderManager.plugins[__provider].__class__.Meta, model)

        try:
            del raw_data['__provider']
        except (UnknownFieldError, KeyError):
            pass

        return super(ProviderContainerMixin, cls).__new__(pmclass, raw_data, *args, **kwargs)


class ProviderParameters(ProviderContainerMixin):
    def __new__(cls, raw_data=None, *args, **kwargs):
        return super(ProviderParameters, cls).__new__(cls, 'model_parameters', raw_data, *args, **kwargs)
