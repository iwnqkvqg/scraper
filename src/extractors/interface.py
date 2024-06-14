class Extractor:
    name: str

    def get_value(self, *args, **kwargs) -> str:
        return kwargs.get(self.name, "")
