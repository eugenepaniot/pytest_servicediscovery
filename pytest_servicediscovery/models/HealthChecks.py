from schematics.types import StringType, ModelType, ListType

from pytest_servicediscovery.models.Base import Model


class HealthCheck(Model):
    id = StringType(required=True)
    node = StringType(required=True)
    name = StringType(required=True)
    status = StringType(required=True, choices=['unknown', 'passing', 'warning', 'critical'])
    output = StringType(required=True)


class HealthChecks(Model):
    checks = ListType(ModelType(HealthCheck), default=[])
