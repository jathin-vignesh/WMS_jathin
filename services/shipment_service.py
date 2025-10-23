from sqlalchemy.orm import Session
from models.order_model import Order
from fastapi import HTTPException

def trigger_shipment(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order ID not found")
    if order.status == "Shipment started":
        raise HTTPException(status_code=400, detail="Status already updated")
    order.status = "Shipment started"
    db.commit()
    db.refresh(order)
    return order
