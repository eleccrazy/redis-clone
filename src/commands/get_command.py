"""
file: src/commands/get_command.py

This file contains the implementation of the GET command for the Redis clone server.

Created by Gizachew Bayness Kassa on 2025-02-19
"""

from typing import List

from src.storage.storage import Storage

from .base_command import BaseCommand


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
