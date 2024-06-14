from abc import ABCMeta, abstractmethod
from typing import Dict


class Filter:
    __metaclass__ = ABCMeta

    @abstractmethod
    def accept(self, post: Dict[str, str]) -> bool:
        raise NotImplementedError
