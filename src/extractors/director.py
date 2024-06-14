import re

from src.extractors.interface import Extractor


class DirectorExtractor(Extractor):

    def __init__(self) -> None:
        self.name = "director"

    def get_value(self, *args, **kwargs) -> str:
        # First paranthesis in the title
        # Director's name can optinnally be translated
        # Multiple names can be listed, separated by comas
        # Alien Anthology (Ридли Скотт / Ridley Scott, Джеймс Кэмерон / James Cameron, Дэвид Финчер / David Fincher, Жан-Пьер Жёне / Jean-Pierre Jeunet)
        match = re.search(r"\(([^)]+)\)", kwargs.get("title", ""))
        names = match.group(1) if match else ""
        directors = []
        for name in names.split(","):
            variants = name.split("/")
            if len(variants) == 1:
                directors.append(name.strip())
            else:
                directors.append(variants[1].strip())
        return ", ".join(directors)
