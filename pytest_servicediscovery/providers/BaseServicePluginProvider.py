from pytest_servicediscovery.providers.BasePluginProvider import BasePluginProvider


class BaseServicePluginProvider(BasePluginProvider):
    @property
    def service_address(self):
        raise NotImplementedError()

    @property
    def service_addresses(self):
        raise NotImplementedError()

    @property
    def service_health_checks(self):
        """Abstract property to return service_health_checks

        :return: HealthChecks Model
        :rtype: HealthChecks
        """
        raise NotImplementedError()
