from schematics.types import IntType

from pytest_servicediscovery.models.HealthChecks import HealthChecks
from pytest_servicediscovery.models.Null import NullProviderParameter
from pytest_servicediscovery.models.Services import Address
from pytest_servicediscovery.models.configuration.PluginContainerMixin import PluginConfiguration
from pytest_servicediscovery.models.types import IPAddressOrDomainType
from pytest_servicediscovery.providers.BaseServicePluginProvider import BaseServicePluginProvider


class StaticServiceParameter(PluginConfiguration):
    """StaticServiceParameter cfg parameters"""
    ip = IPAddressOrDomainType(required=True)
    port = IntType(required=True, min_value=1, max_value=65535)


class StaticServiceProviderClass(BaseServicePluginProvider):
    """**StaticServiceProviderClass**

        DiscoveryProvider that implement's methods to work with static service address definition
    """

    class Meta(object):
        name = "static"
        model = StaticServiceParameter
        model_parameters = NullProviderParameter

    @property
    def service_address(self):
        """Return service_address for the first service in a list

        - Example::

            Address(ip=10.186.106.2, port=8300)

        :return: Address Model
        :rtype: Address
        """
        return self.service_addresses[0]

    @property
    def service_addresses(self):
        """Return service_addresses for the service

        - Example::

            [
                Address(ip=10.186.106.2, port=8300),
                Address(ip=10.186.106.3, port=8300)
            ]

        :return: tuple of Address Models
        :rtype: tuple
        """
        return tuple(map(lambda p: Address(dict(ip=p['ip'], port=p['port'])), self.cfg))

    @property
    def service_health_checks(self):
        """Return Service HealthChecks

        :rtype: HealthChecks
        :return: Service HealthChecks
        """
        return HealthChecks()
