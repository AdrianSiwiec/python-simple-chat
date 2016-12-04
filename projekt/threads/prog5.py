"""
manager kontekstu: with lock
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
            with lock:
                print("Thread:", self.id)
                raise Exception("Ex")
                time.sleep(self.time_interval)


t1 = MyThread("Fast", 0.5)
t2 = MyThread("Slow", 1)
t1.start()
t2.start()

while True:
    time.sleep(0.6)
    lock.acquire()
    print("T1.alive:", t1.is_alive())
    print("T2.alive:", t2.is_alive())
    lock.release()
