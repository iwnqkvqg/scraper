from src.extractors.interface import Extractor


class TitleExtractor(Extractor):

    def __init__(self) -> None:
        self.name = "title"
