"""
Producer - Consumer: Condition variable object
"""
import threading
import time
import random


class Q:
    def __init__(self):
        self.queue = []
        self.cond = threading.Condition()  # condition obiekt (będziemy na nim osadzać sekcję krytyczną)

    def push(self, x):
        self.queue.append(x)

    def pop(self):
        ret = self.queue[0]
        del self.queue[0]
        return ret

    def empty(self):
        return len(self.queue) == 0


q = Q()
x = 0


class Producer(threading.Thread):
    def __init__(self, name, time_interval=0):
        super().__init__(daemon=True)
        self.name = name
        self.time_interval = True

    def run(self):
        while True:
            with q.cond:  # jezeli lock wolny, watek wchodzi w sekcje krytyczna
                if random.randint(1, 3) == 1:
                    global x
                    q.push(x)
                    print(self.name + ": dodal element:", x)
                    x += 1
                    q.cond.notifyAll()  # obudzenie pozostałych watkow, ktore zostalu zawieszone metoda q.cond.wait()
            time.sleep(self.time_interval)


class Consumer(threading.Thread):
    def __init__(self, name, time_interval=0):
        super().__init__(daemon=True)
        self.name = name
        self.time_interval = time_interval

    def run(self):
        while True:
            with q.cond:
                while q.empty():
                    print(self.name + ": nothing to eat")
                    q.cond.wait()  # kolejka pusta, wątek zawieszony na obiekcie q.cond
                print(self.name + " is consuming:", q.pop())
                """
                q.cond.notify()
                q.cond.wait()
                """
            time.sleep(self.time_interval)


Producer("Producer 1", 1).start()
Consumer("Consumer 1", 1).start()
Consumer("Consumer 2", 1).start()
Consumer("Consumer 3", 1).start()

while True:
    pass
