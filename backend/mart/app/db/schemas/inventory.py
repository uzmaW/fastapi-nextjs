from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel



class InventoryItem(BaseModel):
    product_id: int
    quantity: int = 0

class InventoryItemCreate(InventoryItem):
    id: int
    created_at: Optional[datetime] = None
    
class InventoryRequest(InventoryItem):
    pass
    

class InventoryUpdate(InventoryItem):
    status: Optional[str] = None
    updated_at: Optional[datetime] = None

class InventoryOut(InventoryItemCreate, InventoryUpdate):
    class Config:
        from_attributes = True