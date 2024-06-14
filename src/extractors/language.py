import re

from src.extractors.interface import Extractor


UNKNOWN = "?"


class LanguageExtractor(Extractor):

    def __init__(self) -> None:
        self.name = "language"
        self.explicit = re.compile(r"\bOrig[^ ]+ \(?([^ )+]+)", re.IGNORECASE)
        # Original (Spa)
        # Original Spa
        # Original spa
        # Original Sp
        # Orig. Spa
        self.implicit = re.compile(
            r"\[[\d-]+, (?:Аргентина|Боливия|Венесуэла|Гватемала|Гондурас|Доминиканская Республика|Испания|Колумбия|Коста-Рика|Куба|Мексика|Никарагуа|Панама|Парагвай|Перу|Пуэрто-Рико|Сальвадор|Уругвай|Чили|Эквадор).*\bOriginal",
            re.IGNORECASE,
        )
        # [2024, Испания...] + Original

    def get_value(self, *args, **kwargs) -> str:
        title = kwargs.get("title", "")
        match = self.explicit.search(title)
        language = match.group(1) if match else ""
        if language:
            return language
        match = self.implicit.search(title)
        language = "Spa" if match else ""
        if language:
            return language
        if "Original" in title:
            return UNKNOWN
        return ""
