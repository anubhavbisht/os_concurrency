from threading import Thread, Condition
from typing import Callable
import random
import time

class H2O:
    def __init__(self):
        self.condition = Condition()
        self.hydrogens = 0
        self.oxygens = 0

    def hydrogen(self, releaseHydrogen: Callable[[], None]) -> None:
        with self.condition:
            while self.hydrogens == 2:
                self.condition.wait()
            self.hydrogens += 1

            # Wait until there are 2 H and 1 O to form a molecule
            while not (self.hydrogens == 2 and self.oxygens == 1):
                self.condition.wait()

            # Bond
            releaseHydrogen()

            self.hydrogens -= 1

            if self.hydrogens == 0 and self.oxygens == 0:
                self.condition.notify_all()

    def oxygen(self, releaseOxygen: Callable[[], None]) -> None:
        with self.condition:
            while self.oxygens == 1:
                self.condition.wait()
            self.oxygens += 1

            # Wait until there are 2 H and 1 O to form a molecule
            while not (self.hydrogens == 2 and self.oxygens == 1):
                self.condition.wait()

            # Bond
            releaseOxygen()

            self.oxygens -= 1

            if self.hydrogens == 0 and self.oxygens == 0:
                self.condition.notify_all()


h2o = H2O()

def run(c):
    if c == 'H':
        h2o.hydrogen(lambda: print('H', end=''))
    else:
        h2o.oxygen(lambda: print('O', end=''))

sequence = list("OOHHHH")
random.shuffle(sequence)

threads = [Thread(target=run, args=(c,)) for c in sequence]
for t in threads:
    t.start()
for t in threads:
    t.join()