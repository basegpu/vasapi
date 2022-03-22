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
        return [lambda place=ii+1: TestProvider.GetResult(year, Sex.W, place) for ii in range(size)]


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

def test_container_set():
    container = ResultContainer(TestProvider)
    assert container.GetCacheSize().Items == 0
    item = TestProvider.GetResult(2022, Sex.W, 1)
    container.Set(2022, Sex.W, 1, item)
    assert container.GetCacheSize().Items == 1
    container.Get(2022, Sex.W, 1)
    assert container.GetCacheSize().Items == 1

def test_container_cache_init():
    container = ResultContainer(TestProvider)
    initConfig = {
        2000: 1,
        2010: 10
    }
    container.InitResultList(initConfig)
    assert container.GetCacheSize().Items == 0
    container.ProcessNextResult()
    assert container.GetCacheSize().Items == 1
    container.ProcessNextResult()
    container.ProcessNextResult()
    container.ProcessNextResult()
    assert container.GetCacheSize().Items == 4
