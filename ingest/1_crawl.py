import os
from pydantic import BaseModel
from typing import List
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy


class PageParams(BaseModel):
    url: str
    selector: str | None = None


async def main(urls: List[PageParams]):
    for url in urls:
        print("*" * 10, url, "*" * 10)
        await crawl(url)


async def crawl(page: PageParams):
    # Configure a 2-level deep crawl
    config = CrawlerRunConfig(
        deep_crawl_strategy=BFSDeepCrawlStrategy(max_depth=2, include_external=False),
        scraping_strategy=LXMLWebScrapingStrategy(),
        verbose=True,
        wait_for=page.selector,
        css_selector=page.selector,
        stream=True,
    )
    async with AsyncWebCrawler() as crawler:
        results = crawler.arun("https://bolagsverket.se", config=config)

        async for result in await results:
            if result.markdown and result.markdown.strip():
                local_path = f"data/{result.url.split(':')[-1].strip('/')}.md"
                os.makedirs(os.path.dirname(local_path), exist_ok=True)
                with open(local_path, "w") as f:
                    f.write(result.markdown)
            else:
                print("No content at", result.url, result.html)


if __name__ == "__main__":
    asyncio.run(
        main(
            [
                PageParams(url="https://bolagsverket.se", selector=".pagecontent"),
                PageParams(url="https://skatteverket.se"),
            ]
        )
    )
