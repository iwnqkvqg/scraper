"""Monitor specific RuTracker topics for updates
"""

from argparse import Namespace
from datetime import datetime
from typing import Optional
import asyncio
import os
import yaml

from httpx import AsyncClient
from loguru import logger

from src.extractors.director import DirectorExtractor
from src.extractors.label import LabelExtractor
from src.extractors.language import LanguageExtractor
from src.extractors.topic_title import TitleExtractor
from src.extractors.url import URLExtractor
from src.extractors.year import YearExtractor
from src.filters.by_languages import ByLanguages
from src.history.gzip import GzipHistory
from src.reporters.csv import CSVReporter
from src.reporters.interface import REPORTER, Reporter
from src.scrapers.interface import Config
from src.scrapers.rut import Rut


TODAY = datetime.today().strftime("%Y-%m-%d")


def _get_client(base_url: str, proxy: Optional[str] = None) -> AsyncClient:
    with open("config/headers.yaml", "r") as fd:
        headers = yaml.safe_load(fd)
        return AsyncClient(
            headers=headers,
            proxy=proxy,
            base_url=base_url,
        )


def _load_config(file_name: str) -> Config:
    logger.debug(f"Loading configuration file {file_name}")
    try:
        with open(file_name) as fd:
            return Config(**yaml.safe_load(fd))
    except FileNotFoundError:
        logger.error(f"Configuration file {file_name} not found")
        exit(1)
    except yaml.YAMLError as e:
        logger.error(f"Configuration file {file_name} is not valid YAML")
        exit(1)


def _get_reporter(reporter: REPORTER) -> Reporter:
    global TODAY
    return {
        REPORTER.CSV: CSVReporter,
    }[
        reporter
    ](TODAY)


async def main(args: Namespace) -> None:
    try:
        config = _load_config(args.config)
        async with _get_client(config.base_url, config.proxy) as client, GzipHistory(
            config.history
        ) as history, _get_reporter(config.reporter) as reporter:
            tasks = []
            for topic in config.topics:
                if topic.disabled:
                    continue
                scraper = Rut(
                    base_url=config.base_url,
                    client=client,
                    extractors=[
                        LabelExtractor(),
                        URLExtractor(),
                        LanguageExtractor(),
                        YearExtractor(),
                        DirectorExtractor(),
                        TitleExtractor(),
                    ],
                    filters=[ByLanguages(["Spanish"])],
                    history=history,
                    reporter=reporter,
                    top=config.top,
                    topic=topic,
                )
                tasks.append(scraper.run())
            logger.debug(f"{len(tasks)} topics will be processed")
            await asyncio.gather(*tasks)
    except asyncio.exceptions.CancelledError:
        pass


if __name__ == "__main__":

    from argparse import ArgumentParser

    DEFAULT_CONFIG = "config/settings.yaml"

    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        "-c",
        "--config",
        default=DEFAULT_CONFIG,
        help=f"Configuration file. Default: {DEFAULT_CONFIG}",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Print debug messages",
    )
    args = parser.parse_args()

    logger.remove()
    logger.add(
        f"{TODAY}.log",
        backtrace=True,
        diagnose=False,
        level=os.environ.get("LOG_LEVEL", "DEBUG" if args.verbose else "INFO"),
    )

    asyncio.run(main(args))
