import argparse
from pathlib import Path

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from settings import CRAWLER_SETTINGS
from crawler.spiders.books import BooksSpider
from crawler.spiders.webscraper import WebScraperSpider

def _positive_int(value: str) -> int:
    pages = int(value)
    if pages < 1:
        raise argparse.ArgumentTypeError("must be at least 1")
    return pages


def main(args) -> None:
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)

    settings = {
        **CRAWLER_SETTINGS,
    }
    spiders = [BooksSpider, WebScraperSpider]
    
    process = CrawlerProcess(settings=settings)
    for spider in spiders:
        process.crawl(spider, max_pages=args.max_pages)
    process.start()

def setup_arguments():
    """
    Setup arguments for the main program, including spider, max pages, and output file.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--max_pages", 
        type=_positive_int, 
        default=1,
        help="maximum number of pages to crawl (default: 1)")
    parser.add_argument(
        "--output",
        default="output",
        help="path to a folder containing JSON output files (default: output)",
    )
    
    return parser.parse_args()

if __name__ == "__main__":
    args = setup_arguments()
    main(args)