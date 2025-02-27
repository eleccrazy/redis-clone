"""
file: ttl_commands.py

This module implements the EXPIRE command for the Redis clone server.
The EXPIRE command sets a time-to-live (TTL) for a key in the server storage.

Created By: Gizachew Bayness Kassa on 2025-02-28
"""

from typing import List

from src.data.storage import Storage

from .base_command import BaseCommand


class ExpireCommand(BaseCommand):
    """
    ExpireCommand - A command class for the EXPIRE command in the Redis clone server.
    """

    async def execute(self, storage: Storage, *args: List[str]) -> str:
        """
        Execute the EXPIRE command with the given arguments.

        Usage:
            EXPIRE key seconds
        Returns:
            "1" if the TTL was set, or "0" if the key does not exist.
        """
        if len(args) != 2:
            return "ERR wrong number of arguments for 'EXPIRE' command"
        key, ttl_str = args
        try:
            ttl = int(ttl_str)
        except ValueError:
            return "ERR invalid expire time"

        result = storage.expire(key, ttl)
        return str(result)
