import pytest
from vasaloppet.ResultContainer import *
from vasaloppet.models import Sex

def test_container_init():
    container = ResultContainer()

def test_cachedic_tryget():
    cache = CacheDic[int, str](lambda: '')
    key = 314
    value = cache.TryGet(key)
    assert value is None

def test_cachedic_getorinit():
    cache = CacheDic[int, str](lambda: '')
    key = 314
    value = cache.GetOrInit(key)
    assert value == ''

def test_cachedic_addorupdate():
    cache = CacheDic[int, str](lambda: '')
    key = 314
    assert cache.TryGet(key) == None
    cache.AddOrUpdate(key, 'pi')
    assert cache.TryGet(key) == 'pi'
    cache.AddOrUpdate(key, 'tau')
    assert cache.TryGet(key) == 'tau'
