from ..db.schemas.inventory import InventoryItemCreate, InventoryOut
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.conn import get_db
from ..db.models.inventory import InventoryItem as Inventory
from pydantic import BaseModel


class InventoryController:
    def __init__(self):
        self.router = APIRouter(prefix="/inventory", tags=["inventory"])
        self.router.add_api_route("/add", self.add_inventory, methods=["POST"], response_model=InventoryOut)
        self.router.add_api_route("/update/{item_id}", self.update_inventory_quantity, methods=["PUT"], 
                                  response_model=InventoryOut)

    @staticmethod
    async def add_inventory(
        inventory: InventoryItemCreate,
        db: Session = Depends(get_db)
    ):
        new_item = Inventory(**inventory.dict())
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item

    @staticmethod
    async def update_inventory_quantity(
        item_id: int,
        quantity: int,
        db: Session = Depends(get_db),
        refund: bool = False
    ):
        inventory_item = db.query(Inventory).filter(Inventory.product_id == item_id).first()
        if not inventory_item:
            raise HTTPException(status_code=404, detail="Inventory item not found")
        
        if refund:
            inventory_item.quantity = inventory_item.quantity + quantity
        else:
            inventory_item.quantity = inventory_item.quantity - quantity
        
        db.commit()
        db.refresh(inventory_item)
        
        return {"message": "Inventory quantity updated successfully", "item": inventory_item}


    async def get_inventory_quantity(
        item_id: int,
        db: Session = Depends(get_db)
    ):
        inventory_item = db.query(Inventory).filter(Inventory.product_id == item_id).first()
        if not inventory_item:
            raise HTTPException(status_code=404, detail="Inventory item not found")
        
        return inventory_item.quantity
    
    


