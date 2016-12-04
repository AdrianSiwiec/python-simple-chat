from meta import Final
class A(object):
    pass
class B(A, metaclass=Final):
    pass
print(isinstance(B, Final))
try:
    class C(B):
        pass
except TypeError:
    print("Cannot inherit from final class")
