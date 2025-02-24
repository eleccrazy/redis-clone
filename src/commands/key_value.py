"""
file: key_value.py

This module implements basic Redis-like key-value commands such as SET, GET, DEL, and EXISTS.
It interacts with the in-memory storage to perform these operations.

Commands:
- SET key value [EX seconds] - Stores a value for a given key, optionally with an expiration.
- GET key - Retrieves the value of a given key.
- DEL key - Deletes a key from storage.
- EXISTS key - Checks if a key exists in storage.
- EXPIRE key seconds - Sets a time-to-live (TTL) for a key.

Created By: Gizachew Bayness Kassa on 2025-02-20
"""

from typing import List

from src.data.storage import Storage

from .base_command import BaseCommand


class SetCommand(BaseCommand):
    """
    SetCommand - A command class for the SET command in the Redis clone server.
    """

    async def execute(self, storage: Storage, *args: List[str]) -> str:
        """
        Execute the SET command with the given arguments.
        """
        # Check if the correct number of arguments is provided
        if len(args) != 2:
            return "ERR wrong number of arguments for 'SET' command"

        key, value = args
        return storage.set(key, value)  # Set the key-value pair in the server store


class GetCommand(BaseCommand):
    """
    GetCommand - A command class for the GET command in the Redis clone server.
    """

    async def execute(self, storage: Storage, *args: List[str]) -> str:
        """
        Execute the GET command with the given arguments
        """
        # Check if the correct number of arguments is provided
        if len(args) != 1:
            return "ERR wrong number of arguments for 'GET' command"

        key = args[0]
        return storage.get(key)


class DeleteCommand(BaseCommand):
    """
    Execute the DEL command with the given key name
    """

    async def execute(self, storage: Storage, *args: List[str]) -> str:
        # Check if key name is passed
        if len(args) != 1:
            return "ERR wrong number of arguments for 'DEL' command"
        key = args[0]

        # Check if key exists
        if storage.get(key) == "(nil)":
            return "(integer) 0"

        # Delete the key and return 1 to indicate one key was deleted
        storage.delete(key)
        return "(integer) 1"
