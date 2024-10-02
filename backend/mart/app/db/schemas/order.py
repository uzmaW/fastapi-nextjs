from sqlmodel import Field
from pydantic import BaseModel
from datetime import datetime

class OrderBase(BaseModel):
    user_id: int
    first_name: str
    last_name: str
    email: str
    address: str
    zipcode: str
    place: str
    phone: str
    paid_amount: float
    stripe_token: str

class OrderCreate(OrderBase):
    pass

class OrderRead(OrderBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True