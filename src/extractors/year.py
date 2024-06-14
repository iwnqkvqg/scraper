import re

from src.extractors.interface import Extractor


class YearExtractor(Extractor):

    def __init__(self) -> None:
        self.name = "year"

    def get_value(self, *args, **kwargs) -> str:
        # [2024
        # [2024-2025
        match = re.search(r"\[(\d{4}(?:-\d{4})?)", kwargs.get("title", ""))
        year = match.group(1) if match else ""
        return year
