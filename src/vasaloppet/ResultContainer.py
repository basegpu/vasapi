import sys
from .CacheDic import *
from .models import Sex, Result, CacheSize

class SexResults(CacheDic[int, type(Result)]):
    def __init__(self, resultCall) -> None:
        super(SexResults, self).__init__(resultCall)

class YearResults(CacheDic[type(Sex), type(SexResults)]):
    def __init__(self, resultForSex) -> None:
        super(YearResults, self).__init__(lambda sex: SexResults(resultForSex(sex)))

class ResultCache(CacheDic[int, type(YearResults)]):
    def __init__(self, resultForYear) -> None:
        super(ResultCache, self).__init__(lambda y: YearResults(resultForYear(y)))

class ResultContainer:

    def __init__(self, getter) -> None:
        lambdaChain = lambda year: lambda sex: lambda place: getter(year, sex, place)
        self.__cache = ResultCache(lambdaChain)

    def Get(self, year, sex, place) -> Result:
        return self.__cache.GetOrInit(year).GetOrInit(sex).GetOrInit(place)

    def GetCacheSize(self) -> CacheSize:
        N = 0
        size = 0
        for y, yr in self.__cache.items():
            for s,sr in yr.items():
                N += len(sr)
                size += sum([sys.getsizeof(r) for i,r in sr.items()])
        return CacheSize(N, size)
