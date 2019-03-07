from hamcrest import assert_that, is_, instance_of
from schematics.exceptions import ValidationError
from schematics.types import StringType, DictType

import validators

from pytest_servicediscovery.exceptions import DuplicateSecret, SecretNotFoundException


class IPAddressOrDomainType(StringType):
    """A field that stores a valid IPv4 or IPv6 address or Domain Name"""

    whitelist = ['localhost']

    def validate_(self, value, context=None):
        if any(value == w for w in self.whitelist):
            return

        if not validators.ip_address.ipv4(value) \
                and not validators.ip_address.ipv6(value) \
                and not validators.domain(value):
            raise ValidationError('Invalid value: "%s"' % value)


class Secrets(dict):
    """This doesn't work as expected"""
    def __setitem__(self, key, value):
        if key in self:
            raise DuplicateSecret(key)

        assert_that(value, is_(instance_of(unicode)), "The secret '%s' has unicode typed value" % key)

        super(Secrets, self).__setitem__(key, value)

    def __getattr__(self, item):
        return self[item]

    def __getitem__(self, key):
        if key in self.keys():
            return dict.__getitem__(self, key)
        else:
            raise SecretNotFoundException(key)


class SecretsType(DictType):
    """This doesn't work as expected"""
    primitive_type = Secrets
    native_type = Secrets
