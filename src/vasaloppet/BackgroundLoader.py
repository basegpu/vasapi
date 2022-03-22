import threading, time
from .utils import *

class BackgroundLoader:

    def __init__(self, container):
        self.__container = container
        # start filling the list with results, ready to be parsed for details
        initCall = self.__container.InitResultList
        x = threading.Thread(target=self.Task, args=('init result list', initCall), daemon=True)
        x.start()

    def Task(self, name, callBack):
        log_to_console('Thread %s: starting'%name)
        callBack()
        log_to_console('Thread %s: finished'%name)