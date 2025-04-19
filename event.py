import threading

class MyEvent:
    def __init__(self):
        self.flag = False
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)
    
    def wait(self):
        with self.condition:
            while not self.flag:
                self.condition.wait()
    
    def set(self):
        with self.condition:
            self.flag = True
            self.condition.notify_all()
    
    def clear(self):
        with self.condition:
            self.flag = False

event = MyEvent()

def waiter(i):
    print(f"Thread {i} waiting for event...")
    event.wait()
    print(f"Thread {i} received event!")

threads = [threading.Thread(target=waiter, args=(i,)) for i in range(3)]
for t in threads:
    t.start()

threading.Event().wait(2)  # simulate delay
print("Main thread setting event!")
event.set()

for t in threads:
    t.join()
