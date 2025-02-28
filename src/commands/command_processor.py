"""
command_processor.py - Command Processing Module

This module is responsible for parsing and routing Redis-like commands to their
respective handlers. It imports command implementations (e.g., SetCommand, GetCommand)
and executes them using the provided storage.

Created by Gizachew Bayness Kassa on 2025-02-20
"""

from src.data.storage import Storage

from .key_value import DeleteCommand, GetCommand, SetCommand
from .keys_command import KeysCommand
from .ttl_commands import ExpireCommand, TTLCommand


async def process_command(command: str, storage: Storage) -> str:
    """
    Parse the command string and execute the corresponding command.

    Args:
        command (str): The command string received from the client.
        storage: The storage instance to perform data operations.

    Returns:
        str: The response from the command execution.
    """
    parts = command.split(" ")
    command_name = parts[0].upper()
    args = parts[1:]

    # Dispatch to the appropriate command handler
    if command_name == "SET":
        handler = SetCommand()
    elif command_name == "GET":
        handler = GetCommand()
    elif command_name == "DEL":
        handler = DeleteCommand()
    elif command_name == "KEYS":
        handler = KeysCommand()
    elif command_name == "EXPIRE":
        handler = ExpireCommand()
    elif command_name == "TTL":
        handler = TTLCommand()
    else:
        return "Unknown command"

    # If the response integer, then return as redis like (integer) response
    response = await handler.execute(storage, *args)
    # Check the response type is string to use isdigit() method
    if (isinstance(response, str) and response.isdigit()) or isinstance(response, int):
        return f"(integer) {response}"
    return response
