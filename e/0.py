from proxy import Proxy
class A:
    Test0 = 'test0'
    def __init__(self):
        self.test1 = 'test1'
    def test2(self):
        return 'test2'

class B(A):
    pass

b = B()
p = Proxy(b)
print(p.TeSt0)
print(p.TEST1)
print(p.tESt2())
p.tEsT3 = 'test3'
print(b.test3)
try:
    print(b.TEST3)
except:
    print('b.TEST3 not defined')
p.obj = 'obj'
print(b.obj)
p.Test0 = 'TEST0'
print(p.TEst0)
print(b.Test0)
try:
    print(b.test0)
except:
    print('b.test0 not defined')
print(id(b) == id(p.obj))
print(p.obj.test2())
#taki odczyt nie bedzie testowany:
#print(p.obj)
