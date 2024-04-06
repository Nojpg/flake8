"""
    Когда процесс пытается захватить блокировку дважды вложенно с помощью конструкции with lock:, вторая попытка
    захвата блокировки приводит к возникновению исключения RuntimeError, и выполнение процесса прерывается.
"""

from multiprocessing import Process
from multiprocessing import Lock


def task(lock):
    print('Process acquiring lock...', flush=True)
    with lock:
        print('Process acquiring lock again...', flush=True)
        with lock:
            pass


if __name__ == '__main__':
    lock = Lock()
    process = Process(target=task, args=(lock,))
    process.start()
    process.join()
