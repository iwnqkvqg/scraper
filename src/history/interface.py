from abc import ABCMeta, abstractmethod
from typing import Optional, Self, Set

from loguru import logger


class History:
    __metaclass__ = ABCMeta

    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        self.history: Set[str] = set()
        self.null_history_entry_warning = False
        self.open()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_value, exc_tb) -> None:
        self.close()

    def __contains__(self, entry: str) -> bool:
        return entry in self.history

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_value, exc_tb) -> None:
        self.close()

    def add(self, entry: Optional[str]) -> None:
        if not entry and not self.null_history_entry_warning:
            logger.warning("Some entries won't be added to history")
            self.null_history_entry_warning = True
        if entry:
            self.history.add(entry)

    @abstractmethod
    def close(self) -> None:
        """Cleanup"""
        raise NotImplementedError

    @abstractmethod
    def open(self) -> None:
        """Initialize history handler"""
        raise NotImplementedError
