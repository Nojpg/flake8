"""
Дедлок возникает, когда поток thread1 захватывает блокировку lock, а затем ждет события, которое должно
установиться в потоке thread2. Однако поток thread2 не может установить событие, пока не захватит ту же блокировку
lock, на которую ожидает поток thread1. Оба потока блокируются и ждут, что приводит к дедлоку.
"""

import threading

lock = threading.Lock()
event = threading.Event()


def thread1():
    with lock:
        event.wait()


def thread2():
    with lock:
        event.set()


t1 = threading.Thread(target=thread1)
t2 = threading.Thread(target=thread2)

t1.start()
t2.start()

t1.join()
t2.join()
