from collections import OrderedDict
from typing import List

from src.extractors.language import UNKNOWN
from src.filters.interface import Filter


class ByLanguages(Filter):

    def __init__(self, languages: List[str], allow_unknown: bool = False) -> None:
        self.languages = [l.lower() for l in languages]
        self.allow_unknown = allow_unknown

    def accept(self, post: OrderedDict[str, str]) -> bool:
        """Rutracker convension is to use 3-letter language codes, although sometimes a 2-letter code is used."""
        language = post.get("language", "").lower()
        if not language:
            return False
        if language == UNKNOWN and self.allow_unknown:
            return True
        return any(lang.startswith(language) for lang in self.languages)
