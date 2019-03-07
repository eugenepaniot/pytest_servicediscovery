import pytest
import yaml
from contextlib2 import ExitStack as nullcontext
from hamcrest import assert_that, equal_to

from pytest_servicediscovery.factories.ConfiguationFactories import ConfiguationFactory
from pytest_servicediscovery.providers import ProviderManager


@pytest.mark.parametrize(
    'svc', [
        pytest.param(yaml.load("""
                            secrets:
                              - name: secret1
                                provider: plaintext
                                parameters:
                                  - value: secret1

                              - name: secret2
                                provider: plaintext
                                parameters:
                                  - value: secret2
                            """)
                     )
    ]
)
def plaintext_secrets_check_servicediscovery(svc):
    secrets = {}
    for secret in svc["secrets"]:
        secrets[secret['name']] = ProviderManager.plugins[secret['provider']].call(
            parameters=secret['parameters'],
        ).value

    assert_that(secrets['secret1'], equal_to("secret1"))
    assert_that(secrets['secret2'], equal_to("secret2"))


def secrets_access_check_servicediscovery():
    configuration = yaml.load("""
                    discovery:
                      providers:
                        - name: static_secrets_access_check_servicediscovery
                          plugin: static
                          parameters:
                            - ip: localhost
                              port: 1
                        
                        - name: plaintext
                          plugin: plaintext
                          
                      services:
                        - name: test
                          provider: static_secrets_access_check_servicediscovery
                          parameters: []
                          
                          secrets:
                            - name: secret1
                              provider: plaintext
                              parameters:
                                - value: secret1
                    """)

    cfg = ConfiguationFactory.create(configuration=configuration['discovery'])

    for svcs_index, svc in enumerate(cfg['services']):
        _service = svc['_ConfigurationService__service']

        with nullcontext():
            assert_that(_service['secrets']['secret1'], equal_to("secret1"))

        with pytest.raises(KeyError):
            assert_that(_service['secrets']['secret2'])
