from datetime import datetime
from pydantic import BaseModel

class PaymentBase(BaseModel):
    order_id: int
    amount: float
    status: str = "PENDING"

class PaymentCreate(PaymentBase):
    pass

class PaymentResponse(PaymentBase):
    id: int
    created_at: datetime