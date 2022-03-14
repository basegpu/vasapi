import pytest
from vasaloppet.MultiLevelCacheDic import *

def test_cachedic_tryget():
    cache = MultiLevelCacheDic[int, str](lambda x: str(x))
    key = 314
    value = cache.TryGet(key)
    assert value is None

def test_cachedic_getorinit():
    cache = MultiLevelCacheDic[int, str](lambda x: str(x))
    key = 314
    value = cache.GetOrInit(key)
    assert value == '314'

def test_cachedic_addorupdate():
    cache = MultiLevelCacheDic[int, str](lambda x: str(x))
    key = 314
    assert cache.TryGet(key) == None
    cache.AddOrUpdate(key, 'pi')
    assert cache.TryGet(key) == 'pi'
    cache.AddOrUpdate(key, 'tau')
    assert cache.TryGet(key) == 'tau'

def test_cachedic_integrate_count_str():
    cache = MultiLevelCacheDic[int, str](lambda x: str(x))
    count = lambda x: len(x)
    assert cache.Integrate(count) == 0
    cache.GetOrInit(123)
    assert cache.Integrate(count) == 1

