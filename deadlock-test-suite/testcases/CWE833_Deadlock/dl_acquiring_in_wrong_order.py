"""
    Создаются два объекта Lock - lock1 и lock2.
    Создаются два процесса:
        process1 вызывает функцию task с аргументами 1, lock1 и lock2.
        process2 вызывает функцию task с аргументами 2, lock2 и lock1.
    Каждый процесс пытается захватить блокировки в разном порядке:
        process1 пытается сначала захватить lock1, а затем lock2.
        process2 пытается сначала захватить lock2, а затем lock1.
    После захвата каждой блокировки процесс ждет 1 секунду (используя функцию sleep(1)),
    чтобы имитировать длительную операцию.
    Если блокировки захвачены в неправильном порядке, то возможен случай, когда process1 захватывает lock1,
    а затем пытается захватить lock2, в то время как process2 уже захватил lock2 и пытается захватить lock1.
    Это приводит к взаимоблокировке, когда каждый процесс ожидает освобождения блокировки, которая захвачена
    другим процессом, и выполнение обоих процессов приостанавливается навсегда.
"""

from time import sleep
from multiprocessing import Process
from multiprocessing import Lock


def task(number, lock1, lock2):
    print(f'Process {number} acquiring lock 1...', flush=True)
    with lock1:
        sleep(1)
        print(f'Process {number} acquiring lock 2...', flush=True)
        with lock2:
            pass


if __name__ == '__main__':
    lock1 = Lock()
    lock2 = Lock()
    process1 = Process(target=task, args=(1, lock1, lock2))
    process2 = Process(target=task, args=(2, lock2, lock1))
    process1.start()
    process2.start()
    process1.join()
    process2.join()
