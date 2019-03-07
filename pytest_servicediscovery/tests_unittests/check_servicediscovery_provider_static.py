import pytest
import yaml
from hamcrest import assert_that, equal_to

from pytest_servicediscovery.factories.ConfiguationFactories import ConfiguationFactory
from pytest_servicediscovery.models.Services import Address
from pytest_servicediscovery.plugin import Parameters
from pytest_servicediscovery.providers.StaticServiceProvider import StaticServiceProviderClass


@pytest.mark.parametrize(
    'cfg', [
        pytest.param(yaml.load("""
                            discovery:
                              providers:
                                - name: static
                                  plugin: static
                                  parameters:
                                    - ip: localhost
                                      port: 1

                                    - ip: localhost
                                      port: 2
                            """)
                     )
    ]
)
def provider_static_verify_cfg_check_servicediscovery(cfg):
    cfg_providers = ConfiguationFactory.build(configuration=dict(providers=cfg['discovery']
                                                                 .get('providers', dict()))
                                              )['providers']

    ps = StaticServiceProviderClass().new(
        cfg=cfg_providers[0].parameters, name=cfg_providers[0].name
    ).call(parameters=Parameters())

    assert_that(ps.service_address, equal_to(
        Address(
            dict(ip='localhost', port=1)
        )
    ))

    assert_that(ps.service_addresses[0], equal_to(
        Address(
            dict(ip='localhost', port=1)
        )
    ))

    assert_that(ps.service_addresses[1], equal_to(
        Address(
            dict(ip='localhost', port=2)
        )
    ))
