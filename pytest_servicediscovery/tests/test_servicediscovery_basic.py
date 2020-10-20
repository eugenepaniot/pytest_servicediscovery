# """
# **To execute plugin tests, just add following options to the py.test command:**
#
# ```
# --pyargs pytest_servicediscovery.tests
# ```
#
# """
import logging
import allure
from hamcrest import assert_that, equal_to_ignoring_case

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


@allure.epic('Basic checks')
@allure.title("Basic checks in Service Discover")
@allure.feature("Basic checks feature")
class TestBasicServiceDiscovery(object):
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Test if service has all health-checks passed")
    def test_service_health_checks(self, __service):
        """
        Test if given service has all health-checks passed
        """
        for check in __service.health_checks['checks']:
            with allure.step('Testing health-check "%s" for "%s" fixture on "%s" node' % (check.id,
                                                                                          __service['name'],
                                                                                          check.node)):

                log.info('Health check "%s", status "%s" : %s' % (check.id, check.status, check.output))
                assert_that(check.status, equal_to_ignoring_case('passing'), "Service check should be passed")
