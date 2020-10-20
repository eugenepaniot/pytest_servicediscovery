import logging
import os
import pkgutil
import pprint
import warnings

import pytest
import yaml
from pytest_factoryboy import register

import pytest_servicediscovery
from pytest_servicediscovery.exceptions import DuplicateFixture, WrongConfiguration
from pytest_servicediscovery.factories.ConfiguationFactories import ConfiguationFactory
from pytest_servicediscovery.factories.Fixtures import ServiceFixtureFactory

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

registered_services = dict()

warnings.filterwarnings("ignore", category=DeprecationWarning)


class Iters(object):
    def __str__(self):
        return repr(self)

    def __repr__(self):
        model = self.__class__.__name__

        return "{}({})".format(model, pprint.pformat(self.it, indent=0))

    def __init__(self, it=None, *args, **kwargs):
        if it is None:
            self.it = []
        else:
            self.it = next(iter(it))

            if self.it is None:
                self.it = []

        super(Iters, self).__init__(*args, **kwargs)

    def __getitem__(self, idx):
        return self.it[idx]

    def __len__(self):
        return len(self.it)


class Parameters(Iters):
    pass


class Cfg(Iters):
    pass


def pytest_configure(config):
    log2 = logging.getLogger(pytest_configure.__name__)
    log2.addHandler(logging.StreamHandler())
    log2.setLevel(logging.DEBUG)

    for loader, module_name, is_pkg in pkgutil.walk_packages(pytest_servicediscovery.__path__,
                                                             pytest_servicediscovery.__name__ + '.'):
        if is_pkg:
            continue

        if not module_name.startswith(pytest_servicediscovery.__name__ + '.providers.') \
                or ".Base" in module_name:
            continue

        log2.info("Loading module \"%s\"" % module_name)
        loader.find_module(module_name).load_module(module_name)


def fixture_register(svcs):
    if svcs['name'] in globals():
        raise DuplicateFixture(svcs['name'])

    log.info("Inspecting \"%s\" fixture" % svcs['name'])

    _service = svcs['_ConfigurationService__service']

    register(ServiceFixtureFactory, svcs['name'],
             name=svcs['name'],
             address=_service.address,
             addresses=_service.addresses,
             health_checks=_service.health_checks,
             secrets=_service.secrets
             )

    registered_services[svcs['name']] = _service
    log.info("Fixture \"%s\" successfully registered" % svcs['name'])


@pytest.hookimpl
def pytest_sessionstart(session):
    try:
        if not os.path.isfile("./services.yaml"):
            log.warning("Configuration file services.yaml not found")
            return

        if not os.access("./services.yaml", os.R_OK):
            log.warning("Configuration file services.yaml is not readable")
            return
        with open("services.yaml", 'r') as stream:
            configuration = yaml.load(stream)

            if not configuration:
                raise WrongConfiguration('Empty configuration')

            if 'discovery' not in configuration:
                raise WrongConfiguration('"discovery" key not found in configuration')

            cfg = ConfiguationFactory.build(configuration=configuration['discovery'])

            for svcs_index, svcs in enumerate(cfg['services']):
                fixture_register(svcs)

    except Exception as e:
        pytest.exit(e.message)


def pytest_generate_tests(metafunc):
    if '_TestBasicServiceDiscovery__service' in metafunc.fixturenames:
        metafunc.parametrize("_TestBasicServiceDiscovery__service",
                             registered_services.values(),
                             ids=registered_services.keys()
                             )
