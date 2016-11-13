"""
problem z lockiem: watek posiadajacy lock, na ktorym wykonujemy lock.acquire() 
tez prowadzi do zablokowania watku, co moze prowadzic do zakleszczenia.
Rozwiazaniem jest uzycie threading.RLock (Reentrance Lock).
"""

import threading
import time

lock = threading.Lock()
#lock = threading.RLock()

class MyThread(threading.Thread):
	def __init__(self, id, time_interval):
		super().__init__(daemon=True)
		self.id = id
		self.time_interval = time_interval
	def run(self):
		while True:
			lock.acquire()
			print("Mam locka")
			lock.acquire()
			print("Thread:", self.id)
			time.sleep(self.time_interval)
			lock.release()
			print("Ciagle mam locka")
			time.sleep(10)
			lock.release()
			
t1 = MyThread("Fast",1)
t2 = MyThread("Slow",1)
t1.start()
t2.start()

while True:
	time.sleep(1)
	lock.acquire()
	print("T1.alive:", t1.is_alive()) 
	print("T2.alive:", t2.is_alive())
	lock.release()



	