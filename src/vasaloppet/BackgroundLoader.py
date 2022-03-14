import threading, time
from .utils import *

class BackgroundLoader:

    def __init__(self, callBack):
        x = threading.Thread(target=self.Task, args=('dummy', callBack), daemon=True)
        x.start()

    def Task(self, name, callBack):
        log_to_console('Thread %s: starting'%name)
        callBack()
        while True:
            time.sleep(10)
            log_to_console('Thread %s: still running...'%name)