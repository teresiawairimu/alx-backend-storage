#!/usr/bin/env python3
"""Cache module for storing and retrieving data using Redis"""

import redis
import uuid
from typing import Union, Callable, Optional

"""Data type aliases"""
DataType = Union[str, int, float, bytes]
ConvertFunction = Optional[Callable[[bytes], DataType]]


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
