from threading import Thread, Condition

class FizzBuzz:
    def __init__(self, n: int):
        self.n = n
        self.current = 1
        self.cv = Condition()

    def fizz(self, printFizz):
        while True:
            with self.cv:
                while self.current <= self.n and (
                    self.current % 3 != 0 or self.current % 5 == 0
                ):
                    self.cv.wait()
                if self.current > self.n:
                    self.cv.notify_all()
                    break
                printFizz()
                self.current += 1
                self.cv.notify_all()

    def buzz(self, printBuzz):
        while True:
            with self.cv:
                while self.current <= self.n and (
                    self.current % 5 != 0 or self.current % 3 == 0
                ):
                    self.cv.wait()
                if self.current > self.n:
                    self.cv.notify_all()
                    break
                printBuzz()
                self.current += 1
                self.cv.notify_all()

    def fizzbuzz(self, printFizzBuzz):
        while True:
            with self.cv:
                while self.current <= self.n and (
                    self.current % 3 != 0 or self.current % 5 != 0
                ):
                    self.cv.wait()
                if self.current > self.n:
                    self.cv.notify_all()
                    break
                printFizzBuzz()
                self.current += 1
                self.cv.notify_all()

    def number(self, printNumber):
        while True:
            with self.cv:
                while self.current <= self.n and (
                    self.current % 3 == 0 or self.current % 5 == 0
                ):
                    self.cv.wait()
                if self.current > self.n:
                    self.cv.notify_all()
                    break
                printNumber(self.current)
                self.current += 1
                self.cv.notify_all()


def printFizz():
    print("fizz")


def printBuzz():
    print("buzz")


def printFizzBuzz():
    print("fizzbuzz")


def printNumber(x):
    print(x)


fb = FizzBuzz(15)

t1 = Thread(target=fb.fizz, args=(printFizz,))
t2 = Thread(target=fb.buzz, args=(printBuzz,))
t3 = Thread(target=fb.fizzbuzz, args=(printFizzBuzz,))
t4 = Thread(target=fb.number, args=(printNumber,))

t1.start()
t2.start()
t3.start()
t4.start()

t1.join()
t2.join()
t3.join()
t4.join()
