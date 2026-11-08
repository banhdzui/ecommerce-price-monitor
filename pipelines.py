from decimal import Decimal, InvalidOperation

from sqlalchemy import select
from scrapy.exceptions import DropItem

from database import SessionLocal, init_db
from models import Product, ProductSource, ProductCategory


class PostgreSQLPipeline:

    def open_spider(self, spider):
        """
        Called when the spider starts.
        """
        init_db()

        self.session = SessionLocal()

    def close_spider(self, spider):
        """
        Called when the spider finishes.
        """
        self.session.close()

    def process_item(self, item, spider):
        """
        Called for each scraped item.
        """

        try:
            price = Decimal(str(item["price"]))

            if not price.is_finite() or price < 0:
                raise ValueError("Invalid price")

            source = item["source"]
            category = item["category"]
            title = item["title"]
            price = item["price"]
            price_unit = item["price_unit"]
            description = item["description"]
            url = item["url"]

            # check if the source already exists and insert a new source if not
            new_source = self.session.scalar(
                select(ProductSource).where(
                    ProductSource.name == source
                )
            )

            if new_source is None:
                new_source = ProductSource(
                    name = source
                )
                self.session.add(new_source)
                self.session.flush()
            source_id = new_source.id 

            # check if the category already exists and insert a new category if not 
            new_category = self.session.scalar(
                select(ProductCategory).where(
                    ProductCategory.name==category
                )
            )
            if new_category is None:
                new_category = ProductCategory(
                    name=category
                )
                self.session.add(new_category)
                self.session.flush()
            category_id = new_category.id 

            # check if the product already exists
            product = self.session.scalar(
                select(Product).where(
                    Product.url == url,
                    Product.title == title,
                )
            )

            if product is None:
                product = Product(
                    title=title,
                    url = url,
                    price = price,
                    price_unit = price_unit,
                    description=description,
                    source_id=source_id,
                    category_id = category_id,
                )

                self.session.add(product)
                self.session.flush()

            else:
                print(f"the product {title} already exists!")    
            self.session.commit()
            return item

        except (
            KeyError,
            ValueError,
            InvalidOperation,
        ) as exc:

            self.session.rollback()

            raise DropItem(
                f"Invalid product data: {exc}"
            )

        except Exception:
            self.session.rollback()
            spider.logger.exception("Database insertion failed")
            raise