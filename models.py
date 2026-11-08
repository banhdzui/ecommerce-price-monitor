from datetime import datetime, timezone

from sqlalchemy import (
    Column,
    Integer,
    Text,
    Numeric,
    ForeignKey,
    UniqueConstraint,
)

from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)

    title = Column(Text, nullable=False)
    url = Column(Text, nullable=False)
    price = Column(Numeric(10,2), nullable=False)
    price_unit = Column(Text, nullable=False)
    description = Column(Text, nullable=True)

    source_id = Column(
        Integer,
        ForeignKey("product_sources.id"),
        nullable=False,
    )

    category_id = Column(
        Integer,
        ForeignKey("product_sources.id")
    )
    
    __table_args__ = (
        UniqueConstraint(
            "url",
            name="uq_product_url_id",
        ),
    )

class ProductCategory(Base):
    __tablename__ = "product_categories"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)

class ProductSource(Base):
    __tablename__ = "product_sources"

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)


