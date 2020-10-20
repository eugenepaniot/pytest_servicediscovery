import inspect
import logging


def logthis(level=None, sensitive=False):
    log = logging.getLogger(__name__)
    if not level:
        level = logging.DEBUG

    def _decorator(fn):
        def _decorated(*arg, **kwargs):
            def crop_sensitive_data(value, ratio):
                length = max(len(value) * ratio, 1)
                return value[:int(length)] + '*** SENSITIVE ***' + value[-int(length):] \
                    if sensitive else value

            ret = fn(*arg, **kwargs)
            log.log(level,
                    "Called function '%s.%s(arg=%r, kwargs=%r), got return value: %r",
                    fn.__module__, fn.__name__, arg, kwargs, crop_sensitive_data(ret, 0.1))

            return ret
        return _decorated
    return _decorator


def private(method):
    class_name = inspect.stack()[1][3]

    def privatized_method(*args, **kwargs):
        call_frame = inspect.stack()[1][0]

        # Only methods of same class should be able to call
        # private methods of the class, and no one else.
        if 'self' in call_frame.f_locals:
            caller_class_name = call_frame.f_locals['self'].__class__.__name__
            if caller_class_name == class_name:
                return method(*args, **kwargs)
        raise Exception("can't call private method")

    return privatized_method
