from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel

class InventoryItem(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    product_id: int
    quantity: int
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    stock_status: str = Field(default="in_stock")
    class Config:
        arbitrary_types_allowed = True

