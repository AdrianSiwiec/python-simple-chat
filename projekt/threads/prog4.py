"""
Demonstracja działania threading.Lock(); 
niebezpieczenstwo deadlocku (wątek otrzymuje locka a następnie go nie zwalnia, bo np. rzucony zostaje wyjatek)
"""
import threading
import time

lock = threading.Lock()

class MyThread(threading.Thread):
	def __init__(self, id, time_interval):
		super().__init__(daemon=True)
		self.id = id
		self.time_interval = time_interval
	def run(self):
		while True:
			try:
				lock.acquire()
				print("Thread:", self.id)
				raise Exception()
				print("Thread:", self.id)
				lock.release()
				time.sleep(self.time_interval)
			except Exception as e:
				print(type(e))

t1 = MyThread("Fast",0.5)
t2 = MyThread("Slow",1)
t1.start()
t2.start()

while True:
	time.sleep(0.6)
	lock.acquire()
	print("T1.alive:", t1.is_alive()) 
	print("T2.alive:", t2.is_alive())
	lock.release()



	