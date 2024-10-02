from datetime import datetime
from pydantic import BaseModel
from sqlmodel import SQLModel, Field
from typing import Optional

class Payment(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int
    amount: float
    status: str
    created_at: datetime = Field(default_factory=datetime.now(datetime.UTC))

