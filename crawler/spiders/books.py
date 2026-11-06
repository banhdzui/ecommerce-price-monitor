import scrapy

class BooksSpider(scrapy.Spider):
    name = "book.toscrape"
    start_urls = ["https://books.toscrape.com/"]

    def __init__(self, max_pages=1000, name = None, **kwargs):
        super().__init__(name, **kwargs)
        self.max_pages = max_pages
        self.page_count = 0 

    def parse(self, response):
        self.page_count += 1 

        for book in response.css("article.product_pod"):
            yield{
                "source": self.name,
                "title": book.css("h3 a::attr(title)").get(),
                "price": book.css("p.price_color::text").get(),
                "url": response.urljoin(book.css("h3 a::attr(href)").get())
            }
        if self.page_count >= self.max_pages:
            return 
        
        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
    



