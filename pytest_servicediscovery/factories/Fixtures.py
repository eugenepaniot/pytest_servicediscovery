import logging
import factory

from pytest_servicediscovery.models.Services import ServiceFixture


class ServiceFixtureFactory(factory.Factory):
    class Meta(object):
        model = ServiceFixture

    name = None
    secrets = dict()
    address = dict()
    addresses = list()
    health_checks = dict()

    @factory.post_generation
    def post(svc, *args, **kwargs):
        log = logging.getLogger(__name__)
        log.setLevel(logging.INFO)

        log.info("Fixture \"%s\" requested" % svc.name)
