"""
file: server.py

Entry point for the Redis clone server.

Created by Gizachew Bayness Kassa on 2025-02-20
"""

from asyncio import run

from src.network.server import RedisCloneServer


def main():
    # Initialize the Redis clone server
    server = RedisCloneServer(host="127.0.0.1", port=6378)
    try:
        run(server.start())  # Start the server
    except KeyboardInterrupt:
        # Gracefully shut down the server on keyboard interrupt
        print("Server shut down gracefully.")


if __name__ == "__main__":
    main()
