def _attrOrCallable(obj, atr):
    if (callable(atr)):
        def f(*args, **kwargs):
            return atr(obj, *args, **kwargs)
        
        return f;
    return atr


class Proxy:

    def __init__(self, obj):
        object.__setattr__(self, "obj", obj)

    def __getattr__(self, attr):
        for i in self.obj.__dict__:
            if (i.lower() == attr.lower()):
                return object.__getattribute__(self.obj, i)
#                ret = getattr(self.obj, i)
#                return _attrOrCallable(self.obj, ret)
#                return ret

        for cls in self.obj.__class__.__mro__:
            for i in cls.__dict__:
                if (i.lower() == attr.lower()):
                    return object.__getattribute__(self.obj, i)
#                    ret = getattr(cls, i)
#                    return _attrOrCallable(self.obj, ret)
#                    return ret

        return 42

    def __setattr__(self, attr, val):
        for i in self.obj.__dict__:
            if (i.lower() == attr.lower()):
                self.obj.__dict__[i] = val
#                self.obj.__setattr__(i, val)
                return

        for cls in self.obj.__class__.__mro__:
            for i in cls.__dict__:
                if (i.lower() == attr.lower()):
                    self.obj.__dict__[i] = val
#                    setattr(cls, i, val)
                    return

        object.__setattr__(self.obj, attr.lower(), val)
