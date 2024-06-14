from src.extractors.interface import Extractor


class URLExtractor(Extractor):

    def __init__(self) -> None:
        self.name = "url"
