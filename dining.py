import threading
from time import sleep
from random import uniform

class DiningPhilosophers:
    def __init__(self):
        self.forks = [threading.Lock() for _ in range(5)]

    def wantsToEat(self, philosopher,
                   pickLeftFork,
                   pickRightFork,
                   eat,
                   putLeftFork,
                   putRightFork):
        
        left = philosopher
        right = (philosopher + 1) % 5
        
        # Philosopher 4 picks right fork first to break deadlock cycle
        first, second = (right, left) if philosopher == 4 else (left, right)

        with self.forks[first]:
            with self.forks[second]:
                # Pick up forks
                if first == left:
                    pickLeftFork()
                    pickRightFork()
                else:
                    pickRightFork()
                    pickLeftFork()

                eat()

                # Put down forks
                if first == left:
                    putRightFork()
                    putLeftFork()
                else:
                    putLeftFork()
                    putRightFork()
def pickLeft(): print(f"{threading.current_thread().name} picked left fork")
def pickRight(): print(f"{threading.current_thread().name} picked right fork")
def putLeft(): print(f"{threading.current_thread().name} put down left fork")
def putRight(): print(f"{threading.current_thread().name} put down right fork")
def eat(): 
    print(f"{threading.current_thread().name} is eating 🍝")
    sleep(uniform(0.1, 0.3))  # Simulate time to eat

dp = DiningPhilosophers()

def philosopher_thread(i):
    for _ in range(3):  # Each philosopher eats 3 times
        sleep(uniform(0.1, 0.4))  # Think
        dp.wantsToEat(i, pickLeft, pickRight, eat, putLeft, putRight)

# Launch threads
threads = []
for i in range(5):
    t = threading.Thread(target=philosopher_thread, args=(i,), name=f"Philosopher {i}")
    threads.append(t)
    t.start()

for t in threads:
    t.join()
