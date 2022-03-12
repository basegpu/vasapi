import pytest, uuid
from vasaloppet.ResultContainer import *
from vasaloppet.models import *

def test_cachedic_tryget():
    cache = CacheDic[int, str](lambda x: str(x))
    key = 314
    value = cache.TryGet(key)
    assert value is None

def test_cachedic_getorinit():
    cache = CacheDic[int, str](lambda x: str(x))
    key = 314
    value = cache.GetOrInit(key)
    assert value == '314'

def test_cachedic_addorupdate():
    cache = CacheDic[int, str](lambda x: str(x))
    key = 314
    assert cache.TryGet(key) == None
    cache.AddOrUpdate(key, 'pi')
    assert cache.TryGet(key) == 'pi'
    cache.AddOrUpdate(key, 'tau')
    assert cache.TryGet(key) == 'tau'

def MakeResult(year, sex, place):
    lopper = LopperItem('Daria Cologna', 'SUI', sex.name, 'pros', uuid.uuid4())
    overall = OverallItem('03:14:15', 1000, 'VL0')
    return Result(year, place, lopper, overall)

def test_container_init():
    container = ResultContainer(MakeResult)

def test_container_get():
    container = ResultContainer(MakeResult)
    assert container.Get(2022, Sex.W, 1) is not None

def test_container_cache():
    container = ResultContainer(MakeResult)
    result = container.Get(2022, Sex.W, 1)
    assert container.Get(2022, Sex.W, 1) == result

