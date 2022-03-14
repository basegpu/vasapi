import pytest, uuid
from vasaloppet.ResultContainer import ResultContainer
from vasaloppet.models import *

def MakeResult(year, sex, place):
    lopper = LopperItem('Daria Cologna', 'SUI', sex.name, 'pros', uuid.uuid4())
    overall = OverallItem('03:14:15', 1000, 'VL0')
    return ResultDetail(year, place, lopper, overall)

def test_container_init():
    container = ResultContainer(MakeResult)

def test_container_get():
    container = ResultContainer(MakeResult)
    assert container.Get(2022, Sex.W, 1) is not None

def test_container_cache():
    container = ResultContainer(MakeResult)
    result = container.Get(2022, Sex.W, 1)
    assert container.Get(2022, Sex.W, 1) == result

def test_container_count():
    container = ResultContainer(MakeResult)
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