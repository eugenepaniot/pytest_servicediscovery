from pytest_servicediscovery.models.configuration.ProviderContainerMixin import ProviderParameters
from pytest_servicediscovery.models.configuration.PluginContainerMixin import PluginConfiguration


class NullProviderCfg(PluginConfiguration):
    pass


class NullProviderParameter(ProviderParameters):
    pass
