#!/usr/bin/env python3
"""Cache module for storing and retrieving data using Redis"""

import redis
import uuid
from typing import Union


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
