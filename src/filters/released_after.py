from collections import OrderedDict
from typing import Union

from src.filters.interface import Filter


class ReleasedAfter(Filter):

    def __init__(self, year: Union[int, str]) -> None:
        self.year = year

    def accept(self, post: OrderedDict[str, str]) -> bool:
        year = post.get("year")
        if not year:
            return False
        return year == str(self.year)
