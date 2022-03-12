from typing import TypeVar
from .models import Sex, Result
from .VasaloppetResultsWrapper import *

TKey = TypeVar('TKey')
TValue = TypeVar('TValue')

class CacheDic(dict[TKey, TValue]):

	def __init__(self, vInit) -> None:
		super().__init__()
		self.__vInit = vInit

	def TryGet(self, key: TKey) -> TValue:
		return self.get(key)

	def GetOrInit(self, key: TKey) -> TValue:
		value = self.TryGet(key)
		if value is None:
			value = self.__vInit(key)
			self[key] = value
		return value

	def AddOrUpdate(self, key: TKey, value: TValue) -> None:
		self[key] = value


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

	def __init__(self, getter):
		lambdaChain = lambda year: lambda sex: lambda place: getter(year, sex, place)
		self.__cache = ResultCache(lambdaChain)

	def Get(self, year, sex, place):
		return self.__cache.GetOrInit(year).GetOrInit(sex).GetOrInit(place)
