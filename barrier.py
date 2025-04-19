import threading

class MyBarrier:
    def __init__(self, n):
        self.n = n              
        self.count = 0          
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)
    
    def wait(self):
        with self.condition:
            self.count += 1
            if self.count == self.n:
                self.condition.notify_all()  
                self.count=0
            else:
                self.condition.wait()        

barrier = MyBarrier(3)

def worker(i):
    print(f"Worker {i} reached the barrier")
    barrier.wait()
    print(f"Worker {i} passed the barrier")

threads = [threading.Thread(target=worker, args=(i,)) for i in range(6)]

for t in threads:
    t.start()
for t in threads:
    t.join()
