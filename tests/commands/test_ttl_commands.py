"""
File: test_ttl_commands.py

This module contains tests for the TTL commands in the Redis clone server.

Created by Gizachew Bayness Kassa on 2025-02-28
"""

import pytest

from src.commands.ttl_commands import ExpireCommand
from src.data.storage import Storage


# Define fixtures for the Storage and ExpireCommand classes
@pytest.mark.asyncio
async def test_expire_command_sets_ttl():
    storage = Storage()
    storage.set("key1", "value1")
    command = ExpireCommand()

    result = await command.execute(storage, "key1", "10")
    assert result == "1"


# Test with a key that does not exist
@pytest.mark.asyncio
async def test_expire_command_key_does_not_exist():
    storage = Storage()
    command = ExpireCommand()

    result = await command.execute(storage, "nonexistent_key", "10")
    assert result == "0"


# Test with an invalid TTL value
@pytest.mark.asyncio
async def test_expire_command_invalid_ttl():
    storage = Storage()
    storage.set("key1", "value1")
    command = ExpireCommand()

    result = await command.execute(storage, "key1", "invalid_ttl")
    assert result == "ERR invalid expire time"


# Test with the wrong number of arguments
@pytest.mark.asyncio
async def test_expire_command_wrong_number_of_arguments():
    storage = Storage()
    command = ExpireCommand()

    result = await command.execute(storage, "key1")
    assert result == "ERR wrong number of arguments for 'EXPIRE' command"
