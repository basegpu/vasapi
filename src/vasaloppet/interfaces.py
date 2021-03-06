from abc import ABCMeta, abstractmethod
from .models import ResultDetail

class IDataProvider(metaclass=ABCMeta):

    @abstractmethod
    def GetResult(self, year, sex, place) -> ResultDetail:
        pass

    @abstractmethod
    def GetInitList(self, year, size) -> list:
        pass