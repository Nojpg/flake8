"""
    Каждый поток захватывает замок с помощью with condition, после чего вызывает wait(). Вызов wait() блокирует поток
    до тех пор, пока другой поток не вызовет notify() или notify_all() на том же объекте условия.
    Оба потока вызывают condition.acquire() после condition.wait(), что пытается захватить замок второй раз. Однако,
    после вызова wait(), замок уже захвачен, и потоки не могут продолжить выполнение до тех пор, пока замок не будет
    освобожден.
"""

import threading

condition = threading.Condition()


def thread1():
    with condition:
        print("Thread 1: Acquiring lock")
        condition.wait()
        print("Thread 1: Released lock")
        condition.acquire()
        print("Thread 1: Acquired lock again")


def thread2():
    with condition:
        print("Thread 2: Acquiring lock")
        condition.wait()
        print("Thread 2: Released lock")
        condition.acquire()
        print("Thread 2: Acquired lock again")


t1 = threading.Thread(target=thread1)
t2 = threading.Thread(target=thread2)
t1.start()
t2.start()

t1.join()
t2.join()
