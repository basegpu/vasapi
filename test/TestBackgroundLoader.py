import pytest
import time
from vasaloppet.BackgroundLoader import *

class Dummy:
    def __init__(self, N) -> None:
        self.__size = N
        self.__list = []
        self.Counter = 0

    def InitList(self) -> None:
        self.__list = [lambda idx=ii: self.Count(idx) for ii in range(1, self.__size + 1)]

    def Count(self, idx):
        self.Counter += idx

    def NextOne(self) -> bool:
        if len(self.__list) == 0:
            return False
        self.__list.pop(0)()
        return True


class TestBackgroundLoader:

    def test_init(self):
        loader = BackgroundLoader(lambda: print("initCall"), lambda: print("nextOne"), 1)

    def test_few_threads(self):
        dummy = Dummy(10)
        loader = BackgroundLoader(dummy.InitList, dummy.NextOne, 2)
        time.sleep(0.1)
        assert dummy.Counter == 55

    def test_few_items(self):
        dummy = Dummy(2)
        loader = BackgroundLoader(dummy.InitList, dummy.NextOne, 5)
        time.sleep(0.1)
        assert dummy.Counter == 3

    def test_full(self):
        dummy = Dummy(100)
        loader = BackgroundLoader(dummy.InitList, dummy.NextOne, 10)
        time.sleep(1.0)
        assert dummy.Counter == 5050
