from typing import Dict
import csv

from loguru import logger

from src.reporters.interface import Reporter


class CSVReporter(Reporter):

    def __init__(self, today: str) -> None:
        super().__init__(today)
        logger.debug("CSV Reporter ready")

    def close(self):
        self.csv.close()
        logger.debug("Reporter closed")

    def open(self):
        self.csv = open(f"{self.today}-report.csv", "a+")
        self.CSVWriter = csv.writer(self.csv)

    def write_line(self, fields: Dict[str, str]) -> None:
        self.CSVWriter.writerow([self.today, *list(fields.values())])
