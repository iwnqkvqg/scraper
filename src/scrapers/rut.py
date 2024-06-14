from collections import OrderedDict
from typing import AsyncGenerator, List, Optional, cast
import re

from bs4 import BeautifulSoup, NavigableString, Tag
from httpx import (
    AsyncClient,
    ConnectTimeout,
    HTTPStatusError,
    ReadTimeout,
)
from loguru import logger
from tenacity import retry
from tenacity.stop import stop_after_attempt
from tenacity.wait import wait_exponential
from tenacity.retry import retry_if_exception_type

from src.extractors.interface import Extractor
from src.filters.interface import Filter
from src.history.interface import History
from src.reporters.interface import Reporter
from src.scrapers.interface import Scraper, Topic


class Rut(Scraper):

    def __init__(
        self,
        base_url: str,
        client: AsyncClient,
        extractors: List[Extractor],
        history: History,
        reporter: Reporter,
        topic: Topic,
        filters: Optional[List[Filter]] = None,
        top: int = 0,
    ) -> None:
        self.base_url = base_url
        self.client = client
        self.extractors = extractors
        self.history = history
        self.reporter = reporter
        self.topic = topic
        self.filters = filters
        self.top = top
        logger.debug(f"Scraper for topic {self.topic.label} ready")

    def _is_404(self, dom: BeautifulSoup) -> bool:
        messages = dom.find_all(string="Подходящих тем или сообщений не найдено")
        return len(messages) > 0

    @retry(
        reraise=True,
        retry=(
            retry_if_exception_type(ConnectTimeout)
            | retry_if_exception_type(ReadTimeout)
        ),
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=2, min=1, max=5),
    )
    async def run(self) -> None:
        logger.info(f"Processing {self.topic.label}")
        start = 0
        step = 50
        count = 0
        while True:
            try:
                if self.top and start >= self.top * step:
                    logger.info(
                        f"Topic {self.topic.label} processed, {count} new posts found"
                    )
                    break
                url = f"{self.topic.url}&start={start}" if start > 0 else self.topic.url
                response = await self.client.get(url)
                response.raise_for_status()
                dom = BeautifulSoup(
                    "".join(re.sub("<wbr>", "", response.text)), "html.parser"
                )
                if self._is_404(dom):
                    logger.info(
                        f"Topic {self.topic.label} processed, {count} new posts found"
                    )
                    break
                async for post in self._get_new_posts(dom):
                    count += 1
                    self.reporter.write_line(post)
                    self.history.add(post.get("url"))
                start += step
            except (ConnectTimeout, ReadTimeout) as e:
                logger.error(f"Connection timeout. Retrying {self.topic.label}")
                raise e
            except HTTPStatusError as e:
                logger.exception("Something went wrong")
                break

    async def _get_new_posts(
        self, dom: BeautifulSoup
    ) -> AsyncGenerator[OrderedDict[str, str], None]:
        tr: Tag
        for tr in dom.find_all("tr", class_="hl-tr"):
            a: Tag = cast(Tag, tr.find("a", class_="torTopic"))
            if not a or not a.get("href"):
                continue
            url = f"{self.base_url}/{a['href']}"
            if url in self.history:
                continue
            post = OrderedDict(
                [
                    (
                        extractor.name,
                        extractor.get_value(
                            label=self.topic.label, title=self._get_title(a), url=url
                        ),
                    )
                    for extractor in self.extractors
                ]
            )
            if not self.filters or all(filter.accept(post) for filter in self.filters):
                yield post

    def _get_title(self, a: Tag | NavigableString) -> str:
        return re.sub(r"\s+", " ", " ".join(a.stripped_strings))
