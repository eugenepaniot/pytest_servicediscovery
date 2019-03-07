from pytest_servicediscovery.models.HealthChecks import HealthChecks
from pytest_servicediscovery.models.Null import NullProviderParameter, NullProviderCfg
from pytest_servicediscovery.models.Services import Address
from pytest_servicediscovery.providers.BaseSecretPluginProvider import BaseSecretPluginProvider
from pytest_servicediscovery.providers.BaseServicePluginProvider import BaseServicePluginProvider


class NullProviderClass(BaseServicePluginProvider, BaseSecretPluginProvider):
    """**NullProviderClass**

        Used for test purposes only
    """

    class Meta(object):
        name = "null"
        model = NullProviderCfg
        model_parameters = NullProviderParameter

    @property
    def value(self):
        """value property

        :rtype:
        :return: Secret value
        """
        return

    @property
    def service_address(self):
        return Address()

    @property
    def service_addresses(self):
        return [Address()]

    @property
    def service_health_checks(self):
        """Abstract property to return service_health_checks

        :return: HealthChecks Model
        :rtype: HealthChecks
        """
        return HealthChecks()
