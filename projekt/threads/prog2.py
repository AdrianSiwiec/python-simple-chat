"""
Druga metoda tworzenia wątków:
-- tworzymy obiekt typu Thread, w konstruktorze podajemy keyword argument target,
sam przekazywany argument musi byc obiektem callable
-- keyword-arguments konstruktora Thread args i kwargs pozwalaja przekazac do wywolywanego
obiektu wskazanego przez target listę argumentów i keyword argumentów.
"""
import threading
import time


def f1(x):
    while True:
        print(x)
        time.sleep(1)


def f2(thread_name):
    while True:
        print(thread_name)
        time.sleep(0.75)


threading.Thread(target=f1, args=("T1",)).start()
threading.Thread(target=f2, kwargs={"thread_name": "T2"}).start()
