import argparse

from scrapy.crawler import CrawlerProcess

from crawler.settings import CRAWLER_SETTINGS
from crawler.spiders.books import BooksSpider
from crawler.spiders.webscraper import WebScraperSpider

def _positive_int(value: str) -> int:
    pages = int(value)
    if pages < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return pages

configs = {
    "books": BooksSpider,
    "web": WebScraperSpider,
}

def main(args) -> None:
    settings = {
        **CRAWLER_SETTINGS,
        "FEEDS": {
            args.output: {
                "format": "json",
                "encoding": "utf8",
                "overwrite": True,
            }
        },
    }
    process = CrawlerProcess(settings=settings)
    process.crawl(configs[args.spider], max_pages=args.max_pages)
    process.start()

def setup_arguments():
    """
    Setup arguments for the main program, including spider, max pages, and output file.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--spider", 
        type=str, 
        default="books",
        help="The spider is used to crawl (default: books)")
    parser.add_argument(
        "--max_pages", 
        type=_positive_int, 
        default=1,
        help="maximum number of pages to crawl (default: 1)")
    parser.add_argument(
        "--output",
        default="products.json",
        help="path for the JSON output file (default: products.json)",
    )
    
    return parser.parse_args()

if __name__ == "__main__":
    args = setup_arguments()
    main(args)