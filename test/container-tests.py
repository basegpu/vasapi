import pytest, uuid
from vasaloppet.ResultContainer import ResultContainer
from vasaloppet.models import *
from vasaloppet.interfaces import IDataProvider

class TestProvider(IDataProvider):

    def GetResult(year, sex, place) -> ResultDetail:
        lopper = LopperItem('Daria Cologna', 'SUI', sex.name, 'pros', uuid.uuid4())
        overall = OverallItem('03:14:15', 1000, 'VL0')
        return ResultDetail(year, place, lopper, overall)

    def GetInitList(year, size):
        pass

def test_container_init():
    container = ResultContainer(TestProvider)

def test_container_get():
    container = ResultContainer(TestProvider)
    assert container.Get(2022, Sex.W, 1) is not None

def test_container_cache():
    container = ResultContainer(TestProvider)
    result = container.Get(2022, Sex.W, 1)
    assert container.Get(2022, Sex.W, 1) == result

def test_container_count():
    container = ResultContainer(TestProvider)
    assert container.GetCacheSize().Items == 0
    container.Get(2022, Sex.W, 1)
    assert container.GetCacheSize().Items == 1
    container.Get(2022, Sex.W, 1)
    assert container.GetCacheSize().Items == 1
    container.Get(2022, Sex.W, 314)
    assert container.GetCacheSize().Items == 2
    container.Get(2022, Sex.M, 1)
    assert container.GetCacheSize().Items == 3
    container.Get(1922, Sex.M, 999)
    assert container.GetCacheSize().Items == 4