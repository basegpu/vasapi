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
			value = self.__vInit()
			self[key] = value
		return value

	def AddOrUpdate(self, key: TKey, value: TValue) -> None:
		self[key] = value


class SexResults(CacheDic[int, type(Result)]):
	def __init__(self) -> None:
		super(SexResults, self).__init__(lambda: None)

class YearResults(CacheDic[type(Sex), type(SexResults)]):
	def __init__(self) -> None:
		super(YearResults, self).__init__(lambda: SexResults())

class ResultCache(CacheDic[int, type(YearResults)]):
	def __init__(self) -> None:
		super(ResultCache, self).__init__(lambda: YearResults())


class ResultContainer:

	def __init__(self):
		self.__wrapper = VasaloppetResultsWrapper()
		self.__cache = ResultCache()

	def TryGetResult(self, year, sex, place):
		return self.GetOrAddEmptyForYear(year).TryGet(place)

	def SetResult(self, year, sex, place, result):
		self.GetOrAddEmptyForYear(year).AddOrUpdate(place, result)

	def GetOrAddEmptyForYear(self, year):
		return self.__cacheDic.GetOrAdd(year, CacheDic())
