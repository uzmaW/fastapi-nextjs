from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db.conn import get_db
from ..db.models.order import Order 

class OrderController:
    def __init__(self):
        self.router = APIRouter(prefix="/orders", tags=["orders"])
        self.router.add_api_route("/", self.get_orders, methods=["GET"])
        self.router.add_api_route("/create", self.create_order, methods=["POST"])
        self.router.add_api_route("/get/{order_id}", self.get_order, methods=["GET"])
        self.router.add_api_route("/update/{order_id}", self.update_order, methods=["PUT"])
        self.router.add_api_route("/delete/{order_id}", self.delete_order, methods=["DELETE"])
    
    def get_orders(self, offset: int = 0, limit: int = 100, db: Session = Depends(get_db)):
        return db.query(Order).offset(offset).limit(limit).all()

    def create_order(self, order: Order, db: Session = Depends(get_db)):
        db.add(order)
        db.commit()
        return order

    def get_order(self, order_id: int, db: Session = Depends(get_db)):
        return db.query(Order).filter(Order.id == order_id).first()

    def update_order(self, order_id: int, order: Order, db: Session = Depends(get_db)):
        db.update(order)
        db.commit()
        return order

    
    def delete_order(self, order_id: int, db: Session = Depends(get_db)):
        order = self.db.query(Order).filter(Order.id == order_id).first()
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        self.db.delete(order)
        self.db.commit()
        return {"message": "Order deleted successfully"}
        
        