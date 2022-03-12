import pytest
from vasaloppet.CacheDic import *

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