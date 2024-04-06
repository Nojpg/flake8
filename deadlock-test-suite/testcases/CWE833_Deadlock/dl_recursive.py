"""
    Блокировка захватывается перед вызовом recursive_deadlock_function, а затем пытается захватиться снова внутри
    каждого рекурсивного вызова функции. Дедлок возникает, если блокировка не будет освобождена перед
    следующим рекурсивным вызовом.
"""

import threading

def recursive_deadlock_function(lock, depth):
    if depth > 0:
        print(f"Thread acquiring the lock. Depth: {depth}")
        with lock:
            recursive_deadlock_function(lock, depth - 1)
    else:
        print("Base case reached.")

lock = threading.Lock()


with lock:
    recursive_deadlock_function(lock, 3)
