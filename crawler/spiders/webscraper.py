import scrapy
import string 

class WebScraperSpider(scrapy.Spider):
    """A spider to crawl laptops and their prices from the website webscraper.io"""

    name = "webscaper.io"

    start_urls = ["https://webscraper.io/test-sites/pagination"]

    def __init__(self, max_pages=1000, name = None, **kwargs):
        super().__init__(name, **kwargs)
        self.max_pages = max_pages
        self.page_count = 0 

    def parse(self, response):
        self.page_count += 1
        for car in response.css("div.card"):
            card_head = car.css("div.card-head")
            card_body = car.css("div.card-body")
            card_footer = car.css("div.card-footer")

            price = card_footer.css("span::text").get().replace(" ", "").strip(string.ascii_letters)
            yield {
                "source": self.name,
                "category": "car",
                "title": card_body.css("h3.card-title::attr(title)").get(),
                "price": float(price),
                "price_unit": "USD",
                "description": card_body.css("p.description::text").get(),
                "url": card_body.css("h3.card-title a::attr(href)").get(),
            } 

        if self.page_count >= self.max_pages:
            return 

        pagination = response.css("ul.pagination")
        next_page = pagination.css("a.page-link.next::attr(href)").get()
        print("here:" + next_page)
        if next_page:
            yield response.follow(next_page, self.parse)