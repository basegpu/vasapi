from typing import TypeVar

TKey = TypeVar('TKey')
TValue = TypeVar('TValue')

class MultiLevelCacheDic(dict[TKey, TValue]):

    def __init__(self, vInit, bottom = True) -> None:
        super().__init__()
        self.__vInit = vInit
        self.__bottom = bottom

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

    def Integrate(self, func):
        if self.__bottom:
            return func(self)
        else:
            return sum([value.Integrate(func) for key, value in self.items()])

        