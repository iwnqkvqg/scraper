from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import Dict, Self


class REPORTER(Enum):
    CSV = "csv"


DEFAULT_REPORTER = REPORTER.CSV


class Reporter:
    __metaclass__ = ABCMeta

    def __init__(self, today: str):
        self.today = today
        self.open()

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_value, exc_tb) -> None:
        self.close()

    def __enter__(self) -> Self:
        return self

    def __exit__(self, exc_type, exc_value, exc_tb) -> None:
        self.close()

    @abstractmethod
    def close(self) -> None:
        """Cleanup"""
        raise NotImplementedError

    @abstractmethod
    def open(self) -> None:
        """Initialize reporter"""
        raise NotImplementedError

    @abstractmethod
    def write_line(self, fields: Dict[str, str]) -> None:
        """Write data to the report"""
        raise NotImplementedError
