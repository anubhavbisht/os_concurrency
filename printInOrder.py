from threading import Event


class Foo:
    def __init__(self):
        self.firstIsDone = Event()
        self.secondIsDone = Event()

    def first(self, printFirst: "Callable[[], None]") -> None:

        # printFirst() outputs "first". Do not change or remove this line.
        printFirst()
        self.firstIsDone.set()

    def second(self, printSecond: "Callable[[], None]") -> None:
        self.firstIsDone.wait()
        # printSecond() outputs "second". Do not change or remove this line.
        printSecond()
        self.secondIsDone.set()

    def third(self, printThird: "Callable[[], None]") -> None:
        self.secondIsDone.wait()
        # printThird() outputs "third". Do not change or remove this line.
        printThird()
