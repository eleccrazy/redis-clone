"""
server.py - Redis Clone Network Module

This module implements a basic asynchronous TCP server using Python's asyncio library.
It serves as the network layer for the Redis clone project by handling client connections,
reading incoming messages, and sending responses. Currently, the server echoes back any
received messages to the client, but this functionality can be extended to parse and
execute Redis-like commands.

Key Features:
- Listens on a configurable host and port (default: 127.0.0.1:6379)
- Handles multiple client connections concurrently using asyncio
- Provides a foundation for integrating command parsing and further Redis functionalities

Usage:
    Run the module directly to start the server:
        python src/network/server.py

Created by Gizachew Bayness Kassa on 2025-02-19
"""

from asyncio import StreamReader, StreamWriter, run, start_server

from src.commands.command_processor import process_command
from src.data.storage import Storage


class RedisCloneServer:
    """
    RedisCloneServer - A simple asynchronous TCP server for the Redis clone.

    This class sets up an asynchronous TCP server that listens for incoming client
    connections on a configurable host and port (default: 127.0.0.1:<port>). It handles
    incoming messages from clients, processes commands (currently echoing them back),
    and can be extended to integrate a full Redis-like command parser and data store.
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 6379):
        self.host = host
        self.port = port
        self.storage = Storage()  # Initialize the storage for key-value pairs

    async def handle_client(self, reader: StreamReader, writer: StreamWriter):
        """
        Handle a single client connection.

        Reads messages from the client, processes them, and sends a response.
        Currently, it echoes received messages back to the client.
        """
        addr = writer.get_extra_info("peername")  # Client address
        print(f"New connection from {addr}")  # Log new connection
        try:
            while True:
                # Read a line of data (message) from the client
                data = await reader.readline()
                # If no data is received, the client has closed the connection
                if not data:
                    print(f"Connection closed from {addr}")
                    break
                message = data.decode().strip()
                # Log and echo the received message back to the client (for initial testing)
                print(f"Received from {addr}: {message}")

                # Process the command
                response = await process_command(command=message, storage=self.storage)
                writer.write(
                    (response + "\n").encode()
                )  # Send the response back to the client
                await writer.drain()  # Flush the write buffer
        except Exception as e:
            print(f"Error handling connection from {addr}: {e}")
        finally:
            writer.close()  # Close the connection
            await writer.wait_closed()  # Wait for the connection to close
            print(f"Connection from {addr} has been closed.")  # Log connection closure

    async def start(self):
        """
        Start the TCP server and serve clients indefinitely.
        """
        server = await start_server(
            self.handle_client, self.host, self.port
        )  # Start the server
        addr = server.sockets[0].getsockname()  # Get the server address
        print(f"Serving on {addr}")

        async with server:
            # Serve clients indefinitely
            await server.serve_forever()
