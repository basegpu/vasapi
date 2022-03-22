import threading, time
from .utils import *

class BackgroundLoader:

    def __init__(self, initCall, wait, nextCall, N) -> None:
        i = threading.Thread(target=initCall, daemon=True)
        i.start()
        time.sleep(wait)
        self.__threadPool = [threading.Thread(target=nextCall, daemon=True) for ii in range(N)]
        for t in self.__threadPool:
            t.start()