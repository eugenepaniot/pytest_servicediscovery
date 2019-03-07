class WrongConfiguration(ValueError):
    pass


class WrongImplementation(ValueError):
    pass


class UnexpectedBehavior(Exception):
    pass


class ProviderNotFoundException(WrongConfiguration):
    def __init__(self, message):
        message = "\"%s\" provider cannot be found, it may not be properly configured in the configuration" % message
        super(ProviderNotFoundException, self).__init__(message)


class SecretNotFoundException(WrongConfiguration):
    def __init__(self, message):
        message = "\"%s\" secret cannot be found, it may not be properly configured in the configuration" % message
        super(SecretNotFoundException, self).__init__(message)


class DuplicateProvider(WrongConfiguration):
    def __init__(self, message):
        message = "Provider \"%s\" already registered" % (message)
        super(DuplicateProvider, self).__init__(message)


class DuplicateSecret(WrongConfiguration):
    def __init__(self, message):
        message = "Secret \"%s\" already exists" % (message)
        super(DuplicateSecret, self).__init__(message)


class DuplicateFixture(WrongConfiguration):
    def __init__(self, message):
        message = "Service fixture \"%s\" is already registered" % message
        super(DuplicateFixture, self).__init__(message)
