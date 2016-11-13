"""
Demonstracja niektórych metod wątków
"""
import threading
import time

class MyThread(threading.Thread):
	def __init__(self, id, iter_number):
		super().__init__(daemon=True)
		self.id = id
		self.iter_number = iter_number
	def run(self):
		while self.iter_number:
			print("Thread:", self.id)
			self.iter_number -= 1
			time.sleep(1)

t1 = MyThread("T1",10)
t2 = MyThread("T2",20)
t1.start()
t2.start()

i = 20
while i:
	time.sleep(0.75)
	print("T1.alive:", t1.is_alive()) #True: miedzy start() a wykonaniem funkcji run wątka
	print("T2.alive:", t2.is_alive())
	i-=1
	"""
	if i == 17:
		t1.join() # watek wznowiony dopiero po zakonczeniu dzialania watku t1
	"""



	