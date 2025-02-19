"""
file: src/commands/set_command.py

This file contains the implementation of the SET command for the Redis clone server.

Created by Gizachew Bayness Kassa on 2025-02-19
"""

from typing import List

from src.storage.storage import Storage

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
