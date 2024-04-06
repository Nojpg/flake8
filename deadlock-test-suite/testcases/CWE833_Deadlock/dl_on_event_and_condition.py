"""
    thread1 ждет, когда event1 будет установлено.
    После этого он ждет, пока не будет установлено event2. thread2
    сначала устанавливает event2, а затем ждет, пока будет установлено event1.
    После этого он снова ждет, пока не будет
    установлено event2. Последовательность событий приводит к дедлоку: thread1 ждет, пока event1 не будет установлено.
    thread2 устанавливает event2 и затем ждет, пока event1 не будет установлено.
    Однако event1 никогда не будет установлено, потому что thread1 ждет, пока event2 не будет установлено.
    thread1 ждет, пока event2 не будет установлено.
    Но event2 никогда не будет установлено, потому что thread2 также ждет его установки.
"""
import threading

event1 = threading.Event()
event2 = threading.Event()

condition = threading.Condition()


def thread1():
    with condition:
        print("Thread 1: Waiting for event 1")
        event1.wait()
        print("Thread 1: Event 1 occurred, waiting for event 2")
        event2.wait()
        print("Thread 1: Event 2 occurred")


def thread2():
    with condition:
        print("Thread 2: Waiting for event 2")
        event2.set()
        event1.wait()
        print("Thread 2: Event 1 occurred, waiting for event 1")
        event2.wait()
        print("Thread 2: Event 2 occurred")


t1 = threading.Thread(target=thread1)
t2 = threading.Thread(target=thread2)
t1.start()
t2.start()

t1.join()
t2.join()
