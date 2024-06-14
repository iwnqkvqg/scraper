from abc import ABCMeta, abstractmethod
from typing import List, Optional

from pydantic import BaseModel, NonNegativeInt

from src.reporters.interface import REPORTER, DEFAULT_REPORTER


class Topic(BaseModel):
    disabled: bool = False
    label: str
    url: str


class Config(BaseModel):
    base_url: str
    history: str
    proxy: Optional[str]
    reporter: REPORTER = DEFAULT_REPORTER
    topics: List[Topic]
    top: NonNegativeInt = 0


class Scraper:
    __metaclass__ = ABCMeta

    @abstractmethod
    def run(self) -> None:
        """Start processing topics defined in the configuration"""
        raise NotImplementedError
