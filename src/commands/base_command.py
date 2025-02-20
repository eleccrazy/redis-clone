"""
file: src/commands/base_command.py

This file contains the abstract BaseCommand class for the Redis clone server commands.

Created by Gizachew Bayness Kassa on 2025-02-19
"""

from abc import ABC, abstractmethod
from typing import List

from src.data.storage import Storage


class BaseCommand(ABC):
    """
    BaseCommand - An abstract base class for Redis clone server commands.
    """

    @abstractmethod
    def execute(self, storage: Storage, args: List[str]) -> str:
        pass
