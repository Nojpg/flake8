"""
    Cоздается объект Lock.
    Запускается новый процесс с функцией task, которая пытается захватить замок, затем вызывает исключение,
    и после этого пытается освободить замок (что никогда не произойдет из-за исключения).
    Главный процесс ожидает 1 секунду.
    Главный процесс пытается захватить тот же замок, который уже захвачен в дочернем процессе.
"""

from time import sleep
from multiprocessing import Process
from multiprocessing import Lock


def task(lock):
    print('Process acquiring lock...', flush=True)
    lock.acquire()
    raise Exception('Something bad happened')
    print('Process releasing lock...', flush=True)
    lock.release()


if __name__ == '__main__':
    lock = Lock()
    process = Process(target=task, args=(lock,))
    process.start()
    sleep(1)
    print('Main acquiring lock...')
    lock.acquire()
    lock.release()
