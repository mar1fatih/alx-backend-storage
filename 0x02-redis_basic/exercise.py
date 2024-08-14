#!/usr/bin/env python3
"""redis file"""
import redis
import uuid
from functools import wraps
from typing import Callable


def count_calls(method: Callable) -> Callable:
    """ counts how many times methods are called """
    key = method.__qualname__
    @wraps(method)
    def wrapper(self, *args, **kwds):
        """ wrapped function """
        self._redis.incr(key)
        return method(self, *args, **kwds)
    return wrapper


class Cache:
    """class cache"""
    def __init__(self):
        """constructor"""
        self._redis = redis.Redis()
        self._redis.flushdb()


    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """generate a random key"""
        _id: str = uuid.uuid4()
        self._redis.set(_id, data)
        return _id


    def get(self, key, fn: Optional[Callable]
            = None) -> Union[bytes, int, str, float]:
        """get method"""
        val = self._redis.get(key)
        if fn:
            return fn(val)
        return val


    def get_str(self, key: str) -> str:
        """ get str """
        return self._redis.get(key, str)


    def get_int(self, key: str) -> int:
        """ get int """
        return self._redis.get(key, int)
