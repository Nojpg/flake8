import threading


class DeadlockClass:
    def __init__(self):
        self.lock = threading.Lock()

    def method(self):
        print("Acquiring lock...")
        self.lock.acquire()
        print("Acquiring lock again...")
        self.lock.acquire()
        print("Error")


deadlock_instance = DeadlockClass()
deadlock_instance.method()
