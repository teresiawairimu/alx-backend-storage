#!/usr/bin/env python3
"""Cache module for storing and retrieving data using Redis"""

import redis
import uuid
from typing import Union, Callable, Optional
from functools import wraps


"""Data type aliases"""
DataType = Union[str, int, float, bytes]
ConvertFunction = Optional[Callable[[bytes], DataType]]


def count_calls(method: Callable) -> Callable:
    """Decorator to count the number of times a method is called

    Parameters
    method: Callable
        The method to be decorated
    Returns
    Callable
        The decorated method with a call count increment.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        key = method.__qualname__
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Decorator to store the history of inputs and outputs

    Parameter
    method: Callable
        The method to be decorated

    Returns
    Callable
        The decorated method with a call history
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"
        self._redis.rpush(input_key, str(args))
        output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(output))
        return output
    return wrapper


class Cache:
    """A class used to interact with a Redis cache to store and retrieve data.
    Attributes
    _redis: redis.Redis
        The redis client insgtance used to store and retrieve data.
    """

    def __init__(self) -> None:
        """Initializes Cache class, sets up Redis client flushes database"""
        self. _redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Stores given data in Redis, returns a radomly generated key

        Parameters
        data: Union[str, bytes, int, float]
            The data to be stored in Redis

        Returns
        str
            The key under which data is stored
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: ConvertFunction = None) -> Optional[DataType]:
        """
        Retrieves value associated with key, optionally applies conversion
        Parameters
        key: str
            The key to retrieve the value
        fn: ConvertFunction
            Optional callable to convert retrieved value to desired type
        Returns
        Optional[DataType]
           The retrieved value, converted using callable if provided,
           or None if key doesn't exist
           """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn:
            return fn(value)
        return value

    def get_str(self, key: str) -> Optional[str]:
        """Retrieves the value associated with a key as a string
        Parameters
        key: str
            The key for which to retrieve the value
        Returns
        Optional[str]
            The retrieved value as a string, None if the key doesn't exist
        """
        return self.get(key, lambda d: d.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        """Retrieves the value associated with a key as an integer
        Parameters
        key: str
            The key to retrieve the value
        Returns
        Optional[int]
            The retrieved value as an integer, None if the key doesn't exist
        """
        return self.get(key, int)

    @staticmethod
    def replay(method: Callable) -> None:
        """Displays the history of calls of a function

        Parameters
        method: Callable
            The method whose call history will be displayed

        Returns
        None
            Purpose is to print call history
        """
        redis_instance = method.__self__._redis
        method_name = method.__qualname__
        input_key = f"{method_name}: inputs"
        output_key = f"{method_name}: outputs"
        inputs = redis_instance.lrange(input_key, 0, -1)
        outputs = redis_instance.lrange(output_key, 0, -1)
        print(f"{method_name} was called {len(inputs)} times:")
        for inp, out in zip(inputs, outputs):
            decoded_inp = inpu.decode('utf-8')
            decoded_out = out.decode('utf-8')
            print(f"{method_name}(*{decode_inp}) -> {decoded_out}")
