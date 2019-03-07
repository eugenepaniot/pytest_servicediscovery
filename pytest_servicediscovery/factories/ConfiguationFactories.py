import factory

from pytest_servicediscovery.models.configuration.Configuration import Configuration


class ConfiguationFactory(factory.Factory):
    class Meta(object):
        model = Configuration

    configuration = None
