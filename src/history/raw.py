import os, os.path

from loguru import logger

from src.history.interface import History


class RawHistory(History):

    def __init__(self, file_name: str):
        super().__init__(file_name)
        logger.debug("Raw history handler ready")

    def close(self) -> None:
        logger.debug("Saving history to disk")
        os.makedirs(os.path.dirname(self.file_name), exist_ok=True)
        try:
            with open(self.file_name, "w") as fd:
                for entry in self.history:
                    print(entry, file=fd)
        except Exception as e:
            logger.error(f"Failed to save history: {e}")

    def open(self) -> None:
        logger.debug(f"Reading history file: {self.file_name}")
        try:
            with open(self.file_name, "r") as fd:
                self.history = {entry for entry in fd if entry}
                logger.debug(f"History contains {len(self.history)} entries")
        except FileNotFoundError:
            logger.info("Fresh start (no history found)")
