import pytest
from contextlib2 import ExitStack as nullcontext
from schematics.exceptions import DataError

from pytest_servicediscovery.models.Services import Address
from pytest_servicediscovery.models.configuration.Configuration import ConfigurationService


@pytest.mark.parametrize(
    ('ip', 'port', 'expected_raises'),
    (
        ('127.0.0.1', 1, nullcontext()),
        ('::1', 1, nullcontext()),
        ('::ffff:0.0.0.0', 1, nullcontext()),
        ('64:ff9b::0.0.0.0', 1, nullcontext()),
        ('ffff:ffff:ffff:ffff:ffff:ffff:ffff:ffff', 1, nullcontext()),
        ('example.com', 1, nullcontext()),
        ('example.test', 1, nullcontext()),
        ('example.example', 1, nullcontext()),
        ('example.invalid', 1, nullcontext()),
        ('example.localhost', 1, nullcontext()),
        ('localhost.localdomain', 1, nullcontext()),

        ('ffff:ffff:ffff:ffff:ffff:ffff:ffff:fffff', 1, pytest.raises(DataError)),
        ('127.0.0.1111', 1, pytest.raises(DataError)),
        ('!example.com', 1, pytest.raises(DataError)),

        ('127.0.0.1', 65536, pytest.raises(DataError)),
        ('::1', 65536, pytest.raises(DataError)),
        ('example.com', 65536, pytest.raises(DataError)),
        ('!example.com', 65536, pytest.raises(DataError)),
        ('localhost.localdomain', 65536, pytest.raises(DataError)),
    ),
)
def address_model_check_servicediscovery(ip, port, expected_raises):
    with expected_raises:
        Address(dict(ip=ip, port=port))


@pytest.mark.parametrize(
    ('name', 'provider', 'expected_raises'),
    (
        ('name', 'null', nullcontext()),
        ('name_underlined', 'null', nullcontext()),
        ('name_with_2underline', 'null', nullcontext()),
        ('name-hyphen', 'null', pytest.raises(DataError)),
        ('name-with-2hyphen', 'null', pytest.raises(DataError)),
    ),
)
def configuration_service_model_check_servicediscovery(name, provider, expected_raises):
    with expected_raises:
        ConfigurationService(dict(name=name, provider=provider, parameters=[], secrets=[]))
