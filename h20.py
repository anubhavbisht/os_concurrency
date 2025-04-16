from threading import Semaphore, Barrier, Thread
from typing import Callable


class H2O:
    def __init__(self):
        self.h_sem = Semaphore(2)  # Only 2 hydrogen allowed per molecule
        self.o_sem = Semaphore(1)  # Only 1 oxygen allowed per molecule
        self.barrier = Barrier(3)  # Wait until 3 threads (2H+1O) arrive

    def hydrogen(self, releaseHydrogen: Callable[[], None]) -> None:
        self.h_sem.acquire()  # Claim a hydrogen spot
        self.barrier.wait()  # Wait for full molecule
        releaseHydrogen()  # Print "H"
        self.h_sem.release()  # Release for next round

    def oxygen(self, releaseOxygen: Callable[[], None]) -> None:
        self.o_sem.acquire()  # Claim an oxygen spot
        self.barrier.wait()  # Wait for full molecule
        releaseOxygen()  # Print "O"
        self.o_sem.release()  # Release for next round


h2o = H2O()
input_water = "HOHHOH"


def run(c):
    if c == "H":
        h2o.hydrogen(lambda: print("H", end=""))
    else:
        h2o.oxygen(lambda: print("O", end=""))


threads = [Thread(target=run, args=(c,)) for c in input_water]

for t in threads:
    t.start()
for t in threads:
    t.join()
