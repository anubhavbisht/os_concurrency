import threading

class MyCondition:
    def __init__(self, lock=None):
        self.lock = lock or threading.Lock()
        self.waiting = []  

    def acquire(self):
        self.lock.acquire()
    
    def release(self):
        self.lock.release()

    def wait(self):
        event = threading.Event()
        self.waiting.append(event)
        self.release()
        event.wait()   # Block here
        self.acquire()

    def notify(self):
        if self.waiting:
            event = self.waiting.pop(0)
            event.set()   # Wake up one waiting thread

    def notify_all(self):
        for event in self.waiting:
            event.set()
        self.waiting.clear()

    def __enter__(self):
        self.acquire()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.release()

# Testing
cond = MyCondition()

def worker(i):
    with cond:
        print(f"Thread {i} waiting")
        cond.wait()
        print(f"Thread {i} resumed")

threads = [threading.Thread(target=worker, args=(i,)) for i in range(3)]
for t in threads:
    t.start()

threading.Event().wait(2)  # simulate delay
print("Main thread notifying all")
with cond:
    cond.notify_all()

for t in threads:
    t.join()
