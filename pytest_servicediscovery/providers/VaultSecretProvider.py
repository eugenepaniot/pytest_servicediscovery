import hvac
from hamcrest import assert_that, has_key
from schematics.types import StringType, IntType

from pytest_servicediscovery.decorators import logthis
from pytest_servicediscovery.models.configuration.PluginContainerMixin import PluginConfiguration
from pytest_servicediscovery.models.configuration.ProviderContainerMixin import ProviderParameters
from pytest_servicediscovery.models.types import IPAddressOrDomainType
from pytest_servicediscovery.providers import ProviderManager
from pytest_servicediscovery.providers.BaseSecretPluginProvider import BaseSecretPluginProvider
import sys
if sys.version_info.major == 3:
    unicode = str


class VaultSecretProviderConfiguration(PluginConfiguration):
    ipAddress = IPAddressOrDomainType(required=True)
    port = IntType(min_value=1, max_value=65535, default=8200)
    scheme = StringType(choices=["http", "https"], default="http")
    namespace = StringType()
    token = StringType()


class VaultSecretProviderParameter(ProviderParameters):
    object = StringType(required=True, metadata=dict(description="The object path"))


class VaultSecretProvider(BaseSecretPluginProvider):
    """**VaultCrossProviderSDSecretProvider**"""

    class Meta(object):
        name = "vault"
        model = VaultSecretProviderConfiguration
        model_parameters = VaultSecretProviderParameter

    vault = None

    def new(self, cfg, *args, **kwargs):
        """Method to construct class

        :rtype: VaultSecretProvider
        :param cfg: Provider configuration
        :return: VaultSecretProvider
        """
        super(VaultSecretProvider, self).new(cfg, *args, **kwargs)

        c = self.cfg[0]

        self.vault = hvac.Client(url='%s://%s:%u' % (c.scheme, c.ipAddress, c.port),
                                 token=c.token,
                                 namespace=c.namespace,
                                 verify=False)

        return self

    @property
    @logthis()
    def value(self):
        """value property

        :rtype:
        :return: Secret value
        """
        read = self.vault.read(self.parameters[0].get('object'))

        assert_that(read, 'Data should no is not empty by the path %s' % self.parameters[0].get('object'))

        assert_that(read, has_key('data'))
        assert_that(read['data'], has_key('value'))

        return unicode(read['data']['value'])


class VaultCrossProviderSDSecretProviderConfiguration(VaultSecretProviderConfiguration):
    consulProvider = StringType(required=True)
    serviceName = StringType(default="vault")

    def __init__(self, *args, **kwargs):
        if isinstance(args[0], dict):
            assert_that(args[0], has_key("consulProvider"), "consulProvider in parameters")
            assert_that(args[0], has_key("serviceName"), "consulProvider in parameters")

            sd = ProviderManager.plugins[args[0]['consulProvider']].call(
                parameters=[dict(serviceName=args[0]['serviceName'])]
            )

            if 'ipAddress' not in args[0]:
                args[0]['ipAddress'] = sd.service_address.ip

            if 'port' not in args[0]:
                args[0]['port'] = sd.service_address.port

        super(VaultCrossProviderSDSecretProviderConfiguration, self).__init__(*args, **kwargs)


class VaultCrossProviderSDSecretProvider(VaultSecretProvider):
    """**VaultCrossProviderSDSecretProvider**"""

    class Meta(object):
        name = "vault-consul"
        model = VaultCrossProviderSDSecretProviderConfiguration
        model_parameters = VaultSecretProviderParameter
