from threading import Thread, Event, Lock, Condition


class MySemaphore:
    def __init__(self, count):
        self.counter = count
        self.lock = Lock()
        self.condition = Condition(self.lock)

    def acquire(self):
        with self.condition:
            while self.counter == 0:
                self.condition.wait()
            self.counter -= 1

    def release(self):
        with self.condition:
            self.counter += 1
            self.condition.notify()


sem = MySemaphore(2)


def worker(i):
    print(f"Worker {i} trying to acquire semaphore")
    sem.acquire()
    print(f"Worker {i} acquired semaphore")
    Event().wait(1)
    sem.release()
    print(f"Worker {i} released semaphore")


threads = [(Thread(target=worker, args=(i,))) for i in range(5)]
for t in threads: t.start()
for t in threads: t.join()