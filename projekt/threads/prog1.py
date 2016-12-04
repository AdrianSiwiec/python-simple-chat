"""
Pierwsza metoda tworzenia wątków: dziedziczymy po klasie Thread z modułu threading.
Aby dostac watek, musimy wywołać konstruktor klasy Thread.
Kazdy watek uruchamiamy metodą .start()
"""
import threading


class MyThread(threading.Thread):
    def __init__(self, id):
        super().__init__(daemon=False)
        # deamon=TRue: watek-demon konczy swoje dzialanie z chwila, kiedy konczy dzialanie watek glowny
        self.id = id

    def run(self):
        while True:
            print(self.id)


t1 = MyThread("T1")
t2 = MyThread("T2")
t1.start()
t2.start()

while True:
    print("Main Thread")
