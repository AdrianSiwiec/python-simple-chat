class Singleton(type):

    _instances = {}

    def __call__(cls, *args, **kwargs):
        if (Singleton._instances.get(cls) == None):
            Singleton._instances[cls] = super().__call__(*args, **kwargs)
        return Singleton._instances[cls]


class Final(type):

    def __init__(self, cls, fathers, *args, **kwargs):
        for c in fathers:
            if (isinstance(c, Final)):
                raise TypeError


#class S(metaclass = Final):
#    pass
#
#
#class A(S, metaclass = Final):
#
#    def __init__(self, n):
#        self.n = n
