class inst:

    def __init__(self, cls):
        self.cls = cls
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        return self.cls(*args, **kwargs)

    def __getattr__(self, attr):
        return getattr(self.cls, attr)

    def numOfInst(self):
        print("Liczba instancji klasy {}: {}".format(self.cls.__name__, self.count))

#@inst
#class A:
#
#    def __init__(self, name, job = "none"):
#        self.name = name
#        self.job = job
#
#    def show(self, *args, **kwargs):
#        print("show", args, kwargs)
#
#    def __str__(self):
#        return "Person: {}, job: {}".format(self.name, self.job)
#
#a = A("a", job = "manager")
#aa = A("aa")
#print(a)
#print(aa)
#A.numOfInst()
#a.show("ok", ok = "OK")
#A.show(a, "ok")
#
#class C:
#
#    def f(self):
#        print(self.a)
#
#@inst
#class D(C):
#
#    def __init__(self, a):
#        self.a = a
#
#    def __str__(self):
#        return str(self.a)
#
#d = D("d")
#d = D("h")
#d.f()
#D.f(d)
#print(d)
#D.numOfInst()
