from schematics.types import ModelType, StringType, ListType

from pytest_servicediscovery.exceptions import UnexpectedBehavior, ProviderNotFoundException, WrongConfiguration
from pytest_servicediscovery.models.Base import Model
from pytest_servicediscovery.models.Null import NullProviderCfg
from pytest_servicediscovery.models.Services import Service
from pytest_servicediscovery.models.configuration.PluginContainerMixin import PluginConfiguration
from pytest_servicediscovery.models.configuration.ProviderContainerMixin import ProviderParameters
from pytest_servicediscovery.models.types import Secrets
from pytest_servicediscovery.providers import ProviderManager, PluginProvidersManager
from pytest_servicediscovery.providers.BaseSecretPluginProvider import BaseSecretPluginProvider
from pytest_servicediscovery.providers.BaseServicePluginProvider import BaseServicePluginProvider


class ServiceWithParameters(Model):
    def __init__(self, *args, **kwargs):
        __args = []
        for a in args:
            if isinstance(a, dict):
                if 'parameters' in a and a['parameters']:
                    for i, _ in enumerate(a['parameters']):
                        if '__provider' in a['parameters'][i]:
                            raise UnexpectedBehavior('__provider already exists')

                        a['parameters'][i]['__provider'] = a.get('provider')

            __args.append(a)

        super(ServiceWithParameters, self).__init__(*__args, **kwargs)


class ProviderWithParameters(Model):
    def __init__(self, *args, **kwargs):
        __args = []
        for a in args:
            if isinstance(a, dict):
                if 'parameters' in a and a['parameters']:
                    for i, _ in enumerate(a['parameters']):
                        if '__plugin' in a['parameters'][i]:
                            raise UnexpectedBehavior('__plugin already exists')

                        a['parameters'][i]['__plugin'] = a.get('plugin')

            __args.append(a)

        super(ProviderWithParameters, self).__init__(*__args, **kwargs)


class DiscoveryProvider(ProviderWithParameters):
    name = StringType(required=True)
    plugin = StringType(required=True)
    parameters = ListType(ModelType(PluginConfiguration), default=[])

    def validate_parameters(self, data, value):
        if not value and hasattr(self, "plugin"):
            plugin = PluginProvidersManager.plugins[self.plugin]
            model = getattr(plugin().__class__.Meta, "model")

            if not issubclass(model, NullProviderCfg):
                raise WrongConfiguration("Provider '%s' require configuration according to model '%s'"
                                         % (self.name, model.__name__))

    def __init__(self, *args, **kwargs):
        super(DiscoveryProvider, self).__init__(*args, **kwargs)
        self.validate()

        if self.name not in ProviderManager.plugins:
            self.log.info("Initialize service discovery \"%s\" provider" % self.name)

            plugin = PluginProvidersManager.plugins[self.plugin]()

            ProviderManager.plugins[self.name] = plugin.new(
                cfg=self.parameters,
                name=self.name
            )


class ConfigurationServiceSecret(ServiceWithParameters):
    name = StringType(required=True)
    provider = StringType(required=True)
    parameters = ListType(ModelType(ProviderParameters), default=[])

    __value = StringType()

    def validate_provider(self, data, value):
        if value not in ProviderManager.plugins.keys():
            raise ProviderNotFoundException(value)

        if not isinstance(ProviderManager.plugins[value], BaseSecretPluginProvider):
            raise WrongConfiguration("Provider '%s' can not be used for secret discovery" % value)

    def __init__(self, *args, **kwargs):
        super(ConfigurationServiceSecret, self).__init__(*args, **kwargs)
        self.validate()

        sd = ProviderManager.plugins[self.provider].call(
            parameters=self.parameters
        )

        self.__value = sd.value
        self.validate()


class ConfigurationService(ServiceWithParameters):
    name = StringType(required=True, regex='^[a-z0-9_]+$')
    provider = StringType(required=True)
    parameters = ListType(ModelType(ProviderParameters), required=True)
    secrets = ListType(ModelType(ConfigurationServiceSecret), required=True)

    __service = ModelType(Service)

    def validate_provider(self, data, value):
        if value not in ProviderManager.plugins.keys():
            raise ProviderNotFoundException(value)

        if not isinstance(ProviderManager.plugins[value], BaseServicePluginProvider):
            raise WrongConfiguration("Provider '%s' can not be used for service discovery" % value)

    def __init__(self, *args, **kwargs):
        super(ConfigurationService, self).__init__(*args, **kwargs)
        self.validate()

        sd = ProviderManager.plugins[self.provider].call(
            parameters=self.parameters
        )

        self.__service = Service(dict(
            name=self.name,
            address=sd.service_address,
            addresses=sd.service_addresses,
            secrets=Secrets(map(lambda x: [x.name, x._ConfigurationServiceSecret__value], self.secrets)),
            health_checks=sd.service_health_checks
        ))

        self.validate()


class Configuration(Model):
    providers = ListType(ModelType(DiscoveryProvider), default=[])
    services = ListType(ModelType(ConfigurationService), default=[])

    def __init__(self, configuration, *args, **kwargs):
        super(Configuration, self).__init__(configuration, *args, **kwargs)

        if 'providers' in configuration:
            self.providers = configuration['providers']

        if 'services' in configuration:
            self.services = configuration['services']

        self.validate()
