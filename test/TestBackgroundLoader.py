import pytest
import time
from vasaloppet.BackgroundLoader import *

class Dummy:
    def __init__(self, N) -> None:
        self.__size = N
        self.__list = []
        self.Counter = 0

    def InitList(self) -> None:
        self.__list = [lambda idx=ii: idx for ii in range(1, self.__size)]

    def NextOne(self) -> bool:
        if len(self.__list) == 0:
            return false
        incr = self.__list.pop(0)()
        self.Counter += incr


class TestBackgroundLoader:

    def test_init(self):
        loader = BackgroundLoader(lambda: print("initCall"), 0.5, lambda: print("nextOne"), 1)

    def test_dummy(self):
        dummy = Dummy(10)
        loader = BackgroundLoader(dummy.InitList, 0.5, dummy.NextOne, 2)
        time.sleep(0.1)
        assert dummy.Counter == 3
