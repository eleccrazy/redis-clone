"""
file: test_keys_command.py

This module contains tests for the KEYS command in the Redis clone server.

Created by Gizachew Bayness Kassa on 2025-02-24
"""

import pytest

from src.commands.keys_command import KeysCommand
from src.data.storage import Storage


# Define fixtures for the Storage and KeysCommand classes
@pytest.fixture
def storage():
    return Storage()


# Define a fixture for the KeysCommand class
@pytest.fixture
def keys_command():
    return KeysCommand()


# Test with no keys in the storage
@pytest.mark.asyncio
async def test_keys_command_no_keys(keys_command, storage):
    result = await keys_command.execute(storage)
    assert result == "ERR wrong number of arguments for 'KEYS' command"


# Test with empty string key as argument
@pytest.mark.asyncio
async def test_keys_command_empty_string_key(keys_command, storage):
    result = await keys_command.execute(storage, "")
    assert result == "(empty array)"


# Test with a single key in the storage
@pytest.mark.asyncio
async def test_keys_command_single_key(keys_command, storage):
    storage.set("key1", "value1")
    result = await keys_command.execute(storage, "key1")
    assert result == "1) key1"


# Test with multiple keys in the storage
@pytest.mark.asyncio
async def test_keys_command_multiple_keys(keys_command, storage):
    storage.set("key1", "value1")
    storage.set("key2", "value2")
    storage.set("another_key", "value3")
    result = await keys_command.execute(storage, "key*")
    assert result == "1) key1\n2) key2"


# Test with no matching keys in the storage
@pytest.mark.asyncio
async def test_keys_command_no_matching_keys(keys_command, storage):
    storage.set("key1", "value1")
    storage.set("key2", "value2")
    result = await keys_command.execute(storage, "nomatch*")
    assert result == "(empty array)"


# Test with invalid arguments
@pytest.mark.asyncio
async def test_keys_command_invalid_arguments(keys_command, storage):
    result = await keys_command.execute(storage, "key1", "key2")
    assert result == "ERR wrong number of arguments for 'KEYS' command"


# Test with pattern matching
@pytest.mark.asyncio
async def test_keys_command_pattern_matching(keys_command, storage):
    storage.set("key1", "value1")
    storage.set("key2", "value2")
    storage.set("another_key", "value3")
    result = await keys_command.execute(storage, "key*")
    assert result == "1) key1\n2) key2"


# Test with wildcard matching: *key*
@pytest.mark.asyncio
async def test_keys_command_wildcard_matching(keys_command, storage):
    storage.set("key1", "value1")
    storage.set("key2", "value2")
    storage.set("another_key", "value3")
    result = await keys_command.execute(storage, "*key*")
    assert result == "1) key1\n2) key2\n3) another_key"
