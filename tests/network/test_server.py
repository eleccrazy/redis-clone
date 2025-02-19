"""
file: test_server.py

This file contains tests for the RedisCloneServer class in src/network/server.py.
It uses the pytest and asyncio libraries to test the server's functionality.

Created by Gizachew Bayness Kassa on 2025-02-19
"""

import asyncio

import pytest
import pytest_asyncio

from src.network.server import RedisCloneServer


# Define fixtures for the server and a helper function to send messages to the server
@pytest_asyncio.fixture(scope="module")
async def server() -> None:
    """Fixture to start the RedisCloneServer before tests and stop it after."""
    server = RedisCloneServer(host="127.0.0.1", port=6378)
    server_task = asyncio.create_task(server.start())
    await asyncio.sleep(1)  # Give time for the server to start
    yield  # Run tests
    server_task.cancel()  # Stop server after tests


# Define a helper function to send messages to the server and get a response
async def send_message(message: str) -> str:
    """Helper function to send a message to the server and get a response."""
    reader, writer = await asyncio.open_connection("127.0.0.1", 6378)

    writer.write((message + "\n").encode())  # Send message
    await writer.drain()

    response = await reader.readline()  # Read response
    writer.close()
    await writer.wait_closed()

    return response.decode().strip()


# Define tests for the server
@pytest.mark.asyncio
async def test_echo_response(server: RedisCloneServer) -> None:
    """Test that the server echoes back the correct message."""
    message = "Hello, Redis Clone!"
    response = await send_message(message)
    assert response == f"Echo: {message}"


@pytest.mark.asyncio
async def test_multiple_clients(server: RedisCloneServer) -> None:
    """Test that multiple clients can connect and receive responses."""
    messages = ["Client 1", "Client 2", "Client 3"]
    responses = await asyncio.gather(*(send_message(msg) for msg in messages))

    for msg, resp in zip(messages, responses):
        assert resp == f"Echo: {msg}"


@pytest.mark.asyncio
async def test_empty_message(server: RedisCloneServer) -> None:
    """Test sending an empty message."""
    response = await send_message("")
    assert response == "Echo:"  # The server should still echo an empty message
