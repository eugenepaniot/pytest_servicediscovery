from schematics.types import IntType, StringType, ModelType, ListType

from pytest_servicediscovery.models.Base import Model
from pytest_servicediscovery.models.HealthChecks import HealthChecks

from pytest_servicediscovery.models.types import IPAddressOrDomainType, SecretsType


class Address(Model):
    ip = IPAddressOrDomainType()
    port = IntType(min_value=1, max_value=65535)


class Service(Model):
    name = StringType(required=True)
    address = ModelType(Address, required=True)
    addresses = ListType(ModelType(Address), required=True)
    secrets = SecretsType(StringType, )
    health_checks = ModelType(HealthChecks)


class ServiceFixture(Service):
    def __init__(self, name, address, addresses, secrets, health_checks, *args, **kwargs):
        super(ServiceFixture, self).__init__(*args, **kwargs)

        self.name = name
        self.address = address
        self.addresses = addresses
        self.health_checks = health_checks
        self.secrets = secrets

        self.validate()
