from threading import Event, Thread
from typing import Callable


class FooBar:
    def __init__(self, n):
        self.n = n
        self.flag1 = Event()  # For foo -> bar
        self.flag2 = Event()  # For bar -> foo

    def foo(self, printFoo: Callable[[], None]) -> None:
        for i in range(self.n):
            if i != 0:
                self.flag2.wait()  # Wait for bar to finish
                self.flag2.clear()  # Reset bar's signal
            printFoo()
            self.flag1.set()  # Signal bar to proceed

    def bar(self, printBar: Callable[[], None]) -> None:
        for i in range(self.n):
            self.flag1.wait()  # Wait for foo to finish
            self.flag1.clear()  # Reset foo's signal
            printBar()
            self.flag2.set()  # Signal foo to proceed


def printFoo():
    print("foo", end="")


def printBar():
    print("bar", end="")


foobar = FooBar(5)
t1 = Thread(target=foobar.foo, args=(printFoo,))
t2 = Thread(target=foobar.bar, args=(printBar,))

t1.start()
t2.start()

t1.join()
t2.join()
