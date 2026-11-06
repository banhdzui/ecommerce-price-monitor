from scrapy import signals
from scrapy.crawler import CrawlerProcess

from crawler.spiders.books import BooksSpider

def test_bookspider():
    """Test the crawler for book.toscrape website"""
    books = []
    
    # create a callback and connect the callback to Scrapy's signal
    def collect_item(item, response, spider):
        books.append(dict(item))

    process = CrawlerProcess(
        settings ={
            "LOG_LEVEL": "INFO"
        }
    )
    crawler = process.create_crawler(BooksSpider)
    crawler.signals.connect(
        collect_item,
        signal=signals.item_scraped
    )

    #schedule and start crawling 
    process.crawl(crawler, max_pages=1)
    process.start()

    # Check the first item 
    assert len(books) == 20, f"The number of books on the first page must be 20, not {len(books)}."
    first_book = books[0]
    assert first_book["title"].lower() == "a light in the attic", f"The title should be 'A light in the attic', not {first_book['title']}"
    assert first_book["price"] == "£51.77", f"The price should be £51.77, not {first_book['price']}."