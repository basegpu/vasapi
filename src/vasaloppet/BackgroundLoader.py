import threading, time
from .utils import *

class BackgroundLoader:

    def __init__(self, initCall, nextCall, N) -> None:
        i = threading.Thread(target=initCall, daemon=True)
        i.start()
        self.__done = False
        self.__running = 0
        self.__nThreads = N
        while i.is_alive() or not self.__done:
            if self.__running < self.__nThreads:
                t = threading.Thread(target=self.Task, args=(nextCall,), daemon=True)
                t.start()

    def Task(self, callBack):
        with threading.Lock():
            self.__running += 1
        done = not callBack()
        with threading.Lock():
            self.__done = done
            self.__running -= 1
