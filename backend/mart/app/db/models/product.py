from datetime import datetime
from typing import List, Optional
from sqlmodel import Field, Relationship, SQLModel

class Category(SQLModel, table=True):
    __tablename__ = 'category'

    id: int = Field(primary_key=True)
    name: str = Field(unique=True, nullable=False)
    slug: str = Field(unique=True, nullable=False)

    products: List["Product"] = Relationship(back_populates="category")

class ProductImages(SQLModel, table=True):
    __tablename__ = "product_images"

    id: int = Field(primary_key=True, index=True)
    image_url: str = Field(nullable=False)
    product_id: Optional[int] = Field(default=None, foreign_key="product.id")

class ProductDiscounts(SQLModel, table=True):
    __tablename__ = "product_discounts"

    id: int = Field(primary_key=True, index=True)
    product_id: Optional[int] = Field(default=None, foreign_key="product.id")
    discount_price: float = Field(nullable=False) 

class ProductVariants(SQLModel, table=True):
    __tablename__ = "product_variants"
    id: int = Field(primary_key=True, index=True)
    name: str = Field(nullable=False)
    price: float = Field(nullable=False)
    stock: int = Field(nullable=False)
    product_id: Optional[int] = Field(default=None, foreign_key="product.id")

class Product(SQLModel, table=True):
    __tablename__ = 'product'

    id: int = Field(primary_key=True)
    category_id: int = Field(foreign_key="category.id")
    name: str = Field(unique=True, nullable=False)
    slug: str = Field(unique=True, nullable=False)
    description: str = Field(nullable=True)
    price: float = Field(nullable=False)
    thumbnail: str = Field(nullable=True)
    created_at: datetime = Field(nullable=False)
    updated_at: datetime = Field(nullable=False)

    category: Category = Relationship(back_populates="products")
    images: List[ProductImages] = Relationship(back_populates="product")
    variants: List[ProductVariants] = Relationship(back_populates="product")
    discounts: List[ProductDiscounts] = Relationship(back_populates="product")






  

