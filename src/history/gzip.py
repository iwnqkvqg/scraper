from typing import Optional
import gzip
import os, os.path

from loguru import logger

from src.history.interface import History


DEFAULT_HISTORY: str = "config/history.gz"


class GzipHistory(History):

    def __init__(self, file_name: Optional[str]) -> None:
        super().__init__(file_name or DEFAULT_HISTORY)
        logger.debug("Gzip history handler ready")

    def close(self) -> None:
        logger.debug("Saving history to disk")
        os.makedirs(os.path.dirname(self.file_name), exist_ok=True)
        try:
            with gzip.open(self.file_name, "wb") as fd:
                for entry in self.history:
                    fd.write(f"{entry}\n".encode())
        except Exception as e:
            logger.error(f"Failed to save history: {e}")

    def open(self) -> None:
        logger.debug(f"Reading history file: {self.file_name}")
        try:
            with gzip.open(self.file_name, "r") as fd:
                self.history = {entry.decode().strip() for entry in fd if entry}
                logger.debug(f"History contains {len(self.history)} entries")
        except FileNotFoundError:
            logger.info("Fresh start (no history found)")
        except gzip.BadGzipFile as e:
            logger.error(f"{self.file_name} is not a gzipped file")
            raise e
