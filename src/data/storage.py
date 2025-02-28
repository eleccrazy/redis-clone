"""
file: src/storage/storage.py

This file contains the implementation of the Storage class for the Redis clone server.

Created by Gizachew Bayness Kassa on 2025-02-19
"""

import time


class Storage:
    """
    Storage - A simple key-value storage class for the Redis clone server.

    The Storage class provides methods to set, get, and delete key-value pairs.
    """

    def __init__(self):
        self.data = {}  # Initialize an empty dictionary to store key-value pairs

    def set(self, key: str, value: str, ttl: int = None) -> str:
        """Stores a key-value pair."""
        # Create expiration time if ttl is provided
        expire_time = ttl + time.time() if ttl is not None else None
        self.data[key] = (value, expire_time)
        return "OK"

    def get(self, key: str) -> str:
        """Retrieves the value of a key, or (nil) if not found."""
        # Check if the key exists and has not expired
        value, expire_time = self.data.get(key, (None, None))
        if expire_time and expire_time < time.time():
            self.delete(key)
            return "(nil)"
        return value if value is not None else "(nil)"

    def delete(self, key: str) -> str:
        """Deletes a key if it exists."""
        return self.data.pop(key, "(nil)")

    def keys(self) -> str:
        """Returns a list of all keys in the storage."""
        valid_keys = [
            key
            for key, (_, expire_time) in self.data.items()
            if not expire_time or expire_time > time.time()
        ]
        return valid_keys

    def expire(self, key: str, ttl: int) -> int:
        """Sets a time-to-live (TTL) for a key.
        Returns:
            1 if the TTL was set, or 0 if the key does not exist.
        """
        if key not in self.data:
            return 0
        expire_time = ttl + time.time()
        _, old_expire_time = self.data[key]
        self.data[key] = (self.data[key][0], expire_time)
        return 1

    def ttl(self, key: str) -> int:
        """Returns the time-to-live (TTL) of a key in seconds."""
        if key not in self.data:
            return -2
        _, expire_time = self.data[key]
        if expire_time is None:
            return -1
        # check if the key has expired
        if expire_time < time.time():
            self.delete(key)
            return -2
        ttl = expire_time - time.time()
        return int(ttl)
