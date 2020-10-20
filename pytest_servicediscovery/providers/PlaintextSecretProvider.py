from schematics.types import StringType

from pytest_servicediscovery.decorators import logthis
from pytest_servicediscovery.models.Null import NullProviderCfg
from pytest_servicediscovery.models.configuration.ProviderContainerMixin import ProviderParameters
from pytest_servicediscovery.providers.BaseSecretPluginProvider import BaseSecretPluginProvider
import sys
if sys.version_info.major == 3:
    unicode = str


class PlaintextSecretProvideParameter(ProviderParameters):
    value = StringType(required=True)


class PlaintextSecretProvider(BaseSecretPluginProvider):
    """**PlaintextSecretProvider**

        Make possible to pass secrets in plaintext to configuration
    """

    class Meta(object):
        name = "plaintext"
        model = NullProviderCfg
        model_parameters = PlaintextSecretProvideParameter

    @property
    @logthis()
    def value(self):
        """value property

        :rtype:
        :return: Secret value
        """
        return unicode(self.parameters[0]['value'])
