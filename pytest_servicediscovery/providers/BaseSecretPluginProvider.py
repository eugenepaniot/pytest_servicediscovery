from pytest_servicediscovery.providers.BasePluginProvider import BasePluginProvider


class BaseSecretPluginProvider(BasePluginProvider):
    @property
    def value(self):
        """value property

        :rtype:
        :return: Secret value
        """
        raise NotImplementedError()
