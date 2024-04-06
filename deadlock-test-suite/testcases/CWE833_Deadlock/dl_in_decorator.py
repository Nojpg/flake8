import threading


def deadlock_decorator(func):
    lock = threading.Lock()

    def wrapper():
        print("Acquiring lock...")
        lock.acquire()
        print("Acquiring lock again...")
        lock.acquire()
        print("Error")
        return func()

    return wrapper


@deadlock_decorator
def deadlock_function():
    raise Exception('Something bad happened')


deadlock_function()
