from queue import Queue


def _attrOrCallable(obj, atr):
    if (callable(atr)):

        def f(*args, **kwargs):
            return atr(obj, *args, **kwargs)

        return f
    return atr


class MRO:

    def __init__(self, obj):
        self.obj = obj

    def __getattr__(self, attr):
        q = Queue()

        for i in self.obj.__dict__:
            if (i == attr):
                return _attrOrCallable(self.obj, getattr(self.obj, attr))

        q.put(self.obj.__class__)

        while (not q.empty()):
            cls = q.get()

#            print(cls)

            for i in reversed(cls.__bases__):
                q.put(i)

            for i in cls.__dict__:
#                print("    ", end = "", flush = True)
#                print(i)
                if (i == attr):
                    return _attrOrCallable(self.obj, getattr(cls, attr))
        return _attrOrCallable(self.obj, getattr(self.obj, attr))
