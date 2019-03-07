import jks
from OpenSSL import crypto
from schematics.types import StringType

from pytest_servicediscovery.decorators import logthis
from pytest_servicediscovery.models.configuration.PluginContainerMixin import \
    PluginConfiguration
from pytest_servicediscovery.models.configuration.ProviderContainerMixin import \
    ProviderParameters
from pytest_servicediscovery.providers.BaseSecretPluginProvider import \
    BaseSecretPluginProvider


class JKSSecretProvideConfiguration(PluginConfiguration):
    passphrase = StringType(required=True,
                            metadata=dict(description="Keystore password"))
    jks_file = StringType(required=True,
                          serialized_name='jksFile',
                          metadata=dict(description="Keystore filename"))


class JKSSecretProviderParameter(ProviderParameters):
    key_alias = StringType(required=True,
                           serialized_name='keyAlias',
                           metadata=dict(
                               description='Alias for the stored key or certificate'
                           ))
    type = StringType(required=True,
                      choices=['ca', 'cert', 'key'],
                      metadata=dict(
                          description='Specify what to extract - ca, cert or key'
                      ))
    key_password = StringType(required=True,
                              serialized_name='keyPassword',
                              metadata=dict(
                                  description='Password for the private key'
                              ))


class JKSSecretProvider(BaseSecretPluginProvider):
    """**JKSSecretProvider**"""

    class Meta(object):
        name = 'jks'
        model = JKSSecretProvideConfiguration
        model_parameters = JKSSecretProviderParameter

    _ASN1 = crypto.FILETYPE_ASN1
    _PEM = crypto.FILETYPE_PEM

    keystore = None
    ca_cert = None
    ca_certs = ''
    trusted_certs = None
    client_cert = None
    client_key = None
    p = None

    def new(self, cfg, *args, **kwargs):
        """Method to construct class

        :rtype: JKSSecretProvider
        :param cfg: Provider configuration
        :return: JKSSecretProvider
        """
        super(JKSSecretProvider, self).new(cfg, *args, **kwargs)

        c = self.cfg[0]
        self.keystore = jks.KeyStore.load(
            c['jks_file'],
            c['passphrase']
        )

        return self

    def extract_truststore(self):
        self.trusted_certs = [crypto.load_certificate(self._ASN1, cert.cert)
                              for cert in self.keystore.certs.values()]
        for x in self.trusted_certs:
            ca_cert = crypto.dump_certificate(self._PEM, x)
            self.ca_certs += ca_cert
        self.log.info('Loaded {} authorities'
                      ''.format(len(self.trusted_certs)))

    def extract_client_key(self):
        pk_entry = self.keystore.private_keys[self.p.key_alias]
        if not pk_entry.is_decrypted():
            pk_entry.decrypt(self.p.key_password)

        pkey = crypto.load_privatekey(self._ASN1, pk_entry.pkey)
        cert = crypto.load_certificate(
            self._ASN1,
            pk_entry.cert_chain[0][1]
        )

        self.client_key = crypto.dump_privatekey(self._PEM, pkey)
        self.client_cert = crypto.dump_certificate(self._PEM, cert)

    @property
    @logthis(sensitive=True)
    def value(self):
        """value property

        :rtype:
        :return: Secret value
        """

        self.p = self.parameters[0]

        if self.p.type == 'ca':
            self.extract_truststore()
            return self.ca_certs
        elif self.p.type == 'cert':
            self.log.info('Loading "{}" client certificate'
                          ''.format(self.p.key_alias))
            self.extract_client_key()
            return self.client_cert
        elif self.p.type == 'key':
            self.log.info('Loading "{}" client key'
                          ''.format(self.p.key_alias))
            self.extract_client_key()
            return self.client_key
