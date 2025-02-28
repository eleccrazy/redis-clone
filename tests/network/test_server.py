"""
file: test_server.py

This file contains tests for the RedisCloneServer class in src/network/server.py.
It uses pytest and asyncio to verify that the server correctly handles client
connections and delegates command processing via the command processor module.

Created by Gizachew Bayness Kassa on 2025-02-19
"""

import asyncio
from typing import Any, AsyncGenerator

import pytest
import pytest_asyncio

from src.network.server import RedisCloneServer


# Define a fixture to start the RedisCloneServer before tests and stop it after
@pytest_asyncio.fixture(scope="module")
async def server() -> AsyncGenerator[RedisCloneServer, Any]:
    """Fixture to start the RedisCloneServer before tests and stop it after."""
    server = RedisCloneServer(host="127.0.0.1", port=6378)
    server_task = asyncio.create_task(server.start())
    await asyncio.sleep(1)  # Give the server time to start
    yield server  # Run tests with the server running
    server_task.cancel()  # Cancel the server task after tests complete


@pytest_asyncio.fixture(scope="module")
def event_loop():
    """Create a module-scoped event loop for async tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


async def send_message(message: str) -> str:
    """Helper function to send a message to the server and get a response."""
    reader, writer = await asyncio.open_connection("127.0.0.1", 6378)
    writer.write((message + "\n").encode())
    await writer.drain()
    response = await reader.readline()
    writer.close()
    await writer.wait_closed()
    return response.decode().strip()


@pytest.mark.asyncio
async def test_set_and_get(server: RedisCloneServer) -> None:
    """Test that the server correctly processes SET and GET commands."""
    # Test the SET command
    set_response = await send_message("SET mykey myvalue")
    assert set_response == "OK"

    # Test the GET command for the same key
    get_response = await send_message("GET mykey")
    assert get_response == "myvalue"


@pytest.mark.asyncio
async def test_unknown_command(server: RedisCloneServer) -> None:
    """Test that an unknown command returns an appropriate error message."""
    response = await send_message("FOO bar")
    assert response == "Unknown command"


@pytest.mark.asyncio
async def test_empty_message(server: RedisCloneServer) -> None:
    """Test sending an empty message returns an appropriate error message."""
    response = await send_message("")
    assert response == "Unknown command"


# Test the set command for the wrong number of arguments
@pytest.mark.asyncio
async def test_set_wrong_number_of_arguments(server: RedisCloneServer) -> None:
    response = await send_message("SET key")
    assert response == "ERR wrong number of arguments for 'SET' command"


# Test the get command for the wrong number of arguments
@pytest.mark.asyncio
async def test_get_wrong_number_of_arguments(server: RedisCloneServer) -> None:
    response = await send_message("GET")
    assert response == "ERR wrong number of arguments for 'GET' command"


# Test the del command for the wrong number of arguments
@pytest.mark.asyncio
async def test_del_wrong_number_of_arguments(server: RedisCloneServer) -> None:
    response = await send_message("DEL")
    assert response == "ERR wrong number of arguments for 'DEL' command"


# Test the del command for the key that does not exist
@pytest.mark.asyncio
async def test_del_key_not_exist(server: RedisCloneServer) -> None:
    response = await send_message("DEL key")
    assert response == "(integer) 0"


# Test the del command for the key that exists
@pytest.mark.asyncio
async def test_del_key_exist(server: RedisCloneServer) -> None:
    response = await send_message("DEL mykey")
    assert response == "(integer) 1"


# Test the get command for the key that does not exist
@pytest.mark.asyncio
async def test_get_key_not_exist(server: RedisCloneServer) -> None:
    response = await send_message("GET mykey")
    assert response == "(nil)"


# Test the keys command for the wrong number of arguments
@pytest.mark.asyncio
async def test_keys_wrong_number_of_arguments(server: RedisCloneServer) -> None:
    response = await send_message("KEYS")
    assert response == "ERR wrong number of arguments for 'KEYS' command"


# Test the keys command for the empty string key
@pytest.mark.asyncio
async def test_keys_empty_string_key(server: RedisCloneServer) -> None:
    response = await send_message("KEYS")
    assert response == "ERR wrong number of arguments for 'KEYS' command"


# Test the keys command for the single key in the storage
@pytest.mark.asyncio
async def test_keys_single_key(server: RedisCloneServer) -> None:
    # Set mykey to a value
    await send_message("SET mykey myvalue")
    response = await send_message("KEYS mykey")
    assert response == "1) mykey"


# Test the keys command for the multiple keys in the storage
@pytest.mark.asyncio
async def test_keys_multiple_keys(server: RedisCloneServer) -> None:
    response = await send_message("KEYS my*")
    assert response == "1) mykey"


# Test the keys command for the no matching keys in the storage
@pytest.mark.asyncio
async def test_keys_no_matching_keys(server: RedisCloneServer) -> None:
    response = await send_message("KEYS nomatch*")
    assert response == "(empty array)"


# Test the keys command for the pattern matching
@pytest.mark.asyncio
async def test_keys_pattern_matching(server: RedisCloneServer) -> None:
    response = await send_message("KEYS my*")
    assert response == "1) mykey"


# Test the keys command for the pattern matching
@pytest.mark.asyncio
async def test_keys_pattern_matching(server: RedisCloneServer) -> None:
    response = await send_message("KEYS my*")
    assert response == "1) mykey"


# Test the keys command for the pattern matching
@pytest.mark.asyncio
async def test_keys_pattern_matching(server: RedisCloneServer) -> None:
    response = await send_message("KEYS my*")
    assert response == "1) mykey"


# Test the keys command for the pattern matching
@pytest.mark.asyncio
async def test_keys_pattern_matching(server: RedisCloneServer) -> None:
    response = await send_message("KEYS my*")
    assert response == "1) mykey"


# Test the expire command for valid key and ttl
@pytest.mark.asyncio
async def test_expire_valid_key_ttl(server: RedisCloneServer) -> None:
    await send_message("SET mykey myvalue")
    response = await send_message("EXPIRE mykey 10")
    assert response == "(integer) 1"
