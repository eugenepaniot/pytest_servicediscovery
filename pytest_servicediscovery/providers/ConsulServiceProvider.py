import consul
from hamcrest import assert_that, is_, not_, empty
from schematics.types import StringType, IntType

from pytest_servicediscovery.decorators import logthis, private
from pytest_servicediscovery.models.HealthChecks import HealthChecks, HealthCheck
from pytest_servicediscovery.models.Services import Address
from pytest_servicediscovery.models.configuration.PluginContainerMixin import PluginConfiguration
from pytest_servicediscovery.models.configuration.ProviderContainerMixin import ProviderParameters
from pytest_servicediscovery.models.types import IPAddressOrDomainType
from pytest_servicediscovery.providers.BaseServicePluginProvider import BaseServicePluginProvider


class ConsulServiceProvider(PluginConfiguration):
    """ConsulServiceProvider Model for configuration parameters"""
    ipAddress = IPAddressOrDomainType(required=True)
    port = IntType(min_value=1, max_value=65535, default=8500)
    token = StringType()


class ConsulServiceParameters(ProviderParameters):
    """ConsulServiceParameters Model for input parameters"""
    serviceName = StringType(required=True, min_length=1)
    tag = StringType(default=None, regex='^[a-z0-9_]+$')
    near = StringType(default=None, regex='^[a-z0-9_]+$')


class ConsulServiceProviderClass(BaseServicePluginProvider):
    """**ConsulServiceProviderClass**

        DiscoveryProvider that implement's methods to work with Consul
    """

    class Meta(object):
        name = "consul"
        model = ConsulServiceProvider
        model_parameters = ConsulServiceParameters

    consul = None
    service_name = None
    near = None
    tag = None

    def new(self, cfg, *args, **kwargs):
        """Method to construct class

        :rtype: ConsulServiceProviderClass
        :param cfg: Provider configuration
        :return: ConsulServiceProvider
        """
        super(ConsulServiceProviderClass, self).new(cfg, *args, **kwargs)

        c = self.cfg[0]

        self.consul = consul.Consul(host=c.ipAddress,
                                    port=c.port,
                                    token=c.token,
                                    verify=False)

        return self

    def call(self, parameters):
        super(ConsulServiceProviderClass, self).call(parameters)

        self.service_name = self.parameters[0].get('serviceName')
        self.tag = self.parameters[0].get('tag')

        return self

    @property
    @logthis()
    def service_address(self):
        """Return service_address for the first service in a list

        - Example::

            Address(ip=10.186.106.2, port=8300)

        :return: Address Model
        :rtype: Address
        """
        return self.service_addresses[0]

    @property
    @logthis()
    def service_addresses(self):
        """Return service_addresses for the service

        - Example::

            [
                Address(ip=10.186.106.2, port=8300),
                Address(ip=10.186.106.3, port=8300)
            ]

        :return: tuple of Address Models
        :rtype: tuple
        """

        return tuple(map(lambda p: Address(dict(ip=p['ServiceAddress'] if p['ServiceAddress'] else p['Address'],
                                                port=p['ServicePort'])),
                         self.__get_consul_services()))

    @property
    def service_health_checks(self):
        """Return Service HealthChecks

        - Example::

            HealthChecks(
                checks=[
                    HealthCheck(status=passing, output=Agent alive and reachable, id=serfHealth, name=Serf Health Status),
                    HealthCheck(status=passing, output=Agent alive and reachable, id=serfHealth, name=Serf Health Status),
                    HealthCheck(status=passing, output=Agent alive and reachable, id=serfHealth, name=Serf Health Status)
                ]
            )

        :rtype: HealthChecks
        :return: Service HealthChecks
        """

        def get_health_check_model(checks):
            for hcs in checks:
                for hc in hcs['Checks']:
                    yield HealthCheck(dict(id="%s" % hc['CheckID'],
                                           node="%s" % hc['Node'],
                                           name=hc['Name'],
                                           status=hc['Status'],
                                           output=hc['Output']
                                           ))

        checks = self.__get_consul_service_health()
        if not checks:
            return HealthChecks()

        return HealthChecks(dict(checks=get_health_check_model(checks)))

    @private
    @logthis()
    def __get_consul_services(self, *args, **kwargs):
        """Function returns all entries from service catalog definition for given service

        - Example::

            [
                [
                  {
                    "ID": "0dfaa9e2-a79f-8c61-3e6c-59352d1c8b9c",
                    "Node": "ip-172.22.1.93.eu-west-1.compute.internalaws.griddynamics.netvm",
                    "Address": "172.22.1.93",
                    "Datacenter": "dc1",
                    "TaggedAddresses": {
                      "lan": "172.22.1.93",
                      "wan": "172.22.1.93"
                    },
                    "NodeMeta": {
                      "consul-network-segment": ""
                    },
                    "ServiceKind": "",
                    "ServiceID": "zookeeper",
                    "ServiceName": "zookeeper",
                    "ServiceTags": [],
                    "ServiceAddress": "",
                    "ServiceWeights": {
                      "Passing": 1,
                      "Warning": 1
                    },
                    "ServiceMeta": {},
                    "ServicePort": 2181,
                    "ServiceEnableTagOverride": false,
                    "ServiceProxyDestination": "",
                    "ServiceProxy": {},
                    "ServiceConnect": {},
                    "CreateIndex": 22044,
                    "ModifyIndex": 22044
                  }
                ]
            ]

        :rtype: list
        :param service:
        :param args:
        :param kwargs:
        :return: Full service definition from consul service catalog
        """

        index, data = self.consul.catalog.service(service=self.service_name, tag=self.tag, near=self.near,
                                                  *args, **kwargs)
        assert_that(data, is_(not_(empty())), "Consul service discovery response should not be empty")

        return data

    @private
    @logthis()
    def __get_consul_service_health(self, *args, **kwargs):
        """Function returns all entries from service health catalog definition for given service

        - Example::

            [
              {
                "Node": {
                  "ID": "40e4a748-2192-161a-0510-9bf59fe950b5",
                  "Node": "foobar",
                  "Address": "10.1.10.12",
                  "Datacenter": "dc1",
                  "TaggedAddresses": {
                    "lan": "10.1.10.12",
                    "wan": "10.1.10.12"
                  },
                  "Meta": {
                    "instance_type": "t2.medium"
                  }
                },
                "Service": {
                  "ID": "redis",
                  "Service": "redis",
                  "Tags": ["primary"],
                  "Address": "10.1.10.12",
                  "Meta": {
                    "redis_version": "4.0"
                  },
                  "Port": 8000,
                  "Weights": {
                    "Passing": 10,
                    "Warning": 1
                  }
                },
                "Checks": [
                  {
                    "Node": "foobar",
                    "CheckID": "service:redis",
                    "Name": "Service 'redis' check",
                    "Status": "passing",
                    "Notes": "",
                    "Output": "",
                    "ServiceID": "redis",
                    "ServiceName": "redis",
                    "ServiceTags": ["primary"]
                  },
                  {
                    "Node": "foobar",
                    "CheckID": "serfHealth",
                    "Name": "Serf Health Status",
                    "Status": "passing",
                    "Notes": "",
                    "Output": "",
                    "ServiceID": "",
                    "ServiceName": "",
                    "ServiceTags": []
                  }
                ]
              }
            ]

        :param service:
        :return:
        :param args:
        :param kwargs:
        :return: Full service definition in consul health service catalog
        """
        index, data = self.consul.health.service(service=self.service_name, tag=self.tag, near=self.near,
                                                 *args, **kwargs)
        assert_that(data, is_(not_(empty())), "Consul service health checks discovery response should not be empty")

        return data
