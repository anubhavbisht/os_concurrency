from threading import Condition


class ZeroEvenOdd:
    def __init__(self, n):
        self.n = n
        self.cv = Condition()
        self.count = 1
        self.printZero = True

    # printNumber(x) outputs "x", where x is an integer.
    def zero(self, printNumber: "Callable[[int], None]") -> None:
        while True:
            with self.cv:
                while not self.printZero and (self.count <= self.n):
                    self.cv.wait()
                if self.count > self.n:
                    self.cv.notify_all()
                    break
                printNumber(0)
                self.printZero = False
                self.cv.notify_all()

    def even(self, printNumber: "Callable[[int], None]") -> None:
        while True:
            with self.cv:
                while (self.printZero or self.count % 2 != 0) and (
                    self.count <= self.n
                ):
                    self.cv.wait()
                if self.count > self.n:
                    self.cv.notify_all()
                    break
                printNumber(self.count)
                self.printZero = True
                self.count += 1
                self.cv.notify_all()

    def odd(self, printNumber: "Callable[[int], None]") -> None:
        while True:
            with self.cv:
                while (self.printZero or self.count % 2 == 0) and (
                    self.count <= self.n
                ):
                    self.cv.wait()
                if self.count > self.n:
                    self.cv.notify_all()
                    break
                printNumber(self.count)
                self.printZero = True
                self.count += 1
                self.cv.notify_all()
