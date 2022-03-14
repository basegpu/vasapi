import sys
from .MultiLevelCacheDic import *
from .models import Sex, ResultDetail, CacheSize

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

    def __init__(self, getter) -> None:
        lambdaChain = lambda year: lambda sex: lambda place: getter(year, sex, place)
        self.__cache = ResultCache(lambdaChain)

    def Get(self, year, sex, place) -> ResultDetail:
        return self.__cache.GetOrInit(year).GetOrInit(sex).GetOrInit(place)

    def GetCacheSize(self) -> CacheSize:
        N = self.__cache.Integrate(lambda x: len(x))
        size = self.__cache.Integrate(lambda x: sum([sys.getsizeof(r) for i,r in x.items()]))
        return CacheSize(N, size)
