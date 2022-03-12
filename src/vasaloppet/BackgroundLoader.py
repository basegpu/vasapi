import threading, time
from .utils import *

class BackgroundLoader:

    def __init__(self):
        x = threading.Thread(target=self.Task, args=('dummy',), daemon=True)
        x.start()

    def Task(self, name):
        log_to_console('Thread %s: starting'%name)
        while True:
            time.sleep(10)
            log_to_console('Thread %s: still running...'%name)