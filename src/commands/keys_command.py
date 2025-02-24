"""
file: keys_command.py

This module implements the KEYS command for the Redis clone server.
The KEYS command returns all keys matching a given pattern.

Created by Gizachew Bayness Kassa on 2025-02-24
"""

import fnmatch
from typing import List

from src.data.storage import Storage

from .base_command import BaseCommand


class KeysCommand(BaseCommand):
    """
    KeysCommand - A command class for the KEYS command in the Redis clone server.
    """

    async def execute(self, storage: Storage, *args: List[str]) -> str:
        """
        Execute the KEYS command with the given arguments.

        Usage:
            KEYS pattern

        Returns a formatted list of keys matching the pattern.
        """
        if len(args) != 1:
            return "ERR wrong number of arguments for 'KEYS' command"

        pattern = args[0]
        all_keys = storage.keys()  # Retrieve all keys from the store
        matching_keys = [key for key in all_keys if fnmatch.fnmatch(key, pattern)]

        # Format the output similar to Redis's array output:
        if not matching_keys:
            return "(empty array)"

        result_lines = []
        for index, key in enumerate(matching_keys, start=1):
            result_lines.append(f"{index}) {key}")
        return "\n".join(result_lines)
