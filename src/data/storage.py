"""
file: src/storage/storage.py

This file contains the implementation of the Storage class for the Redis clone server.

Created by Gizachew Bayness Kassa on 2025-02-19
"""


class Storage:
    """
    Storage - A simple key-value storage class for the Redis clone server.

    The Storage class provides methods to set, get, and delete key-value pairs.
    """

    def __init__(self):
        self.data = {}  # Initialize an empty dictionary to store key-value pairs

    def set(self, key: str, value: str) -> str:
        """Stores a key-value pair."""
        self.data[key] = value
        return "OK"

    def get(self, key: str) -> str:
        """Retrieves the value of a key, or (nil) if not found."""
        return self.data.get(key, "(nil)")

    def delete(self, key: str) -> str:
        """Deletes a key if it exists."""
        return self.data.pop(key, "(nil)")
