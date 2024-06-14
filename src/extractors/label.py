from src.extractors.interface import Extractor


class LabelExtractor(Extractor):

    def __init__(self) -> None:
        self.name = "label"
