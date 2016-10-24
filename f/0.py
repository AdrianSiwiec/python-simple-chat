from mro import MRO


class A:
    a = "a"


class B(A):

    def f(self):
        print("f in B")

    def g():
        print("g in B")

    def h(self, times):
        print(self.d * times)


class C(A):

    def f(self):
        print("f in C")


class D(B, C):

    def __init__(self, d):
        self.d = d


d = D("d")
m = MRO(d)
try:
    print(m.a)
    print(m.d)
    d.f()
    m.f()
    m.h(4)
except AttributeError:
    print("AttributeError")
try:
    m.dom
except AttributeError:
    print("AttributeError")
try:
    d.g()
except TypeError:
    print("TypeError")
try:
    m.g()
except TypeError:
    print("TypeError")
