from datetime import datetime
from .product import Product
from .user import User
from sqlmodel import SQLModel, Field, Relationship

class Order(SQLModel, table=True):
    __tablename__ = "order"

    id: int = Field(primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    first_name: str = Field(max_length=20)
    last_name: str = Field(max_length=20)
    email: str = Field(max_length=50)
    address: str = Field(max_length=100)
    zipcode: str = Field(max_length=10)
    place: str
    phone: str
    created_at: datetime = Field(nullable=False)
    updated_at: datetime = Field(nullable=False)
    paid_amount: float = Field(nullable=False)
    stripe_token: str = Field(max_length=100)

    user: "User" = Relationship(back_populates="orders")
    items: list["OrderItem"] = Relationship(back_populates="order")

class OrderItem(SQLModel, table=True):
    __tablename__ = "order_item"

    id: int = Field(primary_key=True)
    order_id: int = Field(foreign_key="order.id")
    product_id: int = Field(foreign_key="product.id")
    quantity: int = Field(nullable=False)
    price: float = Field(nullable=False)

    order: "Order" = Relationship(back_populates="items")
    product: "Product" = Relationship(back_populates="order_items")
    discount_price: float = Field(nullable=False)
    