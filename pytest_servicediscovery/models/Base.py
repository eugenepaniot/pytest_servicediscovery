import logging
import schematics


class Model(schematics.models.Model):
    def __init__(self, *args, **kwargs):
        self.log = logging.getLogger(__name__)
        self.log.setLevel(logging.DEBUG)

        super(Model, self).__init__(strict=True, validate=True, *args, **kwargs)

    def __str__(self):
        return repr(self)

    def __repr__(self):
        model = self.__class__.__name__
        info = self._repr_info()

        if info:
            return '<%s: %s>' % (model, info)
        else:
            if hasattr(self, "_data"):
                __ = ", ".join(["{}={}".format(k, v) for k, v in self._data.items()])
            elif hasattr(self, "to_primitive"):
                __ = self.to_primitive()
            else:
                setattr(self, '_data', dict())
                __ = ", ".join(["{}={}".format(k, v) for k, v in self.items()])

            return "\n{}({})".format(model, __)
