from threading import Condition, Thread
from typing import Callable


class FooBar:
    def __init__(self, n):
        self.n = n
        self.condition = Condition()
        self.foo_turn = True  # Start with foo

    def foo(self, printFoo: Callable[[], None]) -> None:
        for _ in range(self.n):
            with self.condition:
                while not self.foo_turn:
                    self.condition.wait()
                printFoo()
                self.foo_turn = False
                self.condition.notify()

    def bar(self, printBar: Callable[[], None]) -> None:
        for _ in range(self.n):
            with self.condition:
                while self.foo_turn:
                    self.condition.wait()
                printBar()
                self.foo_turn = True
                self.condition.notify()


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
