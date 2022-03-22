import threading, time
from .utils import *

class BackgroundLoader:

    def __init__(self, initCall, nextCall) -> None:
        i = threading.Thread(target=initCall, daemon=True)
        i.start()
        time.sleep(3.0)
        n1 = threading.Thread(target=nextCall, daemon=True)
        n1.start()
        n2 = threading.Thread(target=nextCall, daemon=True)
        n2.start()