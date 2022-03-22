import sys
from .utils import *
from .MultiLevelCacheDic import *
from .models import Sex, ResultDetail, CacheSize
from .interfaces import IDataProvider

class SexResults(MultiLevelCacheDic[int, type(ResultDetail)]):
    def __init__(self, resultCall) -> None:
        super(SexResults, self).__init__(resultCall, True)

class YearResults(MultiLevelCacheDic[type(Sex), type(SexResults)]):
    def __init__(self, resultForSex) -> None:
        super(YearResults, self).__init__(lambda sex: SexResults(resultForSex(sex)), False)

class ResultCache(MultiLevelCacheDic[int, type(YearResults)]):
    def __init__(self, resultForYear) -> None:
        super(ResultCache, self).__init__(lambda y: YearResults(resultForYear(y)), False)

class ResultContainer:

    def __init__(self, dataProvider) -> None:
        self.__dataProvider = dataProvider
        getter = self.__dataProvider.GetResult
        lambdaChain = lambda year: lambda sex: lambda place: getter(year, sex, place)
        self.__cache = ResultCache(lambdaChain)

    def Get(self, year, sex, place) -> ResultDetail:
        return self.__cache.GetOrInit(year).GetOrInit(sex).GetOrInit(place)

    def Set(self, year, sex, place, value) -> None:
        self.__cache.GetOrInit(year).GetOrInit(sex).AddOrUpdate(place, value)

    def GetCacheSize(self) -> CacheSize:
        N = self.__cache.Integrate(lambda x: len(x))
        size = self.__cache.Integrate(lambda x: sum([sys.getsizeof(r) for i,r in x.items()]))
        return CacheSize(N, size)

    def InitResultList(self, initConfig):
        self.__initList = []
        for year,N in initConfig.items():
            newCalls = self.__dataProvider.GetInitList(year, N)
            self.__initList.extend(newCalls)

    def ProcessNextResult(self):
        loadResult = self.__initList.pop(0)
        result = loadResult()
        self.Set(result.Year, result.Lopper.Sex, result.Place, result)
        log_to_console('added %s to cache'%result)
