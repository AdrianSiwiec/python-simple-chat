from private import Private 

@Private('data', 'size')
class Doubler:
	def __init__(self, label, start):
		self.label = label
		self.data = start
	
	def size(self):
		return len(self.data)
	
	def double(self):
		for i in range(self.size()):
			self.data[i] = self.data[i]*2
			
	def display(self):
		print("%s => %s" % (self.label, self.data))


X = Doubler('X to ', [1,2,3])
Y = Doubler('Y to ', [-10, -20, -30])


print(X.label)
X.display()
X.double()
X.display()
print(Y.label)
Y.display()
Y.label = "mielonka"
Y.display()
Y.double()
Y.display()

try:
	print(X.size())
except TypeError as e:
	print(e)
