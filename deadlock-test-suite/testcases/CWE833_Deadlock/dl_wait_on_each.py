"""
    Создается главный процесс.
    Создается дочерний процесс, который выполняет функцию task.
    Главный процесс вызывает join() для дочернего процесса, что означает, что он будет ждать,
    пока дочерний процесс не завершится.
    В функции task дочерний процесс вызывает current_process() и parent_process() для получения текущего процесса и его
    родителя соответственно.
    Дочерний процесс печатает информацию о текущем процессе и его родителе, а затем вызывает join() для
    родительского процесса (то есть главного процесса в данном случае).
    Главный процесс также печатает информацию о текущем процессе и ожидает завершения дочернего процесса
    с помощью join().
"""
from multiprocessing import parent_process
from multiprocessing import current_process
from multiprocessing import Process


def task():
    current = current_process()
    parent = parent_process()
    print(f'[{current.name}] waiting on [{parent.name}]...', flush=True)
    parent.join()


if __name__ == '__main__':
    current = current_process()
    child = Process(target=task)
    child.start()
    print(f'[{current.name}] waiting on [{child.name}]...', flush=True)
    child.join()
